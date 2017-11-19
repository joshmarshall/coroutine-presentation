import functools
import socket
from code.selector import READ, WRITE
from code.jsonrpc import loads, msg


BUFFER_SIZE = 4096
UNFINISHED = object()
MAX_CLIENTS = 256


class Future(object):

    def __init__(self):
        self.callbacks = []
        self.rvalue = UNFINISHED
        self.xvalue = UNFINISHED

    @property
    def finished(self):
        return self.rvalue != UNFINISHED or self.xvalue != UNFINISHED

    def add_done_callback(self, callback):
        if self.finished:
            return callback(self)
        self.callbacks.append(callback)

    def set_result(self, result):
        self.rvalue = result
        for callback in self.callbacks:
            callback(self)

    def set_exception(self, exc):
        self.xvalue = exc
        for callback in self.callbacks:
            callback(self)

    def result(self):
        if not self.finished:
            raise NotDone("Future is unfinished.")
        if self.xvalue is not UNFINISHED:
            raise self.xvalue
        else:
            return self.rvalue


class NotDone(Exception):
    pass


def run(gen, cb):
    context = {"gen": gen}

    def callback(result):
        try:
            result = context["future"].result()
        except Exception as exception:
            return context["gen"].throw(exception)
        try:
            context["future"] = context["gen"].send(result)
            context["future"].add_done_callback(callback)
        except StopIteration:
            cb(result)

    # priming the pump
    context["future"] = context["gen"].send(None)
    context["future"].add_done_callback(callback)


def coroutine(fn):

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        future = Future()
        gen = fn(*args, **kwargs)
        run(gen, lambda x: future.set_result(x))
        return future

    return wrapped


def wait(selector, fd, event):
    future = Future()

    def callback(fd, selector):
        selector.remove_fd(fd, event)
        future.set_result((fd, selector))

    selector.add_fd(fd, event, callback)
    return future


def result(value):
    future = Future()
    future.set_result(value)
    return future


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
