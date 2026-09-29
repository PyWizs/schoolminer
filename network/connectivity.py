# network/connectivity.py

import socket
import socks
from urllib.parse import urlparse


def has_internet(proxy=None):
    try:
        if proxy and not proxy == "socks5://127.0.0.1:8080":
            parsed = urlparse(proxy)

            sock = socks.socksocket()
            sock.set_proxy(
                socks.SOCKS5,
                parsed.hostname,
                parsed.port
            )
        else:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

        sock.settimeout(10)
        sock.connect(("1.1.1.1", 53))
        sock.close()

        return True

    except (OSError, ValueError):
        return False