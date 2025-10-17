#!/bin/bash
# Create compressed database backup

echo "📦 Creating database backup..."

# Create data directory
mkdir -p data

# Export schema only (structure without data)
echo "1️⃣ Exporting database schema..."
pg_dump -U raneem -s open_datasets > data/schema_only.sql
echo "   ✅ Schema saved: data/schema_only.sql"

# Export sample data (first 10000 records)
echo "2️⃣ Exporting sample data..."
psql -U raneem -d open_datasets -c "\COPY (SELECT * FROM datasets LIMIT 10000) TO 'data/datasets_sample.csv' WITH CSV HEADER"
echo "   ✅ Sample saved: data/datasets_sample.csv"

# Export statistics
echo "3️⃣ Exporting statistics..."
psql -U raneem -d open_datasets -c "\COPY (SELECT source_platform, COUNT(*) FROM datasets GROUP BY source_platform) TO 'data/platform_stats.csv' WITH CSV HEADER"
echo "   ✅ Stats saved: data/platform_stats.csv"

echo ""
echo "✅ Backup complete!"
echo ""
echo "Files created:"
echo "  - data/schema_only.sql (database structure)"
echo "  - data/datasets_sample.csv (10,000 sample records)"
echo "  - data/platform_stats.csv (statistics)"
echo ""
echo "To export FULL database (warning: large file):"
echo "  pg_dump -U raneem open_datasets | gzip > data/full_backup.sql.gz"
