"""
LinkedInsight FastAPI Application.

Main entry point for the LinkedInsight API. This module:
- Initializes the FastAPI application
- Sets up database connection and tables
- Registers all API routers
- Configures CORS middleware
- Provides health check and system test endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai, skills, jobs
from app.db.sql import init_db

# Initialize FastAPI application
app = FastAPI(
    title="LinkedInsight",
    description="AI-powered career & skills navigator",
    version="0.1.0",
)

# Configure CORS middleware
# Allows requests from localhost and typical development origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:8000",  # FastAPI default
        "http://localhost:8080",  # Alternative dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],   # Allow all headers
)

# Register routers
# All API endpoints are organized into routers by domain
app.include_router(ai.router)
app.include_router(skills.router)
app.include_router(jobs.router)


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    This function runs once when the application starts. It:
    - Initializes the database and creates all tables
    - Prints a startup message confirming successful initialization
    """
    print("=" * 60)
    print("LinkedInsight API Starting...")
    print("=" * 60)
    
    # Initialize database (creates tables if they don't exist)
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {str(e)}")
        raise
    
    print("✓ All routers registered")
    print("✓ CORS middleware configured")
    print("=" * 60)
    print("LinkedInsight API is ready!")
    print("=" * 60)


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns a simple status check to verify the API is running.
    Useful for load balancers and monitoring systems.
    
    **Returns:**
    ```json
    {
        "status": "ok"
    }
    ```
    """
    return {"status": "ok"}


@app.get("/test/system")
def test_system():
    """
    System test endpoint to verify end-to-end functionality.
    
    This endpoint tests all major components of the system:
    - Database connectivity
    - Skills graph functionality
    - Embeddings service
    - Vector store connectivity
    
    **Returns:**
    ```json
    {
        "db": "ok",
        "graph": "ok",
        "embeddings": "ok",
        "vector_store": "ok"
    }
    ```
    
    If any component fails, it will be marked as "error" with details.
    """
    results = {
        "db": "ok",
        "graph": "ok",
        "embeddings": "ok",
        "vector_store": "ok"
    }
    
    # Test database
    try:
        from app.db.sql import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        results["db"] = f"error: {str(e)}"
    
    # Test skills graph
    try:
        from app.core.graph import get_all_skills, get_graph_stats
        stats = get_graph_stats()
        assert isinstance(stats, dict)
    except Exception as e:
        results["graph"] = f"error: {str(e)}"
    
    # Test embeddings (just verify import works, don't make API call)
    try:
        from app.core.embeddings import embed_text, EMBED_MODEL
        assert EMBED_MODEL is not None
    except Exception as e:
        results["embeddings"] = f"error: {str(e)}"
    
    # Test vector store
    try:
        from app.db.vector_store import get_collection_stats
        stats = get_collection_stats()
        assert isinstance(stats, dict)
    except Exception as e:
        results["vector_store"] = f"error: {str(e)}"
    
    return results

