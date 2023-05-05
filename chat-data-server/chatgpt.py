import os
import pandas as pd
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from conf.config import OPENAI_MODEL


def read_data(file_path):
    if file_path.endswith('.csv') or file_path.endswith('.txt'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json') or file_path.endswith('.jsonl'):
        df = pd.read_json(file_path)
    return df


def api_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key


def file_agent(file_path, model_name=OPENAI_MODEL):
    df = read_data(file_path)
    agent = create_pandas_dataframe_agent(
        OpenAI(model_name=model_name, temperature=0), df, verbose=True)
    return agent


def sql_agent(db_uri, model_name=OPENAI_MODEL):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db)
    agent_executor = create_sql_agent(
        llm=OpenAI(model_name=model_name, temperature=0),
        toolkit=toolkit,
        verbose=True)
    return agent_executor
