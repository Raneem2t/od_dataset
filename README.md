# Open Data Downloader

PostgreSQL-based system for collecting and analyzing datasets from government open data portals with multi-language support and translation capabilities.

## 📊 Database Overview

- **Total Datasets**: 1,782,694 records
- **Languages**: English (69.2%), French (20.5%), Spanish (4.0%), Italian (3.1%), Dutch (1.2%), Portuguese (0.7%), Other (1.3%)
- **Database**: PostgreSQL
- **Tables**:
  - `datasets` - Original collected data
  - `en_datasets` - English translated version

## 🚀 Quick Start

### 1. Setup PostgreSQL Database

```bash
# Start PostgreSQL
brew services start postgresql

# Create database
createdb -U raneem open_datasets

# Create tables (schema will be provided in data/schema_only.sql)
psql -U raneem -d open_datasets -f data/schema_only.sql
```

### 2. Configure Database Connection

Edit `database_config.py` with your credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'open_datasets',
    'user': 'raneem',
    'password': ''
}
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 📥 Getting the Data

### Option A: Import Sample Data (Quick)

```bash
# Export sample data from your existing database
python export_database.py

# Or use the provided CSV samples in data/ directory
```

### Option B: Collect Fresh Data (Slow)

```bash
# Run the Europa downloader
python europa_massive_downloader.py
```

### Option C: Restore from Backup

If a full database backup is available:

```bash
# Restore from compressed backup
gunzip -c data/full_backup.sql.gz | psql -U raneem open_datasets
```

## 🔧 Available Tools

### Database Viewer
Interactive CLI to explore the database:
```bash
python database_viewer.py
```

### Language Analysis
Analyze language distribution:
```bash
python language_analysis.py
```

### Translation System
Translate non-English datasets to English:
```bash
# Set OpenAI API key
export OPENAI_API_KEY=your_key

# Run translation
python translate_datasets.py
```

### Export Data
Export database to CSV files:
```bash
python export_database.py
```

## 📁 Project Structure

```
od_dataset/
├── database_config.py          # PostgreSQL connection settings
├── database_viewer.py          # Interactive database explorer
├── europa_massive_downloader.py # Data collection script
├── language_analysis.py        # Language detection and analysis
├── translate_datasets.py       # Multi-language translation system
├── export_database.py          # Export to CSV
├── data/                       # Data directory
│   ├── schema_only.sql        # Database schema
│   ├── datasets_sample.csv    # Sample data
│   └── *_stats.csv            # Statistics
└── insights_engine/           # Expert routing system
```

## 🗄️ Database Schema

### `datasets` table
- `id` - Primary key
- `title` - Dataset title
- `description` - Dataset description
- `keywords` - Array of keywords
- `source_url` - Original URL
- `source_platform` - Origin platform (data.europa.eu, etc.)
- `organization` - Publishing organization
- `format` - Available formats (CSV, JSON, etc.)
- `license` - Data license
- Plus 10+ additional metadata fields

### `en_datasets` table
Same as `datasets` table plus:
- `title_en` - English translation of title
- `description_en` - English translation of description
- `detected_language` - Detected source language

## 🌍 Data Sources

- Europa Open Data Portal (data.europa.eu)
- USA Data.gov
- Saudi Arabia Open Data Portal

## 📝 Notes

**Database data is NOT included in this repository** due to size (1.7M+ records). You must either:
1. Use the sample data provided in `data/` directory
2. Collect fresh data using the downloaders
3. Contact the repository owner for a full database backup

## 🔐 Security

- Never commit `.env` files or API keys
- Database credentials should be in environment variables
- `.gitignore` excludes sensitive files

## 📄 License

[Add your license here]

## 👤 Author

Raneem2t
