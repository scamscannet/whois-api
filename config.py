import os

import mongoengine
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO = os.getenv("MONGO")
    DATABASE = os.getenv("DATABASE") if os.getenv("DATABASE") else "whoisapi"
    def connect(self):
        mongoengine.connect(host=self.MONGO, db=self.DATABASE)