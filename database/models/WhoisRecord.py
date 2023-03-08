import datetime
import uuid

from mongoengine import *


class WhoisRecord(Document):
    rid = StringField(default=str(uuid.uuid4()))
    domain = StringField()
    whois_server = StringField()
    unformatted_response = StringField()
    timestamp = DateTimeField(default=datetime.datetime.now())
