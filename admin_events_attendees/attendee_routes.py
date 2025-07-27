from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from database import get_db, Attendee
from schemas import AttendeeCreate, AttendeeUpdate, AttendeeResponse
from auth import get_current_user, require_scope, audit_service

router = APIRouter()

@router.post("/", response_model=AttendeeResponse, status_code=status.HTTP_201_CREATED)
async def create_attendee(
    attendee: AttendeeCreate,
    request: Request,
    current_user = Depends(get_current_user),
    _: str = Depends(require_scope("write:attendees")),
    db: Session = Depends(get_db)
):
    """Create a new attendee (requires authentication and write:attendees scope)"""
    try:
        # Check if attendee with same document already exists
        existing_attendee = db.query(Attendee).filter(
            Attendee.document_type == attendee.document_type,
            Attendee.document_number == attendee.document_number
        ).first()
        
        if existing_attendee:
            audit_service.log_action(
                db=db,
                action="CREATE_ATTENDEE_FAILED",
                user_id=current_user.id,
                resource="attendees",
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent"),
                details=f"Duplicate document: {attendee.document_type} - {attendee.document_number}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendee with this document already exists"
            )
        
        # Create new attendee
        attendee_data = attendee.model_dump() if hasattr(attendee, 'model_dump') else attendee.dict()
        db_attendee = Attendee(**attendee_data)
        db.add(db_attendee)
        db.commit()
        db.refresh(db_attendee)
        
        # Log successful creation
        audit_service.log_action(
            db=db,
            action="CREATE_ATTENDEE",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Created attendee: {db_attendee.name} (ID: {db_attendee.attendee_id})"
        )
        
        return db_attendee
        
    except HTTPException:
        # Re-raise HTTPExceptions (like duplicate document)
        raise
    except Exception as e:
        db.rollback()
        error_message = str(e) if str(e) else "Unknown database error occurred"
        audit_service.log_action(
            db=db,
            action="CREATE_ATTENDEE_ERROR",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Error creating attendee: {error_message}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating attendee: {error_message}"
        )

@router.get("/", response_model=List[AttendeeResponse])
async def get_all_attendees(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    _: str = Depends(require_scope("read:attendees")),
    db: Session = Depends(get_db)
):
    """Get all attendees with pagination (requires authentication and read:attendees scope)"""
    try:
        attendees = db.query(Attendee).offset(skip).limit(limit).all()
        
        # Log access
        audit_service.log_action(
            db=db,
            action="READ_ATTENDEES",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Retrieved {len(attendees)} attendees (skip: {skip}, limit: {limit})"
        )
        
        return attendees
        
    except Exception as e:
        audit_service.log_action(
            db=db,
            action="READ_ATTENDEES_ERROR",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Error retrieving attendees: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving attendees"
        )

@router.get("/{attendee_id}", response_model=AttendeeResponse)
async def get_attendee(
    attendee_id: int,
    request: Request,
    current_user = Depends(get_current_user),
    _: str = Depends(require_scope("read:attendees")),
    db: Session = Depends(get_db)
):
    """Get a specific attendee by ID (requires authentication and read:attendees scope)"""
    attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    
    if attendee is None:
        audit_service.log_action(
            db=db,
            action="READ_ATTENDEE_NOT_FOUND",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Attendee not found: {attendee_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee not found"
        )
    
    # Log access
    audit_service.log_action(
        db=db,
        action="READ_ATTENDEE",
        user_id=current_user.id,
        resource="attendees",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details=f"Retrieved attendee: {attendee.name} (ID: {attendee_id})"
    )
    
    return attendee

@router.put("/{attendee_id}", response_model=AttendeeResponse)
async def update_attendee(
    attendee_id: int,
    attendee_update: AttendeeUpdate,
    request: Request,
    current_user = Depends(get_current_user),
    _: str = Depends(require_scope("write:attendees")),
    db: Session = Depends(get_db)
):
    """Update an attendee (requires authentication and write:attendees scope)"""
    db_attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    
    if db_attendee is None:
        audit_service.log_action(
            db=db,
            action="UPDATE_ATTENDEE_NOT_FOUND",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent"),
            details=f"Attendee not found for update: {attendee_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee not found"
        )
    
    try:
        # Check for duplicate document if document info is being updated
        if attendee_update.document_type or attendee_update.document_number:
            new_doc_type = attendee_update.document_type or db_attendee.document_type
            new_doc_number = attendee_update.document_number or db_attendee.document_number
            
            # Only check if the document is actually changing
            if (new_doc_type != db_attendee.document_type or 
                new_doc_number != db_attendee.document_number):
                
                existing_attendee = db.query(Attendee).filter(
                    Attendee.document_type == new_doc_type,
                    Attendee.document_number == new_doc_number,
                    Attendee.attendee_id != attendee_id
                ).first()
                
                if existing_attendee:
                    audit_service.log_action(
                        db=db,
                        action="UPDATE_ATTENDEE_FAILED",
                        user_id=current_user.id,
                        resource="attendees",
                        ip_address=request.client.host if request.client else "unknown",
                        user_agent=request.headers.get("user-agent"),
                        details=f"Duplicate document on update: {new_doc_type} - {new_doc_number}"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Another attendee with this document already exists"
                    )
        
        # Update fields
        attendee_data = attendee_update.dict(exclude_unset=True)
        for key, value in attendee_data.items():
            setattr(db_attendee, key, value)
        
        db_attendee.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_attendee)
        
        # Log successful update
        audit_service.log_action(
            db=db,
            action="UPDATE_ATTENDEE",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent"),
            details=f"Updated attendee: {db_attendee.name} (ID: {attendee_id})"
        )
        
        return db_attendee
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        audit_service.log_action(
            db=db,
            action="UPDATE_ATTENDEE_ERROR",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent"),
            details=f"Error updating attendee {attendee_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating attendee: {str(e)}"
        )

