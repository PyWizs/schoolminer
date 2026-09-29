import socket


class NetworkSocket:

    PORT = 60000

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

        self.sock.bind(("0.0.0.0", self.PORT))

        self.callback = callback

    def send(self, ip, data, broadcast=False):
        if broadcast:
            self.sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_BROADCAST,
                1
            )
            ip = "255.255.255.255"

        self.sock.sendto(
            data.encode(),
            (ip, self.PORT)
        )

    def receive(self):
        while True:
            data, ip = self.sock.recvfrom(4096)

            message = data.decode()
            address = ip[0]

            if self.callback:
                self.callback(message, address)