from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

FRONTEND_URL = os.getenv("FRONTEND_URL")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

if not all([MONGO_URI, DB_NAME, ATLAS_VECTOR_SEARCH_INDEX_NAME, LLM_MODEL_NAME, FRONTEND_URL, JWT_SECRET_KEY, JWT_ALGORITHM]):
    raise ValueError("Missing enviroment variables in env")