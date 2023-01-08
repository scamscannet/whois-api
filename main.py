from fastapi import FastAPI
from starlette.responses import RedirectResponse
from models.whois.whois import Whois
from models.api.whois_response import WhoisResponse
from whois.parser import parse_whois_request_to_model
from whois.whois import response_to_key_value_json, make_whois_request

app = FastAPI(
    title="Whois API"
)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    RedirectResponse("/docs")

@app.get("/whois/{domain}", response_model=WhoisResponse)
def request_whois_data_for_domain(domain: str):
    text, whois_server = make_whois_request(domain)
    unformatted_dict = response_to_key_value_json(text)
    try:
        parsed = parse_whois_request_to_model(text, whois_server)
    except Exception as e:
        print(e)
        parsed = Whois()
    return WhoisResponse(
        parsed=parsed,
        json_format=unformatted_dict,
        raw=text
    )
