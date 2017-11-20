from code.jsonrpc import loads, msg
from code.selector import Selector, READ, WRITE
import socket
import sys
import time


MAX_CLIENTS = 256
BUFFER_SIZE = 4096
HEARTBEAT_INTERVAL = 5


class Client(object):

    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.address = address
        self.port = port
        self.recv_data = b""
        self.send_data = msg({"method": "connect"})

    def register(self, selector):
        selector.add_fd(self.sock, READ, self.read_callback)
        selector.add_fd(self.sock, WRITE, self.write_callback)
        print("Connecting to {} {}".format(self.address, self.port))
        connect_no = self.sock.connect_ex((self.address, self.port))
        if connect_no not in (0, socket.errno.EINPROGRESS):
            print("Error connecting: {}".format(connect_no))
            return self.cleanup()
        selector.add_callback(time.time() + HEARTBEAT_INTERVAL, self.heartbeat)

    def cleanup(self, selector):
        selector.remove_fd(self.sock, READ)
        selector.remove_fd(self.sock, WRITE)
        self.sock.close()

    def send(self, message):
        self.send_data += msg(message)

    def heartbeat(self, selector):
        self.send({"method": "heartbeat"})
        selector.add_callback(time.time() + HEARTBEAT_INTERVAL, self.heartbeat)

    def read_callback(self, sock, selector):
        try:
            self.recv_data += sock.recv(BUFFER_SIZE)
        except socket.error as error:
            print("Server closed: {}".format(error))
            self.cleanup(selector)

        result, remaining = loads(self.recv_data)
        if result:
            self.recv_data = remaining
            print("Received from server: {}".format(result))

    def write_callback(self, sock, selector):
        if self.send_data:
            try:
                sock.sendall(self.send_data)
            except socket.error as error:
                print("Server closed: {}".format(error))
                self.cleanup(selector)
            self.send_data = b""


def main():
    selector = Selector()
    host = sys.argv[1]
    port = int(sys.argv[2])
    clients = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    for i in range(clients):
        client = Client(host, port)
        client.register(selector)

    while True:
        selector.wait()


if __name__ == "__main__":
    main()
