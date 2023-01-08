from models.whois.ip.ip_whois import IpWhois as Wh

server = "whois.ripe.net"


class IpWhois(Wh):
    _date_keys = {
        'last-modified': 'updated_date',
        'created': 'registration_date',
        'registrar registration Expiration Date': 'expiration_date'
    }

    _general_keys = {
        'domain name': 'domain',
        'registrar whois server': 'whois',
        'name server': 'name_servers',
    }

    _registrar_keys = {
        'registrar': 'name',
        'registrar iana id': 'iana_id',
        'registrar url': 'url',
        'registrar abuse contact email': 'abuse_mail',
        'registrar abuse contact phone': 'abuse_phone',
    }

    _contact_keys = {
        f"{cloudflare_type} {attribute}": [value, local_type]
        for attribute, value in
        [['name', 'name'], ['organization', 'organization'], ['street', 'street'], ['City', 'city'],
         ['state/province', 'state'], ['postal code', 'postal_code'], ['country', 'country'], ['phone', 'phone'],
         ['fax', 'fax'], ['email', 'email']]
        for cloudflare_type, local_type in
        [['registrant', 'registrant'], ['admin', 'admin'], ['tech', 'tech'], ['billing', 'billing']]
    }
