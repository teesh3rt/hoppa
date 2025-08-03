from dataclasses import dataclass
from enum import Enum

ASSUMING_HTTP_VERSION = "HTTP/1.1"


@dataclass
class HTTPResponseRaw:
    version: str
    code: int
    reason: str
    headers: dict[str, str]
    body: str

    def __repr__(self) -> str:
        headers = ""
        for k, v in self.headers.items():
            headers += f"{k}: {v}\r\n"

        resp = f"{self.version} {self.code} {self.reason}\r\n{headers}\r\n{self.body}"
        return resp


@dataclass
class HTTPResponseCode:
    number: int
    reason: str

    def __repr__(self) -> str:
        return f"{self.number} {self.reason}"


class HTTPResponseType(Enum):
    OK = HTTPResponseCode(200, "OK")
    NotFound = HTTPResponseCode(404, "Not Found")
    InternalServerError = HTTPResponseCode(500, "Internal Server Error")


class HTTPResponse:
    def __init__(
        self, type: HTTPResponseType, body: str, headers: dict[str, str] = {}
    ) -> None:
        self.type = type
        self.body = body
        self.headers = headers

    def __repr__(self) -> str:
        headers = ""
        for k, v in self.headers.items():
            headers += f"{k}: {v}\r\n"

        resp = f"{ASSUMING_HTTP_VERSION} {self.type}\r\n{headers}\r\n{self.body}"
        return resp
