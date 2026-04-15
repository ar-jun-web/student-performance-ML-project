"""
Pydantic schemas for request/response validation.
These define the exact shape of data going in and out of our API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ══════════════════════════════════════════════════════════════
# REQUEST SCHEMAS
# ══════════════════════════════════════════════════════════════

class PredictionRequest(BaseModel):
    """Input data for student performance prediction."""
    hours_studied: int = Field(..., ge=0, le=12, description="Daily study hours (0-12)")
    previous_scores: int = Field(..., ge=0, le=100, description="Last exam score (0-100)")
    extracurricular: bool = Field(..., description="Participates in extracurricular activities")
    sleep_hours: int = Field(..., ge=4, le=12, description="Average nightly sleep (4-12)")
    sample_papers: int = Field(..., ge=0, le=10, description="Practice papers completed (0-10)")
    target_score: Optional[int] = Field(None, ge=0, le=100, description="Target performance index")


# ══════════════════════════════════════════════════════════════
# RESPONSE SCHEMAS
# ══════════════════════════════════════════════════════════════

class EngineeredFeatures(BaseModel):
    """Calculated engineered features used by the model."""
    study_sleep_ratio: float
    total_effort: float
    previous_score_normalized: float
    sleep_efficiency: float


class PredictionResult(BaseModel):
    """Core prediction output."""
    score: float = Field(..., description="Predicted performance index (0-100)")
    grade: str = Field(..., description="Performance grade: excellent, good, average, poor")
    status: str = Field(..., description="Human-readable status label")
    message: str = Field(..., description="Personalized feedback message")
    model_name: str = Field(..., description="Name of the ML model used")


class GoalAnalysis(BaseModel):
    """Gap analysis between current and target score."""
    target_score: int
    current_score: float
    gap: float
    progress_percentage: float
    on_track: bool


class Recommendation(BaseModel):
    """A single improvement recommendation."""
    icon: str
    title: str
    description: str


class PeerComparison(BaseModel):
    """Student vs class average comparison."""
    category: str
    student_score: float
    class_average: float
    difference: float
    is_strength: bool


class Insight(BaseModel):
    """Personalized study insight."""
    icon: str
    title: str
    description: str
    level: str = Field(..., description="success, info, or warning")


class PredictionResponse(BaseModel):
    """Complete API response with prediction + all analytics."""
    prediction: PredictionResult
    engineered_features: EngineeredFeatures
    goal_analysis: Optional[GoalAnalysis] = None
    recommendations: list[Recommendation] = []
    peer_comparison: list[PeerComparison] = []
    insights: list[Insight] = []
    timestamp: datetime


class HealthResponse(BaseModel):
    """API health check response."""
    status: str
    model_loaded: bool
    model_name: Optional[str] = None
    version: str


# ══════════════════════════════════════════════════════════════
# AUTH SCHEMAS
# ══════════════════════════════════════════════════════════════

class SignupRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=6)
    name: str
    department: Optional[str] = None
    year: Optional[int] = Field(None, ge=1, le=4)


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    user_id: Optional[str] = None
    access_token: Optional[str] = None
    message: str
