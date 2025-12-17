from fastapi import FastAPI, UploadFile
import pandas as pd
import joblib
import traceback
from git_metadata import get_git_metadata  
from logger import log_analysis_result
import sqlite3, json, pandas as pd

# Import local modules
from api import analysis
from descriptions import get_description
from fastapi.responses import FileResponse

app = FastAPI()

# Load model, label encoder, and expected feature order
bug_model = joblib.load("models/xgb_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
expected_features = joblib.load("models/feature_order.pkl")  # saved during training

@app.get("/")
async def root():
    return {"status": "ok", "message": "Smart Bug Tracker API is running"}

@app.post("/analyze")
async def analyze_code(file: UploadFile):
    try:
        # Read uploaded file
        code = await file.read()
        code_str = code.decode("utf-8")

        # Extract features + rule IDs
        features, rule_ids = analysis.extract_features_from_code(code_str, file_name=file.filename)
        
        # ✅ Add Git metadata
        git_meta = get_git_metadata(file.filename)
        for k, v in git_meta.items():
            features[k] = v if isinstance(v, (int, float)) else 0  # numeric only

        # Reindex to match training schema
        features = features.reindex(columns=expected_features, fill_value=0)

        # Debug print
        #print("Extracted features:", features.columns.tolist())
        #print("Feature values:", features.to_dict(orient="records")[0])
        #print("Rule IDs detected:", rule_ids)

        # ✅ Reindex DataFrame to match training order
        features = features.reindex(columns=expected_features)

        # Predict severity
        prediction = bug_model.predict(features)
        severity = label_encoder.inverse_transform(prediction)[0]
        confidence = float(max(bug_model.predict_proba(features)[0]))

        # ✅ Deduplicate rule IDs before mapping
        unique_rules = list(set(rule_ids)) if rule_ids else []

        # Pair rule ID with suggestion
        rule_descriptions = [
    f"{i+1}. [{rule}] {get_description(rule)}"
    for i, rule in enumerate(unique_rules)
] if unique_rules else ["No rules detected."]


        log_analysis_result(
            file_name=file.filename,
            severity=severity,
            confidence=confidence,
            rules_detected=unique_rules,
            features=features.to_dict(orient="records")[0],
            git_meta=git_meta
        )
        
        return {
            "file": file.filename,
            "severity": severity,
            "confidence": confidence,
            "rule_descriptions": rule_descriptions,
            "features": features.to_dict(orient="records")[0],
            "rules_detected": unique_rules,
            "git_metadata": git_meta
        }

    except Exception as e:
        print("Error in /analyze:", traceback.format_exc())
        # ✅ Ensure rule_ids is defined even in error case
        return {"error": str(e), "rules_detected": []}
    
@app.get("/stats")
def get_stats():
    conn = sqlite3.connect("bugtracker.db")
    df = pd.read_sql_query("SELECT severity, confidence, timestamp FROM analyses", conn)
    conn.close()

    stats = {
        "total_analyses": len(df),
        "severity_counts": df["severity"].value_counts().to_dict(),
        "avg_confidence": round(df["confidence"].mean(), 2),
        "recent": df.tail(10).to_dict(orient="records")
    }
    return stats

@app.get("/rules")
def get_rules():
    conn = sqlite3.connect("bugtracker.db")
    df = pd.read_sql_query("SELECT rules, timestamp FROM analyses", conn)
    conn.close()

    all_rules = []
    for r in df["rules"]:
        try:
            all_rules.extend(json.loads(r))
        except:
            pass

    rule_counts = pd.Series(all_rules).value_counts().to_dict()
    return {"rule_counts": rule_counts}

@app.get("/dashboard")
def dashboard():
    return FileResponse("dashboard.html")

@app.get("/confidence_trend")
def confidence_trend():
    conn = sqlite3.connect("bugtracker.db")
    df = pd.read_sql_query("SELECT confidence, timestamp FROM analyses ORDER BY timestamp ASC", conn)
    conn.close()

    trend = {
        "timestamps": df["timestamp"].tolist(),
        "confidences": df["confidence"].tolist()
    }
    return trend
