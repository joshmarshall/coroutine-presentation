import asyncio
import traceback
import sys

from l013_aiofreq import Stream
from l012_terminal import Terminal, log_prompt


def quit(term, stream):
    term.stop()
    stream.stop()


async def add(stream, val):
    stream.add(int(val))


async def remove(stream, val):
    stream.remove(int(val))


async def beep(stream, val, seconds=0.5):
    await chord(stream, seconds, val)


async def chord(stream, seconds, *notes):
    notes = [int(n) for n in notes]
    await asyncio.wait([add(stream, n) for n in notes])
    await asyncio.sleep(float(seconds))
    await asyncio.wait([remove(stream, n) for n in notes])


async def wait(stream, seconds):
    await asyncio.sleep(float(seconds))


async def evaluate(stream, *value):
    value = " ".join(value)
    values = [v.strip() for v in value.split(";")]
    for value in values:
        parts = value.strip().split(" ")
        cmd, args = parts[0], [p for p in parts[1:] if p]
        if not cmd:
            continue

        if cmd not in COMMANDS:
            log_prompt("Unknown command.")
            return

        try:
            await COMMANDS[cmd](stream, *args)
        except Exception:
            print("Error running command: {0}({1})\n{2}".format(
                cmd, args, traceback.format_exc()))
            raise

    log_prompt()


COMMANDS = {
    "add": add,
    "remove": remove,
    "chord": chord,
    "beep": beep,
    "wait": wait,
    "eval": evaluate
}


async def reader(term, chunk, stream):
    chunk = chunk.strip()
    if not chunk:
        return

    if chunk in ["quit", "exit"]:
        return quit(term, stream)

    await evaluate(stream, chunk)


def main():
    loop = asyncio.get_event_loop()
    stream = Stream(loop)

    term = Terminal(loop)
    term.add_callback(reader, stream)

    tasks = asyncio.wait([term.start(), stream.start()])

    log_prompt("Ready.")

    loop.run_until_complete(tasks)

    loop.close()

    print("Finished.", file=sys.stderr)


if __name__ == "__main__":
    main()
