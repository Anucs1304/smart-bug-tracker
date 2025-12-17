# smart-bug-tracker

## Overview
Smart Bug Tracker is a prototype system that combines **static analysis tools** with **machine learning models** to automatically detect, classify, and prioritize bugs in source code.  
It provides:
- Automated bug detection and severity classification
- Context-aware suggestions for fixes
- Transparent logging in a SQLite database
- Interactive dashboard visualizations (severity distribution, rule frequency, confidence trends)

---

## Features
- **FastAPI backend** with endpoints:
  - `/analyze` → analyze uploaded files
  - `/stats` → aggregate severity levels
  - `/rules` → track rule frequency
  - `/confidence_trend` → monitor prediction stability
- **Batch analysis script** (`batch_analyze.py`) for reproducible multi-file testing
- **SQLite database** (`bugtracker.db`) for structured storage of results
- **Dashboard** (`dashboard.html`) powered by Chart.js for interactive visualization
- **Machine learning models** (Random Forest, XGBoost) for severity prediction

---

## Project Structure
- Smart-Bug-Tracker
  - api
    - app.py       → FastAPI entry point
    - test_api.py  → API testing
    - analysis.py  → analysis endpoints
  - dashboard
    - dashboard.html → chart.js dashboard
  - data
    - processed      → cleaned or feature-engineered data
    - raw            → original buggy files or datasets
    - immo_data.csv  → example dataset
  - database
    - bugtrackerdb   → SQLite database
  - models
    - feature_order.pkl   → feature ordening
    - label_encoder.pkl   → encoder for categorical labels
    - xgb_model.pkl       → trained XGBoost model
  - notebooks
    - bugtracker_dev.ipynb → experiments and development notebook
  - src
    - descriptions.py  → rule description
    - git_metadata.py  → commit metadata extraction
    - logger.py        → logging utilities
    - model.py         → ML model integration
    - retrain.py       → model retraining script
  - tests
    - batch_analysis.py      → batch workflow script
    - buggy_complexity.py    → synthetic bug files
    - buggy_docstring.py     → synthetic bug files
    - buggy_security.py      → synthetic bug files
    - buggy_style.py         → synthetic bug files
    - test_analysis.py       → unit test
 ---

 
## 🚀 Installation & Setup
1. Clone the repository:
   bash
   git clone https://github.com/yourusername/SMART-BUG-TRACKER.git
   cd SMART-BUG-TRACKER

2. Create a virtual environment and install dependencies:
   conda create -n bugtracker python=3.9
   conda activate bugtracker

3. Run the FastAPI backend:
   uvicorn api.app:app --reload

4. Open the dashboard
   Launch dashboard.html in a browser to view visualizations.

---
## Usage
1. Start the FastAPI server:
   bash
   uvicorn api.app:app --reload
2. Open the interactive API docs in your browser:
   Swagger UI: http://127.0.0.1:8000/docs
