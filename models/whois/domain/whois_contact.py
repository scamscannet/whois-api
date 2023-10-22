from pydantic import BaseModel

from utils.geolocation import Location


class WhoisContact(BaseModel):
    type: str = None
    name: str = None
    organization: str = None
    email: str = None
    phone: str = None
    street: str = None
    city: str = None
    state: str = None
    postal_code: str = None
    country: str = None
    fax: str = None
    location: Location = None


class WhoisContactWrapper(BaseModel):
    registrant: WhoisContact = WhoisContact()
    admin: WhoisContact = WhoisContact()
    billing: WhoisContact = WhoisContact()
    tech: WhoisContact = WhoisContact()
