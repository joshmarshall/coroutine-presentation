import time

from tornado import gen
from tornado.testing import AsyncTestCase, gen_test


class TestTornado(AsyncTestCase):

    @gen_test
    async def test_sleep(self):
        now = time.time()
        await gen.sleep(1)
        self.assertTrue(time.time() - now >= 1)
