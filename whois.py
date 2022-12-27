from whois_request import raw_whois_request
from tld_whois_server import TldToWhoisServer


def find_parent_whois_server_in_response(response: str):
    splitted_response = response.lower().split('\n')
    for line in splitted_response:
        if 'whois' in line and not line.startswith('%'):
            key, data = line.replace('http://', '').replace('https://', '').replace(' ', '').split(':')
            return data
    return None


def make_whois_request(domain: str) -> (str, str):
    tld_to_whois = TldToWhoisServer()
    tld_to_whois.load()
    whois_server = tld_to_whois.whois_server_for_tld(domain.split('.')[1])
    used_servers = []
    last_used_whois_server = None
    while whois_server:
        whois_data = raw_whois_request(whois_server, domain)
        last_used_whois_server = whois_server
        used_servers.append(whois_server)
        if whois_data:
            new_server = find_parent_whois_server_in_response(whois_data).replace("\r", "")
            if whois_server != new_server and not new_server in used_servers:
                whois_server = new_server
            else:
                whois_server = None
        else:
            raise Exception("Error while making whois request")
    return whois_data, last_used_whois_server


def response_to_json(response: str):
    for line in response.split('\n'):
        if ':' not in line:
            continue
        key_raw, data_raw = line.split(':', 1)
        key = key_raw.strip()
        data = data_raw.strip()
        yield key, data
