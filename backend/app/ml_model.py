"""
ML Model loader and prediction engine.
This wraps your existing ML model (enhanced_model.pkl) into a reusable class.
Your model code stays EXACTLY the same - we're just wrapping it.
"""

import os
import numpy as np
import pandas as pd
import joblib


class AcademyFlowModel:
    """Wrapper around the trained AcademyFlow ML model."""

    def __init__(self):
        self.model_package = None
        self.model_loaded = False
        self.model_type = None

    def load(self) -> bool:
        """Load the ML model from .pkl file. Returns True if successful."""
        # Search for model file in multiple locations
        search_paths = [
            "enhanced_model.pkl",
            "model.pkl",
            "../MLmodels/enhanced_model.pkl",
            "../MLmodels/model.pkl",
            "MLmodels/enhanced_model.pkl",
            "MLmodels/model.pkl",
        ]

        for path in search_paths:
            if os.path.exists(path):
                try:
                    model_package = joblib.load(path)
                    if isinstance(model_package, dict):
                        self.model_package = model_package
                        self.model_loaded = True
                        self.model_type = "enhanced"
                        print(f"Loaded enhanced model from: {path}")
                        return True
                    else:
                        self.model_package = {"best_model": model_package}
                        self.model_loaded = True
                        self.model_type = "basic"
                        print(f"Loaded basic model from: {path}")
                        return True
                except Exception as e:
                    print(f"Failed to load model from {path}: {e}")
                    continue

        print("ERROR: No model file found!")
        return False

    @property
    def model_name(self) -> str:
        """Get the name of the loaded model."""
        if not self.model_loaded:
            return "Not loaded"
        return self.model_package.get("best_model_name", "Linear Regression")

    @staticmethod
    def calculate_engineered_features(
        hours: int, prev_score: int, extra: int, sleep: int, papers: int
    ) -> dict:
        """
        Calculate advanced engineered features.
        This is the EXACT same logic from your app.py.
        """
        return {
            "Study_Sleep_Ratio": hours / (sleep + 1),
            "Total_Effort": hours + papers,
            "Previous_Score_Normalized": prev_score / 100,
            "Sleep_Efficiency": sleep * prev_score / 100,
        }

    def predict(
        self,
        hours_studied: int,
        previous_scores: int,
        extracurricular: int,
        sleep_hours: int,
        sample_papers: int,
    ) -> float:
        """
        Make a prediction using the loaded model.
        This is the EXACT same prediction logic from your app.py.
        Returns: Predicted performance index (0-100)
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded. Call load() first.")

        eng_features = self.calculate_engineered_features(
            hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers
        )

        if self.model_type == "enhanced":
            features_df = pd.DataFrame(
                {
                    "Hours Studied": [hours_studied],
                    "Previous Scores": [previous_scores],
                    "Extracurricular Activities": [extracurricular],
                    "Sleep Hours": [sleep_hours],
                    "Sample Question Papers Practiced": [sample_papers],
                    "Study_Sleep_Ratio": [eng_features["Study_Sleep_Ratio"]],
                    "Total_Effort": [eng_features["Total_Effort"]],
                    "Previous_Score_Normalized": [eng_features["Previous_Score_Normalized"]],
                    "Sleep_Efficiency": [eng_features["Sleep_Efficiency"]],
                }
            )
            model = self.model_package["best_model"]
        else:
            features_df = np.array(
                [[hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers]]
            )
            model = self.model_package["best_model"]

        prediction = float(model.predict(features_df)[0])
        prediction = np.clip(prediction, 0, 100)

        return prediction


# Singleton instance - loaded once, reused across requests
model_instance = AcademyFlowModel()
