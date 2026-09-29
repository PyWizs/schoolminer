# network/proxy.py

import asyncio
import pproxy


class ProxyServer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.host = host
        self.port = port

    def start(self):
        asyncio.run(self._start())

    async def _start(self):
        server = pproxy.Server(
            f"http+socks4+socks5://{self.host}:{self.port}"
        )

        args = {
            "rserver": [],
            "verbose": print,
        }

        handler = await server.start_server(args)

        try:
            await asyncio.Event().wait()
        finally:
            handler.close()
            await handler.wait_closed()