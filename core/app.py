# core/app.py

from network.proxy import ProxyServer

import threading
import time #movaghat

class App:
    def __init__(self):
        self.proxysv = ProxyServer()
        self.threadproxy = None

    def run(self):
        self.threadproxy = threading.Thread(target=self.proxysv.start, daemon=True)
        self.threadproxy.start()

        print("Proxy Started")
        time.sleep(1000) #movaghat