from litestar import Litestar, get
from litestar.config.cors import CORSConfig

from who_is import whois as whois_lookup

from models.whois_response import WhoisResponse


@get("/query")
async def whois(domain: str) -> WhoisResponse:
    result = whois_lookup(domain)
    return WhoisResponse(**result.json(), raw=result.raw)

cors_config = CORSConfig(allow_origins=["*"])

app = Litestar([whois], cors_config=cors_config)
