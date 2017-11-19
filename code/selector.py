import select
import time


READ = object()
WRITE = object()
VALID_EVENTS = (READ, WRITE)


class Selector(object):

    def __init__(self):
        self.read_entries = {}
        self.write_entries = {}
        self.callbacks = []

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def _get_entries(self, event_type):
        if event_type not in VALID_EVENTS:
            raise ValueError("Invalid event type: {}".format(event_type))
        return self.read_entries if event_type is READ else self.write_entries

    def add_fd(self, fp, event_type, callback):
        fd = fp.fileno() if hasattr(fp, "fileno") else fp
        fd_entries = self._get_entries(event_type)
        fd_entries.setdefault(fd, []).append((fp, callback))

    def remove_fd(self, fp, event_type):
        fd = fp.fileno() if hasattr(fp, "fileno") else fp
        fd_entries = self._get_entries(event_type)
        del fd_entries[fd]

    def add_callback(self, callback_time, callback_func):
        self.callbacks.append((callback_time, callback_func))

    def wait(self, timeout=None):
        exception_keys = \
            list(self.read_entries.keys()) + list(self.write_entries.keys())
        readable, writable, exceptions = select.select(
            self.read_entries.keys(), self.write_entries.keys(),
            exception_keys, timeout)
        for fd in readable:
            if fd not in self.read_entries:
                continue
            for fp, cb in self.read_entries[fd]:
                cb(fp, self)
        for fd in writable:
            if fd not in self.write_entries:
                continue
            for fp, cb in self.write_entries[fd]:
                cb(fp, self)
        for exception in exceptions:
            print("Unhandled exception in fileno: {}", format(exception))

        for callback_info in self.callbacks[:]:
            callback_time, callback_fn = callback_info
            if callback_time > time.time():
                continue
            self.callbacks.remove(callback_info)
            callback_fn(self)
