#!/usr/bin/env python3
"""
Database Seeder for Rohis Management System
Supports both SQLite (dev) and PostgreSQL (production)
"""
import os
import sys
from app import app, db, bcrypt
from models import User

# Default password for all initial accounts
INITIAL_PASSWORD = "rohis2026"

# Member data - Update this with your actual members
members = [
    {"email": "muhammad.syathir@gdajogja.sch.id", "name": "Muhammad Syathir", "class": "10-D", "role": "admin"},
    {"email": "aqillah.hasanah@gdajogja.sch.id", "name": "Aqillah Hasanah", "class": "10-C", "role": "admin"},
    {"email": "ghozy.suciawan@gdajogja.sch.id", "name": "Ghozy Suciawan", "class": "10-D", "role": "ketua"},
    {"email": "haidar.nasirodin@gdajogja.sch.id", "name": "Haidar Nasirodin", "class": "10-A", "role": "admin"},
    {"email": "khoirun.istiqomah@gdajogja.sch.id", "name": "Khoirun Istiqomah", "class": "10-C", "role": "admin"},
    {"email": "mufadilla.legisa@gdajogja.sch.id", "name": "Mufadilla Legisa", "class": "10-B", "role": "admin"},
    {"email": "rauf.akmal@gdajogja.sch.id", "name": "Rauf Akmal", "class": "10-A", "role": "admin"},
    {"email": "rifqy.daaris@gdajogja.sch.id", "name": "Rifqy Daaris", "class": "10-A", "role": "admin"},
    {"email": "aiesha.makaila@gdajogja.sch.id", "name": "Aiesha Makaila", "class": "10-D", "role": "member"},
    {"email": "arya.rahadian@gdajogja.sch.id", "name": "Arya Rahadian", "class": "10-B", "role": "member"},
    {"email": "aulia.meilinda@gdajogja.sch.id", "name": "Aulia Meilinda", "class": "10-A", "role": "member"},
    {"email": "devone.nalandra@gdajogja.sch.id", "name": "Devone Nalandra", "class": "10-B", "role": "member"},
    {"email": "dzakya.prasetya@gdajogja.sch.id", "name": "Dzakya Prasetya", "class": "10-A", "role": "member"},
    {"email": "evan.farizqi@gdajogja.sch.id", "name": "Evan Farizqi", "class": "10-B", "role": "member"},
    {"email": "faiq.asyam@gdajogja.sch.id", "name": "Faiq Asyam", "class": "10-A", "role": "member"},
    {"email": "hammam.prasetyo@gdajogja.sch.id", "name": "Hammam Prasetyo", "class": "10-B", "role": "member"},
    {"email": "husein.syamil@gdajogja.sch.id", "name": "Husein Syamil", "class": "10-C", "role": "member"},
    {"email": "irfan.ansari@gdajogja.sch.id", "name": "Irfan Ansari", "class": "10-B", "role": "member"},
    {"email": "kemas.tamada@gdajogja.sch.id", "name": "Kemas Tamada", "class": "10-D", "role": "member"},
    {"email": "muhammad.ismoyo@gdajogja.sch.id", "name": "Muhammad Ismoyo", "class": "10-D", "role": "member"},
    {"email": "nabila.patricia@gdajogja.sch.id", "name": "Nabila Patricia", "class": "10-A", "role": "member"},
    {"email": "naufal.syuja@gdajogja.sch.id", "name": "Naufal Syuja", "class": "10-D", "role": "member"},
    {"email": "tengku.harahap@gdajogja.sch.id", "name": "Tengku Harahap", "class": "10-B", "role": "member"},
    {"email": "zahra.layla@gdajogja.sch.id", "name": "Zahra Layla", "class": "10-D", "role": "member"},
    {"email": "zalfa.zahira@gdajogja.sch.id", "name": "Zalfa Zahira", "class": "10-C", "role": "member"},
]

def check_database_connection():
    """Verify database connection before seeding"""
    try:
        with app.app_context():
            # Try to connect to database
            db.engine.connect()
            db_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')
            
            # Hide password in output
            if 'postgresql://' in db_url or 'postgres://' in db_url:
                db_type = "PostgreSQL (Production)"
            elif 'sqlite:///' in db_url:
                db_type = "SQLite (Development)"
            else:
                db_type = "Unknown"
            
            print(f"✅ Database connection successful!")
            print(f"📊 Database type: {db_type}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if DATABASE_URL environment variable is set")
        print("2. Verify database credentials are correct")
        print("3. Ensure database migrations have been run: flask db upgrade")
        return False

