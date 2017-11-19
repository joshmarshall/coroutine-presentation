from code.jsonrpc import msg, loads
import socket


MAX_CLIENTS = 10
BUFFER_SIZE = 4096


class Server(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), 0))
        self.address, self.port = self.sock.getsockname()
        self.sock.listen(MAX_CLIENTS)

    def wait(self):
        client_sock, client_addr = self.sock.accept()
        while True:
            data = client_sock.recv(BUFFER_SIZE)
            result, _ = loads(data)
            print("Received {}".format(result))
            client_sock.sendall(msg({"result": "ok", "id": result["id"]}))


def main():
    server = Server()
    print("Listening on {} {}".format(server.address, server.port))
    server.wait()


if __name__ == "__main__":
    main()
