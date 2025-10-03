#!/usr/bin/env python3
"""
Analyze strategic datasets for Saudi Arabia's objectives
"""

import json
import re

def main():
    # Read the JSON file
    with open('/Users/raneem/VS/od_dataset/open_datasets.json', 'r') as f:
        datasets = json.load(f)

    # Define strategic categories and keywords
    strategic_categories = {
        'Nuclear Safety & Radiation': [
            'nuclear', 'radiation', 'radioactive', 'reactor', 'uranium', 'nuclear safety', 
            'nuclear power', 'nuclear regulatory', 'radiation safety', 'nuclear waste'
        ],
        'Solar & Renewable Energy': [
            'solar radiation', 'solar energy', 'solar resource', 'photovoltaic', 'solar data',
            'renewable energy', 'solar power', 'solar irradiance', 'wind energy', 'clean energy'
        ],
        'Research & Innovation': [
            'national institute', 'research data', 'scientific data', 'innovation', 'technology',
            'research and development', 'r&d', 'laboratory data'
        ],
        'Standards & Regulations': [
            'standards', 'regulations', 'compliance', 'quality framework', 'technical standards',
            'regulatory framework', 'safety standards', 'certification'
        ],
        'Energy Efficiency & Performance': [
            'energy efficiency', 'performance data', 'energy performance', 'efficiency standards',
            'energy monitoring', 'energy analytics'
        ],
        'International Collaboration': [
            'international', 'collaboration', 'partnership', 'global', 'worldwide',
            'international cooperation', 'multi-country'
        ]
    }

    # Find strategic datasets
    strategic_datasets = []

    for dataset in datasets:
        title = dataset.get('title', '').lower()
        description = dataset.get('description', '').lower()
        keywords = [k.lower() for k in dataset.get('keywords', [])]
        organization = dataset.get('organization', '')
        
        # Combine text for searching
        combined_text = f"{title} {description} {' '.join(keywords)}"
        
        # Check each strategic category
        for category, category_keywords in strategic_categories.items():
            for keyword in category_keywords:
                if keyword.lower() in combined_text:
                    strategic_datasets.append({
                        'category': category,
                        'title': dataset.get('title', ''),
                        'organization': organization,
                        'description': dataset.get('description', '')[:200] + '...',
                        'url': dataset.get('source_url', ''),
                        'keywords': dataset.get('keywords', [])[:10],  # First 10 keywords
                        'matched_keyword': keyword
                    })
                    break  # Only add once per dataset
            
            if len(strategic_datasets) >= 50:  # Limit to avoid too much output
                break

    # Sort by category and print results
    strategic_datasets.sort(key=lambda x: (x['category'], x['title']))

    print('STRATEGIC DATASETS FOR SAUDI ARABIA\'S OBJECTIVES')
    print('=' * 80)

    current_category = None
    for dataset in strategic_datasets:
        if dataset['category'] != current_category:
            current_category = dataset['category']
            print(f'\n{current_category.upper()}')
            print('-' * 50)
        
        print(f'\n• {dataset["title"]}')
        print(f'  Organization: {dataset["organization"]}')
        print(f'  Description: {dataset["description"]}')
        print(f'  URL: {dataset["url"]}')
        print(f'  Key Keywords: {", ".join(dataset["keywords"][:5])}')
        print(f'  Strategic Match: {dataset["matched_keyword"]}')

if __name__ == "__main__":
    main()