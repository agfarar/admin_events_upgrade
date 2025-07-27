"""
Script para crear un usuario administrador inicial
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal, User, create_tables
from auth import auth_service
import getpass

def create_admin_user():
    """Create initial admin user"""
    # Create tables if they don't exist
    create_tables()
    
    db = SessionLocal()
    
    try:
        print("=== Admin Events - Crear Usuario Administrador ===")
        print()
        
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            print(f"Ya existe un usuario administrador: {existing_admin.username}")
            response = input("¿Desea crear otro administrador? (s/N): ").lower()
            if response != 's':
                return
        
        # Get user input
        username = input("Nombre de usuario: ").strip()
        if not username:
            print("Error: El nombre de usuario es requerido")
            return
        
        # Check if username exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"Error: El usuario {username} ya existe")
            return
        
        email = input("Email: ").strip()
        if not email or '@' not in email:
            print("Error: Email válido es requerido")
            return
        
        # Check if email exists
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            print(f"Error: El email {email} ya está registrado")
            return
        
        password = getpass.getpass("Contraseña: ")
        password_confirm = getpass.getpass("Confirmar contraseña: ")
        
        if password != password_confirm:
            print("Error: Las contraseñas no coinciden")
            return
        
        if len(password) < 8:
            print("Error: La contraseña debe tener al menos 8 caracteres")
            return
        
        # Create admin user
        hashed_password = auth_service.get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print()
        print("✅ Usuario administrador creado exitosamente!")
        print(f"Usuario: {username}")
        print(f"Email: {email}")
        print("Permisos: Administrador")
        print()
        print("Puede iniciar sesión usando estos credenciales en /auth/login")
        
    except Exception as e:
        db.rollback()
        print(f"Error creando usuario administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
