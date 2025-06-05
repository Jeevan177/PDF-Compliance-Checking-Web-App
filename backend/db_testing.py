#!/usr/bin/env python3
"""
Quick test script to verify PostgreSQL connection with your credentials
"""
import psycopg2
from sqlalchemy import create_engine, text
import sys

# Your database credentials
DB_CONFIG = {
    'database': 'SDassignment',
    'user': 'postgres',  
    'password': 'jeevan',
    'host': 'localhost',
    'port': '5432'
}

DATABASE_URL = "postgresql://postgres:jeevan@localhost:5432/SDassignment"

def test_psycopg2_connection():
    """Test connection using psycopg2 (direct connection)"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ psycopg2 connection successful")
        print(f"  PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ psycopg2 connection failed: {e}")
        return False

def test_sqlalchemy_connection():
    """Test connection using SQLAlchemy (what FastAPI will use)"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user;"))
            db_info = result.fetchone()
            print(f"✓ SQLAlchemy connection successful")
            print(f"  Connected to database: {db_info[0]}")
            print(f"  Connected as user: {db_info[1]}")
        engine.dispose()
        return True
    except Exception as e:
        print(f"✗ SQLAlchemy connection failed: {e}")
        return False

def check_existing_tables():
    """Check what tables already exist in the database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"✓ Found {len(tables)} existing tables:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("✓ No existing tables found (fresh database)")
            
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error checking tables: {e}")
        return False

def main():
    print("=== Database Connection Test ===\n")
    print(f"Testing connection to: {DB_CONFIG['database']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"User: {DB_CONFIG['user']}\n")
    
    # Test 1: Direct psycopg2 connection
    print("1. Testing psycopg2 connection...")
    if not test_psycopg2_connection():
        print("\n❌ Basic connection failed. Please check:")
        print("   - PostgreSQL is running")
        print("   - Database 'SDassignment' exists")
        print("   - User 'postgres' has access")
        print("   - Password is correct")
        sys.exit(1)
    
    print("\n2. Testing SQLAlchemy connection...")
    if not test_sqlalchemy_connection():
        sys.exit(1)
    
    print("\n3. Checking existing tables...")
    check_existing_tables()
    
    print("\n🎉 All connection tests passed!")
    print("\nYou can now run:")
    print("1. python setup_database.py  # To create tables")
    print("2. uvicorn app.main:app --reload  # To start the API")

if __name__ == "__main__":
    main()