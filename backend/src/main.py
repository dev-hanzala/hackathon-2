"""FastAPI application initialization."""

import logging
import os
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.health import router as health_router
from src.api.v1 import router as v1_router
from src.config import settings
from src.db.database import init_db
from src.middleware.logging_middleware import LoggingMiddleware, setup_logging

# Setup logging first
setup_logging(log_level="DEBUG" if settings.debug else "INFO")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="""
## Todo Application API

A RESTful API for managing todo tasks with user authentication.

### Features
- **User Authentication**: JWT-based registration and signin
- **Task Management**: Create, read, update, delete, and complete tasks
- **Data Isolation**: Users can only access their own tasks
- **Performance**: Optimized queries with composite indexes (<2s for 100+ tasks)
- **Monitoring**: Comprehensive logging for request tracking and debugging

### Authentication
All task endpoints require authentication via JWT Bearer token.

1. Register a new user: `POST /api/v1/auth/register`
2. Sign in: `POST /api/v1/auth/signin`
3. Include the returned `access_token` in subsequent requests:
   ```
   Authorization: Bearer <access_token>
   ```

### API Versions
- **Current**: v1
- **Base URL**: `/api/v1`

### Error Responses
All endpoints follow consistent error response format:
```json
{
  "detail": "Error message description"
}
```

**Status Codes:**
- `200` - Success
- `201` - Created
- `204` - No Content (successful deletion)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (e.g., email already registered)
- `500` - Internal Server Error

### Rate Limiting
Currently no rate limiting. Production deployment should add rate limiting middleware.

### Support
- **Repository**: https://github.com/your-org/hackathon-2
- **Documentation**: See `/docs` for interactive API documentation
- **Health Check**: `GET /health`
    """,
    version="0.1.0",
    debug=settings.debug,
    # OpenAPI documentation URLs
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    # API metadata
    contact={
        "name": "Todo API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    # OpenAPI tags for grouping endpoints
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and status endpoints",
        },
        {
            "name": "auth",
            "description": "User authentication operations (register, signin, logout)",
        },
        {
            "name": "tasks",
            "description": "Task management operations (CRUD operations)",
        },
    ],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database and run migrations on startup."""
    try:
        # Run Alembic migrations using subprocess to avoid import conflicts
        logger.info("Running database migrations...")

        # Get the path to backend directory
        backend_dir = Path(__file__).parent.parent
        alembic_ini_path = backend_dir / "alembic.ini"

        if alembic_ini_path.exists():
            # Run alembic upgrade head using subprocess
            result = subprocess.run(
                [sys.executable, "-m", "alembic", "upgrade", "head"],
                cwd=str(backend_dir),
                capture_output=True,
                text=True,
                env={**dict(os.environ), "DATABASE_URL": settings.database_url},
            )

            if result.returncode == 0:
                logger.info("✅ Database migrations applied successfully")
                if result.stdout:
                    logger.debug(result.stdout)
            else:
                logger.error(f"❌ Migration failed: {result.stderr}")
                logger.info("Falling back to manual table initialization...")
        else:
            logger.warning(f"⚠️ alembic.ini not found at {alembic_ini_path}, skipping migrations")

    except Exception as e:
        logger.error(f"❌ Failed to run migrations: {e}")
        logger.info("Falling back to manual table initialization...")

    # Fallback: Ensure tables exist (for development/testing)
    try:
        init_db()
        logger.info("✅ Database tables initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware (T151)
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health_router)
app.include_router(v1_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Todo API", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
