from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop


@gen.coroutine
def fetch(url):
    response = yield AsyncHTTPClient().fetch(url, raise_error=False)
    print("URL<{0}> responded".format(url))
    raise gen.Return(response.code)


@gen.coroutine
def wait():
    futures = []
    for url in ["http://google.com", "http://app.ustudio.com"]:
        futures.append(fetch(url))

    results = []

    for future in futures:
        result = yield future
        results.append(result)

    raise gen.Return(results)


def main():
    print(IOLoop.current().run_sync(wait))


if __name__ == "__main__":
    main()
