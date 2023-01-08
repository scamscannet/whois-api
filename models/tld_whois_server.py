import requests


class TldToWhoisServer:
    tld_to_whois = dict()

    def __int__(self):
        self.load()

    def load(self):
        response = requests.get('https://www.nirsoft.net/whois-servers.txt')
        data = response.text.split('\n')
        for line in data:
            if line.startswith(';'):
                continue
            d = line.split(' ')
            if len(d) >= 2:
                tld = d[0]
                whois_server = d[1]
                self.tld_to_whois[tld] = whois_server

    def whois_server_for_tld(self, tld: str):
        try:
            return self.tld_to_whois[tld]
        except:
            return 'whois.iana.org'
