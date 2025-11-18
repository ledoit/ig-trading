#!/usr/bin/env python3
"""
Initialize the IG Trading database.
Run this once to set up the database schema.
"""

from database import init_database

if __name__ == "__main__":
    print("Initializing IG Trading database...")
    init_database()
    print("Database initialization complete!")

