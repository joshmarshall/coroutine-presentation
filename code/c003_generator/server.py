import socket
from code.selector import Selector, READ, WRITE
from code.jsonrpc import loads, msg
from code.c003_generator.future import coroutine, wait, result


BUFFER_SIZE = 4096
MAX_CLIENTS = 256


class Server(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.bind((socket.gethostname(), 0))
        self.address, self.port = self.sock.getsockname()
        self.recv_data = {}
        self.send_data = {}

    @coroutine
    def accept(self, selector):
        print("Listening on {} {}".format(self.address, self.port))
        self.sock.listen(MAX_CLIENTS)
        while True:
            yield wait(selector, self.sock, READ)
            client_sock, client_addr = self.sock.accept()
            print("New connection on {}".format(client_addr))
            yield self.handle_client(selector, client_sock)

    @coroutine
    def handle_client(self, selector, client_sock):
        while True:
            data = yield recv(selector, client_sock, BUFFER_SIZE)
            result, _ = loads(data)
            print("Received from client: {}".format(result))
            response = msg({"result": "ok", "id": result["id"]})
            yield sendall(selector, client_sock, response)


@coroutine
def recv(selector, sock, numbytes):
    data = b""
    yield wait(selector, sock, READ)
    data = sock.recv(numbytes)
    yield result(data)


@coroutine
def sendall(selector, sock, data):
    yield wait(selector, sock, WRITE)
    sock.sendall(data)
    yield result(None)


def main():
    selector = Selector()

    server = Server()
    server.accept(selector)

    while True:
        selector.wait()


if __name__ == "__main__":
    main()
