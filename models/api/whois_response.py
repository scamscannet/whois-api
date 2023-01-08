from pydantic import BaseModel

from models.whois.ip.ip_whois import IpWhois
from models.whois.domain.whois import Whois


class WhoisResponse(BaseModel):
    parsed: Whois
    json_format: dict
    raw: str

class IpWhoisResponse(BaseModel):
    parsed: IpWhois
    json_format: dict
    raw: str