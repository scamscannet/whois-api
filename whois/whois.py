from whois.whois_request import raw_whois_request
from models.tld_whois_server import TldToWhoisServer

tld_to_whois = TldToWhoisServer()


def find_parent_whois_server_in_response(response: str):
    splitted_response = response.lower().split('\n')
    for line in splitted_response:

        if 'whois' in line and not (line.startswith('%') or line.startswith(">>>")):
            try:
                key, data = line.replace('http://', '').replace('https://', '').replace(' ', '').split(':')
                return data
            except:
                continue
    return ""


def make_whois_request(domain: str) -> (str, str):
    whois_server = tld_to_whois.whois_server_for_tld(domain.split('.')[1])
    used_servers = []
    last_used_whois_server = None
    current_whois_data = None
    while whois_server:
        try:
            whois_data = raw_whois_request(whois_server, domain)
        except:
            break
        last_used_whois_server = whois_server
        used_servers.append(whois_server)
        if whois_data:
            current_whois_data = whois_data
            try:
                new_server = find_parent_whois_server_in_response(whois_data).replace("\r", "")
                if new_server and whois_server != new_server and not new_server in used_servers and "whois" in new_server:
                    whois_server = new_server
                else:
                    whois_server = None
            except:
                whois_server = None

    if current_whois_data:
        return current_whois_data, last_used_whois_server

    else:
        raise Exception("Error while making whois request")


def make_ip_whois_request(ip: str) -> (str, str):
    tld_to_whois = TldToWhoisServer()
    tld_to_whois.load()
    whois_server = tld_to_whois.whois_server_for_tld(ip.split('.')[1])
    used_servers = []
    last_used_whois_server = None
    current_whois_data = None
    while whois_server:
        if "/" in whois_server:
            break
        try:
            fip = ip
            if whois_server == "whois.arin.net":
                fip = "n + " + fip
            whois_data = raw_whois_request(whois_server, fip)
        except:
            break
        last_used_whois_server = whois_server
        used_servers.append(whois_server)
        if whois_data:
            current_whois_data = whois_data
            try:
                new_server = find_parent_whois_server_in_response(whois_data).replace("\r", "")
                if new_server and whois_server != new_server and not new_server in used_servers:
                    whois_server = new_server
                else:
                    whois_server = None
            except:
                whois_server = None

    if current_whois_data:
        return current_whois_data, last_used_whois_server

    else:
        raise Exception("Error while making whois request")


def response_to_json(response: str):
    for line in response.split('\n'):
        if ':' not in line:
            continue
        key_raw, data_raw = line.split(':', 1)
        key = key_raw.strip()
        data = data_raw.strip()
        yield key, data


def response_to_key_value_json(response: str):
    return_dict = dict()
    for line in response.split('\n'):
        if ':' not in line:
            continue
        key_raw, data_raw = line.split(':', 1)
        key = key_raw.strip()
        data = data_raw.strip()
        if key not in return_dict.keys():
            return_dict[key] = data
        else:
            if isinstance(return_dict[key], list):
                return_dict[key].append(data)
            else:
                return_dict[key] = [return_dict[key], data]
    return return_dict
