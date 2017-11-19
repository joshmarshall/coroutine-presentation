from code.jsonrpc import loads, msg

import socket
import sys
import time


BUFFER_SIZE = 4096
HEARTBEAT_INTERVAL = 5


class Client(object):

    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port

    def wait(self):
        print("Connecting to {} {}".format(self.address, self.port))
        self.sock.connect((self.address, self.port))
        self.sock.sendall(msg({"method": "connect"}))

        while True:
            data = self.sock.recv(BUFFER_SIZE)
            result, _ = loads(data)
            print("Received from server: {}".format(result))
            time.sleep(HEARTBEAT_INTERVAL)
            self.sock.sendall(msg({"method": "heartbeat"}))


def main():
    client = Client(sys.argv[1], int(sys.argv[2]))
    client.wait()


if __name__ == "__main__":
    main()
