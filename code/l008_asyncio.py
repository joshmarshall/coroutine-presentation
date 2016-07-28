import asyncio
import aiohttp
import json
import struct


@asyncio.coroutine
def fetch(url):
    response = yield from aiohttp.request("GET", url)
    body = yield from response.read()
    response.close()
    print(response.status, "Content-length", len(body))


@asyncio.coroutine
def handle_client(reader, writer):
    message = yield from read_message(reader)
    print("CLIENT:", message["message"])
    ret_bytes = encode_message({"message": "thanks for all the fish"})
    writer.write(ret_bytes)
    yield from writer.drain()
    writer.close()


@asyncio.coroutine
def read_message(reader):
    data = yield from reader.read(4)
    length = struct.unpack("i", data)[0]
    data = yield from reader.read(length)
    return json.loads(data.decode("utf8"))


def encode_message(message):
    ret_message = json.dumps(message).encode("utf8")
    ret_bytes = struct.pack("i", len(ret_message)) + ret_message
    return ret_bytes


@asyncio.coroutine
def handle_message(client):
    reader, writer = yield from client
    msg_bytes = encode_message({"message": "so long"})
    writer.write(msg_bytes)
    yield from writer.drain()
    message = yield from read_message(reader)
    print("SERVER:", message["message"])


def main():
    urls = ["http://google.com", "http://app.ustudio.com"]
    tasks = asyncio.wait([fetch(url) for url in urls])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    print("-----------")

    init = asyncio.start_server(handle_client, "127.0.0.1", 8001, loop=loop)
    server = loop.run_until_complete(init)

    client = asyncio.open_connection("127.0.0.1", 8001)
    response = handle_message(client)
    loop.run_until_complete(response)
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

    print("Finished.")


if __name__ == "__main__":
    main()
