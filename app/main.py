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
from app.core.graph import add_skill, add_prerequisite

# Initialize FastAPI application
app = FastAPI(
    title="LinkedInsight",
    description="AI-powered career & skills navigator",
    version="0.1.0",
)

# Configure CORS middleware
# Allows requests from localhost and typical development origins
# In development, we allow all localhost origins for flexibility
import re

def is_localhost_origin(origin: str) -> bool:
    """Check if origin is localhost or 127.0.0.1"""
    if not origin:
        return False
    pattern = r'^https?://(localhost|127\.0\.0\.1)(:\d+)?$'
    return bool(re.match(pattern, origin))


def seed_skills_graph():
    """
    Seed the skills graph with initial data.
    
    This function populates the graph with common tech skills and their
    prerequisite relationships to provide a useful starting point for users.
    """
    # Programming Languages (foundational)
    add_skill("Python")
    add_skill("JavaScript")
    add_skill("Java")
    add_skill("C++")
    add_skill("SQL")
    
    # Web Development
    add_skill("HTML")
    add_skill("CSS")
    add_skill("React")
    add_skill("Node.js")
    add_skill("Express.js")
    add_skill("TypeScript")
    add_skill("Next.js")
    
    # Data Science & ML
    add_skill("Pandas")
    add_skill("NumPy")
    add_skill("Matplotlib")
    add_skill("Scikit-learn")
    add_skill("Machine Learning")
    add_skill("Deep Learning")
    add_skill("TensorFlow")
    add_skill("PyTorch")
    add_skill("Data Science")
    add_skill("Statistics")
    add_skill("Linear Algebra")
    add_skill("Calculus")
    
    # Backend & DevOps
    add_skill("REST API")
    add_skill("GraphQL")
    add_skill("Docker")
    add_skill("Kubernetes")
    add_skill("AWS")
    add_skill("Linux")
    add_skill("Git")
    
    # Databases
    add_skill("PostgreSQL")
    add_skill("MongoDB")
    add_skill("Redis")
    
    # Now add prerequisite relationships
    
    # Web Development prerequisites
    add_prerequisite("React", "JavaScript")
    add_prerequisite("React", "HTML")
    add_prerequisite("React", "CSS")
    add_prerequisite("Node.js", "JavaScript")
    add_prerequisite("Express.js", "Node.js")
    add_prerequisite("TypeScript", "JavaScript")
    add_prerequisite("Next.js", "React")
    add_prerequisite("Next.js", "TypeScript")
    
    # Data Science prerequisites
    add_prerequisite("Pandas", "Python")
    add_prerequisite("NumPy", "Python")
    add_prerequisite("Matplotlib", "Python")
    add_prerequisite("Scikit-learn", "Python")
    add_prerequisite("Scikit-learn", "NumPy")
    add_prerequisite("Scikit-learn", "Pandas")
    add_prerequisite("Machine Learning", "Python")
    add_prerequisite("Machine Learning", "Statistics")
    add_prerequisite("Machine Learning", "Linear Algebra")
    add_prerequisite("Deep Learning", "Machine Learning")
    add_prerequisite("Deep Learning", "Calculus")
    add_prerequisite("TensorFlow", "Python")
    add_prerequisite("TensorFlow", "Machine Learning")
    add_prerequisite("PyTorch", "Python")
    add_prerequisite("PyTorch", "Machine Learning")
    add_prerequisite("Data Science", "Python")
    add_prerequisite("Data Science", "Statistics")
    add_prerequisite("Data Science", "Pandas")
    
    # Backend prerequisites
    add_prerequisite("REST API", "JavaScript")
    add_prerequisite("REST API", "Python")
    add_prerequisite("GraphQL", "JavaScript")
    add_prerequisite("Docker", "Linux")
    add_prerequisite("Kubernetes", "Docker")
    add_prerequisite("AWS", "Linux")
    
    # Database prerequisites
    add_prerequisite("PostgreSQL", "SQL")
    add_prerequisite("MongoDB", "JavaScript")
    add_prerequisite("Redis", "Linux")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default
        "http://localhost:3001",  # Alternative Next.js port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://localhost:8000",  # FastAPI default (for testing)
        "http://localhost:8001",  # FastAPI alternative port
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",  # Also allow any localhost port
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
    
    # Seed skills graph with initial data
    try:
        seed_skills_graph()
        print("✓ Skills graph seeded with initial data")
    except Exception as e:
        print(f"⚠ Skills graph seeding failed: {str(e)}")
        # Don't raise - graph can be populated via API
    
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

