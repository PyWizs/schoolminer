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
        if has_internet():
            self.proxynow = f"socks5://127.0.0.1:{config.PROXYPORT}"
            return self.proxynow

        if self.proxynow and has_internet(self.proxynow):
            return self.proxynow

        self.proxynow = None
        self.network.send("", "WHO_HAS_INTERNET?", broadcast=True)
        return None
    
    def receive(self, message, ip):
        if message == "WHO_HAS_INTERNET?":
            if has_internet():
                self.network.send(ip, "I_HAVE_INTERNET")

        elif message == "I_HAVE_INTERNET":
            self.proxynow = f"socks5://{ip}:{config.PROXYPORT}"