from whois.whois import make_whois_request, response_to_key_value_json

domain = "lidl.com"
reference_whois_server = "whois.eurodns.com"
reference_creation_date = "2000-02-20T00:00:00Z"

def test_whois_request():
    text, whois_server = make_whois_request("lidl.com")
    assert whois_server == reference_whois_server

    unformatted_dict = response_to_key_value_json(text)
    creation_date_in_whois = unformatted_dict["Creation Date"]
    assert creation_date_in_whois == reference_creation_date
