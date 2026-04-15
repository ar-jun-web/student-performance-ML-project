"""
Analytics engine - generates insights, recommendations, and comparisons.
This is the EXACT same logic from your Streamlit app's tabs, extracted into functions.
"""


def get_grade_info(prediction: float) -> dict:
    """Determine grade class, status, and message from prediction score."""
    if prediction >= 85:
        return {
            "grade": "excellent",
            "status": "EXCELLENT",
            "message": "Outstanding performance! Keep up the excellent work!",
        }
    elif prediction >= 70:
        return {
            "grade": "good",
            "status": "GOOD",
            "message": "Strong performance with room to reach excellence!",
        }
    elif prediction >= 50:
        return {
            "grade": "average",
            "status": "AVERAGE",
            "message": "Decent performance. Increase efforts to improve further.",
        }
    else:
        return {
            "grade": "poor",
            "status": "NEEDS IMPROVEMENT",
            "message": "Focus on fundamentals and increase study time.",
        }


def get_goal_analysis(prediction: float, target_score: int) -> dict:
    """Calculate gap between current prediction and target score."""
    gap = target_score - prediction
    progress_pct = min((prediction / target_score) * 100, 100)
    return {
        "target_score": target_score,
        "current_score": round(prediction, 1),
        "gap": round(max(gap, 0), 1),
        "progress_percentage": round(progress_pct, 1),
        "on_track": prediction >= target_score,
    }


def get_recommendations(
    hours_studied: int,
    previous_scores: int,
    extracurricular: bool,
    sleep_hours: int,
    sample_papers: int,
    prediction: float,
    target_score: int,
) -> list[dict]:
    """Generate personalized recommendations to reach the target score."""
    if prediction >= target_score:
        return []

    recommendations = []

    if hours_studied < 8:
        recommendations.append(
            {
                "icon": "book",
                "title": "Increase Study Time",
                "description": f"Try studying {min(hours_studied + 2, 10)} hours/day to boost performance",
            }
        )

    if sample_papers < 7:
        recommendations.append(
            {
                "icon": "document",
                "title": "Practice More Papers",
                "description": f"Complete {min(sample_papers + 3, 10)} practice papers for better preparation",
            }
        )

    if sleep_hours < 7:
        recommendations.append(
            {
                "icon": "moon",
                "title": "Improve Sleep",
                "description": "Aim for 7-8 hours of sleep for better memory retention",
            }
        )

    if not extracurricular:
        recommendations.append(
            {
                "icon": "trophy",
                "title": "Join Activities",
                "description": "Extracurricular activities correlate with better performance",
            }
        )

    return recommendations[:3]


def get_peer_comparison(
    hours_studied: int,
    previous_scores: int,
    extracurricular: bool,
    sleep_hours: int,
    sample_papers: int,
) -> list[dict]:
    """Compare student scores against class averages."""
    # Class averages (same as your Streamlit app)
    avg_scores = [60, 70, 65, 60, 50]

    student_scores = [
        (hours_studied / 12) * 100,
        previous_scores,
        (sleep_hours / 12) * 100,
        (sample_papers / 10) * 100,
        100 if extracurricular else 20,
    ]

    categories = ["Study Time", "Academic", "Sleep", "Practice", "Activities"]

    comparisons = []
    for cat, student, avg in zip(categories, student_scores, avg_scores):
        diff = student - avg
        comparisons.append(
            {
                "category": cat,
                "student_score": round(student, 1),
                "class_average": avg,
                "difference": round(diff, 1),
                "is_strength": diff > 10,
            }
        )

    return comparisons


def get_insights(
    hours_studied: int,
    previous_scores: int,
    extracurricular: bool,
    sleep_hours: int,
    sample_papers: int,
) -> list[dict]:
    """Generate personalized study insights. Same logic as your Tab 4."""
    insights = []

    # Study time insights
    if hours_studied >= 8:
        insights.append(
            {
                "icon": "book",
                "title": "Excellent Study Commitment",
                "description": f"Your {hours_studied} hours of daily study is exceptional. Maintain this consistency!",
                "level": "success",
            }
        )
    elif hours_studied >= 5:
        insights.append(
            {
                "icon": "book-open",
                "title": "Good Study Routine",
                "description": f"{hours_studied} hours is solid, but pushing to 7-8 hours can significantly boost results.",
                "level": "info",
            }
        )
    else:
        insights.append(
            {
                "icon": "clock",
                "title": "Increase Study Time",
                "description": f"Only {hours_studied} hours/day may not be enough. Try gradually increasing to 6-7 hours.",
                "level": "warning",
            }
        )

    # Sleep insights
    if 7 <= sleep_hours <= 9:
        insights.append(
            {
                "icon": "moon",
                "title": "Optimal Sleep Schedule",
                "description": f"{sleep_hours} hours of sleep is perfect for memory consolidation and cognitive function.",
                "level": "success",
            }
        )
    elif sleep_hours < 7:
        insights.append(
            {
                "icon": "moon",
                "title": "Sleep More",
                "description": f"{sleep_hours} hours may not be enough. Aim for 7-8 hours to improve retention and focus.",
                "level": "warning",
            }
        )
    else:
        insights.append(
            {
                "icon": "clock",
                "title": "Too Much Sleep?",
                "description": f"{sleep_hours} hours might be excessive. 7-8 hours is optimal for most students.",
                "level": "info",
            }
        )

    # Practice insights
    if sample_papers >= 7:
        insights.append(
            {
                "icon": "document",
                "title": "Excellent Exam Prep",
                "description": f"{sample_papers} practice papers shows strong preparation. This is a top predictor of success!",
                "level": "success",
            }
        )
    elif sample_papers >= 4:
        insights.append(
            {
                "icon": "document",
                "title": "Good Practice Routine",
                "description": f"{sample_papers} papers is decent. Push to 7-8 for maximum exam confidence.",
                "level": "info",
            }
        )
    else:
        insights.append(
            {
                "icon": "document",
                "title": "Practice More",
                "description": f"Only {sample_papers} papers practiced. This is crucial - aim for at least 6-7 before exams.",
                "level": "warning",
            }
        )

    # Extracurricular insights
    if extracurricular:
        insights.append(
            {
                "icon": "trophy",
                "title": "Well-Rounded Profile",
                "description": "Extracurricular participation builds discipline and correlates with higher academic performance.",
                "level": "success",
            }
        )
    else:
        insights.append(
            {
                "icon": "target",
                "title": "Consider Activities",
                "description": "Joining clubs or sports can improve time management and overall academic outcomes.",
                "level": "info",
            }
        )

    # Previous scores insight
    if previous_scores >= 85:
        insights.append(
            {
                "icon": "star",
                "title": "Strong Academic Foundation",
                "description": f"{previous_scores}% shows excellent prior knowledge. Build on this momentum!",
                "level": "success",
            }
        )
    elif previous_scores >= 70:
        insights.append(
            {
                "icon": "chart",
                "title": "Solid Performance",
                "description": f"{previous_scores}% is good. Focus on weak topics to push into the 85+ range.",
                "level": "info",
            }
        )
    else:
        insights.append(
            {
                "icon": "trending-down",
                "title": "Foundation Building Needed",
                "description": f"{previous_scores}% suggests knowledge gaps. Consider focused revision on core topics.",
                "level": "warning",
            }
        )

    return insights
