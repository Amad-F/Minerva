import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = "mysql+pymysql://root:12345678@localhost:3306/minerva_db"
    
    # This is the permanent directory for the university documents (slides)
    DOCUMENT_DIRECTORY = "B:\\Modules"
