import json
import struct
import uuid


def msg(message):
    message.setdefault("jsonrpc", "2.0")
    message.setdefault("id", uuid.uuid4().hex[:8])
    return dumps(message)


def dumps(obj):
    message = json.dumps(obj).encode("utf8")
    msg_length = len(message)
    return struct.pack(">i{}s".format(msg_length), msg_length, message)


def loads(message):
    if len(message) < 4:
        return None, message
    msg_length = struct.unpack(">i", message[:4])[0]
    if len(message[4:]) < msg_length:
        return None, message
    _, data = struct.unpack(
        ">i{}s".format(msg_length), message[:4 + msg_length])
    return json.loads(data.decode("utf8")), message[4 + msg_length:]
