from fastapi import FastAPI

from models.api.whois_response import WhoisResponse
from parser import parse_whois_request_to_model
from whois import make_whois_request, response_to_key_value_json

app = FastAPI(
    title="Whois API"
)

@app.get("/whois/{domain}", response_model=WhoisResponse)
def request_whois_data_for_domain(domain: str):
    text, whois_server = make_whois_request(domain)
    unformatted_dict = response_to_key_value_json(text)
    parsed = parse_whois_request_to_model(text, whois_server)
    return WhoisResponse(
        parsed=parsed,
        json_format=unformatted_dict,
        raw=text
    )
