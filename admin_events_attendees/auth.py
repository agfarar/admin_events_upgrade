import secrets
import pyotp
import qrcode
import io
import base64
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db, User, RefreshToken, AuditLog
from schemas import TokenData
from config import (
    JWT_SECRET_KEY, 
    JWT_ALGORITHM, 
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_TOKEN_EXPIRE_DAYS,
    BCRYPT_ROUNDS,
    MFA_ENABLED,
    MFA_ISSUER
)

# JWT Security
security = HTTPBearer()

class AuthService:
    def __init__(self):
        # Use bcrypt directly with configured rounds
        from config import BCRYPT_ROUNDS
        self.bcrypt_rounds = BCRYPT_ROUNDS
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            # Convert strings to bytes for bcrypt
            plain_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(plain_bytes, hashed_bytes)
        except (ValueError, TypeError):
            return False
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        # Convert password to bytes and hash with salt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: int, db: Session) -> str:
        """Create and store refresh token"""
        # Generate secure random token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Revoke existing refresh tokens for user
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).update({"is_revoked": True})
        
        # Create new refresh token
        refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at
        )
        db.add(refresh_token)
        db.commit()
        
        return token
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            token_type: str = payload.get("type", "access")
            
            if username is None or user_id is None:
                return None
            
            return TokenData(
                username=username, 
                user_id=user_id,
                scopes=payload.get("scopes", [])
            )
        except JWTError:
            return None
    
    def refresh_access_token(self, refresh_token: str, db: Session) -> Optional[Dict[str, Any]]:
        """Create new access token from refresh token"""
        # Find refresh token in database
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        ).first()
        
        if not db_token:
            return None
        
        # Get user
        user = db.query(User).filter(User.id == db_token.user_id).first()
        if not user or not user.is_active:
            return None
        
        # Create new access token
        access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username, "user_id": user.id, "scopes": self.get_user_scopes(user)},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    def revoke_refresh_token(self, refresh_token: str, db: Session) -> bool:
        """Revoke a refresh token"""
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token
        ).first()
        
        if db_token:
            db_token.is_revoked = True
            db.commit()
            return True
        return False
    
    def get_user_scopes(self, user: User) -> list[str]:
        """Get user permissions/scopes"""
        scopes = ["read:attendees"]
        if user.is_admin:
            scopes.extend(["write:attendees", "delete:attendees", "admin"])
        else:
            scopes.append("write:attendees")
        return scopes
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_account_locked(self, user: User) -> bool:
        """Check if user account is locked due to failed login attempts"""
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            return True
        return False
    
    def increment_login_attempts(self, user: User, db: Session):
        """Increment failed login attempts and lock account if necessary"""
        user.login_attempts += 1
        
        # Lock account after 5 failed attempts for 15 minutes
        if user.login_attempts >= 5:
            user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
        
        db.commit()
    
    def reset_login_attempts(self, user: User, db: Session):
        """Reset login attempts on successful login"""
        user.login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.now(timezone.utc)
        db.commit()

# MFA Service
class MFAService:
    def generate_secret(self) -> str:
        """Generate MFA secret"""
        return pyotp.random_base32()
    
    def generate_qr_code(self, secret: str, username: str) -> str:
        """Generate QR code for MFA setup"""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name=MFA_ISSUER
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def verify_mfa_code(self, secret: str, code: str) -> bool:
        """Verify MFA code"""
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)

# Audit Service
class AuditService:
    def log_action(
        self, 
        db: Session, 
        action: str, 
        user_id: Optional[int] = None,
        resource: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[str] = None
    ):
        """Log user action for audit trail"""
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        db.add(audit_log)
        db.commit()

# Dependency instances
auth_service = AuthService()
mfa_service = MFAService()
audit_service = AuditService()

# Dependencies for route protection
async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if credentials is None:
        # Log failed authentication attempt
        audit_service.log_action(
            db=db,
            action="AUTH_FAILED",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Missing authorization header"
        )
        raise credentials_exception
    
    token_data = auth_service.verify_token(credentials.credentials)
    if token_data is None:
        # Log failed authentication attempt
        audit_service.log_action(
            db=db,
            action="AUTH_FAILED",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Invalid token"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current authenticated admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

def require_scope(required_scope: str):
    """Decorator to require specific scope"""
    async def scope_checker(
        request: Request,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
    ):
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = auth_service.verify_token(credentials.credentials)
        if not token_data or required_scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required scope: {required_scope}"
            )
        return token_data
    return scope_checker
