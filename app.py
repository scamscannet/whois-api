from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.response import Redirect
from litestar.status_codes import HTTP_301_MOVED_PERMANENTLY

from who_is import whois as whois_lookup

from models.whois_response import WhoisResponse


@get("/query")
async def whois(domain: str) -> WhoisResponse:
    result = whois_lookup(domain)
    return WhoisResponse(**result.json(), raw=result.raw)

@get("/", status_code=HTTP_301_MOVED_PERMANENTLY)
async def redirect_to_docs() -> Redirect:
    return Redirect(path="/schema/elements")

cors_config = CORSConfig(allow_origins=["*"])

openapi_config = OpenAPIConfig(
    title="Octobyte Whois API",
    description="REST API providing Whois lookups for domains and IPs",
    version="0.1",

)
app = Litestar([whois], cors_config=cors_config, openapi_config=openapi_config)
