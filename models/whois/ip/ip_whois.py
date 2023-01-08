import dateutil.parser
from pydantic import BaseModel

from geolocation import get_location
from models.whois.ip.ip_whois_contact import IpWhoisContact
from models.whois.ip.ip_whois_date import IpWhoisDate
from models.whois.ip.ip_whois_organisation import IpWhoisOrganisation


class IpWhois(BaseModel):
    # params
    ip: str = None
    addresses = []
    whois: str = None

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
            if address:
                loc_obj = get_location(" ".join(address.split()))
                print(loc_obj)
                self.addresses.append(loc_obj)
                print(self.addresses)

