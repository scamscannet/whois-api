import time

import requests

from whois.whois import make_whois_request

domains = requests.get("https://raw.githubusercontent.com/chainapsis/phishing-block-list/main/block-list.txt").text.split("\n")
t_start = time.time()
for domain in domains:
    print(domain)
    text, whois_server = make_whois_request(domain)
t_end = time.time()

total_time = t_end - t_start
print(f"{round(t_end - t_start, 2)} seconds => {round((t_end - t_start) / len(domains), 4)}")