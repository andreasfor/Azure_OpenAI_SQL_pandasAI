# main_app.py

import streamlit as st
import sqlite3
import pandas as pd
import sql_db
from prompts.prompts import SYSTEM_MESSAGE
from azure_openai import get_completion_from_messages
#from pandas_azure_openai import return_pandas_agent
from pandas_azure_openai import PandasAIClass
from main_app_folder.support_functions import SupportMainApp
from PIL import Image
import json
import os

def query_database(query, conn):
    """ Run SQL query and return results in a dataframe """
    return pd.read_sql_query(query, conn)

# Create or connect to SQLite database
conn = sql_db.create_connection()

# Schema Representation for finances table
schemas = sql_db.get_schema_representation()

#---------------------------------------------------
    # STEP 0 Visualuza an example of the financial dataframe
#---------------------------------------------------

st.title("Step 0. An example of the financial table")

example_query = "SELECT * FROM finances LIMIT 5"
sql_example_results_df = query_database(example_query, conn)

st.dataframe(sql_example_results_df)

#---------------------------------------------------
    # STEP 1 Extract a subset of the data 
#---------------------------------------------------

st.title("Step 1. SQL Query Generator with GPT-4")
st.write("Enter your message to generate SQL and view results.")

# Input field for the user to type a message
user_message_extract_subset = st.text_input("Enter your message:", key="1")

if user_message_extract_subset:
    # Format the system message with the schema
    formatted_system_message = SYSTEM_MESSAGE.format(schema=schemas['finances'])

    # Use GPT-4 to generate the SQL query
    response = get_completion_from_messages(formatted_system_message, user_message_extract_subset)
    json_response = json.loads(response)
    query = json_response['query']

    # Display the generated SQL query
    st.write("Generated SQL Query:")
    st.code(query, language="sql")

    try:
        # Run the SQL query and display the results
        sql_results = query_database(query, conn)
        st.write("Query Results:")
        st.dataframe(sql_results)

    except Exception as e:
        st.write(f"An error occurred: {e}")

#---------------------------------------------------
    # STEP 2.1 Ask a question about the subset
#---------------------------------------------------

    # Only proceed if we have a subset of the data
    if not sql_results.empty:

        st.title("Step 2.1. Ask a question about the subset above")

        # Input field for the user to type a message
        user_message_query_subset = st.text_input("Enter your message:", key="2")

        try:
            
            pandas_agent_no_chart = PandasAIClass.return_pandas_agent_no_chart(subset_data=sql_results)
            #pandas_agent = return_pandas_agent(subset_data=sql_results)

            # Chat with the agent
            response_math_query = pandas_agent_no_chart.chat(user_message_query_subset)
            # print(response)

            # Display the generated SQL query
            st.write("Generated results:")
            st.write(response_math_query)

            try:
                # Remove temp images
                os.remove("temp_chart.png")
            except:
                pass

        except Exception as e:
            st.write(f"An error occurred: {e}")

#---------------------------------------------------
# STEP 2.2 Plot a graph based on the subset of the data
#---------------------------------------------------

    # Only proceed if we have a subset of the data
    if not sql_results.empty:

        st.title("Step 2.2. Frame a question for making a graph of the subset above")

        user_message_query_subset_graph = None

        # Input field for the user to type a message
        user_message_query_subset_graph = st.text_input("Enter your message:", key="3")
        
        if user_message_query_subset_graph != None:

            try:

                # Remove temp images
                SupportMainApp.remove_png_files(folder_path="temp_charts")

                pandas_agent_chart = PandasAIClass.return_pandas_agent_with_chart(subset_data=sql_results, save_chart=True, user_defined_path="temp_charts")

                # If the query is based on graph, then the agent will save the image
                response_chart_query = pandas_agent_chart.chat(user_message_query_subset_graph)

                response_image = None
                
                # This function will retrive the temp image, the image name is genereted as a hash key and therefore I use the first image and not call it by name
                response_image = SupportMainApp.get_first_png_image_in_folder(folder_path="temp_charts")

                if response_image != None:

                    # Display the generated SQL query
                    st.write("Generated graph:")
                    st.image(response_image)

                    # Remove temp images
                    SupportMainApp.remove_png_files(folder_path="temp_charts")

                else:
                    st.write("No graph was returned")

            except Exception as e:
                st.write(f"An error occurred: {e}")
