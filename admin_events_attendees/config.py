from decouple import config

# JWT Configuration
JWT_SECRET_KEY = config("JWT_SECRET_KEY", default="your-super-secret-key-change-this-in-production")
JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
JWT_REFRESH_TOKEN_EXPIRE_DAYS = config("JWT_REFRESH_TOKEN_EXPIRE_DAYS", default=7, cast=int)

# Database Configuration
DATABASE_URL = config("DATABASE_URL", default="sqlite:///./attendees.db")

# Security
BCRYPT_ROUNDS = config("BCRYPT_ROUNDS", default=12, cast=int)

# Application
DEBUG = config("DEBUG", default=True, cast=bool)
HOST = config("HOST", default="0.0.0.0")
PORT = config("PORT", default=3000, cast=int)

# Rate Limiting
RATE_LIMIT_PER_MINUTE = config("RATE_LIMIT_PER_MINUTE", default=100, cast=int)

# MFA Configuration
MFA_ENABLED = config("MFA_ENABLED", default=False, cast=bool)
MFA_ISSUER = config("MFA_ISSUER", default="AdminEvents")
