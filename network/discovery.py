# network/discovery.py

from .connectivity import has_internet
from .transport import NetworkSocket
import config

class Discovery:
    def __init__(self, network: NetworkSocket):
        self.network = network
        self.network.callback = self.receive

        self.proxynow = None

    def find_internet_peer(self):
        if has_internet(self.proxynow):
            self.proxynow = f"socks5://127.0.0.1:{config.PROXYPORT}"
            return f"socks5://127.0.0.1:{config.PROXYPORT}"

        self.network.send("", "WHO_HAS_INTERNET?", broadcast=True)

    def receive(self, message, ip):
        if message == "WHO_HAS_INTERNET?":
            print("runned")
            if has_internet():
                self.network.send(ip, "I_HAVE_INTERNET")

        elif message == "I_HAVE_INTERNET":
            self.proxynow = f"socks5://{ip}:{config.PROXYPORT}"