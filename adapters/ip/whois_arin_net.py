from adapters.ip.ipadapter import IpAdapter

server = "whois.arin.net"


class IpWhois(IpAdapter):

    _address = ["Address:", "City:", "StateProv:", "PostalCode:", "Country:"]
    _inetnum = "NetRange:"
    _origin = "origin:"