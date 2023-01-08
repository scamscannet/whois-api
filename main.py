from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from models.whois.domain.whois import Whois
from models.api.whois_response import WhoisResponse, IpWhoisResponse
from models.whois.ip.ip_whois import IpWhois
from whois.parser import parse_whois_request_to_model, parse_ip_whois_request_to_model
from whois.whois import response_to_key_value_json, make_whois_request

app = FastAPI(
    title="Whois API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/ip-whois/{ip}", response_model=IpWhoisResponse)
def request_whois_data_for_domain(ip: str):
    text, whois_server = make_whois_request(ip)
    unformatted_dict = response_to_key_value_json(text)
    try:
        parsed = parse_ip_whois_request_to_model(text, whois_server)
    except Exception as e:
        parsed = IpWhois()
    parsed.ip = ip
    return IpWhoisResponse(
        parsed=parsed,
        json_format=unformatted_dict,
        raw=text
    )
