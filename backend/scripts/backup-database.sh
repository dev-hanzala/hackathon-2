#!/bin/bash
# Database Backup Script for Todo Application
# Usage: ./scripts/backup-database.sh [backup-name]

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$BACKEND_DIR/backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="${1:-backup_$TIMESTAMP}"

# Load environment variables
if [ -f "$BACKEND_DIR/.env" ]; then
    source "$BACKEND_DIR/.env"
fi

# Validate DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL not set in environment"
    echo "   Please set DATABASE_URL in .env file or environment"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Extract connection details from DATABASE_URL
# Format: postgresql+psycopg://user:pass@host:port/db?sslmode=require
DB_URL_CLEAN=$(echo "$DATABASE_URL" | sed 's/postgresql+psycopg/postgresql/')

echo "🔄 Starting database backup..."
echo "   Database: $DB_URL_CLEAN"
echo "   Backup location: $BACKUP_DIR/$BACKUP_NAME.sql"

# Perform backup using pg_dump
if command -v pg_dump &> /dev/null; then
    pg_dump "$DB_URL_CLEAN" > "$BACKUP_DIR/$BACKUP_NAME.sql"
    
    # Compress backup
    gzip "$BACKUP_DIR/$BACKUP_NAME.sql"
    
    # Calculate size
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME.sql.gz" | cut -f1)
    
    echo "✅ Backup completed successfully!"
    echo "   File: $BACKUP_DIR/$BACKUP_NAME.sql.gz"
    echo "   Size: $BACKUP_SIZE"
    echo ""
    echo "📋 To restore this backup:"
    echo "   gunzip $BACKUP_DIR/$BACKUP_NAME.sql.gz"
    echo "   psql \$DATABASE_URL < $BACKUP_DIR/$BACKUP_NAME.sql"
else
    echo "❌ ERROR: pg_dump not found"
    echo "   Install PostgreSQL client tools:"
    echo "   - macOS: brew install postgresql"
    echo "   - Ubuntu: sudo apt-get install postgresql-client"
    echo "   - Windows: Download from postgresql.org"
    exit 1
fi

# Optional: Clean up old backups (keep last 7 days)
if [ "$CLEANUP_OLD_BACKUPS" = "true" ]; then
    echo "🧹 Cleaning up backups older than 7 days..."
    find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -mtime +7 -delete
    echo "✅ Cleanup completed"
fi

echo ""
echo "📊 Backup Summary:"
ls -lh "$BACKUP_DIR"/*.sql.gz | tail -5
