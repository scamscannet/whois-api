import dateutil.parser
from pydantic import BaseModel

from geolocation import get_location
from models.whois.ip.ip_whois_inet import IpNet


class IpWhois(BaseModel):
    # params
    ip: str = None
    addresses = []
    whois: str = None
    ipnet: IpNet = None
    as_id: int = None

    def parse(self, text, whois_server):
        self.whois = whois_server
        for part in text.split("\n\n"):
            address = ""
            for line in part.split("\n"):
                if "address:" in line:
                    try:
                        key, part_address = line.split(":")
                        address += part_address
                    except:
                        pass

                if "inetnum" in line:
                    key, inet = line.split(":")
                    self.ipnet = IpNet(inet.strip())

                if "origin: " in line:
                    print(line)
                    key, asn = line.split(":")
                    self.as_id = int(asn.strip().replace("AS", ""))



            if address:
                loc_obj = get_location(" ".join(address.split()))
                self.addresses.append(loc_obj)

