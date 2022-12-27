from models.whois import Whois as Wh


class Whois(Wh):
    print("Hi")
    assoc_whois_server = "whois.cloudflare.com"
    _date_keys = {
        'Updated Date': 'updated_date',
        'Creation Date': 'registration_date',
        'Registrar Registration Expiration Date': 'expiration_date'
    }

    _general_keys = {
        'Domain Name': 'domain',
        'Registrar WHOIS Server': 'whois',
        'Name Server': 'name_servers',
    }

    _registrar_keys = {
        'Registrar': 'name',
        'Registrar IANA ID': 'iana_id',
        'Registrar URL': 'url',
        'Registrar Abuse Contact Email': 'abuse_mail',
        'Registrar Abuse Contact Phone': 'abuse_phone',
    }

    _contact_keys = {
        f"{cloudflare_type} {attribute}": [value, local_type]
        for attribute, value in [['Name', 'name'], ['Organization', 'organization'], ['Street', 'street'], ['City', 'city'], ['State/Province', 'state'], ['Postal Code', 'postal_code'], ['Country', 'country'], ['Phone', 'phone'], ['Fax', 'fax'], ['Email', 'email']]
        for cloudflare_type, local_type in [['Registrant', 'registrant'], ['Admin', 'admin'], ['Tech', 'tech'], ['Billing', 'billing']]
    }


