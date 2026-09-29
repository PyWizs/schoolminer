# network/discovery.py

from .connectivity import has_internet
from .transport import NetworkSocket

class Discovery:
    def __init__(self, network: NetworkSocket):
        self.network = network
        self.proxynow = None
        self.network.callback = self.receive

    def find_internet_peer(self):
        if has_internet(self.proxynow):
            self.proxynow = "socks5://127.0.0.1:8080"
            return "socks5://127.0.0.1:8080"

        self.network.send("", "WHO_HAS_INTERNET?", broadcast=True)

    def receive(self, message, ip):
        if message == "WHO_HAS_INTERNET?":
            if has_internet():
                self.network.send(ip, "I_HAVE_INTERNET")

        elif message == "I_HAVE_INTERNET":
            self.proxynow = f"socks5://{ip}:8080"