from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from database import get_db, User
from schemas import (
    UserCreate, UserLogin, UserResponse, Token, RefreshTokenRequest,
    MFASetupResponse, MFAVerificationRequest, PasswordChangeRequest,
    AuditLogResponse
)
from auth import (
    auth_service, mfa_service, audit_service, get_current_user, 
    get_current_admin_user, security
)
from config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, MFA_ENABLED

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        audit_service.log_action(
            db=db,
            action="REGISTER_FAILED",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Username already exists: {user.username}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        audit_service.log_action(
            db=db,
            action="REGISTER_FAILED",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Email already exists: {user.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = auth_service.get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Log successful registration
    audit_service.log_action(
        db=db,
        action="USER_REGISTERED",
        user_id=db_user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details=f"User registered: {user.username}"
    )
    
    return db_user

@router.post("/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Authenticate user and return tokens"""
    user = auth_service.authenticate_user(db, user_credentials.username, user_credentials.password)
    
    if not user:
        audit_service.log_action(
            db=db,
            action="LOGIN_FAILED",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Invalid credentials for: {user_credentials.username}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        audit_service.log_action(
            db=db,
            action="LOGIN_FAILED",
            user_id=user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Inactive user attempted login"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # Check if account is locked
    if auth_service.is_account_locked(user):
        audit_service.log_action(
            db=db,
            action="LOGIN_FAILED",
            user_id=user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Account locked - too many failed attempts"
        )
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account temporarily locked due to too many failed login attempts"
        )
    
    # Check MFA if enabled
    if MFA_ENABLED and user.mfa_enabled:
        if not user_credentials.mfa_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA code required"
            )
        
        if not mfa_service.verify_mfa_code(user.mfa_secret, user_credentials.mfa_code):
            auth_service.increment_login_attempts(user, db)
            audit_service.log_action(
                db=db,
                action="MFA_FAILED",
                user_id=user.id,
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent"),
                details="Invalid MFA code"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA code"
            )
    
    # Reset login attempts on successful authentication
    auth_service.reset_login_attempts(user, db)
    
    # Create tokens
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = auth_service.get_user_scopes(user)
    
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "user_id": user.id, "scopes": scopes},
        expires_delta=access_token_expires
    )
    
    refresh_token = auth_service.create_refresh_token(user.id, db)
    
    # Log successful login
    audit_service.log_action(
        db=db,
        action="LOGIN_SUCCESS",
        user_id=user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details="User logged in successfully"
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh", response_model=dict)
async def refresh_token(
    token_request: RefreshTokenRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    result = auth_service.refresh_access_token(token_request.refresh_token, db)
    
    if not result:
        audit_service.log_action(
            db=db,
            action="TOKEN_REFRESH_FAILED",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Invalid refresh token"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    return result

@router.post("/logout")
async def logout_user(
    token_request: RefreshTokenRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user and revoke refresh token"""
    auth_service.revoke_refresh_token(token_request.refresh_token, db)
    
    audit_service.log_action(
        db=db,
        action="LOGOUT",
        user_id=current_user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details="User logged out"
    )
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/change-password")
async def change_password(
    password_request: PasswordChangeRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    # Verify current password
    if not auth_service.verify_password(password_request.current_password, current_user.hashed_password):
        audit_service.log_action(
            db=db,
            action="PASSWORD_CHANGE_FAILED",
            user_id=current_user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Invalid current password"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.hashed_password = auth_service.get_password_hash(password_request.new_password)
    db.commit()
    
    # Revoke all refresh tokens to force re-login
    from database import RefreshToken
    db.query(RefreshToken).filter(RefreshToken.user_id == current_user.id).update(
        {"is_revoked": True}
    )
    db.commit()
    
    audit_service.log_action(
        db=db,
        action="PASSWORD_CHANGED",
        user_id=current_user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details="Password changed successfully"
    )
    
    return {"message": "Password changed successfully"}

# MFA endpoints
@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Setup MFA for user"""
    if not MFA_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled on this server"
        )
    
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled for this user"
        )
    
    # Generate secret
    secret = mfa_service.generate_secret()
    qr_code = mfa_service.generate_qr_code(secret, current_user.username)
    
    # Store secret temporarily (not enabled until verified)
    current_user.mfa_secret = secret
    db.commit()
    
    return {
        "secret": secret,
        "qr_code_url": qr_code
    }

@router.post("/mfa/verify")
async def verify_mfa_setup(
    mfa_request: MFAVerificationRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verify and enable MFA"""
    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA setup not initiated"
        )
    
    if not mfa_service.verify_mfa_code(current_user.mfa_secret, mfa_request.mfa_code):
        audit_service.log_action(
            db=db,
            action="MFA_SETUP_FAILED",
            user_id=current_user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Invalid MFA verification code"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA code"
        )
    
    # Enable MFA
    current_user.mfa_enabled = True
    db.commit()
    
    audit_service.log_action(
        db=db,
        action="MFA_ENABLED",
        user_id=current_user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details="MFA enabled for user"
    )
    
    return {"message": "MFA enabled successfully"}

@router.post("/mfa/disable")
async def disable_mfa(
    mfa_request: MFAVerificationRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disable MFA for user"""
    if not current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled for this user"
        )
    
    if not mfa_service.verify_mfa_code(current_user.mfa_secret, mfa_request.mfa_code):
        audit_service.log_action(
            db=db,
            action="MFA_DISABLE_FAILED",
            user_id=current_user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details="Invalid MFA code for disable attempt"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA code"
        )
    
    # Disable MFA
    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    db.commit()
    
    audit_service.log_action(
        db=db,
        action="MFA_DISABLED",
        user_id=current_user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details="MFA disabled for user"
    )
    
    return {"message": "MFA disabled successfully"}

# Admin endpoints
@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get audit logs (admin only)"""
    from database import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users
