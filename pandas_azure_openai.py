import os
import openai
from dotenv import load_dotenv

import pandas as pd
from pandasai import Agent
from pandasai.skills import skill
# from pandasai import SmartDataframe

from pandasai.llm.azure_openai import AzureOpenAI


class PandasAIClass():
    """
    This class creates an instance of a pandas AI agent.
    """

    def return_pandas_agent_no_chart(subset_data):

        load_dotenv()

        azure_openai_api_key = os.getenv("OPENAI_API_KEY")
        azure_openai_api_type = os.getenv("AZURE_OPENAI_API_TYPE")
        azure_openai_api_base = os.getenv("AZURE_OPENAI_API_BASE")
        azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        deployment_name = os.getenv("AZURE_API_DEPLOYMENT_NAME")

        llm = AzureOpenAI(api_token=azure_openai_api_key, 
                    api_base=azure_openai_api_base,
                    api_version=azure_openai_api_version,
                    deployment_name="gpt-4-pandas-ai", 
                    is_chat_model=True)

        agent = Agent(dfs=[subset_data], config={"llm": llm}, memory_size=10)

        return agent
    

    def return_pandas_agent_with_chart(subset_data, save_chart=True, user_defined_path="temp_chart"):

        load_dotenv()

        azure_openai_api_key = os.getenv("OPENAI_API_KEY")
        azure_openai_api_type = os.getenv("AZURE_OPENAI_API_TYPE")
        azure_openai_api_base = os.getenv("AZURE_OPENAI_API_BASE")
        azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        deployment_name = os.getenv("AZURE_API_DEPLOYMENT_NAME")

        llm = AzureOpenAI(api_token=azure_openai_api_key, 
                    api_base=azure_openai_api_base,
                    api_version=azure_openai_api_version,
                    deployment_name="gpt-4-pandas-ai", 
                    is_chat_model=True)

        agent = Agent(dfs=[subset_data], config={"llm": llm, "save_charts": save_chart, "save_charts_path": user_defined_path}, memory_size=10)

        return agent
