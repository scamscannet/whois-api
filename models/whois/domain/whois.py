import dateutil.parser
from pydantic import BaseModel

from utils.geolocation import get_location
from models.whois.domain.whois_contact import WhoisContact, WhoisContactWrapper
from models.whois.domain.whois_date import WhoisDate
from models.whois.domain.whois_registrar import WhoisRegistrar


class Whois(BaseModel):
    # params
    domain: str = None
    registrar: WhoisRegistrar = WhoisRegistrar()
    whois: str = None
    date: WhoisDate = WhoisDate()
    name_servers: list = []
    contact: WhoisContactWrapper = WhoisContactWrapper()

    # Adapter params
    _date_keys: dict
    _general_keys: dict
    _contact_keys: dict
    _registrar_keys: dict

    def parse(self, parsed_text, whois_server):
        self.whois = whois_server
        contact_type = 'registrant' # Placeholder as Registrant is ususally the first used contact type
        for key, data in parsed_text:
            # Parse date
            if key.lower() in self._date_keys:
                attribute = self._date_keys[key.lower()]
                try:
                    setattr(self.date, attribute, dateutil.parser.parse(data, fuzzy=True))
                except Exception:
                    # TODO: Error handling
                    pass
            # Parse general values
            elif key.lower() in self._general_keys:
                attribute = self._general_keys[key.lower()]
                if attribute == 'name_servers':
                    setattr(self, attribute, getattr(self, attribute) + [data])  # Append to list
                else:
                    setattr(self, attribute, data)

            # Parse registrar
            elif key.lower() in self._registrar_keys:
                attribute = self._registrar_keys[key.lower()]
                try:
                    if attribute == "iana_id":
                        try:
                            setattr(self.registrar, attribute, int(data))
                        except:
                            pass
                    else:
                        setattr(self.registrar, attribute, data)

                except Exception:
                    # TODO: Error handling
                    pass

            # Parse Contact
            elif key.lower() in self._contact_keys:
                attribute, raw_local_contact_type = self._contact_keys[key.lower()]
                local_contact_type = raw_local_contact_type.lower()

                # Cache the current contact type in case the whois record
                # defines it only once above the according values
                if not local_contact_type:
                    local_contact_type = contact_type
                else:
                    contact_type = local_contact_type

                attr = getattr(self.contact, local_contact_type)
                setattr(attr, attribute, data)

        contact_types = ["tech", "registrant", "billing", "admin"]
        for contact_type in contact_types:
            contact = getattr(self.contact, contact_type)
            try:
                loc = get_location(f"{contact.organization} {contact.street}, {contact.postal_code} {contact.city}, { contact.country }")
                if loc:
                    contact.location = loc
            except Exception:
                pass
