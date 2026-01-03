"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    full_name: Optional[str]
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}


class UserProfile(BaseModel):
    id: UUID
    email: str
    username: str
    full_name: Optional[str]
    created_at: datetime
    total_assessments: int

    model_config = {"from_attributes": True}


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[str] = None


# Assessment schemas
class AssessmentCreate(BaseModel):
    duration: Optional[str] = None
    itching: bool = False
    bleeding: bool = False
    pain: bool = False
    sun_exposure: Optional[str] = None
    location: Optional[str] = None


class AssessmentResponse(BaseModel):
    success: bool
    assessment_id: str
    risk_level: str
    final_risk_score: float
    final_risk_percentage: str
    image_risk: float
    image_risk_percentage: str
    support_risk: float
    support_risk_percentage: str
    explanations: List[str]
    recommendation: str
    timestamp: str
    disclaimer: str


class AssessmentDetail(BaseModel):
    id: UUID
    user_id: UUID
    risk_level: str
    final_risk_score: float
    image_risk: float
    support_risk: float
    explanations: Optional[List[str]]
    recommendation: Optional[str]
    user_inputs: Optional[dict]
    created_at: datetime
    image_id: Optional[UUID]

    model_config = {"from_attributes": True}

