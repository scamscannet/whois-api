from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = "California"
    country: Optional[str] = "United States"
    country_code: Optional[str] = "US"


class Registrar(BaseModel):
    iana_id: Optional[str] = "292"
    name: Optional[str] = "MarkMonitor, Inc."
    address: Optional[Address] = Address()
    url: Optional[str] = "http://www.markmonitor.com"
    abuse_phone: Optional[str] = "+1.2086851750"
    abuse_email: Optional[str] = "abusecomplaints@markmonitor.com"
    whois: Optional[str] = "whois.markmonitor.com"


class ContactInfo(BaseModel):
    name: Optional[str] = None
    organization: Optional[str] = "Google LLC"
    address: Optional[Address] = Address()
    email: Optional[str] = "Select Request Email Form at https://domains.markmonitor.com/whois/google.com"
    phone: Optional[str] = None
    fax: Optional[str] = None
    registry_id: Optional[str] = None


class Dates(BaseModel):
    raw: Optional[dict] = {
        "created": "1997-09-15T07:00:00+0000",
        "updated": "2024-08-02T02:17:33+0000",
        "expiration": "2028-09-13T07:00:00+0000"
    }
    formatted: Optional[dict] = {
        "created": "1997-09-15T07:00:00+00:00",
        "updated": "2024-08-02T02:17:33+00:00",
        "expiration": "2028-09-13T07:00:00+00:00"
    }


class Contact(BaseModel):
    admin: Optional[ContactInfo] = ContactInfo()
    tech: Optional[ContactInfo] = ContactInfo()
    registrant: Optional[ContactInfo] = ContactInfo()


class WhoisResponse(BaseModel):
    domain: Optional[str] = "google.com"
    name_servers: Optional[List[str]] = [
        "ns1.google.com",
        "ns4.google.com",
        "ns2.google.com",
        "ns3.google.com"
    ]
    status: Optional[List[str]] = [
        "clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)",
        "clientTransferProhibited (https://www.icann.org/epp#clientTransferProhibited)",
        "clientDeleteProhibited (https://www.icann.org/epp#clientDeleteProhibited)",
        "serverUpdateProhibited (https://www.icann.org/epp#serverUpdateProhibited)",
        "serverTransferProhibited (https://www.icann.org/epp#serverTransferProhibited)",
        "serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)"
    ]
    whois_server: Optional[str] = "whois.markmonitor.com"
    registrar: Optional[Registrar] = Registrar()
    dates: Optional[Dates] = Dates()
    contact: Optional[Contact] = Contact()
    raw: Optional[str]
