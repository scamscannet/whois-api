from models.whois.domain.whois import Whois as Wh

server = 'whois.nic.fr'

class Whois(Wh):
    _date_keys = {
        'last-update': 'updated_date',
        'created': 'registration_date',
        'Expiry Date': 'expiration_date'
    }
    _general_keys = {
        'domain': 'domain',
        'nserver': 'name_servers'
    }

    _registrar_keys = {}
    _contact_keys = {
        'registrar': ['name', None]
    }