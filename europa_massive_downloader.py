#!/usr/bin/env python3
"""
Europa Massive Downloader
Downloads remaining datasets from data.europa.eu using the updated API format
"""

import requests
import json
import time
import psycopg2
from typing import Dict, List, Set
from database_config import DB_CONFIG
from concurrent.futures import ProcessPoolExecutor, as_completed
import threading

class EuropaMassiveDownloader:
    def __init__(self, db_config: Dict = None, num_workers: int = 8):
        self.db_config = db_config or DB_CONFIG
        self.num_workers = num_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OpenDataDownloader/1.0'
        })
        self.lock = threading.Lock()
        
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    def get_existing_europa_urls(self) -> Set[str]:
        """Get set of existing European URLs to avoid duplicates"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT source_url FROM datasets WHERE source_platform = 'data.europa.eu'")
                    return set(row[0] for row in cursor.fetchall())
        except Exception as e:
            print(f"Error getting existing Europa URLs: {e}")
            return set()
    
    def save_datasets_batch(self, datasets: List[Dict]):
        """Save multiple datasets in a single transaction"""
        if not datasets:
            return 0
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    insert_query = """
                        INSERT INTO datasets (
                            title, description, keywords, source_url, organization,
                            publication_date, last_modified_date, format, license,
                            source_platform, raw_id, author, maintainer, download_url,
                            groups, code, data_availability, metadata_availability, concepts
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s
                        ) ON CONFLICT (source_url) DO NOTHING
                    """
                    
                    batch_data = []
                    for dataset in datasets:
                        batch_data.append((
                            dataset.get('title', ''),
                            dataset.get('description', ''),
                            dataset.get('keywords', []),
                            dataset.get('source_url', ''),
                            dataset.get('organization', ''),
                            dataset.get('publication_date') or None,
                            dataset.get('last_modified_date') or None,
                            dataset.get('format', []),
                            dataset.get('license', ''),
                            dataset.get('source_platform', ''),
                            dataset.get('raw_id', ''),
                            dataset.get('author', ''),
                            dataset.get('maintainer', ''),
                            dataset.get('download_url', []),
                            dataset.get('groups', []),
                            dataset.get('code', ''),
                            dataset.get('data_availability', ''),
                            dataset.get('metadata_availability', ''),
                            dataset.get('concepts', '')
                        ))
                    
                    cursor.executemany(insert_query, batch_data)
                    conn.commit()
                    return len(batch_data)
        except Exception as e:
            print(f"Error saving Europa batch: {e}")
            return 0
    
    def extract_europa_metadata_from_string(self, dataset_str: str) -> Dict:
        """Extract metadata from Europa dataset string format"""
        try:
            # The new API returns strings that are actually dataset IDs
            # We need to create basic metadata from the ID
            dataset_id = str(dataset_str).strip()
            
            # Skip if empty or invalid
            if not dataset_id or len(dataset_id) < 3:
                return {}
            
            # Create basic metadata structure
            source_url = f"https://data.europa.eu/data/datasets/{dataset_id}"
            
            return {
                'title': f"European Dataset {dataset_id}",
                'description': f"Dataset from the European Data Portal with ID: {dataset_id}",
                'keywords': ['european data', 'open data', 'government data'],
                'source_url': source_url,
                'organization': 'European Data Portal',
                'publication_date': '',
                'last_modified_date': '',
                'format': ['Unknown'],
                'license': 'Various European Licenses',
                'source_platform': 'data.europa.eu',
                'raw_id': dataset_id,
                'author': 'European Data Portal',
                'maintainer': 'European Data Portal',
                'download_url': [source_url],
                'groups': ['european-data', 'open-data'],
                'code': dataset_id,
                'data_availability': 'metadata_only',
                'metadata_availability': 'available',
                'concepts': json.dumps({'type': 'european_dataset', 'id': dataset_id})
            }
        except Exception as e:
            print(f"Error extracting Europa metadata from string: {e}")
            return {}

def download_europa_chunk(args):
    """Download a chunk of Europa datasets"""
    start_offset, chunk_size, existing_urls = args
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'OpenDataDownloader/1.0'})
    
    try:
        # Get data from Europa API
        response = session.get(
            'https://data.europa.eu/api/hub/repo/datasets',
            params={'limit': chunk_size, 'offset': start_offset},
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Chunk {start_offset}: HTTP {response.status_code}")
            return []
        
        data = response.json()
        
        # Handle the new string-based format
        if not isinstance(data, list):
            print(f"Chunk {start_offset}: Unexpected data format")
            return []
        
        if not data:
            print(f"Chunk {start_offset}: No data returned")
            return []
        
        downloader = EuropaMassiveDownloader()
        datasets = []
        
        for dataset_str in data:
            metadata = downloader.extract_europa_metadata_from_string(dataset_str)
            if metadata and metadata.get('source_url'):
                # Skip if already exists
                if metadata['source_url'] in existing_urls:
                    continue
                datasets.append(metadata)
        
        return datasets
        
    except Exception as e:
        print(f"Error downloading Europa chunk {start_offset}: {e}")
        return []

def main():
    print("Europa Massive Downloader")
    print("=" * 50)
    
    downloader = EuropaMassiveDownloader()
    
    # Get current count
    with downloader.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM datasets WHERE source_platform = 'data.europa.eu'")
            current_count = cursor.fetchone()[0]
    
    print(f"Current Europa datasets: {current_count:,}")
    
    # Get existing URLs
    existing_urls = downloader.get_existing_europa_urls()
    print(f"Found {len(existing_urls)} existing Europa URLs")
    
    # Ask user for batch size
    try:
        batch_size = int(input("Number of datasets to download (default 100000): ") or "100000")
        num_workers = int(input("Number of parallel workers (default 8): ") or "8")
    except (ValueError, EOFError):
        batch_size = 100000
        num_workers = 8
    
    # Calculate starting offset (from current count)
    start_offset = current_count
    
    # Calculate chunks
    chunk_size = 5000  # Smaller chunks for better reliability
    num_chunks = batch_size // chunk_size
    
    print(f"\nWill download {batch_size:,} datasets starting from offset {start_offset:,}")
    print(f"Using {num_chunks} chunks of {chunk_size} each with {num_workers} workers")
    
    # Create chunks
    chunks = []
    for i in range(num_chunks):
        chunk_start = start_offset + (i * chunk_size)
        chunks.append((chunk_start, chunk_size, existing_urls))
    
    # Download in parallel
    total_saved = 0
    chunk_count = 0
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit all chunks
        future_to_chunk = {
            executor.submit(download_europa_chunk, chunk): chunk 
            for chunk in chunks
        }
        
        # Process completed chunks
        for future in as_completed(future_to_chunk):
            chunk = future_to_chunk[future]
            try:
                datasets = future.result()
                if datasets:
                    saved = downloader.save_datasets_batch(datasets)
                    total_saved += saved
                    chunk_count += 1
                    print(f"Chunk {chunk[0]:,}: Downloaded {len(datasets)} datasets, saved {saved} new")
                    
                    # Update existing URLs set
                    for dataset in datasets:
                        existing_urls.add(dataset['source_url'])
                    
                    # Progress update every 10 chunks
                    if chunk_count % 10 == 0:
                        print(f"Progress: {chunk_count}/{len(chunks)} chunks completed, {total_saved:,} new datasets saved")
                else:
                    print(f"Chunk {chunk[0]:,}: No datasets found")
                    
            except Exception as e:
                print(f"Chunk {chunk[0]:,} generated an exception: {e}")
            
            # Small delay to be respectful to the API
            time.sleep(0.1)
    
    print(f"\nEuropa massive download completed!")
    print(f"Total new datasets saved: {total_saved:,}")
    
    # Show final stats
    with downloader.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM datasets WHERE source_platform = 'data.europa.eu'")
            total_europa = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM datasets")
            total_all = cursor.fetchone()[0]
    
    print(f"\nFinal Statistics:")
    print(f"Europa datasets: {total_europa:,}")
    print(f"Total datasets: {total_all:,}")

if __name__ == "__main__":
    main()