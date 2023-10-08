import os

import mongoengine
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO = os.getenv("MONGO")
    DATABASE = os.getenv("DATABASE") if os.getenv("DATABASE") else "whoisapi"

    AUTH0_ALGORITHMS = os.getenv("AUTH0_ALGORITHMS")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_ISSUER = os.getenv("AUTH0_ISSUER")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    def connect(self):
        mongoengine.connect(host=self.MONGO, db=self.DATABASE)