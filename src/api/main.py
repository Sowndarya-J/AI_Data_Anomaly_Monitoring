from pathlib import Path
import math
import numbers
from decimal import Decimal
from datetime import date, datetime

import pandas as pd
from fastapi import FastAPI, HTTPException

from src.database.db_connection import get_connection


app = FastAPI(
    title="AI Data Anomaly Monitoring API",
    description="API for AI-powered transaction anomaly monitoring",
    version="1.0.0"
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ANOMALY_FILE = (
    PROJECT_ROOT / "reports" / "anomaly_results.csv"
)


# ============================================================
# JSON CLEANING
# ============================================================

def clean_for_json(data):

    if isinstance(data, dict):
        return {
            str(key): clean_for_json(value)
            for key, value in data.items()
        }

    if isinstance(data, (list, tuple)):
        return [
            clean_for_json(value)
            for value in data
        ]

    if isinstance(data, numbers.Real):

        try:

            value = float(data)

            if math.isnan(value) or math.isinf(value):
                return None

            return value

        except (TypeError, ValueError):

            return data

    if isinstance(data, Decimal):

        if not data.is_finite():
            return None

        return float(data)

    if isinstance(data, (datetime, date)):
        return data.isoformat()

    return data


# ============================================================
# LOAD ANOMALY RESULTS
# ============================================================

def load_anomaly_results():

    if not ANOMALY_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                "Anomaly results file not found. "
                "Run anomaly_detector.py first."
            )
        )

    df = pd.read_csv(ANOMALY_FILE)

    return df


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Data Anomaly Monitoring API",
        "status": "running"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    connection = None

    try:

        connection = get_connection()

        return {
            "status": "healthy",
            "database": "connected",
            "anomaly_results": ANOMALY_FILE.exists()
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

    finally:

        if connection is not None:
            connection.close()


# ============================================================
# SUMMARY
# ============================================================

@app.get("/summary")
def get_summary():

    df = load_anomaly_results()

    total = len(df)

    normal = int(
        (df["anomaly_status"] == "NORMAL").sum()
    )

    anomalies = int(
        (df["anomaly_status"] == "ANOMALY").sum()
    )

    return clean_for_json({
        "total_transactions": total,
        "normal_transactions": normal,
        "anomalies_detected": anomalies
    })


# ============================================================
# ALL ANOMALIES
# ============================================================

@app.get("/anomalies")
def get_anomalies():

    df = load_anomaly_results()

    anomalies = df[
        df["anomaly_status"] == "ANOMALY"
    ]

    records = anomalies.to_dict(
        orient="records"
    )

    return clean_for_json({
        "count": len(records),
        "anomalies": records
    })


# ============================================================
# SINGLE TRANSACTION
# ============================================================

@app.get("/anomalies/{transaction_id}")
def get_anomaly(transaction_id: str):

    df = load_anomaly_results()

    result = df[
        df["transaction_id"].astype(str)
        == transaction_id
    ]

    if result.empty:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    record = result.iloc[0].to_dict()

    return clean_for_json(record)