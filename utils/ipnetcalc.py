def get_all_ips_in_subnet(start: list, end: list):
    cache = []
    ip = []
    # Calculate range for each block
    for x in range(4):
        if start[x] == end[x]:
            ip.append(start[x])
        else:
            ip.append(f"{start[x]}-{end[x]}")

    cache.append(ip)

    range_found = True

    while range_found:
        range_found = False
        # Loop through every ip struct
        for ip in list(cache):
            for pos, part in enumerate(ip):
                if not "-" in str(part):
                    continue
                range_found = True
                range_start, range_end = part.split("-")
                cache.remove(ip)
                for v in range(int(range_start), int(range_end) + 1):
                    ip[pos] = str(v)
                    cache.append(list(ip))
    return [
        ".".join(i) for i in cache
    ]


def sortfunc(ip):
    return tuple(int(part) for part in ip.split('.'))