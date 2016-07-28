import asyncio
import sys


class Terminal(object):

    def __init__(self, loop):
        self.loop = loop
        self.callbacks = []
        self.tasks = []
        self.listening = False

    async def start(self):

        if not self.listening:
            self.listening = True
            self.loop.add_reader(sys.stdin.fileno(), self.on_read)

        while True:
            if not self.listening:
                break

            while self.tasks:
                await self.tasks.pop(0)

            await asyncio.sleep(0.1)

    def stop(self):
        self.loop.remove_reader(sys.stdin.fileno())
        self.listening = False

    def add_callback(self, callback, *args):
        self.callbacks.append((callback, args))

    def on_read(self):
        chunk = sys.stdin.readline().strip()
        if not chunk:
            return
        for callback, args in self.callbacks:
            self.tasks.append(callback(self, chunk, *args))


def log_prompt(message=""):
    message = "{0}\n> ".format(message) if message else "> "
    sys.stderr.write(message)
    sys.stderr.flush()


if __name__ == "__main__":
    import aiohttp

    loop = asyncio.get_event_loop()

    async def handle(term, message):
        if message == "so long":
            print("And thanks for all the fish.", file=sys.stderr)
            term.stop()
        elif message == "answer":
            log_prompt("You aren't going to like it.")
        elif message == "42":
            log_prompt("But what is the ultimate question?")
        elif message.startswith("http://"):
            response = await aiohttp.request("GET", message)
            await response.read()
            log_prompt("Site responded with: {0}".format(response.status))
        else:
            log_prompt("No idea what you are saying.")

    term = Terminal(loop)
    term.add_callback(handle)
    log_prompt("Ready.")
    loop.run_until_complete(term.start())
