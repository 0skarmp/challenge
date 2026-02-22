import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///contacts.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False