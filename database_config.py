"""
Database configuration for Open Data Downloader
"""

import os

# PostgreSQL database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'open_datasets'),
    'user': os.getenv('DB_USER', 'raneem'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Example usage with environment variables:
# export DB_HOST=localhost
# export DB_PORT=5432
# export DB_NAME=open_datasets
# export DB_USER=postgres
# export DB_PASSWORD=your_password