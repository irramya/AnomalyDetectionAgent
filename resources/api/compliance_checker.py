from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
import app_vars as av

router = APIRouter()

def check_duplicates():
    return df[df.duplicated(subset=['TransactionID'])].shape[0]

def check_columns():
    cols = list(df.columns)
    missing = []
    for col in ['Timestamp', 'TransactionID', 'AccountID', 'Amount', 'Merchant', 'TransactionType', 'Location', 'OrderID']: 
        if col not in cols:
            missing.append(col)
    return missing  

# @router.post("/compliance_checker")
def compliance_checker(file_path = av.temp_file):
    """Compliance checker
        Checks if the uploaded file complies with for IFRS and GAAP.
        Returns: dictionary of duplicate count and missing columns for further interpretation.
    """
    if file_path is not None:
        global df
        df = pd.read_csv(file_path)
        duplicate_count = check_duplicates()
        missing_cols = check_columns()
    return {"duplicate_count":duplicate_count, "missing_cols":missing_cols}