import traceback

from diskcache import Cache
from fastapi import FastAPI, Request
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


def add_to_cache(domain: str):
    with Cache('cache') as cache:
        cached_domains = cache.get("domain_whois")
        if cached_domains:
            new_domains = cached_domains.split(",")[-9:]
            new_domains.append(domain)
        else:
            new_domains = [domain]
        cache.set("domain_whois", ','.join(new_domains))

def add_ip_to_cache(ip: str):
    with Cache('cache') as cache:
        cached_domains = cache.get("ip_whois")
        if cached_domains:
            new_domains = cached_domains.split(",")[-9:]
            new_domains.append(ip)
        else:
            new_domains = [ip]
        cache.set("ip_whois", ','.join(new_domains))


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    RedirectResponse("/docs")


@app.get("/whois/{domain}", response_model=WhoisResponse)
def request_whois_data_for_domain(domain: str):
    text, whois_server = make_whois_request(domain)
    unformatted_dict = response_to_key_value_json(text)
    try:
        parsed = parse_whois_request_to_model(text, whois_server)
        add_to_cache(domain)
    except Exception as e:
        print(e)
        parsed = Whois()
    return WhoisResponse(
        parsed=parsed,
        json_format=unformatted_dict,
        raw=text
    )


@app.get("/ip-whois/{ip}")
def request_whois_data_for_domain(ip: str, max_ipnet_size: int = 500):
    text, whois_server = make_whois_request(ip)
    unformatted_dict = response_to_key_value_json(text)
    try:
        parsed = parse_ip_whois_request_to_model(text, whois_server, max_ipnet_size)
        add_ip_to_cache(ip)
    except Exception as e:
        print(e)
        parsed = IpWhois()
    parsed.ip = ip
    return IpWhoisResponse(
        parsed=parsed,
        json_format=unformatted_dict,
        raw=text
    )

@app.get("/history")
def get_last_10_whois_requests():
    with Cache('cache') as cache:
        cached_domains = cache.get("domain_whois")
        if cached_domains:
            domains = cached_domains.split(',')
        else:
            domains = []

        cached_ips = cache.get("ip_whois")
        if cached_ips:
            ips = cached_ips.split(',')
        else:
            ips = []

    return {
        'domain': domains,
        'ip': ips
    }

@app.get('/current-ip')
def get_current_ip(request: Request):
    client_host = request.client.host
    return {"ip": client_host}