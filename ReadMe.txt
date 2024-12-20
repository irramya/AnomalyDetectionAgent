Assumptions:
1. Input data is available in the pre-defined csv format. PDF to table support can be added in upcoming version.
2. Agents can be added at each step for targetted decision making.
    ex: Document parser can identify the type of document and apply the relevant parsing technique.
    Anomaly detector can use transaction/merchant specific anomaly extractions.
    Compliance checker can verify specifically on pre-set standards.
    Report generator can generate more refined summaries.
    In this POC, Agent is implemented only at the report generation stage for simplicity.
3. RAG can be implemented to train on curated internal compliance policies. LLMs are aware of standard compliance frameworks, hence skipping RAG.
4. Several outlier identification techniques like z-score, IQR, IsolationForest (currently used) are available.

Note: 
1. Code left in comments can be used to modify the components. Ex: Each step can be accessed via a separate endpoint (while not used as tools).
2. Refer sample_output to see the agent thought and UI.

Setup:
1. Groq key - Free key available at https://console.groq.com/keys
2. Langchain key - Sign up at https://smith.langchain.com/
Example .env :
GROQ_API_KEY="gsk_QegKaRCRaExGUF5tvbWGdyb3FYN4aEndVrzxrKZFImgVy"
LANGCHAIN_API_KEY="lsv2_pt_60a4a2039de3482a861066bc794_d277bfeeaa"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="KPMG"

Execution:
pip install -r requirements.txt
streamlit run app.py

Requirement:
Agents:
1. Document parser 
    {
        Input: Customer's document.
        Output: Parsed document (extracted financial data).
        Desc: csv should be cleaned and formatted.
            pdf should be converted to tables, cleaned and formatted.
    }

2. Anomaly detector
    {
        Input: Parsed document (extracted financial data), percentage of anomalies
        Output: Flitered anomalies.
        Desc: Detects the given proportion of anomalies using IsolationForest.
    }

3. Compliance checker
    {
        Input: Customer's document.
        Output: Compliance adherence report
        Desc: Financial statements (balance sheet, income statement, cash flow statement) for IFRS and GAAP.
            Tax-related data for IRS compliance.
            Audit trails and documentation for GAP3.
    }

4. Report generator
    {
        Input: Anomalies, Compliance adherence report
        Output: Dashboard reporting format
        Desc: structure and summarize the collated data
    }

UseCase1:
1. Customer's data is fed via file upload.
2. Data is extracted in the correct format.
3. Extracted data is analysed for anomalies.
4. Compliance check based on the type of the data.
5. Collate final results.
6. Display findings on the dashboard.