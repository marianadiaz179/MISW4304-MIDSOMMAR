import os
from dotenv import load_dotenv

load_dotenv()

# Get database configuration from environment variables
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT", "5432")

class Config:
    # Use PostgreSQL if environment variables are set, otherwise SQLite for local development
    if db_user and db_pass and db_host and db_name:
        # Production: PostgreSQL (AWS RDS)
        SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    else:
        # Development: SQLite (local testing)
        SQLALCHEMY_DATABASE_URI = "sqlite:///blacklist_test.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_database.db"
    TESTING = True