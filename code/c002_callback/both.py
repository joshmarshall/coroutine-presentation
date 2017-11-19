from code.selector import Selector
from code.c002_callback.client import Client
from code.c002_callback.server import Server
import sys


def main():
    selector = Selector()

    server = Server()
    server.register(selector)

    for i in range(int(sys.argv[1])):
        client = Client(server.address, server.port)
        client.register(selector)

    while True:
        selector.wait()


if __name__ == "__main__":
    main()
