#!/usr/bin/env python3
"""
Update Database with New Datasets
Collects new datasets from government portals and updates the database
"""

import psycopg2
from database_config import DB_CONFIG
import requests
import time
from datetime import datetime

def collect_from_datagov(limit=100):
    """Collect new datasets from data.gov"""
    print("📥 Collecting from data.gov...")

    base_url = "https://catalog.data.gov/api/3/action/package_search"
    datasets = []

    try:
        response = requests.get(base_url, params={
            'rows': limit,
            'start': 0
        }, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                for pkg in data['result']['results']:
                    datasets.append({
                        'title': pkg.get('title', ''),
                        'description': pkg.get('notes', ''),
                        'source_url': f"https://catalog.data.gov/dataset/{pkg.get('id', '')}",
                        'source_platform': 'data.gov',
                        'organization': pkg.get('organization', {}).get('title', ''),
                        'raw_id': pkg.get('id', '')
                    })
                print(f"   ✅ Collected {len(datasets)} datasets from data.gov")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    return datasets

def collect_from_europa(limit=100):
    """Collect new datasets from data.europa.eu"""
    print("📥 Collecting from data.europa.eu...")

    base_url = "https://data.europa.eu/api/hub/search/datasets"
    datasets = []

    try:
        response = requests.get(base_url, params={
            'limit': limit,
            'offset': 0
        }, timeout=30)

        if response.status_code == 200:
            data = response.json()
            for item in data.get('results', []):
                datasets.append({
                    'title': item.get('title', {}).get('en', ''),
                    'description': item.get('description', {}).get('en', ''),
                    'source_url': f"https://data.europa.eu/data/datasets/{item.get('id', '')}",
                    'source_platform': 'data.europa.eu',
                    'organization': item.get('publisher', {}).get('name', ''),
                    'raw_id': item.get('id', '')
                })
            print(f"   ✅ Collected {len(datasets)} datasets from data.europa.eu")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    return datasets

def insert_datasets(datasets):
    """Insert new datasets into database"""
    print(f"\n💾 Inserting {len(datasets)} datasets into database...")

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            inserted = 0
            duplicates = 0

            for dataset in datasets:
                try:
                    cur.execute('''
                        INSERT INTO datasets (title, description, source_url, source_platform, organization, raw_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (source_url) DO NOTHING
                    ''', (
                        dataset['title'],
                        dataset['description'],
                        dataset['source_url'],
                        dataset['source_platform'],
                        dataset['organization'],
                        dataset['raw_id']
                    ))

                    if cur.rowcount > 0:
                        inserted += 1
                    else:
                        duplicates += 1

                except Exception as e:
                    print(f"   ⚠️  Error inserting: {e}")

            conn.commit()

            print(f"   ✅ Inserted: {inserted} new datasets")
            print(f"   ⏭️  Skipped: {duplicates} duplicates")

            return inserted

def get_database_stats():
    """Get current database statistics"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM datasets')
            total = cur.fetchone()[0]

            cur.execute('''
                SELECT source_platform, COUNT(*)
                FROM datasets
                GROUP BY source_platform
                ORDER BY COUNT(*) DESC
            ''')
            platforms = cur.fetchall()

            return total, platforms

def main():
    print('🔄 DATABASE UPDATE')
    print('=' * 70)

    # Show current stats
    print('\n📊 Current Database Stats:')
    total_before, platforms = get_database_stats()
    print(f'   Total datasets: {total_before:,}')
    for platform, count in platforms:
        print(f'   {platform}: {count:,}')

    # Collect new datasets
    print('\n🌐 Collecting New Datasets...')
    all_datasets = []

    # Collect from data.gov
    datagov_datasets = collect_from_datagov(limit=100)
    all_datasets.extend(datagov_datasets)

    time.sleep(1)  # Rate limiting

    # Collect from Europa
    europa_datasets = collect_from_europa(limit=100)
    all_datasets.extend(europa_datasets)

    print(f'\n📦 Total collected: {len(all_datasets)} datasets')

    # Insert into database
    if all_datasets:
        inserted = insert_datasets(all_datasets)

        # Show updated stats
        print('\n📊 Updated Database Stats:')
        total_after, platforms = get_database_stats()
        print(f'   Total datasets: {total_after:,} (+{total_after - total_before:,})')
        for platform, count in platforms:
            print(f'   {platform}: {count:,}')

        print('\n✅ DATABASE UPDATE COMPLETE')

        # Export updated data
        export = input('\nExport updated database? (yes/no): ').strip().lower()
        if export == 'yes':
            print('\nRunning export...')
            import subprocess
            subprocess.run(['/Library/Frameworks/Python.framework/Versions/3.13/bin/python3', 'export_database.py'])
    else:
        print('\n⚠️  No new datasets collected')

    print('=' * 70)

if __name__ == "__main__":
    main()
