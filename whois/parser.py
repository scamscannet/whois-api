from whois.whois import response_to_json
from adapters import adapters



def parse_whois_request_to_model(text: str, whois_server):
    parsed = response_to_json(text)
    if whois_server not in adapters.keys():
        adapter = adapters['RAA2013']()
    else:
        adapter = adapters[whois_server]()
    adapter.parse(parsed, whois_server)
    return adapter
