"""
Supabase database client using direct REST API.
No heavy SDK needed - just clean HTTP calls.
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Base headers for Supabase REST API
def _headers(access_token: str = None) -> dict:
    token = access_token or SUPABASE_KEY
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

REST_URL = f"{SUPABASE_URL}/rest/v1"
AUTH_URL = f"{SUPABASE_URL}/auth/v1"


# ══════════════════════════════════════════════════════════════
# AUTH OPERATIONS
# ══════════════════════════════════════════════════════════════

def signup(email: str, password: str) -> dict:
    """Register a new user with auto-confirm using admin API."""
    r = httpx.post(
        f"{AUTH_URL}/admin/users",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "email": email,
            "password": password,
            "email_confirm": True,
        },
    )
    r.raise_for_status()
    user_data = r.json()
    # Now login to get access token
    login_data = login(email, password)
    login_data["user"]["id"] = user_data["id"]
    return login_data


def login(email: str, password: str) -> dict:
    """Login and get access token."""
    r = httpx.post(
        f"{AUTH_URL}/token?grant_type=password",
        headers={"apikey": SUPABASE_KEY, "Content-Type": "application/json"},
        json={"email": email, "password": password},
    )
    r.raise_for_status()
    return r.json()


# ══════════════════════════════════════════════════════════════
# STUDENT OPERATIONS
# ══════════════════════════════════════════════════════════════

def create_student_profile(token: str, user_id: str, name: str, department: str = None, year: int = None) -> dict:
    """Create a student profile after signup."""
    r = httpx.post(
        f"{REST_URL}/students",
        headers=_headers(token),
        json={"id": user_id, "name": name, "department": department, "year": year},
    )
    r.raise_for_status()
    return r.json()


def get_student_profile(token: str, user_id: str) -> dict | None:
    """Get a student's profile."""
    r = httpx.get(
        f"{REST_URL}/students?id=eq.{user_id}&select=*",
        headers=_headers(token),
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


# ══════════════════════════════════════════════════════════════
# PREDICTION OPERATIONS
# ══════════════════════════════════════════════════════════════

def save_prediction(token: str, student_id: str, prediction_data: dict) -> dict:
    """Save a prediction to history."""
    r = httpx.post(
        f"{REST_URL}/predictions",
        headers=_headers(token),
        json={
            "student_id": student_id,
            "hours_studied": prediction_data["hours_studied"],
            "previous_scores": prediction_data["previous_scores"],
            "extracurricular": prediction_data["extracurricular"],
            "sleep_hours": prediction_data["sleep_hours"],
            "sample_papers": prediction_data["sample_papers"],
            "predicted_score": prediction_data["predicted_score"],
            "grade": prediction_data["grade"],
            "target_score": prediction_data.get("target_score"),
        },
    )
    r.raise_for_status()
    return r.json()


def get_prediction_history(token: str, student_id: str, limit: int = 20) -> list:
    """Get a student's prediction history."""
    r = httpx.get(
        f"{REST_URL}/predictions?student_id=eq.{student_id}&select=*&order=created_at.desc&limit={limit}",
        headers=_headers(token),
    )
    r.raise_for_status()
    return r.json()


# ══════════════════════════════════════════════════════════════
# GOAL OPERATIONS
# ══════════════════════════════════════════════════════════════

def save_goal(token: str, student_id: str, target_score: int) -> dict:
    """Save a new goal (deactivates old ones)."""
    # Deactivate old goals
    httpx.patch(
        f"{REST_URL}/goals?student_id=eq.{student_id}&is_active=eq.true",
        headers=_headers(token),
        json={"is_active": False},
    )
    # Insert new goal
    r = httpx.post(
        f"{REST_URL}/goals",
        headers=_headers(token),
        json={"student_id": student_id, "target_score": target_score},
    )
    r.raise_for_status()
    return r.json()


def get_active_goal(token: str, student_id: str) -> dict | None:
    """Get a student's current active goal."""
    r = httpx.get(
        f"{REST_URL}/goals?student_id=eq.{student_id}&is_active=eq.true&order=created_at.desc&limit=1",
        headers=_headers(token),
    )
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None
