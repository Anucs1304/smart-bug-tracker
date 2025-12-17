import sqlite3, json, datetime

def log_analysis_result(file_name, severity, confidence, rules_detected, features, git_meta):
    conn = sqlite3.connect("bugtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file TEXT,
        severity TEXT,
        confidence REAL,
        rules TEXT,
        features TEXT,
        git_metadata TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO analyses (file, severity, confidence, rules, features, git_metadata, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        file_name,
        severity,
        confidence,
        json.dumps(rules_detected),
        json.dumps(features),
        json.dumps(git_meta),
        datetime.datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
