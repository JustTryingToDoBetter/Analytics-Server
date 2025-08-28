
#!/usr/bin/env python3
"""
Smoke Test Script for Analytics Server
This script tests if the database connection and basic operations work.
"""

import os
import sys
from datetime import datetime
from sqlalchemy import text

# Add the parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.core.db import db_manager, HealthCheck, Base
    print("✅ Successfully imported database modules")
except ImportError as e:
    print(f"❌ Failed to import database modules: {e}")
    sys.exit(1)

def smoke_test():
    """Run basic smoke tests on the database"""
    
    print("🔥 Starting Smoke Test...")
    print("=" * 50)
    
    try:
        # Test 1: Check database connection
        print("1️⃣  Testing database connection...")
        with db_manager.get_session() as session:
            # Simple query to test connection
            session.execute(text("SELECT 1"))
            print("   ✅ Database connection successful")
        
        # Test 2: Ensure tables exist
        print("2️⃣  Checking if tables exist...")
        Base.metadata.create_all(bind=db_manager.engine)
        print("   ✅ Tables created/verified")
        
        # Test 3: Count existing records
        print("3️⃣  Counting existing healthcheck records...")
        with db_manager.get_session() as session:
            initial_count = session.query(HealthCheck).count()
            print(f"   📊 Found {initial_count} existing records")
        
        # Test 4: Insert a new record
        print("4️⃣  Inserting a new healthcheck record...")
        test_note = f"Smoke test run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        with db_manager.get_session() as session:
            new_record = HealthCheck(note=test_note)
            session.add(new_record)
            session.commit()
            record_id = new_record.id
            print(f"   ✅ Inserted record with ID: {record_id}")
        
        # Test 5: Count records after insert
        print("5️⃣  Counting records after insert...")
        with db_manager.get_session() as session:
            final_count = session.query(HealthCheck).count()
            print(f"   📊 Total records now: {final_count}")
        
        # Test 6: Verify the insert worked
        if final_count == initial_count + 1:
            print("   ✅ Insert verified - count increased by 1")
        else:
            print("   ❌ Insert verification failed - count didn't increase correctly")
            return False
        
        # Test 7: Read the record we just inserted
        print("6️⃣  Reading back the inserted record...")
        with db_manager.get_session() as session:
            inserted_record = session.query(HealthCheck).filter_by(id=record_id).first()
            if inserted_record:
                print(f"   ✅ Found record: ID={inserted_record.id}, Note='{inserted_record.note[:50]}...'")
                print(f"   📅 Created at: {inserted_record.created_at}")
            else:
                print("   ❌ Could not find the inserted record")
                return False
        
        print("=" * 50)
        print("🎉 ALL SMOKE TESTS PASSED!")
        print(f"📊 Final count: {final_count} healthcheck records in database")
        return True
        
    except Exception as e:
        print(f"❌ SMOKE TEST FAILED: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

def main():
    """Main function"""
    print("DATABASE_URL:", os.getenv('DATABASE_URL', 'Not set'))
    print()
    
    success = smoke_test()
    
    if success:
        print("\n🟢 Smoke test completed successfully!")
        sys.exit(0)
    else:
        print("\n🔴 Smoke test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()