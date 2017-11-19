import asyncio
import socket
from code.jsonrpc import msg, loads


BUFFER_SIZE = 4096
MAX_CLIENTS = 256


class Server(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.bind((socket.gethostname(), 0))
        self.address, self.port = self.sock.getsockname()

    async def start(self, loop):
        print("Listening on {} {}".format(self.address, self.port))
        self.sock.listen(MAX_CLIENTS)
        while True:
            client_sock, client_addr = await loop.sock_accept(self.sock)
            loop.create_task(self.handle_client(loop, client_sock))

    async def handle_client(self, loop, client_sock):
        while True:
            data = await loop.sock_recv(client_sock, BUFFER_SIZE)
            result, _ = loads(data)
            print("Received from client: {}".format(result))
            await loop.sock_sendall(
                client_sock, msg({"result": "ok", "id": result["id"]}))


def main():
    server = Server()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start(loop))


if __name__ == "__main__":
    main()
