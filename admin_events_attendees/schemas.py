from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Authentication schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    is_admin: bool = False
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserLogin(BaseModel):
    username: str
    password: str
    mfa_code: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]
    mfa_enabled: bool
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    scopes: List[str] = []

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# MFA schemas
class MFASetupResponse(BaseModel):
    secret: str
    qr_code_url: str

class MFAVerificationRequest(BaseModel):
    mfa_code: str

# Password change schemas
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

# Attendee schemas (from original system)
class DocumentType(str, Enum):
    DNI = "DNI"
    PASAPORTE = "Pasaporte"
    CARNE_EXTRANJERIA = "Carné de Extranjería"
    OTROS = "Otros"

class Gender(str, Enum):
    M = "M"
    F = "F"
    O = "O"

class AttendeeBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    document_type: DocumentType = DocumentType.DNI
    document_number: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None

class AttendeeCreate(AttendeeBase):
    pass

class AttendeeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    document_type: Optional[DocumentType] = None
    document_number: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None

class AttendeeResponse(AttendeeBase):
    attendee_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

# Audit log schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    resource: Optional[str]
    ip_address: Optional[str]
    timestamp: datetime
    details: Optional[str]
    
    class Config:
        orm_mode = True
