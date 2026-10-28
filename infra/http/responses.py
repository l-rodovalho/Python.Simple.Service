import json
from functools import partial
from typing import Any

from aiohttp import web

_dumps = partial(json.dumps, separators=(",", ":"), ensure_ascii=False)


def json_response(data: Any, status: int = 200) -> web.Response:
    return web.json_response(data, status=status, dumps=_dumps)


__all__ = ["json_response"]

