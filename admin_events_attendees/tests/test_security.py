import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db, User, Attendee
from main import app
from auth import auth_service

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    hashed_password = auth_service.get_password_hash("testpassword123")
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    
    # Clean up refresh tokens first to avoid foreign key constraint violation
    from database import RefreshToken
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()
    db.commit()
    
    # Now we can safely delete the user
    db.delete(user)
    db.commit()
    db.close()

@pytest.fixture
def admin_user():
    db = TestingSessionLocal()
    hashed_password = auth_service.get_password_hash("adminpassword123")
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hashed_password,
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    
    # Clean up refresh tokens first to avoid foreign key constraint violation
    from database import RefreshToken
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()
    db.commit()
    
    # Now we can safely delete the user
    db.delete(user)
    db.commit()
    db.close()

@pytest.fixture
def user_token(client, test_user):
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    return token_data["access_token"]

@pytest.fixture
def admin_token(client, admin_user):
    login_data = {
        "username": "admin",
        "password": "adminpassword123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    return token_data["access_token"]

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self, client, setup_database):
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "NewPassword123",
            "is_admin": False
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        assert response.json()["username"] == "newuser"
        assert response.json()["email"] == "newuser@example.com"
    
    def test_register_duplicate_user(self, client, test_user):
        user_data = {
            "username": "testuser",  # Same as existing user
            "email": "different@example.com",
            "password": "NewPassword123",
            "is_admin": False
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_valid_user(self, client, test_user):
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data
        assert token_data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client, test_user):
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_get_current_user(self, client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == "testuser"
    
    def test_change_password(self, client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        password_data = {
            "current_password": "testpassword123",
            "new_password": "NewPassword456"
        }
        response = client.post("/auth/change-password", json=password_data, headers=headers)
        assert response.status_code == 200

class TestAttendees:
    """Test attendee endpoints"""
    
    def test_create_attendee(self, client, user_token, setup_database):
        headers = {"Authorization": f"Bearer {user_token}"}
        attendee_data = {
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "document_type": "DNI",
            "document_number": "12345678",
            "phone_number": "555-1234",
            "address": "Calle 123",
            "gender": "M"
        }
        response = client.post("/attendees/", json=attendee_data, headers=headers)
        assert response.status_code == 201
        assert response.json()["name"] == "Juan Pérez"
    
    def test_create_attendee_duplicate_document(self, client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        attendee_data = {
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "document_type": "DNI",
            "document_number": "12345678",  # Same as previous test
            "phone_number": "555-1234"
        }
        response = client.post("/attendees/", json=attendee_data, headers=headers)
        assert response.status_code == 400
        response_detail = response.json()["detail"]
        assert "already exists" in response_detail or "Error creating attendee" in response_detail
    
    def test_get_attendees(self, client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/attendees/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_attendee_by_id(self, client, user_token):
        headers = {"Authorization": f"Bearer {user_token}"}
        # First create an attendee
        attendee_data = {
            "name": "María García",
            "email": "maria@example.com",
            "document_type": "DNI",
            "document_number": "87654321",
            "phone_number": "555-5678"
        }
        create_response = client.post("/attendees/", json=attendee_data, headers=headers)
        attendee_id = create_response.json()["attendee_id"]
        
        # Get the attendee
        response = client.get(f"/attendees/{attendee_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == "María García"
    
    def test_unauthorized_access(self, client):
        response = client.get("/attendees/")
        assert response.status_code in [401, 403]  # Accept both 401 and 403

class TestSecurity:
    """Test security features"""
    
    def test_rate_limiting(self, client, user_token):
        """Test rate limiting (simplified test)"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Make many requests quickly
        responses = []
        for _ in range(5):
            response = client.get("/attendees/", headers=headers)
            responses.append(response.status_code)
        
        # All should succeed with normal rate limiting
        assert all(status == 200 for status in responses)
    
    def test_security_headers(self, client):
        response = client.get("/")
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
    
    def test_admin_only_endpoints(self, client, user_token, admin_token):
        # Regular user should not access admin endpoints
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/auth/audit-logs", headers=headers)
        assert response.status_code == 403
        
        # Admin user should access admin endpoints
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/auth/audit-logs", headers=admin_headers)
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__])
