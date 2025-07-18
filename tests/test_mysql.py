#!/usr/bin/env python3
"""
Database connection test script for portfolio app.
Run this to check if your database configuration is working.
"""

import os
from dotenv import load_dotenv
from peewee import MySQLDatabase

def test_database_connection():
    # Load environment variables
    load_dotenv()
    
    print("🔍 Testing database connection...")
    print("-" * 40)
    
    # Check environment variables
    required_vars = ["MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST"]
    print("📋 Environment Variables:")
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Hide password for security
            display_value = "****" if "PASSWORD" in var else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: NOT SET")
            return False
    
    # Test database connection
    try:
        print("\n🔌 Attempting database connection...")
        
        mydb = MySQLDatabase(
            os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT", 3306))
        )
        
        # Test connection
        mydb.connect()
        print("   ✅ Connection successful!")
        
        # Test if we can execute queries
        cursor = mydb.execute_sql("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"   ✅ Query test successful: {result}")
        
        mydb.close()
        print("\n🎉 Database connection test PASSED!")
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   - Check if MySQL server is running")
        print("   - Verify database credentials in .env file")
        print("   - Ensure database exists")
        print("   - Check firewall/network settings")
        return False

if __name__ == "__main__":
    test_database_connection()
