import aiohttp
import asyncio
import socket
import unittest

import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop

from l015_testing import asynctest


async def fetch(url):
    response = await aiohttp.request("GET", url)
    body = await response.json()
    return response.status, body


class Handler(tornado.web.RequestHandler):

    async def get(self, value):
        result = await wait(1)
        assert result == 1
        if value == "panic":
            self.set_status(400)
            return self.finish({"message": "don't panic!"})
        return self.finish({"message": "always carry a towel!"})


@asyncio.coroutine
def wait(x):
    yield from asyncio.sleep(1)
    return x


def application():
    return tornado.web.Application([
        ("/(\w+)", Handler)
    ])


AsyncIOMainLoop().install()


def get_unused_port():
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.bind(('localhost', 0))
    _, port = skt.getsockname()
    return port


class TestApplication(unittest.TestCase):

    def setUp(self):
        self.port = get_unused_port()
        self.app = application()
        self.app.listen(self.port)

    @asynctest
    async def test_fetch(self):
        url = "http://localhost:{0}/towel".format(self.port)
        code, response = await fetch(url)
        self.assertEqual(200, code)
        self.assertEqual("always carry a towel!", response["message"])

    @asynctest
    async def test_failure(self):
        url = "http://localhost:{0}/panic".format(self.port)
        code, response = await fetch(url)
        self.assertEqual(400, code)
        self.assertEqual("don't panic!", response["message"])
