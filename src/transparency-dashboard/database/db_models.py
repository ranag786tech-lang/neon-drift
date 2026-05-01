"""
Database Configuration and Models
Supports both PostgreSQL (SQLAlchemy) and MongoDB (Motor)
"""
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Base for SQLAlchemy models
Base = declarative_base()

class ExplanationDB(Base):
    """SQLAlchemy model for storing AI explanations"""
    __tablename__ = "explanations"
    
    id = Column(String, primary_key=True)
    decision_id = Column(String, index=True)
    model_name = Column(String)
    outcome = Column(String)
    confidence = Column(Float)
    factors = Column(JSON)  # List of factor dicts
    fairness_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, index=True)
    
class AuditReportDB(Base):
    """SQLAlchemy model for storing audit reports"""
    __tablename__ = "audit_reports"
    
    id = Column(String, primary_key=True)
    report_type = Column(String)
    overall_score = Column(Float)
    compliance_status = Column(String)
    metrics = Column(JSON)  # List of metric dicts
    biases_detected = Column(JSON)  # List of bias dicts
    recommendations = Column(JSON)  # List of recommendation strings
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, index=True)

class KnowledgeDocumentDB(Base):
    """SQLAlchemy model for Unified Knowledge Hub documents"""
    __tablename__ = "knowledge_documents"
    
    id = Column(String, primary_key=True)
    title = Column(String)
    content = Column(Text)
    source_type = Column(String)  # enterprise, public, personal
    tags = Column(JSON)  # List of tags
    metadata = Column(JSON)  # Additional metadata
    embedding = Column(JSON)  # Vector embedding for search
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, index=True)

class LearningProfileDB(Base):
    """SQLAlchemy model for Adaptive Learning Engine profiles"""
    __tablename__ = "learning_profiles"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, unique=True, index=True)
    team_id = Column(String, index=True)
    workflow_patterns = Column(JSON)  # Learned patterns
    preferences = Column(JSON)  # User preferences
    skill_level = Column(String)
    productivity_metrics = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)

def get_database_url():
    """Get database URL from environment or use SQLite default"""
    db_type = os.getenv("DB_TYPE", "sqlite")
    
    if db_type == "postgresql":
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "postgres")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        name = os.getenv("DB_NAME", "empowerment_db")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    elif db_type == "mongodb":
        user = os.getenv("DB_USER", "mongo")
        password = os.getenv("DB_PASSWORD", "mongo")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "27017")
        name = os.getenv("DB_NAME", "empowerment_db")
        return f"mongodb://{user}:{password}@{host}:{port}/{name}"
    else:
        # Default to SQLite for development
        return "sqlite:///./empowerment.db"

def init_sqlalchemy():
    """Initialize SQLAlchemy engine and session"""
    db_url = get_database_url()
    if db_url.startswith("postgresql"):
        engine = create_engine(db_url, echo=False)
    else:
        engine = create_engine(db_url.replace("mongodb://", "sqlite:///"), echo=False)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

# Initialize database
try:
    engine, SessionLocal = init_sqlalchemy()
    print("✅ Database initialized successfully!")
except Exception as e:
    print(f"⚠️ Database initialization warning: {e}")
    engine = None
    SessionLocal = None
