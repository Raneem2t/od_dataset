#!/usr/bin/env python3
"""
Detailed analysis of top strategic datasets for Saudi Arabia
"""

import json

def analyze_top_datasets():
    # Read the JSON file
    with open('/Users/raneem/VS/od_dataset/open_datasets.json', 'r') as f:
        datasets = json.load(f)

    # Define top strategic datasets by name
    top_strategic_datasets = [
        "National Solar Radiation Database (NSRDB)",
        "U.S. Nuclear Power Plant Inspection Reports", 
        "Photovoltaic Data Acquisition (PVDAQ) Public Datasets",
        "Alternative Fueling Stations",
        "Electricity Data and Statistics Application Programming Interface (API)",
        "Global Historical Climatology Network - Daily (GHCN-Daily), Version 3",
        "National Greenhouse Gas Emission Inventory",
        "RECA Awards by Place of Residence (State/Country) as of [date]",
        "Air Quality Measures on the National Environmental Health Tracking Network",
        "Global Terrorism Database"
    ]

    # Find detailed information for each top dataset
    detailed_analysis = []
    
    for dataset in datasets:
        if dataset.get('title') in top_strategic_datasets:
            detailed_analysis.append({
                'title': dataset.get('title'),
                'organization': dataset.get('organization'),
                'description': dataset.get('description'),
                'keywords': dataset.get('keywords', []),
                'publication_date': dataset.get('publication_date'),
                'last_modified': dataset.get('last_modified_date'),
                'formats': dataset.get('format', []),
                'source_url': dataset.get('source_url'),
                'download_urls': dataset.get('download_url', []),
                'maintainer': dataset.get('maintainer')
            })

    # Sort by organization and print detailed analysis
    detailed_analysis.sort(key=lambda x: x['organization'])
    
    print("TOP STRATEGIC DATASETS - DETAILED ANALYSIS")
    print("=" * 80)
    
    for i, dataset in enumerate(detailed_analysis, 1):
        print(f"\n{i}. {dataset['title']}")
        print(f"   Organization: {dataset['organization']}")
        print(f"   Maintainer: {dataset['maintainer']}")
        print(f"   Publication Date: {dataset['publication_date']}")
        print(f"   Last Modified: {dataset['last_modified']}")
        print(f"   Available Formats: {', '.join(dataset['formats'])}")
        print(f"   Source URL: {dataset['source_url']}")
        
        if dataset['download_urls']:
            print(f"   Download URLs:")
            for url in dataset['download_urls'][:3]:  # Show first 3 URLs
                print(f"     - {url}")
        
        print(f"   Description: {dataset['description'][:300]}...")
        print(f"   Keywords: {', '.join(dataset['keywords'][:10])}")
        print("\n" + "="*80)

if __name__ == "__main__":
    analyze_top_datasets()