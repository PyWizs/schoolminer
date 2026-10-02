import socket
import config

class NetworkSocket:
    def __init__(self, callback=None):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        self.sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.sock.bind(("0.0.0.0", config.PROGRAMPORT))

        self.callback = callback

    def send(self, ip, data, broadcast=False):
        if broadcast:
            self.sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_BROADCAST,
                1
            )
            ip = "255.255.255.255"

        print(f"sending data {data} to ip {ip}")
        self.sock.sendto(
            data.encode(),
            (ip, config.PROGRAMPORT)
        )

    def receive(self):
        while True:
            data, ip = self.sock.recvfrom(4096)

            message = data.decode()
            address = ip[0]

            if self.callback:
                self.callback(message, address)