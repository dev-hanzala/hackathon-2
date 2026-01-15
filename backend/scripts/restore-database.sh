#!/bin/bash
# Database Restore Script for Todo Application
# Usage: ./scripts/restore-database.sh <backup-file>

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_FILE="$1"

# Load environment variables
if [ -f "$BACKEND_DIR/.env" ]; then
    source "$BACKEND_DIR/.env"
fi

# Validate inputs
if [ -z "$BACKUP_FILE" ]; then
    echo "❌ ERROR: No backup file specified"
    echo "Usage: $0 <backup-file>"
    echo ""
    echo "Available backups:"
    ls -lh "$BACKEND_DIR/backups"/*.sql.gz 2>/dev/null || echo "  No backups found"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ ERROR: Backup file not found: $BACKUP_FILE"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL not set in environment"
    exit 1
fi

# Extract connection details
DB_URL_CLEAN=$(echo "$DATABASE_URL" | sed 's/postgresql+psycopg/postgresql/')

echo "⚠️  WARNING: This will REPLACE all data in the database!"
echo "   Database: $DB_URL_CLEAN"
echo "   Backup: $BACKUP_FILE"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 0
fi

echo "🔄 Starting database restore..."

# Decompress if gzipped
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "   Decompressing backup..."
    TEMP_FILE="${BACKUP_FILE%.gz}"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    RESTORE_FILE="$TEMP_FILE"
else
    RESTORE_FILE="$BACKUP_FILE"
fi

# Restore database
if command -v psql &> /dev/null; then
    echo "   Restoring database..."
    psql "$DB_URL_CLEAN" < "$RESTORE_FILE"
    
    # Clean up temp file
    if [ "$RESTORE_FILE" != "$BACKUP_FILE" ]; then
        rm "$RESTORE_FILE"
    fi
    
    echo "✅ Restore completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Verify data: psql \$DATABASE_URL"
    echo "   2. Run migrations if needed: alembic upgrade head"
    echo "   3. Restart application"
else
    echo "❌ ERROR: psql not found"
    echo "   Install PostgreSQL client tools"
    exit 1
fi
