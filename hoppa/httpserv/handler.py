import re
import dataclasses
import log


@dataclasses.dataclass
class HTTPResponseRaw:
    version: str
    code: int
    reason: str
    headers: dict[str, str]
    body: str

    def __repr__(self) -> str:
        headers = ""
        for k, v in self.headers:
            headers += f"{k}: {v}\r\n"

        resp = f"{self.version} {self.code} {self.reason}\r\n{headers}\r\n{self.body}"
        return resp


class HTTPHandler:
    def __init__(self, request: bytes) -> None:
        # self.request = request

        req = request.decode()
        req, body = req.split("\r\n\r\n")
        req, *headers = req.split("\r\n")
        method, uri, http_ver = req.split(" ")

        self.body = body
        self.method = method
        self.uri = uri
        self.http_ver = http_ver
        self.headers = HTTPHandler.headers_from_arr(headers)

    @staticmethod
    def headers_from_arr(header_arr: list[str]) -> dict[str, str]:
        headers = {}
        for header in header_arr:
            name, val = re.match("(.*): (.*)", header).groups()
            headers[name] = val
        return headers

    def handle(self) -> bytes:
        log.info(f"{self.method} {self.uri}", context="httphandler")
        RESPONSE = HTTPResponseRaw(self.http_ver, 200, "OK", {}, "Hello, HTTP!")
        return str(RESPONSE).encode("utf-8")
