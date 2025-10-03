#!/usr/bin/env python3
"""
Language Analysis Script
Analyzes the primary languages present in the database text fields
"""

import psycopg2
from database_config import DB_CONFIG

def detect_language_simple(text):
    """Simple language detection based on common patterns"""
    if not text or len(text.strip()) < 10:
        return 'unknown'
    
    text = text.lower()
    
    # Language indicators based on common words
    if any(word in text for word in ['the', 'and', 'data', 'information', 'report', 'analysis', 'government', 'department', 'national', 'public', 'service', 'administration']):
        return 'english'
    elif any(word in text for word in ['de', 'du', 'des', 'le', 'la', 'les', 'et', 'données', 'france', 'français', 'commune', 'région', 'département', 'gouvernement']):
        return 'french'
    elif any(word in text for word in ['der', 'die', 'das', 'und', 'von', 'für', 'mit', 'deutschland', 'german', 'daten', 'verwaltung', 'regierung']):
        return 'german'
    elif any(word in text for word in ['el', 'la', 'los', 'las', 'de', 'del', 'y', 'datos', 'españa', 'spanish', 'gobierno', 'administración']):
        return 'spanish'
    elif any(word in text for word in ['het', 'de', 'van', 'en', 'nederland', 'dutch', 'gegevens', 'overheid']):
        return 'dutch'
    elif any(word in text for word in ['il', 'la', 'le', 'di', 'del', 'e', 'italia', 'italian', 'dati', 'governo']):
        return 'italian'
    elif any(word in text for word in ['o', 'a', 'os', 'as', 'de', 'do', 'da', 'e', 'brasil', 'portuguese', 'dados', 'governo']):
        return 'portuguese'
    else:
        return 'other'

def main():
    print('🌍 LANGUAGE ANALYSIS OF TEXT FIELDS')
    print('=' * 70)
    
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            print('📊 Analyzing language distribution...')
            
            # Sample analysis on titles and descriptions
            cur.execute('''
                SELECT title, description, source_platform
                FROM datasets 
                WHERE title IS NOT NULL AND title != ''
                ORDER BY RANDOM()
                LIMIT 20000
            ''')
            
            sample_data = cur.fetchall()
            
            language_counts = {}
            platform_languages = {}
            mixed_language_count = 0
            
            for title, desc, platform in sample_data:
                # Analyze title
                title_lang = detect_language_simple(title)
                desc_lang = detect_language_simple(desc) if desc else 'unknown'
                
                # Check for mixed language (title and description different)
                if title_lang != desc_lang and title_lang != 'unknown' and desc_lang != 'unknown':
                    mixed_language_count += 1
                
                # Count primary language (prefer title over description)
                primary_lang = title_lang if title_lang != 'unknown' else desc_lang
                
                language_counts[primary_lang] = language_counts.get(primary_lang, 0) + 1
                
                # Track by platform
                if platform not in platform_languages:
                    platform_languages[platform] = {}
                platform_languages[platform][primary_lang] = platform_languages[platform].get(primary_lang, 0) + 1
            
            print(f'Analyzed {len(sample_data):,} records')
            print()
            
            # 1. Overall language distribution
            print('1️⃣ LANGUAGE DISTRIBUTION (Sample Analysis)')
            print('-' * 50)
            
            total_analyzed = len(sample_data)
            sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
            
            for lang, count in sorted_languages:
                percentage = (count / total_analyzed) * 100
                print(f'  {lang.capitalize()}: {count:,} records ({percentage:.1f}%)')
            
            # 2. Platform-specific language analysis
            print('\n2️⃣ LANGUAGE BY PLATFORM (Top 5 Platforms)')
            print('-' * 50)
            
            # Get top platforms by record count in sample
            top_platforms = sorted(platform_languages.items(), 
                                 key=lambda x: sum(x[1].values()), reverse=True)[:5]
            
            for platform, lang_dist in top_platforms:
                total_platform = sum(lang_dist.values())
                print(f'\n📍 {platform}:')
                platform_sorted = sorted(lang_dist.items(), key=lambda x: x[1], reverse=True)
                for lang, count in platform_sorted:
                    pct = (count / total_platform) * 100
                    print(f'    {lang.capitalize()}: {count:,} ({pct:.1f}%)')
            
            # 3. Mixed language analysis
            print('\n3️⃣ MIXED LANGUAGE CONTENT')
            print('-' * 50)
            mixed_percentage = (mixed_language_count / total_analyzed) * 100
            print(f'  Records with mixed languages: {mixed_language_count:,} ({mixed_percentage:.1f}%)')
            
            # 4. English vs Other languages
            print('\n4️⃣ ENGLISH vs OTHER LANGUAGES')
            print('-' * 50)
            
            english_count = language_counts.get('english', 0)
            other_count = total_analyzed - english_count
            
            english_pct = (english_count / total_analyzed) * 100
            other_pct = (other_count / total_analyzed) * 100
            
            print(f'  English: {english_count:,} records ({english_pct:.1f}%)')
            print(f'  Other languages: {other_count:,} records ({other_pct:.1f}%)')
            
            if english_pct > 50:
                print('  ✅ English is the majority language')
            else:
                print('  ⚠️  English is NOT the majority language')
            
            # 5. Detailed platform analysis
            print('\n5️⃣ PLATFORM-SPECIFIC LANGUAGE PATTERNS')
            print('-' * 50)
            
            # Show expected vs detected for key platforms
            expected_patterns = {
                'data.europa.eu': 'Expected: Multi-language European',
                'data.gov': 'Expected: English (US)',
                'data.gouv.fr': 'Expected: French',
                'data.gov.au': 'Expected: English (AU)',
                'open.canada.ca': 'Expected: English/French'
            }
            
            for platform, expectation in expected_patterns.items():
                if platform in platform_languages:
                    lang_dist = platform_languages[platform]
                    top_lang = max(lang_dist.items(), key=lambda x: x[1])
                    total_platform = sum(lang_dist.values())
                    print(f'\n🔍 {platform}:')
                    print(f'    {expectation}')
                    print(f'    Detected primary: {top_lang[0].capitalize()} ({(top_lang[1]/total_platform)*100:.1f}%)')
            
            print('\n' + '=' * 70)
            print('📋 LANGUAGE ANALYSIS COMPLETE')
            print('=' * 70)

if __name__ == "__main__":
    main()