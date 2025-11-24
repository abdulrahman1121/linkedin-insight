"""
SQL Database Layer for LinkedInsight.

This module provides SQLAlchemy database configuration and session management.
It sets up a SQLite database connection and provides utilities for database
operations including session management and table initialization.

The database file (linkedinsight.db) is stored in the project root directory.
SQLite is used for simplicity and development, but the architecture supports
easy migration to PostgreSQL or other databases in production.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from typing import Generator

# Database file path - stored in project root
# Using absolute path to ensure consistency across different working directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'linkedinsight.db')}"

# Create SQLAlchemy engine
# connect_args={"check_same_thread": False} is required for SQLite to work with FastAPI
# echo=True can be enabled for SQL query logging during development
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL query logging
)

# Create SessionLocal class - factory for creating database sessions
# autocommit=False: Changes must be explicitly committed
# autoflush=False: Objects are not automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base class for SQLAlchemy models
# All model classes will inherit from this Base
Base = declarative_base()


def get_db() -> Generator:
    """
    FastAPI dependency that provides a database session.
    
    This function creates a database session, yields it for use in route handlers,
    and ensures proper cleanup (closing the session) after the request is complete.
    
    This is designed to be used as a FastAPI dependency:
    ```python
    @app.get("/users/{user_id}")
    def get_user(user_id: int, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        return user
    ```
    
    **Usage:**
    - Add `db: Session = Depends(get_db)` to any route handler that needs database access
    - The session is automatically closed after the request completes
    - All database operations should be performed within the request lifecycle
    
    **Yields:**
    - Session: SQLAlchemy database session
    
    **Example:**
    ```python
    from fastapi import Depends
    from app.db.sql import get_db
    from sqlalchemy.orm import Session
    
    @router.get("/users")
    def get_users(db: Session = Depends(get_db)):
        users = db.query(User).all()
        return users
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session, even if an error occurs
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This function creates all tables defined in the models module. It should be
    called once when the application starts or when setting up the database for
    the first time.
    
    **Usage:**
    - Call this function during application startup
    - Safe to call multiple times (won't recreate existing tables)
    - Creates the database file if it doesn't exist
    
    **Example:**
    ```python
    from app.db.sql import init_db
    
    # In application startup
    @app.on_event("startup")
    def startup_event():
        init_db()
    ```
    
    **Note:**
    - This uses SQLAlchemy's `create_all()` which only creates tables that don't exist
    - It does NOT drop existing tables or modify table structure
    - For migrations, use Alembic or similar migration tools
    """
    # Import models here to ensure Base is defined first
    # This ensures all models are registered with the Base before table creation
    from app.db import models
    
    # Create all tables defined in models that inherit from Base
    # This is safe to call multiple times - it only creates tables that don't exist
    Base.metadata.create_all(bind=engine)
    
    print(f"Database initialized at: {DATABASE_URL}")
    print("All tables created successfully.")


def reset_db() -> None:
    """
    Drop all tables and recreate them.
    
    **WARNING:** This will delete all data in the database!
    Only use this in development or testing environments.
    
    **Usage:**
    ```python
    from app.db.sql import reset_db
    
    # In development/testing
    reset_db()
    init_db()
    ```
    """
    from app.db import models
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database reset complete. All tables dropped and recreated.")

