"""
Database configuration and models for DermaSense
"""
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Boolean, LargeBinary, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variable or default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://dermasense_user:dermasense_password@localhost:5432/dermasense_db"
)

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Assessment(Base):
    """Assessment model for storing risk assessment results"""
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Foreign key to users
    
    # Risk assessment results
    risk_level = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH
    final_risk_score = Column(Float, nullable=False)
    image_risk = Column(Float, nullable=False)
    support_risk = Column(Float, nullable=False)
    
    # Explanations and recommendations (stored as JSON)
    explanations = Column(JSON, nullable=True)
    recommendation = Column(Text, nullable=True)
    
    # User inputs (stored as JSON)
    user_inputs = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<Assessment(id={self.id}, user_id={self.user_id}, risk_level={self.risk_level}, created_at={self.created_at})>"


class Image(Base):
    """Image model for storing uploaded images as binary data"""
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Foreign key to assessments
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Foreign key to users
    
    # Image data stored as binary (BYTEA in PostgreSQL)
    image_data = Column(LargeBinary, nullable=False)
    
    # Image metadata
    filename = Column(String(255), nullable=True)
    content_type = Column(String(100), nullable=True)  # e.g., "image/jpeg"
    file_size = Column(Integer, nullable=True)  # Size in bytes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Image(id={self.id}, assessment_id={self.assessment_id}, filename={self.filename}, size={self.file_size})>"


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")


def drop_db():
    """Drop all database tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("✓ Database tables dropped")

