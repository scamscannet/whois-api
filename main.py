from fastapi import FastAPI

from models.whois import Whois
from models.whois_date import WhoisDate
from parser import parse_whois_request_to_model
from whois import response_to_json, make_whois_request

app = FastAPI()

@app.get("/whois/{domain}")
def request_whois_data_for_domain(domain: str):
    text, whois_server = make_whois_request(domain)
    parsed = response_to_json(text)
    parsed = parse_whois_request_to_model(text, whois_server)
    return {
        'raw': text,
        'parsed': parsed
    }
