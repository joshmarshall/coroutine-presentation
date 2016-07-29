import asyncio
import functools
import time
import unittest


def asynctest(method):

    @functools.wraps(method)
    def wrapper(case, *args, **kwargs):

        def timeout():
            loop.stop()
            raise AssertionError("Task timed out.")

        task = method(case, *args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.call_later(5, timeout)
        loop.run_until_complete(task)

    return wrapper


class TestCase(unittest.TestCase):

    @asynctest
    async def test_sleep(self):
        now = time.time()
        await asyncio.sleep(1)
        self.assertTrue(time.time() - now >= 1)

    @asynctest
    async def test_timeout(self):
        with self.assertRaises(AssertionError):
            await asyncio.sleep(6)
