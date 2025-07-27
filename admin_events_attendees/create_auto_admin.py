#!/usr/bin/env python3
"""
Script automático para crear un usuario administrador
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, User, create_tables
from auth import auth_service

def create_auto_admin():
    """Create admin user automatically"""
    # Create tables if they don't exist
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            print(f"✅ Ya existe un usuario administrador: {existing_admin.username}")
            return existing_admin
        
        # Create admin user automatically
        username = "admin"
        email = "admin@admin.com"
        password = "admin123456"  # Contraseña temporal
        
        # Check if username already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            print(f"✅ Usuario ya existe: {existing_user.username}")
            # Make sure user is admin
            if not existing_user.is_admin:
                existing_user.is_admin = True
                db.commit()
                print(f"✅ Usuario convertido a administrador")
            return existing_user
        
        # Create user manually using the same logic as register endpoint
        hashed_password = auth_service.get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"✅ Usuario administrador creado exitosamente:")
        print(f"   - Usuario: {username}")
        print(f"   - Email: {email}")
        print(f"   - Contraseña: {password}")
        print(f"   - ID: {db_user.id}")
        print(f"   - Admin: {db_user.is_admin}")
        print()
        print("⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
        return db_user
        
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    create_auto_admin()
