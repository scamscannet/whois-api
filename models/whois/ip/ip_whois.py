from pydantic import BaseModel

from utils.geolocation import get_location
from models.whois.ip.ip_whois_inet import IpNet


class IpWhois(BaseModel):
    # params
    ip: str = None
    addresses = []
    whois: str = None
    ipnet: IpNet = None
    as_id: int = None

    def parse(self, text, whois_server, max_ipnet_size: int = 500):
        pass
