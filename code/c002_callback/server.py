from code.jsonrpc import loads, msg
from code.selector import READ, WRITE
import socket


MAX_CLIENTS = 256
BUFFER_SIZE = 4096


class Server(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.bind((socket.gethostname(), 0))
        self.address, self.port = self.sock.getsockname()
        self.recv_data = {}
        self.send_data = {}

    def register(self, selector):
        selector.add_fd(self.sock, READ, self.open_callback)
        print("Listening on {} {}".format(self.address, self.port))
        self.sock.listen(MAX_CLIENTS)

    def open_callback(self, sock, selector):
        client_sock, client_addr = self.sock.accept()
        print("New connection on {}".format(client_addr))
        selector.add_fd(client_sock, READ, self.read_callback)
        selector.add_fd(client_sock, WRITE, self.write_callback)
        self.recv_data.setdefault(client_sock.fileno(), b"")
        self.send_data.setdefault(client_sock.fileno(), b"")

    def read_callback(self, client_sock, selector):
        try:
            data = client_sock.recv(BUFFER_SIZE)
        except socket.error as error:
            print("Socket closed: {}".format(error))
            return self.cleanup_client(client_sock, selector)

        self.recv_data[client_sock.fileno()] += data
        result, remaining = loads(self.recv_data[client_sock.fileno()])

        if result:
            print("Received from {}: {}".format(client_sock.fileno(), result))
            self.send_data[client_sock.fileno()] += msg(
                {"result": "ok", "id": result["id"]})
            self.recv_data[client_sock.fileno()] = remaining

    def write_callback(self, client_sock, selector):
        data = self.send_data[client_sock.fileno()]

        if not data:
            return

        try:
            client_sock.sendall(data)
        except socket.error as error:
            print("Socket closed: {}".format(error))
            return self.cleanup_client(client_sock, selector)

        self.send_data[client_sock.fileno()] = b""

    def cleanup_client(self, client_sock, selector):
        del self.recv_data[client_sock.fileno()]
        del self.send_data[client_sock.fileno()]
        selector.remove_fd(client_sock, READ)
        selector.remove_fd(client_sock, WRITE)
