import math
from typing import Any

from pydantic import BaseModel

from utils.ipnetcalc import get_all_ips_in_subnet, sortfunc


class IpNet(BaseModel):
    first_ip: str = None
    last_ip: str = None
    all_ips: list = []

    def __init__(self, raw_inet: str):
        start, end = raw_inet.split(' - ')
        start_ip_as_list = start.split('.')
        end_ip_as_list = end.split('.')

        all_ips = get_all_ips_in_subnet(start_ip_as_list, end_ip_as_list)
        all_ips = all_ips[100:]
        all_ips.sort(key=sortfunc)
        data = {
            'first_ip': start,
            'last_ip': end,
            'all_ips': all_ips
        }
        super().__init__(**data)
