#!/usr/bin/env python3
"""
Export database tables to CSV files
"""

import psycopg2
import csv
from database_config import DB_CONFIG

def export_to_csv():
    print('📦 EXPORTING DATABASE TO CSV')
    print('=' * 70)

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # Export datasets table (sample or full)
            print('\n1️⃣ Exporting datasets table...')

            # Option 1: Export sample (first 10,000 records)
            print('   Exporting sample (10,000 records)...')
            cur.execute('''
                SELECT * FROM datasets
                ORDER BY id
                LIMIT 10000
            ''')

            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            with open('data/datasets_sample.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)

            print(f'   ✅ Saved: data/datasets_sample.csv ({len(rows):,} records)')

            # Export en_datasets table
            print('\n2️⃣ Exporting en_datasets table...')
            cur.execute('''
                SELECT id, title, title_en, description, description_en,
                       detected_language, source_platform, source_url
                FROM en_datasets
                WHERE title_en IS NOT NULL
                LIMIT 10000
            ''')

            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            with open('data/en_datasets_sample.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)

            print(f'   ✅ Saved: data/en_datasets_sample.csv ({len(rows):,} records)')

            # Export statistics
            print('\n3️⃣ Exporting statistics...')

            # Language distribution
            cur.execute('''
                SELECT detected_language, COUNT(*) as count
                FROM en_datasets
                GROUP BY detected_language
                ORDER BY count DESC
            ''')

            with open('data/language_stats.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['language', 'count'])
                writer.writerows(cur.fetchall())

            print('   ✅ Saved: data/language_stats.csv')

            # Platform distribution
            cur.execute('''
                SELECT source_platform, COUNT(*) as count
                FROM datasets
                GROUP BY source_platform
                ORDER BY count DESC
            ''')

            with open('data/platform_stats.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['platform', 'count'])
                writer.writerows(cur.fetchall())

            print('   ✅ Saved: data/platform_stats.csv')

    print('\n' + '=' * 70)
    print('✅ EXPORT COMPLETE')
    print('=' * 70)
    print('\nFiles created:')
    print('  - data/datasets_sample.csv (sample data)')
    print('  - data/en_datasets_sample.csv (English translations sample)')
    print('  - data/language_stats.csv (language distribution)')
    print('  - data/platform_stats.csv (platform distribution)')
    print('\nTo export full database:')
    print('  pg_dump -U raneem -t datasets open_datasets > data/datasets_full.sql')

if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    export_to_csv()
