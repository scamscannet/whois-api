import datetime
from dateutil import parser
from pydantic import BaseModel


class WhoisDate(BaseModel):
    registration_date: datetime.date = None
    expiration_date: datetime.date = None
    updated_date: datetime.date = None

    def process_param(self, key: str, data: str):
        if key.lower() in ['expired', 'expiration', 'expiry', 'expire']:
            self.expiration_date = parser.parse(data, fuzzy=True)
