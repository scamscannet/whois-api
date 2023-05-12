import datetime
import json
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from database.registry.WhoisRecordRegistry import get_record_for_domain_if_existing, store_new_record
from models.whois.domain.whois import Whois
from models.api.whois_response import WhoisResponse, IpWhoisResponse
from models.whois.ip.ip_whois import IpWhois
from whois.parser import parse_whois_request_to_model, parse_ip_whois_request_to_model
from whois.whois import response_to_key_value_json, make_whois_request, make_ip_whois_request, \
    make_recursive_whois_request
from tldextract import extract

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


def caching_whois_request(domain: str, renew: bool = False):
    timestamp = datetime.datetime.now()
    if not renew:
        try:
            text, whois_server, timestamp = get_record_for_domain_if_existing(domain)
            return text, whois_server, timestamp
        except Exception:
            pass
    text, whois_server = make_recursive_whois_request(domain)
    store_new_record(domain=domain, whois_server=whois_server, response=text)
    return text, whois_server, timestamp


def caching_ip_whois_request(domain: str, renew: bool = False):
    timestamp = datetime.datetime.now()
    if not renew:
        try:
            text, whois_server, timestamp = get_record_for_domain_if_existing(domain)
            return text, whois_server, timestamp
        except Exception:
            pass
    text, whois_server = make_ip_whois_request(domain)
    store_new_record(domain=domain, whois_server=whois_server, response=text)
    return text, whois_server, timestamp


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.get("/whois/{domain}", response_model=WhoisResponse, tags=["Domain"])
def request_whois_data_for_domain(domain: str, live: bool = False):
    """Request whois data for a specific domain. The whois data is either queried live or loaded from our cache. The
    timestamp in the response indicates the time of the query. Setting live to true disables the cache and results in querying the latest whois data. """
    extracted_domain = extract(domain)
    parsed_domain = extracted_domain.domain + "." + extracted_domain.suffix

    text, whois_server, timestamp = caching_whois_request(parsed_domain, renew=live)

    unformatted_dict = response_to_key_value_json(text)
    try:
        parsed = parse_whois_request_to_model(text, whois_server)
    except Exception as e:
        parsed = Whois()
    response = WhoisResponse(
        parsed=parsed,
        json_format=unformatted_dict,
        raw=text,
        timestamp=timestamp,
        live=live

    )
    return response


@app.get("/ip-whois/{ip}", tags=["IP"])
def request_whois_data_for_ip(ip: str, max_ipnet_size: int = 64):
    text, whois_server, timestamp = caching_ip_whois_request(ip)
    unformatted_dict = response_to_key_value_json(text)
    try:
        parsed = parse_ip_whois_request_to_model(text, whois_server, max_ipnet_size)
    except Exception as e:
        print(e)
        parsed = IpWhois()
    parsed.ip = ip

    response = IpWhoisResponse(
        parsed=parsed,
        json_format=unformatted_dict,
        raw=text
    )

    return response