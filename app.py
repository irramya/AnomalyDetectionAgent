from fastapi import FastAPI
from fastapi.testclient import TestClient
import app_vars as av
import streamlit as st
import json
import os
from resources.api import report_gen
import pandas as pd
app = FastAPI()
# app.include_router(doc_parser.router)
# app.include_router(anomaly_det.router)
# app.include_router(compliance_checker.router)
app.include_router(report_gen.router)
client = TestClient(app)

st.title("Insignts Dashboard")

# Upload a CSV and store locally
uploaded_file = st.file_uploader("Select a CSV file", type='csv')
if uploaded_file is not None:
    # Create uploads dir
    if not os.path.exists(av.uploaded_files):
        os.makedirs(av.uploaded_files)
    # Save file locally
    with open(av.temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

# ano_prop = st.number_input("Percentage of anomalies required", max_value=100.0, min_value=0.0, value=1.0)/100

if st.button('Generate Results'):
    # Generate Report
    response = client.get('/report_gen')
    result = json.loads(response.json())['summary']
    st.table(result['output'])
    st.write("These are the top anomalies in the transactions")
    df = pd.read_csv(av.temp_anom_file)
    df.sort_values(by=['Amount'], inplace=True)
    st.table(df.tail(5))
    st.table(df.head(5))