@router.delete("/{attendee_id}")
async def delete_attendee(
    attendee_id: int,
    request: Request,
    current_user = Depends(get_current_user),
    _: str = Depends(require_scope("delete:attendees")),
    db: Session = Depends(get_db)
):
    """Delete an attendee (requires authentication and delete:attendees scope - admin only)"""
    db_attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    
    if db_attendee is None:
        audit_service.log_action(
            db=db,
            action="DELETE_ATTENDEE_NOT_FOUND",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Attendee not found for deletion: {attendee_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee not found"
        )
    
    try:
        attendee_name = db_attendee.name
        db.delete(db_attendee)
        db.commit()
        
        # Log successful deletion
        audit_service.log_action(
            db=db,
            action="DELETE_ATTENDEE",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Deleted attendee: {attendee_name} (ID: {attendee_id})"
        )
        
        return {"message": f"Attendee {attendee_name} deleted successfully"}
        
    except Exception as e:
        db.rollback()
        audit_service.log_action(
            db=db,
            action="DELETE_ATTENDEE_ERROR",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Error deleting attendee {attendee_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting attendee: {str(e)}"
        )

@router.get("/search/by-document/{document_type}/{document_number}", response_model=AttendeeResponse)
async def search_attendee_by_document(
    document_type: str,
    document_number: str,
    request: Request,
    current_user = Depends(get_current_user),
    _: str = Depends(require_scope("read:attendees")),
    db: Session = Depends(get_db)
):
    """Search attendee by document type and number (requires authentication and read:attendees scope)"""
    attendee = db.query(Attendee).filter(
        Attendee.document_type == document_type,
        Attendee.document_number == document_number
    ).first()
    
    if attendee is None:
        audit_service.log_action(
            db=db,
            action="SEARCH_ATTENDEE_NOT_FOUND",
            user_id=current_user.id,
            resource="attendees",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details=f"Attendee not found by document: {document_type} - {document_number}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee not found"
        )
    
    # Log successful search
    audit_service.log_action(
        db=db,
        action="SEARCH_ATTENDEE",
        user_id=current_user.id,
        resource="attendees",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details=f"Found attendee by document: {attendee.name} ({document_type} - {document_number})"
    )
    
    return attendee

@router.get("/search/by-email/{email}", response_model=List[AttendeeResponse])
async def search_attendees_by_email(
    email: str,
    request: Request,
    current_user = Depends(get_current_user),
    _: str = Depends(require_scope("read:attendees")),
    db: Session = Depends(get_db)
):
    """Search attendees by email (requires authentication and read:attendees scope)"""
    attendees = db.query(Attendee).filter(Attendee.email.ilike(f"%{email}%")).all()
    
    # Log search
    audit_service.log_action(
        db=db,
        action="SEARCH_ATTENDEES_BY_EMAIL",
        user_id=current_user.id,
        resource="attendees",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details=f"Email search: {email}, found {len(attendees)} results"
    )
    
    return attendees
