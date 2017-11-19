from code.selector import Selector
# from code.c003_generator.client import Client
from code.c003_generator.server import Server
# import sys


def main():
    selector = Selector()

    server = Server()
    server.accept(selector)

    # for i in range(int(sys.argv[1])):
    #     client = Client(server.address, server.port)
    #     client.connect(selector)

    while True:
        selector.wait()


if __name__ == "__main__":
    main()
