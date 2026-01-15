#!/usr/bin/env python3
"""Initialize database tables."""

from src.db.database import init_db

if __name__ == "__main__":
    print("🔧 Initializing database tables...")
    init_db()
    print("✅ Database tables created successfully!")
    print("\nTables created:")
    print("  - user (User accounts)")
    print("  - task (Todo tasks)")
    print("  - session (User sessions)")
