from fastapi import APIRouter
from pydantic import BaseModel, Field
import pandas as pd
import json
import app_vars as av
from sklearn.ensemble import IsolationForest


router = APIRouter()

# @router.post("/anomaly_det")
def anomaly_det(extracted_file=av.temp_ext_file):
    """Anomaly detector
        Uses the extracted data to find anomalies and saves the anomaly data to file.
    """
    df = pd.read_csv(extracted_file)
    X = df[["AccountID", 'Amount']]
    model = IsolationForest(contamination=0.001, random_state=42)
    model.fit(X)
    y_pred = model.predict(X)
    file_path = av.uploaded_files+"/anomalies.csv"
    df[y_pred==-1].to_csv(av.temp_anom_file)