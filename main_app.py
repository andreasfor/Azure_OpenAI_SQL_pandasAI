# main_app.py

import streamlit as st
import sqlite3
import pandas as pd
import sql_db
from prompts.prompts import SYSTEM_MESSAGE
from azure_openai import get_completion_from_messages
from pandas_azure_openai import PandasAIClass
import json

import os
import openai
from dotenv import load_dotenv
import pandas as pd
from pandasai import Agent
from pandasai.skills import skill
# from pandasai import SmartDataframe

from pandasai.llm.azure_openai import AzureOpenAI

def query_database(query):
    """ Run SQL query and return results in a dataframe """
    return pd.read_sql_query(query, conn)


# Create or connect to SQLite database
conn = sql_db.create_connection()

# Schema Representation for finances table
schemas = sql_db.get_schema_representation()
print(schemas['finances'])

# Format the system message with the schema
formatted_system_message = SYSTEM_MESSAGE.format(schema=schemas['finances'])

# Generate the SQL query from the user message
user_message = "Show me all expenses greater than 1000"
# user message = "Sum the total profit where expenses greater than 1000 and count the occurrences. The name of the sum should be PROFIT and the count name should be CNT"
# user_message = "Sum the total profit"

# Use GPT-4 to generate the SQL query
response = get_completion_from_messages(formatted_system_message, user_message)

json_response = json.loads(response)
query = json_response['query']
print(query)

# Run the SQL query
sql_results = query_database(query)
print(sql_results)

# Instantiate a pamdas agent with the subset of the querry results
pandas_agent_no_chart = PandasAIClass.return_pandas_agent_no_chart(subset_data=sql_results)

# Chat with the agent
response = pandas_agent_no_chart.chat("What is the max expense?")
print(response)





