# Database Backup & Restore

## Overview

Scripts for backing up and restoring the Todo application database.

## Prerequisites

- PostgreSQL client tools installed (`pg_dump`, `psql`)
- Access to database (DATABASE_URL in .env)

**Install PostgreSQL client:**
```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql-client

# Windows
# Download from postgresql.org
```

## Backup Database

### Manual Backup

```bash
# Run backup script
./scripts/backup-database.sh

# Or with custom name
./scripts/backup-database.sh my_backup_name
```

**Output:**
- Creates: `backups/backup_YYYYMMDD_HHMMSS.sql.gz`
- Compressed with gzip
- Includes all tables, data, and schema

### Automated Backups

**Option 1: Cron Job (Linux/macOS)**

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /path/to/backend && ./scripts/backup-database.sh >> /var/log/db-backup.log 2>&1

# Add weekly backup on Sunday
0 3 * * 0 cd /path/to/backend && ./scripts/backup-database.sh weekly_backup >> /var/log/db-backup.log 2>&1
```

**Option 2: GitHub Actions (On commit to main)**

```yaml
# .github/workflows/backup.yml
name: Database Backup
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install PostgreSQL client
        run: sudo apt-get install postgresql-client
      - name: Run backup
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          cd backend
          ./scripts/backup-database.sh
      - name: Upload backup
        uses: actions/upload-artifact@v3
        with:
          name: database-backup
          path: backend/backups/*.sql.gz
          retention-days: 30
```

**Option 3: Neon Automatic Backups**

If using Neon database:
- Automatic backups included
- Point-in-time recovery
- No scripts needed
- Configure in Neon dashboard

## Restore Database

### From Backup File

```bash
# List available backups
ls -lh backups/

# Restore from backup
./scripts/restore-database.sh backups/backup_20260115_120000.sql.gz

# Confirm restoration when prompted
```

**⚠️ WARNING**: Restore will **replace all data** in the database!

### Restore Process

1. Script decompresses backup (if gzipped)
2. Drops existing tables
3. Restores schema and data from backup
4. Verifies restoration

### After Restore

```bash
# 1. Run migrations (if schema changed)
alembic upgrade head

# 2. Restart application
uvicorn src.main:app --reload

# 3. Verify data
# - Login to application
# - Check task list
# - Verify user accounts
```

## Backup Configuration

### Environment Variables

```bash
# Optional: Custom backup directory
export BACKUP_DIR=/path/to/backups

# Optional: Auto-cleanup old backups
export CLEANUP_OLD_BACKUPS=true  # Keeps last 7 days
```

### Backup Retention

**Default:**
- Manual script: Keeps all backups
- Optional cleanup: Deletes backups older than 7 days

**Recommended Production:**
- Daily backups: Keep 7 days
- Weekly backups: Keep 4 weeks
- Monthly backups: Keep 12 months

## Backup Strategies

### Strategy 1: Local Development

```bash
# Before major changes
./scripts/backup-database.sh before_migration

# Before data cleanup
./scripts/backup-database.sh before_cleanup
```

### Strategy 2: Production

**Multi-tier backup:**
1. **Continuous**: Neon automatic backups (point-in-time recovery)
2. **Daily**: Scheduled script backups (via cron)
3. **Weekly**: Manual backups before deployments
4. **On-demand**: Before database migrations

### Strategy 3: Disaster Recovery

**Backup locations:**
1. Local: `backend/backups/` (development)
2. Cloud: AWS S3 / Google Cloud Storage (production)
3. Version control: GitHub Actions artifacts (30 days)
4. Provider: Neon automatic backups (7-30 days)

## Troubleshooting

### Issue: `pg_dump` not found

```bash
# Solution: Install PostgreSQL client
brew install postgresql  # macOS
sudo apt-get install postgresql-client  # Ubuntu
```

### Issue: Connection timeout

```bash
# Check database is reachable
psql $DATABASE_URL -c "SELECT 1"

# For Neon: Ensure database not asleep
# First connection may take 5-10 seconds
```

### Issue: Permission denied

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run with correct user permissions
```

### Issue: Out of disk space

```bash
# Check disk space
df -h

# Clean up old backups
rm backups/backup_20*.sql.gz

# Or enable auto-cleanup
export CLEANUP_OLD_BACKUPS=true
```

### Issue: Backup corrupted

```bash
# Test backup integrity
gunzip -t backups/backup_20260115.sql.gz

# If fails, backup is corrupted
# Use previous backup or Neon point-in-time recovery
```

## Advanced Usage

### Backup Specific Tables

```bash
# Modify backup script to include only specific tables
pg_dump $DATABASE_URL -t user -t task > backup_users_tasks.sql
```

### Backup Schema Only (No Data)

```bash
# Schema only
pg_dump $DATABASE_URL --schema-only > schema.sql

# Data only
pg_dump $DATABASE_URL --data-only > data.sql
```

### Remote Backup

```bash
# Backup production to local
DATABASE_URL="postgresql://prod..." ./scripts/backup-database.sh prod_backup

# Upload to S3
aws s3 cp backups/prod_backup.sql.gz s3://my-bucket/backups/
```

## Security Best Practices

1. **Encrypt backups** before uploading to cloud
2. **Restrict backup file permissions**: `chmod 600 backups/*.sql.gz`
3. **Don't commit backups** to git (in .gitignore)
4. **Use secure connection strings** (SSL enabled)
5. **Rotate backup encryption keys** regularly

## Monitoring

### Backup Health Checks

```bash
# Check last backup age
ls -lh backups/*.sql.gz | tail -1

# Verify backup size (should be consistent)
du -h backups/*.sql.gz

# Test restore (in dev environment)
./scripts/restore-database.sh backups/latest.sql.gz
```

### Alerts

Set up alerts for:
- Backup script failures
- Missing daily backups
- Backup size anomalies
- Disk space low

## Related Documentation

- Database setup: `../README.md`
- Migrations: `../alembic/README.md`
- Performance: `./database-performance.md`
- Deployment: `./deployment.md` (Phase III)
