#!/usr/bin/env python3
"""
Dataset Translation Script
Translates non-English datasets to English using language detection and translation
"""

import psycopg2
from database_config import DB_CONFIG
import os
from datetime import datetime

# Translation API setup (using OpenAI for translation)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

def detect_language(text):
    """Simple language detection based on common patterns"""
    if not text or len(text.strip()) < 10:
        return 'unknown'

    text = text.lower()

    # Language indicators
    if any(word in text for word in ['the', 'and', 'data', 'information', 'report']):
        return 'english'
    elif any(word in text for word in ['de', 'du', 'des', 'le', 'la', 'les', 'et', 'données']):
        return 'french'
    elif any(word in text for word in ['der', 'die', 'das', 'und', 'von', 'für', 'daten']):
        return 'german'
    elif any(word in text for word in ['el', 'la', 'los', 'las', 'y', 'datos']):
        return 'spanish'
    elif any(word in text for word in ['het', 'de', 'van', 'en', 'gegevens']):
        return 'dutch'
    elif any(word in text for word in ['il', 'la', 'le', 'di', 'del', 'e', 'dati']):
        return 'italian'
    elif any(word in text for word in ['o', 'a', 'os', 'as', 'do', 'da', 'dados']):
        return 'portuguese'
    else:
        return 'other'

def translate_with_openai(text, source_lang):
    """Translate text using OpenAI API"""
    if not OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Translate the following {source_lang} text to English. Only return the translation, no explanations."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def main():
    print('🌍 DATASET TRANSLATION TO ENGLISH')
    print('=' * 70)

    # Check if OpenAI API key is available
    if not OPENAI_API_KEY:
        print('⚠️  WARNING: No OPENAI_API_KEY found in environment')
        print('   Translation will only detect languages, not translate')
        print('   To enable translation: export OPENAI_API_KEY=your_key')
        print()
        translate_enabled = False
    else:
        print('✅ OpenAI API key found - translation enabled')
        translate_enabled = True

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # First, detect languages for all records
            print('\n📊 Step 1: Detecting languages...')
            cur.execute('SELECT COUNT(*) FROM en_datasets WHERE detected_language IS NULL')
            unprocessed = cur.fetchone()[0]
            print(f'   Records to process: {unprocessed:,}')

            # Process in batches
            batch_size = 10000
            processed = 0

            while True:
                cur.execute('''
                    SELECT id, title, description
                    FROM en_datasets
                    WHERE detected_language IS NULL
                    LIMIT %s
                ''', (batch_size,))

                batch = cur.fetchall()
                if not batch:
                    break

                for record_id, title, description in batch:
                    # Detect language from title
                    lang = detect_language(title)

                    # If English, copy directly
                    if lang == 'english':
                        cur.execute('''
                            UPDATE en_datasets
                            SET title_en = title,
                                description_en = description,
                                detected_language = 'english'
                            WHERE id = %s
                        ''', (record_id,))
                    else:
                        # Store detected language
                        cur.execute('''
                            UPDATE en_datasets
                            SET detected_language = %s
                            WHERE id = %s
                        ''', (lang, record_id))

                    processed += 1

                conn.commit()
                print(f'   Processed: {processed:,} / {unprocessed:,} ({(processed/unprocessed)*100:.1f}%)', end='\r')

            print(f'\n✅ Language detection complete: {processed:,} records processed')

            # Show language distribution
            print('\n📈 Language Distribution:')
            cur.execute('SELECT COUNT(*) FROM en_datasets')
            total_records = cur.fetchone()[0]

            cur.execute('''
                SELECT detected_language, COUNT(*)
                FROM en_datasets
                GROUP BY detected_language
                ORDER BY COUNT(*) DESC
            ''')
            for lang, count in cur.fetchall():
                pct = (count / total_records) * 100 if total_records > 0 else 0
                print(f'   {lang.capitalize()}: {count:,} ({pct:.1f}%)')

            # Translation step (if API key available)
            if translate_enabled:
                print('\n📝 Step 2: Translating non-English records...')
                cur.execute('''
                    SELECT COUNT(*)
                    FROM en_datasets
                    WHERE detected_language != 'english'
                    AND title_en IS NULL
                ''')
                to_translate = cur.fetchone()[0]
                print(f'   Records to translate: {to_translate:,}')
                print('   ⚠️  Note: Translation is slow and costs API credits')

                confirm = input('   Continue with translation? (yes/no): ').strip().lower()
                if confirm == 'yes':
                    # Process translations in small batches
                    trans_batch_size = 100
                    translated = 0

                    while translated < to_translate:
                        cur.execute('''
                            SELECT id, title, description, detected_language
                            FROM en_datasets
                            WHERE detected_language != 'english'
                            AND title_en IS NULL
                            LIMIT %s
                        ''', (trans_batch_size,))

                        batch = cur.fetchall()
                        if not batch:
                            break

                        for record_id, title, description, lang in batch:
                            title_en = translate_with_openai(title, lang) if title else None
                            desc_en = translate_with_openai(description[:500], lang) if description else None

                            cur.execute('''
                                UPDATE en_datasets
                                SET title_en = %s,
                                    description_en = %s
                                WHERE id = %s
                            ''', (title_en or title, desc_en or description, record_id))

                            translated += 1
                            print(f'   Translated: {translated:,} / {to_translate:,} ({(translated/to_translate)*100:.1f}%)', end='\r')

                        conn.commit()

                    print(f'\n✅ Translation complete: {translated:,} records translated')
                else:
                    print('   ⏭️  Translation skipped')

            # Summary
            print('\n' + '=' * 70)
            print('📋 TRANSLATION SUMMARY')
            print('=' * 70)
            cur.execute('SELECT COUNT(*) FROM en_datasets WHERE title_en IS NOT NULL')
            english_ready = cur.fetchone()[0]
            cur.execute('SELECT COUNT(*) FROM en_datasets')
            total = cur.fetchone()[0]

            print(f'Total records: {total:,}')
            print(f'English-ready records: {english_ready:,} ({(english_ready/total)*100:.1f}%)')
            print(f'Pending translation: {total - english_ready:,}')

if __name__ == "__main__":
    main()
