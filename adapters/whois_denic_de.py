from models.whois.whois import Whois as Wh

server = 'whois.denic.de'
class Whois(Wh):
    _date_keys = {
        'changed': 'updated_date',
    }
    _general_keys = {
        'domain': 'domain',
        'nserver': 'name_servers'
    }

    _registrar_keys = {}
    _contact_keys = {}