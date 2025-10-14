import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
