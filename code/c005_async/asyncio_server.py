import asyncio
from functools import partial
from code.jsonrpc import msg, loads


BUFFER_SIZE = 4096
MAX_CLIENTS = 256


class Server(object):

    def __init__(self, address, port):
        self.address = address
        self.port = port

    async def start(self, loop):
        print("Listening on {} {}".format(self.address, self.port))
        await asyncio.start_server(
            partial(self.handle_client, loop), self.address, self.port)

    async def watch_reads(self, reader, outq):
        while True:
            data = await reader.read(BUFFER_SIZE)
            result, _ = loads(data)
            print("Received from client: {}".format(result))
            await outq.put(msg({"result": "ok", "id": result["id"]}))

    async def watch_writes(self, writer, outq):
        while True:
            message = await outq.get()
            writer.write(message)

    async def handle_client(self, loop, reader, writer):
        outq = asyncio.Queue()
        f1 = loop.create_task(self.watch_reads(reader, outq))
        f2 = loop.create_task(self.watch_writes(writer, outq))
        await asyncio.gather(f1, f2)


def main():
    server = Server('localhost', 8000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start(loop))
    loop.run_forever()


if __name__ == "__main__":
    main()
