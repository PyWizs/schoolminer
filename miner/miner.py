import platform
import subprocess

import config


if platform.system() == "Windows":
    XMRIG = "xmrig.exe"
else:
    XMRIG = "xmrig"


command = [
    XMRIG,
    "-o", config.POOL,
    "-u", config.WALLET,
    "-p", "python-miner",
    "--coin", "monero",
    "--proxy",
]


class Miner:
    def __init__(self):
        self.lastusedproxy = None
        self.miner = None

    def start_mining(self, proxynow):
        if proxynow is None:
            print("NO INTERNET")
            if self.miner is not None and self.miner.poll() is None:
                self.stop_miner(self.miner)
            self.lastusedproxy = None
            return

        alive = self.miner is not None and self.miner.poll() is None

        if proxynow == self.lastusedproxy and alive:
            return

        if alive:
            print("Stopping Previous XMRig...")
            self.stop_miner(self.miner)

        self.lastusedproxy = proxynow

        cmd = command.copy()
        cmd.append(proxynow)

        print("Starting XMRig...")
        try:
            self.miner = subprocess.Popen(cmd)
        except FileNotFoundError:
            print(f"XMRig not found: {cmd[0]}")
            self.miner = None
            self.lastusedproxy = None

    def stop_miner(self, miner):
        if miner is None:
            return

        if miner.poll() is None:
            miner.terminate()
            miner.wait()

        self.miner = None