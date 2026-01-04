"""
Database Setup Script

Initializes the PRAISA database and loads mock patient data.
This script should be run once during initial setup.

Usage:
    python scripts/setup_database.py

Author: Mid Engineer
Date: 2026-01-04
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database.loader import load_all_data


def main():
    """
    Main function to set up the database.

    Steps:
    1. Initialize database schema
    2. Load patient data from CSV files
    3. Load visit data from CSV files
    4. Display summary
    """
    print("=" * 80)
    print("PRAISA Database Setup")
    print("=" * 80)
    print()

    try:
        # Load all data (this also initializes the database)
        load_all_data()

        print()
        print("=" * 80)
        print("✓ Database setup completed successfully!")
        print("=" * 80)

    except Exception as e:
        print()
        print("=" * 80)
        print(f"✗ Error during database setup: {str(e)}")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
