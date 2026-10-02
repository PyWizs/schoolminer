# core/app.py

from network.proxy import ProxyServer
from network.discovery import Discovery
from network.transport import NetworkSocket

from miner.miner import Miner

import config

import threading
import time

class App:
    def __init__(self):
        self.network = NetworkSocket()
        self.proxysv = ProxyServer(port=config.PROXYPORT)
        self.miner = Miner()
        self.discovery = Discovery(self.network)

        self.threadproxy = None
        self.threadnetwork = None

    def run(self):
        self.threadproxy = threading.Thread(target=self.proxysv.start, daemon=True)
        self.threadproxy.start()

        self.threadnetwork = threading.Thread(target=self.network.receive, daemon=True)
        self.threadnetwork.start()

        time.sleep(5)

        while True:
            self.discovery.find_internet_peer()
            self.miner.start_mining(self.discovery.proxynow)
            time.sleep(200)
