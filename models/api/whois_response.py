from pydantic import BaseModel

from models.whois import Whois


class WhoisResponse(BaseModel):
    parsed: Whois
    json_format: dict
    raw: str