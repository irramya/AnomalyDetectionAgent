import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from fastapi import APIRouter
from pydantic import BaseModel
import json
from resources.api import doc_parser, anomaly_det, compliance_checker
from resources.prompts import transaction_analyzer
from langchain.tools.base import StructuredTool
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_json_chat_agent
from langchain.agents import AgentExecutor

router = APIRouter()

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class QueryRequest(BaseModel):
    query: str

llm = ChatGroq(
    # model="mixtral-8x7b-32768",
    model="llama3-8b-8192",
    temperature=0.2,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", transaction_analyzer.transaction_analyzer),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ],
)

tools = [
    StructuredTool.from_function(doc_parser.doc_parser),
    StructuredTool.from_function(anomaly_det.anomaly_det),
    StructuredTool.from_function(compliance_checker.compliance_checker)
]

agent = create_json_chat_agent(llm, tools, prompt)

@router.get("/report_gen")
def report_gen():
    input = "Analyze the financial document"
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    response = agent_executor.invoke({'input':input})
    return json.dumps({"summary": response})