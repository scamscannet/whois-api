import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO = os.getenv("MONGO")
    MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
