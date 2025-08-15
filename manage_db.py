#!/usr/bin/env python3
"""
Database management script for Study App
"""

import os
import sys
from app import app, db, User, Note, UserActivity, PDFDocument
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Initialize the database and create tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def create_admin_user():
    """Create an admin user for testing"""
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("⚠️  Admin user already exists!")
            return
        
        admin = User(
            username='admin',
            email='admin@studyapp.com',
            password_hash=generate_password_hash('admin123'),
            points=100,
            time_spent=120,
            created_at=datetime.utcnow(),
            preferences='{}'
        )
        
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")

def reset_database():
    """Reset the database (delete all data)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database reset successfully!")

def show_database_info():
    """Show database information"""
    with app.app_context():
        user_count = User.query.count()
        note_count = Note.query.count()
        activity_count = UserActivity.query.count()
        pdf_count = PDFDocument.query.count()
        
        print("📊 Database Information:")
        print(f"   Users: {user_count}")
        print(f"   Notes: {note_count}")
        print(f"   Activities: {activity_count}")
        print(f"   PDF Documents: {pdf_count}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_db.py [command]")
        print("Commands:")
        print("  init     - Initialize database tables")
        print("  admin    - Create admin user")
        print("  reset    - Reset database (delete all data)")
        print("  info     - Show database information")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_database()
    elif command == 'admin':
        create_admin_user()
    elif command == 'reset':
        confirm = input("⚠️  This will delete all data. Are you sure? (y/N): ")
        if confirm.lower() == 'y':
            reset_database()
        else:
            print("❌ Database reset cancelled.")
    elif command == 'info':
        show_database_info()
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == '__main__':
    main()