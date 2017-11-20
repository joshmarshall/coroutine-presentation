# Coroutine Presentation

## Overview

This presentation (and code) was delivered to:

* PyTexas, November 19th, 2017
* and Austin Web Python User Group on July 28th, 2016

It's intent was to cover the history of async Python programming, language
evolution from iterators to generators to native coroutines, and provide
example library usage, sample async programs, and generally attempt to keep
fallacies to a minimum.

The code expects Python 3.6, even though it demonstrates concepts dating back
to 2.1/2.2.

Videos here:
* (PyTexas video forthcoming)
* AWPUG - https://youtu.be/8JIOxiHUwIA?t=14m25s

Both presentation files (in Keynote and in PDF form) are included, although I
recommend the PyTexas version for clarity / updates (it also includes Python
3.6 features).

## Coding Examples

The samples can appear a bit chaotic at first, so I've added a map for
navigating the `code` folder. I recommend creating a virtualenv to run this
code, and install the `requirements.txt` file:

```
pip install -r requirements.txt
```

It's also recommended / required to run these examples through Python 3, even though some of the concepts are much older.

### JSONRPC TCP Server Evolution

This part of the code creates a straightforward (and quite limited) JSONRPC
server / client for demonstrating how a blocking server can be turned into an
asynchronous server with successive Python language features. Note that the
code is simplified to show a model, not a real-life service -- I'm not catching
protocol errors, clients closing sockets, long messages, read / write buffering, etc.

* `code/jsonrpc.py`
    * Simple serializer / deserializer for a simple JSONRPC protocol
    * Protocol structure: `{int32 length; char[length] message}`
    * Example request: `\x00\x00\x005{"method": "foo", "jsonrpc": "2.0", "id": "e549a9cb"}`
    * Example response: `\x00\x00\x004{"result": "ok", "id": "e549a9cb", "jsonrpc": "2.0"}`
    * Exposes `msg(<dict>)` for returning a wire-friendly byte string
    * Exposes `loads(<bytes>)` which returns a tuple of `<result:dict>, <remaining:bytes>`.
* `code/selector.py`
    * Simple event loop wrapping `select` (which is not advised for any real use case) to show callbacks on file descriptors for READ / WRITE events.
    * Exposes `Selector` loop, as well as `READ` and `WRITE` event flags.
    * See `c00*/server.py` and `c00*/client.py` for usage.
* `code/c001_sync/server.py`
    * Sample blocking JSONPRC server
    * Run with `python3 -m code.c001_sync.server`
* `code/c001_sync/client.py`
    * Sample blocking JSONPRC client
    * Run with `python3 -m code.c001_sync.server HOST PORT`
* `code/c002_callback/server.py`
    * Sample callback-oriented JSONRPC server, uses a `select` based implementation that tracks file descriptor events.
    * Run with `python3 -m code.c002_callback.server`
* `code/c002_callback/client.py`
    * Sample callback-oriented JSONRPC client, uses a `select` based implementation and can run many clients concurrently.
    * Run with `python3 -m code.c002_callback.client HOST PORT NCLIENTS`
* `code/c002_callback/both.py`
    * Shows running both server and client in the same event loop, and can run many clients concurrently.
    * Run with `python3 -m code.c002_callback.both NCLIENTS`
* `code/c003_generator/server.py`
    * Updating `select`-based server to use generators as simple coroutine with a simple trampoline.
    * Run with `python3 -m code.c003_generator.server`
* `code/c003_generator/future.py`
    * This file contains a simple (partial) `Future` implementation, as well as the `coroutine` decorator / trampoline and the `wait` wrapper which takes a file descriptor, an event, and returns a `Future`.
* `code/c004_yieldfrom/server.py`
    * Updating `select`-based server to use subgenerator delegation, which improves nested generator behavior.
    * Run with `python3 -m code.c004_yieldfrom.server`
* `code/c005_async/server.py`
    * Replaces the `select` based event loop with `asyncio` file descriptor events and uses `async` / `await` keywords for true coroutines.
    * Run with `python3 -m code.c005_async.server`
* `code/c005_async/asyncio_server.py`
    * "Final form" -- uses `asyncio.start_server` for TCP server instantiation, and creates concurrent read and write coroutines for true bidirectional support.
    * Run with `python3 -m code.c005_async.asyncio_server`

## Other Coroutine Examples

* `code/l001_iter.py` - Example (and usage) of a plain-ol' iterator.
* `code/l002_gen.py` - Example (and usage) of a plain-ol' generator.
* `code/l003_yieldco.py` - Sample event loop using old-school (no `send()`) generators
* `code/l004_gensend.py` - Example (and usage) of modern generator with `send()`
* `code/l005_tornado_example.py` - Example of tornado using yield + send()
* `code/l006_yield_from.py` - Example of subgenerator delegation (yield from)
* `code/l007_exceptions.py` - Example of throwing exceptions with subgenerators
* `code/l008_asyncio.py` - URL fetcher and TCP client / server examples with asyncio
* `code/l009_hybrid.py` - Combining asyncio and Tornado on one event loop
* `code/l010_await.py` - Using Python 3.5 async + await with native coroutines
* `code/l011_hybrid_await.py` - Combining async and Tornado on one event loop with native coroutines
* `code/l012_terminal.py` - Building a simple stdin line reader with asyncio
* `code/l013_aiofreq.py` - Building a simple async audio sample generator with asyncio
* `code/l014_music.py` - Combining terminal and aiofreq (see commands.txt)
* `code/l015_testing.py` - Show simple asyncio + await unittest examples
* `code/l016_tornado_testing.py` - Same testing, but with tornado.testing
* `code/l017_service.py` - Build an HTTP service with Tornado, aiohttp, and uvloop
* `code/l018_tasks.py` - Show simple usage of asyncio Loop, Task, and Future
* `code/commands.txt` - Run `cat commands.txt | python3 l014_music.py | ./play.sh`
* `code/play.sh` - Expects sox / sox play to be installed - pipe aiofreq streams to this to play audio on the commandline as it streams.
