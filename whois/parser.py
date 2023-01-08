from whois.whois import response_to_json
from adapters.domain import adapters
from adapters.ip import adapters as ip_adapters



def parse_whois_request_to_model(text: str, whois_server):
    parsed = response_to_json(text)
    if whois_server not in adapters.keys():
        adapter = adapters['RAA2013']()
    else:
        adapter = adapters[whois_server]()
    adapter.parse(parsed, whois_server)
    return adapter

def parse_ip_whois_request_to_model(text: str, whois_server):
    if whois_server not in ip_adapters.keys():
        adapter = ip_adapters['whois.ripe.net']()
    else:
        adapter = ip_adapters[whois_server]()
    adapter.parse(text, whois_server)
    return adapter
