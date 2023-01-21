import dateutil.parser
from pydantic import BaseModel

from models.whois.domain.whois_contact import WhoisContact
from models.whois.domain.whois_date import WhoisDate
from models.whois.domain.whois_registrar import WhoisRegistrar


class Whois(BaseModel):
    # params
    domain: str = None
    registrar: WhoisRegistrar = WhoisRegistrar()
    whois: str = None
    date: WhoisDate = WhoisDate()
    name_servers: list = []
    contact: list = []

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
                    setattr(self.registrar, attribute, data)
                except Exception:
                    # TODO: Error handling
                    pass

            # Parse Contact
            elif key.lower() in self._contact_keys:
                existing_contacts = {contact.type: contact for contact in self.contact}
                attribute, raw_local_contact_type = self._contact_keys[key.lower()]
                local_contact_type = raw_local_contact_type.capitalize() if raw_local_contact_type else raw_local_contact_type
                # Cache the current contact type in case the whois record
                # defines it only once above the according values
                if not local_contact_type:
                    local_contact_type = contact_type
                else:
                    contact_type = local_contact_type

                # Check if a contact obj exists to the according type
                if local_contact_type in existing_contacts.keys():
                    contact_obj = existing_contacts[local_contact_type]
                    setattr(contact_obj, attribute, data)
                else:
                    contact_obj = WhoisContact()
                    contact_obj.type = local_contact_type
                    setattr(contact_obj, attribute, data)
                    self.contact.append(contact_obj)