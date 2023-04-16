from typing import List as L, Optional as O, Union as U, Dict as D, Callable as C, Any
from aiofauna import Request
from ipaddress import ip_address, ip_network, IPv4Address, IPv6Address, IPv4Network, IPv6Network
import socket

def get_host_by_ip(ip:str)->O[str]:
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None
    
def get_ip_by_host(host:str)->O[str]:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None
    
def get_free_port()->int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
    
def coalesce(args:L[Any])->O[Any]:
    for arg in args:
        if arg not in [None, ""]:
            return arg
    return None

def get_ip(req:Request)->O[str]:
    args = [
        req.headers.get("X-Forwarded-For"),
        req.headers.get("X-Real-IP"),
        req.headers.get("CF-Connecting-IP"),
        req.host
    ]
    
    ip = coalesce(args)
    
    if ip:
        return ip.split(",")[0].strip()    
    return None