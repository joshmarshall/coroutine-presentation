import functools


UNFINISHED = object()


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
