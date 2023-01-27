from pydantic import BaseModel

from models.whois.ip.ip_whois import IpWhois
from models.whois.ip.ip_whois_inet import IpNet
from utils.geolocation import get_location

server = None

class IpAdapter(IpWhois):
    _address: list
    _inetnum: str
    _origin: str

    def parse(self, text, whois_server, max_ipnet_size: int = 500):
        self.whois = whois_server
        for part in text.split("\n\n"):
            address = ""
            for line in part.split("\n"):
                if any(t in line for t in self._address):
                    try:
                        key, part_address = line.split(":")
                        address += part_address
                    except:
                        pass
                if self._inetnum in line:
                    key, inet = line.split(":")
                    self.ipnet = IpNet(inet.strip(), max_ipnet_size=max_ipnet_size)

                if self._origin in line:
                    key, asn = line.split(":")
                    self.as_id = int(asn.strip().replace("AS", ""))



            if address:
                loc_obj = get_location(" ".join(address.split()))
                self.addresses.append(loc_obj)