def seed_members():
    """Seed the database with initial member data"""
    with app.app_context():
        print("\n" + "="*60)
        print("🌱 ROHIS DATABASE SEEDER")
        print("="*60 + "\n")
        
        # Check database connection
        if not check_database_connection():
            sys.exit(1)
        
        # Create tables if they don't exist (PostgreSQL safe)
        try:
            db.create_all()
            print("✅ Database tables verified/created\n")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            print("💡 Try running: flask db upgrade")
            sys.exit(1)
        
        # Seed members
        added_count = 0
        skipped_count = 0
        error_count = 0
        
        print(f"📝 Processing {len(members)} members...\n")
        
        for m in members:
            try:
                # Check if user already exists
                existing = User.query.filter_by(email=m["email"]).first()
                if existing:
                    print(f"⏭️  Skipped (exists): {m['name']} ({m['email']})")
                    skipped_count += 1
                    continue
                
                # Hash password
                hashed_pw = bcrypt.generate_password_hash(
                    INITIAL_PASSWORD
                ).decode("utf-8")
                
                # Create new user
                user = User(
                    email=m["email"],
                    password=hashed_pw,
                    name=m["name"],
                    class_name=m["class"],
                    role=m["role"],
                    must_change_password=True
                )
                
                db.session.add(user)
                print(f"✅ Added: {m['name']} ({m['role']}) - {m['email']}")
                added_count += 1
                
            except Exception as e:
                print(f"❌ Error adding {m['email']}: {e}")
                error_count += 1
                continue
        
        # Commit all changes
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("📊 SEEDING SUMMARY")
            print("="*60)
            print(f"✅ Successfully added: {added_count} users")
            print(f"⏭️  Skipped (existing): {skipped_count} users")
            if error_count > 0:
                print(f"❌ Errors: {error_count} users")
            print(f"\n🔑 Initial password for all users: '{INITIAL_PASSWORD}'")
            print("⚠️  Users must change password on first login")
            print("="*60 + "\n")
            
            if added_count > 0:
                print("🎉 Seeding completed successfully!\n")
                
                # Show admin accounts
                admin_users = [m for m in members if m["role"] in ["admin", "ketua", "pembina"]]
                if admin_users:
                    print("👑 ADMIN ACCOUNTS:")
                    for admin in admin_users:
                        print(f"   📧 {admin['email']} ({admin['role']})")
                    print()
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Database commit failed: {e}")
            print("All changes have been rolled back.")
            sys.exit(1)

def clear_database():
    """Clear all users from database (use with caution!)"""
    with app.app_context():
        response = input("\n⚠️  WARNING: This will delete ALL users from the database!\n"
                        "Are you sure? Type 'YES' to confirm: ")
        
        if response != "YES":
            print("❌ Operation cancelled.")
            return
        
        try:
            count = User.query.delete()
            db.session.commit()
            print(f"✅ Deleted {count} users from database.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error clearing database: {e}")

def show_stats():
    """Show database statistics"""
    with app.app_context():
        try:
            total_users = User.query.count()
            admins = User.query.filter_by(role='admin').count()
            ketua = User.query.filter_by(role='ketua').count()
            pembina = User.query.filter_by(role='pembina').count()
            members = User.query.filter_by(role='member').count()
            
            print("\n" + "="*60)
            print("📊 DATABASE STATISTICS")
            print("="*60)
            print(f"Total Users: {total_users}")
            print(f"  👑 Admins: {admins}")
            print(f"  👑 Ketua: {ketua}")
            print(f"  👔 Pembina: {pembina}")
            print(f"  👤 Members: {members}")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"❌ Error fetching statistics: {e}")

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "seed":
            seed_members()
        elif command == "clear":
            clear_database()
        elif command == "stats":
            show_stats()
        elif command == "help":
            print("\n" + "="*60)
            print("ROHIS DATABASE SEEDER - USAGE")
            print("="*60)
            print("python seeder.py seed   - Seed database with initial data")
            print("python seeder.py stats  - Show database statistics")
            print("python seeder.py clear  - Clear all users (DANGEROUS!)")
            print("python seeder.py help   - Show this help message")
            print("="*60 + "\n")
        else:
            print(f"❌ Unknown command: {command}")
            print("Run 'python seeder.py help' for usage information")
    else:
        # Default: run seeder
        seed_members()