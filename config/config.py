import os
from dotenv import load_dotenv
load_dotenv()


class config:
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    API_URL = os.getenv("API_URL")
    CLIENT_SIDE_URL = os.getenv("CLIENT_SIDE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")