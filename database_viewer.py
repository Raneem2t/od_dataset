#!/usr/bin/env python3
"""
Database Viewer - Simple interface to explore the datasets database
"""

import psycopg2
from database_config import DB_CONFIG

def main():
    print("📊 DATASET DATABASE VIEWER")
    print("=" * 50)
    
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            while True:
                print("\nOptions:")
                print("1. View total dataset count")
                print("2. View datasets by platform")
                print("3. Search datasets by keyword")
                print("4. View sample datasets")
                print("5. Exit")
                
                choice = input("\nEnter choice (1-5): ").strip()
                
                if choice == "1":
                    cur.execute("SELECT COUNT(*) FROM datasets")
                    total = cur.fetchone()[0]
                    print(f"\n📈 Total datasets: {total:,}")
                
                elif choice == "2":
                    cur.execute("""
                        SELECT source_platform, COUNT(*) 
                        FROM datasets 
                        GROUP BY source_platform 
                        ORDER BY COUNT(*) DESC
                    """)
                    results = cur.fetchall()
                    print(f"\n📊 Datasets by platform:")
                    for platform, count in results:
                        print(f"  {platform}: {count:,}")
                
                elif choice == "3":
                    keyword = input("Enter keyword to search: ").strip()
                    if keyword:
                        cur.execute("""
                            SELECT title, source_platform, source_url 
                            FROM datasets 
                            WHERE title ILIKE %s OR description ILIKE %s
                            LIMIT 10
                        """, (f"%{keyword}%", f"%{keyword}%"))
                        results = cur.fetchall()
                        print(f"\n🔍 Found {len(results)} datasets matching '{keyword}':")
                        for title, platform, url in results:
                            print(f"  {title[:60]}... ({platform})")
                            print(f"    {url}")
                
                elif choice == "4":
                    cur.execute("""
                        SELECT title, description, source_platform, source_url 
                        FROM datasets 
                        ORDER BY RANDOM() 
                        LIMIT 5
                    """)
                    results = cur.fetchall()
                    print(f"\n🎲 Random sample datasets:")
                    for i, (title, desc, platform, url) in enumerate(results, 1):
                        print(f"\n{i}. {title}")
                        print(f"   Platform: {platform}")
                        print(f"   Description: {desc[:100]}...")
                        print(f"   URL: {url}")
                
                elif choice == "5":
                    print("👋 Goodbye!")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()