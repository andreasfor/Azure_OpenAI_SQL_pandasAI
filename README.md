# Azure_OpenAI_SQL_pandasAI
A POC of how to use a LLM to construct SQL code and then query the database and create a subtable. In addition, the subtable can be queried with pandasAI. 

This code is based on this repository: https://github.com/NikhilSehgal123/Azure-OpenAI-SQL and https://www.youtube.com/watch?v=_VKMToxWv4E&list=PL-d_nfayLssA_k5RyfwoRtDLhyRXAq7d9&index=2&t=623s

------------------------------------------

Create virtual environment

python -m venv .venv

source .venv\Scripts\activate  # On Mac, use:.venv/bin/activate 

------------------------------------------

And create a .env file with Azure Open AI credentials 
