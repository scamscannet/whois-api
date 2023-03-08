from whois.whois import make_recursive_whois_request, make_whois_request

x, y = make_recursive_whois_request("metamask.mx")
print(x)
print("Done")
z, t = make_whois_request("metamask.mx")
print(z)