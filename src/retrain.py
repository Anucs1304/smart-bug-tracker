import sqlite3
import json
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

DB_PATH = "bugtracker.db"
MODEL_PATH = "models/xgb_model.pkl"
LABEL_ENCODER_PATH = "models/label_encoder.pkl"
FEATURE_ORDER_PATH = "models/feature_order.pkl"

def safe_json_loads(value):
    if value is None:
        return {}
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str) and value.strip() == "":
        return {}
    try:
        return json.loads(value)
    except Exception:
        return {}

def load_historical_df():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT file, severity, confidence, rules, features, git_metadata, timestamp FROM analyses", conn)
    conn.close()
    return df

def build_training_matrix(df: pd.DataFrame):
    # Parse JSON columns
    features_parsed = df["features"].apply(safe_json_loads)
    git_meta_parsed = df["git_metadata"].apply(safe_json_loads)

    # Normalize JSON into columns
    X_features = pd.json_normalize(features_parsed)
    X_git = pd.json_normalize(git_meta_parsed)

    # Keep only numeric columns (models need numbers)
    X_features = X_features.select_dtypes(include=["number"]).fillna(0)
    X_git = X_git.select_dtypes(include=["number"]).fillna(0)

    # Merge feature blocks
    X = pd.concat([X_features, X_git], axis=1).fillna(0)

    # Target
    y = df["severity"].astype(str)

    return X, y

def retrain():
    df = load_historical_df()
    if df.empty:
        print("No historical data found. Skipping retrain.")
        return

    X, y = build_training_matrix(df)

    # Encode labels
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # Save feature order for inference alignment
    joblib.dump(list(X.columns), FEATURE_ORDER_PATH)

    # Train/validation split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    # Train model
    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="mlogloss",
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_val)
    print(classification_report(y_val, y_pred, target_names=le.classes_))

    # Save artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, LABEL_ENCODER_PATH)
    print("Model and label encoder saved.")

if __name__ == "__main__":
    retrain()
