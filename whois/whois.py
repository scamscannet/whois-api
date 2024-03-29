from whois.whois_request import raw_whois_request
from models.tld_whois_server import TldToWhoisServer

tld_to_whois = TldToWhoisServer()


def find_parent_whois_server_in_response(response: str):
    splitted_response = response.lower().split('\n')
    for line in splitted_response:

        if line.startswith('%') or line.startswith(">>>") or line.startswith("#"):
            continue

        if 'whois' in line.lower():
            try:
                key, data = line.replace('http://', '')\
                    .replace('whois://', '')\
                    .replace('rwhois://', '') \
                    .replace('https://', '') \
                    .replace(' ', '')\
                    .split(':')

            except Exception:
                continue

            if 'refer' in key or 'whoisserver' in key.lower():
                yield data


def make_recursive_whois_request(domain: str) -> (str, str):
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
            whois_server = None
            try:
                new_servers = find_parent_whois_server_in_response(whois_data)
                for new_server in new_servers:

                    if new_server and whois_server != new_server and not new_server in used_servers:
                        whois_server = new_server.replace("\r", "")
                        break
            except:
                whois_server = None

    if current_whois_data:
        return current_whois_data, last_used_whois_server

    else:
        raise Exception("Error while making whois request")


def make_whois_request(domain: str) -> (str, str):
    whois_server = tld_to_whois.whois_server_for_tld(domain.split('.')[1])
    try:
        whois_data = raw_whois_request(whois_server, domain)
    except:
        raise Exception("Error while making whois request")

    if whois_data:
        return whois_data, whois_server
    else:
        raise Exception("Error while making whois request")


def make_ip_whois_request(ip: str) -> (str, str):
    whois_server = 'whois.iana.org'
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
            whois_server = None

            try:
                new_servers = find_parent_whois_server_in_response(whois_data)
                for new_server in new_servers:
                    if new_server and whois_server != new_server and not new_server in used_servers:
                        whois_server = new_server.replace("\r", "")
                        break
            except Exception as e:
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
