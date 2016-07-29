import asyncio
import unittest
import uvloop

# from l015_testing import asynctest


async def wait(x):
    await asyncio.sleep(1)
    return x


class TestAsyncIOElements(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

        def timeout():
            self.loop.stop()
            raise AssertionError("Task timed out!")

        self.loop.call_later(2, timeout)

    def test_task(self):
        task = self.loop.create_task(wait(1))
        task.add_done_callback(lambda: self.loop.stop())
        # will block until success or timeout
        self.loop.run_forever()

    def test_future(self):
        future = self.loop.create_future()

        def callback():
            future.set_result(10)

        self.loop.call_later(1, callback)

        def stop(f):
            self.loop.stop()

        future.add_done_callback(stop)
        # will block until success or timeout
        self.loop.run_forever()

        self.assertEqual(10, future.result())

    def test_uvloop(self):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)

        async def uvwait(x):
            assert isinstance(asyncio.get_event_loop(), uvloop.Loop)
            result = await wait(x)
            return result

        result = loop.run_until_complete(uvwait(1))
        self.assertEqual(1, result)
