from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
import app_vars as av
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder

router = APIRouter()

class QueryRequest(BaseModel):
    file_path: str

# @router.post("/doc_parser")
def doc_parser(file_path = av.temp_file):
    """Document parser
        Uses the uploaded file to extract data in the required format and saves the extracted data to file.
    """
    df = pd.read_csv(file_path)
    df.dropna(axis='rows', inplace=True)
    df["AccountID"]=df["AccountID"].apply(lambda x: int(x[3:]))
    df['Timestamp']=df['Timestamp'].apply(lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M"))
    encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore').fit(df[["Merchant", "TransactionType", "Location"]])
    encoded = encoder.transform(df[["Merchant", "TransactionType", "Location"]])
    enc_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out())
    X = pd.concat([df[['AccountID', 'Amount']], enc_df], axis=1)
    X.to_csv(av.temp_ext_file)