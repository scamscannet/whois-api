'''
Program to fetch whois information of a domain name
'''
import socket, sys
import whois


# Perform a generic whois query to a server and get the reply
def raw_whois_request(server, domain):
    # socket connection
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, 43))
    except Exception as e:
        print(f"Error while connecting to {server}")
        return
    # send data

    s.send(f"{domain}\r\n".encode())

    # receive reply
    msg = ''
    while len(msg) < 10000:
        chunk = s.recv(100)
        if (chunk.decode() == ''):
            break
        msg = msg + chunk.decode()

    return msg
