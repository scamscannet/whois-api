import math
from typing import Any

from pydantic import BaseModel


class IpNet(BaseModel):
    first_ip: str = None
    last_ip: str = None
    all_ips: list = []
    network_prefix: int = 32

    def __init__(self, raw_inet: str):
        all_ips = []
        network_prefix = 32
        start, end = raw_inet.split(' - ')
        start_ip_list = start.split('.')
        end_ip_list = end.split('.')

        for x in range(len(start_ip_list)):
            if start_ip_list[x] == end_ip_list[x]:
                continue

            end_ip_diff = end_ip_list[x]
            start_ip_diff = start_ip_list[x]
            base_ip = ".".join(start.split(".")[:x])
            for v in range(int(start_ip_diff), int(end_ip_diff)):
                all_ips.append(f"{base_ip}.{v}")

            ips_in_subnet_count = len(base_ip)

            network_prefix = 32 - math.log(ips_in_subnet_count + 1)

        data = {
            'first_ip': start,
            'last_ip': end,
            'network_prefix': network_prefix,
            'all_ips': all_ips
        }
        super().__init__(**data)