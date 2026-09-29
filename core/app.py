# core/app.py

from network.proxy import ProxyServer
from network.discovery import Discovery
from network.transport import NetworkSocket

import threading
import time

class App:
    def __init__(self):
        self.network = NetworkSocket()
        self.proxysv = ProxyServer()
        self.discovery = Discovery(self.network)

        self.threadproxy = None
        self.threadnetwork = None

    def run(self):
        self.threadproxy = threading.Thread(target=self.proxysv.start, daemon=True)
        self.threadproxy.start()

        self.threadnetwork = threading.Thread(target=self.network.receive, daemon=True)
        self.threadnetwork.start()

        while True:
            self.discovery.find_internet_peer()
            time.sleep(200)
