# Coroutine Presentation

This presentation (and code) was delivered to Austin Web Python User Group on
July 28th, 2016. It's intent was to cover the history of async Python
programming, language evolution from iterators to generators to native
coroutines, and provide example library usage, sample async programs, and
generally attempt to keep fallacies to a minimum.

The code expects Python 3.5.2, even though it demonstrates concepts dating back
to 2.1/2.2.

Video here: https://youtu.be/8JIOxiHUwIA?t=14m25s


## Coding Examples

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
