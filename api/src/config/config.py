import os
from dotenv import load_dotenv

load_dotenv()

# For testing, use SQLite if PostgreSQL is not available
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

class Config:
    # Use SQLite for testing if PostgreSQL connection fails
    if db_user and db_pass and db_host and db_name:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    else:
        # Fallback to SQLite for testing
        SQLALCHEMY_DATABASE_URI = "sqlite:///blacklist_test.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
