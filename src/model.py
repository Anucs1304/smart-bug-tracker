
import joblib
import numpy as np
import pandas as pd


class BugSeverityModel:
    def __init__(self, model_path: str, label_encoder_path: str):
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(label_encoder_path)

    def predict(self, features: pd.DataFrame):
        """Predict severity label and confidence for given features."""
        y_pred = self.model.predict(features.drop(columns=["file"], errors="ignore"))
        y_pred_labels = self.label_encoder.inverse_transform(y_pred)

        if hasattr(self.model, "predict_proba"):
            confidences = np.max(self.model.predict_proba(features.drop(columns=["file"], errors="ignore")), axis=1)
        else:
            confidences = [None] * len(y_pred)

        return list(zip(y_pred_labels, confidences))
