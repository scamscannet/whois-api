from pydantic import BaseModel

class WhoisRegistrar(BaseModel):
    name: str = None
    iana_id: int = None
    url: str = None
    #whois: str = None
    abuse_mail: str = None
    abuse_phone: str = None

