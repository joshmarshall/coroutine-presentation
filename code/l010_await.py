import asyncio


class Session(object):

    @classmethod
    def connect(cls):
        return Session()

    async def __aenter__(self):
        print("Creating session...")
        await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_typ, exc, tb):
        # can also handle exceptions as necessary
        await asyncio.sleep(1)
        print("Disconnected.")

    async def __aiter__(self):
        self.records = [Record(), Record()]
        return self

    async def __anext__(self):
        print("Finding record...")
        await asyncio.sleep(1)
        if not self.records:
            raise StopAsyncIteration()
        return self.records.pop(0)

    def find(self):
        return self


class Record(object):

    async def update(self, **kwargs):
        await asyncio.sleep(1)
        print("Updating record: {0}".format(kwargs))


async def wait():
    async with Session.connect() as session:
        i = 0
        async for record in session.find():
            i += 1
            await record.update(foo=i)


def main():
    loop = asyncio.get_event_loop()
    print("Starting...")
    loop.run_until_complete(wait())
    print("Finishing...")
    loop.close()


if __name__ == "__main__":
    main()
