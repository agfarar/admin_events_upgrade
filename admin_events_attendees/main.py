from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

# Import modules
from database import create_tables
from auth_routes import router as auth_router
from attendee_routes import router as attendee_router
from middleware import (
    SecurityHeadersMiddleware, 
    RateLimitMiddleware, 
    RequestLoggingMiddleware
)
from config import DEBUG, HOST, PORT

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Admin Events Attendees API...")
    create_tables()
    print("Database tables created successfully")
    yield
    # Shutdown
    print("Shutting down Admin Events Attendees API...")

# Create FastAPI app
app = FastAPI(
    title="Admin Events - Attendees Microservice",
    description="""
    Microservicio de Asistentes para el sistema Admin Events.
    
    ## Funcionalidades de Seguridad
    
    * **Autenticación JWT**: Sistema de login/logout con tokens seguros
    * **Autorización basada en scopes**: Control granular de permisos
    * **MFA (Multi-Factor Authentication)**: Autenticación de dos factores opcional
    * **Auditoría completa**: Log de todas las acciones de usuarios
    * **Rate Limiting**: Protección contra ataques de fuerza bruta
    * **Headers de seguridad**: Protección XSS, clickjacking, etc.
    
    ## Funcionalidades de Negocio
    
    * **Gestión de Asistentes**: CRUD completo para asistentes a eventos
    * **Búsqueda avanzada**: Por documento, email, etc.
    * **Validaciones**: Documentos únicos, emails válidos, etc.
    """,
    version="1.0.0",
    contact={
        "name": "Admin Events Team",
        "email": "admin@events.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# Add security middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(attendee_router, prefix="/attendees", tags=["Attendees"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API Root endpoint with basic information"""
    return {
        "message": "Admin Events - Attendees Microservice",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "JWT Authentication",
            "Multi-Factor Authentication (MFA)",
            "Role-based Access Control",
            "Audit Logging",
            "Rate Limiting",
            "Security Headers"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "auth": "/auth",
            "attendees": "/attendees"
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
@app.head("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "attendees-microservice",
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors"""
    print(f"Global exception handler caught: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": "error"
        }
    )

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Endpoint not found: {request.url.path}",
            "type": "error"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info" if not DEBUG else "debug",
        access_log=True
    )
