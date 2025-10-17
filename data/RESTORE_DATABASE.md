# Restore Full Database

The full database (683MB compressed, 1.7M+ records) has been split into 8 parts to fit GitHub's file size limits.

## Restore Instructions

### 1. Rejoin the split files:
```bash
cat database_part_* > full_database_backup.sql.gz
```

### 2. Verify integrity (optional):
```bash
gunzip -t full_database_backup.sql.gz
```

### 3. Create database:
```bash
createdb -U raneem open_datasets
```

### 4. Restore data:
```bash
gunzip -c full_database_backup.sql.gz | psql -U raneem open_datasets
```

Or restore directly from parts:
```bash
cat database_part_* | gunzip | psql -U raneem open_datasets
```

## Files

- `database_part_aa` through `database_part_ah` - Split database backup (8 parts)
- Total size: 683MB compressed
- Uncompressed: ~3-4GB
- Records: 1,782,694 datasets

## Verification

After restoration, verify:
```bash
psql -U raneem -d open_datasets -c "SELECT COUNT(*) FROM datasets;"
# Should return: 1782694

psql -U raneem -d open_datasets -c "SELECT COUNT(*) FROM en_datasets;"
# Should return: 1782694
```
