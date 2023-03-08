from database.models.WhoisRecord import WhoisRecord
from config import Config

Config().connect()


def store_new_record(domain: str, whois_server: str, response: str):
    doc = WhoisRecord(
        domain=domain,
        whois_server=whois_server,
        unformatted_response=response,
    ).save()
    return doc.rid


def get_record_for_domain_if_existing(domain: str) -> (str, str):
    record = WhoisRecord.objects(domain=domain).order_by("-timestamp").first()
    if record:
        return record.unformatted_response, record.whois_server
    raise Exception("Not found")
