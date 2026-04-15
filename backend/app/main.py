"""
AcademyFlow API - FastAPI Backend
Serves the ML model as a REST API for the Flutter mobile app.

Run with: uvicorn app.main:app --reload
"""

from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    PredictionRequest,
    PredictionResponse,
    PredictionResult,
    EngineeredFeatures,
    GoalAnalysis,
    Recommendation,
    PeerComparison,
    Insight,
    HealthResponse,
    SignupRequest,
    LoginRequest,
    AuthResponse,
)
from app.ml_model import model_instance
from app.analytics import (
    get_grade_info,
    get_goal_analysis,
    get_recommendations,
    get_peer_comparison,
    get_insights,
)
from app import database as db


# ══════════════════════════════════════════════════════════════
# APP SETUP
# ══════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML model when the server starts."""
    loaded = model_instance.load()
    if not loaded:
        print("WARNING: ML model failed to load!")
    yield


app = FastAPI(
    title="AcademyFlow API",
    description="Student Performance Prediction API - Powered by Machine Learning",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow Flutter app to connect from any origin (we'll restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ══════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.get("/", tags=["General"])
async def root():
    """Welcome endpoint."""
    return {
        "app": "AcademyFlow API",
        "version": "1.0.0",
        "docs": "/docs",
        "message": "Student Performance Prediction API is running!",
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Check API health and model status."""
    return HealthResponse(
        status="healthy" if model_instance.model_loaded else "degraded",
        model_loaded=model_instance.model_loaded,
        model_name=model_instance.model_name if model_instance.model_loaded else None,
        version="1.0.0",
    )


@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_performance(request: PredictionRequest):
    """
    Predict student performance based on study habits.

    Takes 5 input features and returns:
    - Predicted performance score (0-100)
    - Grade classification
    - Goal gap analysis (if target_score provided)
    - Personalized recommendations
    - Peer comparison data
    - Study insights
    """
    if not model_instance.model_loaded:
        raise HTTPException(
            status_code=503,
            detail="ML model is not loaded. Please try again later.",
        )

    # Convert extracurricular bool to int for the model
    extra_int = 1 if request.extracurricular else 0

    # Run prediction (same logic as your Streamlit app)
    try:
        prediction = model_instance.predict(
            hours_studied=request.hours_studied,
            previous_scores=request.previous_scores,
            extracurricular=extra_int,
            sleep_hours=request.sleep_hours,
            sample_papers=request.sample_papers,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Get grade info
    grade_info = get_grade_info(prediction)

    # Calculate engineered features (for transparency)
    eng = model_instance.calculate_engineered_features(
        request.hours_studied,
        request.previous_scores,
        extra_int,
        request.sleep_hours,
        request.sample_papers,
    )

    # Build response
    response = PredictionResponse(
        prediction=PredictionResult(
            score=round(prediction, 1),
            grade=grade_info["grade"],
            status=grade_info["status"],
            message=grade_info["message"],
            model_name=model_instance.model_name,
        ),
        engineered_features=EngineeredFeatures(
            study_sleep_ratio=round(eng["Study_Sleep_Ratio"], 3),
            total_effort=eng["Total_Effort"],
            previous_score_normalized=eng["Previous_Score_Normalized"],
            sleep_efficiency=eng["Sleep_Efficiency"],
        ),
        peer_comparison=[
            PeerComparison(**comp)
            for comp in get_peer_comparison(
                request.hours_studied,
                request.previous_scores,
                request.extracurricular,
                request.sleep_hours,
                request.sample_papers,
            )
        ],
        insights=[
            Insight(**ins)
            for ins in get_insights(
                request.hours_studied,
                request.previous_scores,
                request.extracurricular,
                request.sleep_hours,
                request.sample_papers,
            )
        ],
        timestamp=datetime.now(),
    )

    # Add goal analysis if target provided
    if request.target_score is not None:
        response.goal_analysis = GoalAnalysis(
            **get_goal_analysis(prediction, request.target_score)
        )
        response.recommendations = [
            Recommendation(**rec)
            for rec in get_recommendations(
                request.hours_studied,
                request.previous_scores,
                request.extracurricular,
                request.sleep_hours,
                request.sample_papers,
                prediction,
                request.target_score,
            )
        ]

    return response


# ══════════════════════════════════════════════════════════════
# AUTH ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.post("/api/auth/signup", response_model=AuthResponse, tags=["Auth"])
async def signup(request: SignupRequest):
    """Register a new student."""
    try:
        auth_data = db.signup(request.email, request.password)
        user_id = auth_data["user"]["id"]
        access_token = auth_data["access_token"]

        # Create student profile
        db.create_student_profile(access_token, user_id, request.name, request.department, request.year)

        return AuthResponse(
            user_id=user_id,
            access_token=access_token,
            message="Signup successful!",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/auth/login", response_model=AuthResponse, tags=["Auth"])
async def login(request: LoginRequest):
    """Login and get access token."""
    try:
        auth_data = db.login(request.email, request.password)
        return AuthResponse(
            user_id=auth_data["user"]["id"],
            access_token=auth_data["access_token"],
            message="Login successful!",
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")


# ══════════════════════════════════════════════════════════════
# HISTORY ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.get("/api/history", tags=["History"])
async def get_history(authorization: str = Header(...)):
    """Get prediction history for the logged-in student."""
    try:
        token = authorization.replace("Bearer ", "")
        # Decode user ID from JWT
        import json, base64
        payload = json.loads(base64.urlsafe_b64decode(token.split(".")[1] + "=="))
        user_id = payload["sub"]
        history = db.get_prediction_history(token, user_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
