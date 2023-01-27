from adapters.ip.ipadapter import IpAdapter

server = "whois.ripe.net"


class IpWhois(IpAdapter):
    _address = ["address:"]
    _inetnum = "inetnum"
    _origin = "origin:"