import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
load_dotenv()
openai_api_key = os.getenv('OPEN_AI_KEY')
database_user = os.getenv('DB_USER') 
database_password = os.getenv('DB_PASSWORD') 
database_host = os.getenv('DB_HOST')  
database_name = os.getenv('DB_NAME') 
database_instance = SQLDatabase.from_uri(f"mysql+pymysql://{database_user}:{database_password}@{database_host}/{database_name}")