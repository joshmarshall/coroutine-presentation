import asyncio
import math
import struct
import sys
import time


# glorious 8kHz, 8bit, single channel
SAMPLE_RATE = 8000
SLEEP_TIME = 0.05
MAX_AMPLITUDE = 0.8
A_CONSTANT = pow(2, 1/12.0)


class Stream(object):

    def __init__(self, loop):
        self.frequencies = []
        self.loop = loop
        self.stopped = False

    async def start(self):
        last_sample = 0
        last_time = time.time()

        while True:
            if self.stopped:
                break

            diff = time.time() - last_time
            last_time = time.time()

            samples = int(SAMPLE_RATE * diff)
            offset = last_sample % SAMPLE_RATE
            last_sample = offset + samples

            if samples:
                r = normalize([
                    sum([
                        sample(freq, i, SAMPLE_RATE)
                        for freq in self.frequencies
                    ])
                    for i in range(offset, last_sample)
                ])

                sys.stdout.buffer.write(struct.pack('B' * samples, *r))
                sys.stdout.flush()

            await asyncio.sleep(max(SLEEP_TIME - diff, 0))

    def add(self, n):
        val = note(n)
        if val not in self.frequencies:
            self.frequencies.append(val)
        return val

    def remove(self, n):
        val = note(n)
        if val in self.frequencies:
            self.frequencies.remove(val)
        return val

    def stop(self):
        self.stopped = True


def note(n, base=16.35):
    frequency = base * pow(A_CONSTANT, n)
    return frequency


def sample(freq, i, rate):
    return math.sin(math.pi * 2 * freq * i / rate) * 127


def normalize(xs):
    diff_max = max((max(xs), math.sqrt(min(xs) ** 2)))
    diff = 1
    if diff_max:
        diff = 127 / diff_max
    return [int((x * diff) * MAX_AMPLITUDE) + 127 for x in xs]


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    stream = Stream(loop)
    stream.add(60)

    async def timeout():
        await asyncio.sleep(3)
        stream.stop()

    tasks = asyncio.wait([stream.start(), timeout()])
    loop.run_until_complete(tasks)
    print("Finished.")
