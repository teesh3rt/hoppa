from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from typing import Tuple
from httpserv.handler import HTTPHandler
import log


def detect_is_http(req_body: bytes):
    return any(
        req_body.startswith(method.encode() + b" ")
        for method in [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "HEAD",
            "OPTIONS",
            "PATCH",
            "TRACE",
            "CONNECT",
        ]
    )


class NetHandlerThread(Thread):
    def __init__(self, nh, conn: socket, addr: Tuple[str, int]):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):
        log.debug(f"new nhthread started for {self.addr}", context="nhthread")
        req = self.conn.recv(1024)

        if detect_is_http(req):
            log.debug(
                "http header detected! routing as http request...", context="nhthread"
            )
            self.handle_http_request(req)

        self.conn.close()

    def handle_http_request(self, req_body: bytes):
        # Since we know this is HTTP, it (most likely) must be valid UTF-8
        http = HTTPHandler(req_body)
        resp: bytes = http.handle()
        self.conn.sendall(resp)


class NetHandler:
    def __init__(self, host: str):
        self.host = host
        self.port = 5432
        self.socket = socket(AF_INET, SOCK_STREAM)

    def listen(self):
        log.debug(
            f"nethandler started listening on {self.host}:{self.port}",
            context="nethandler",
        )
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        while True:
            conn, addr = self.socket.accept()
            log.debug(f"new connection from {addr}", context="nethandler")
            t = NetHandlerThread(self, conn, addr)
            t.start()
