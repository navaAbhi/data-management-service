from dotenv import load_dotenv
from decouple import config

load_dotenv()

DATABASE_URI = config("DATABASE_URI")
DATABASE_NAME = config("DATABASE_NAME")
BACKEND_CORS_ORIGINS = config("BACKEND_CORS_ORIGINS")
