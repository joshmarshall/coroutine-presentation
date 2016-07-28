def gensend(n):
    i = 0
    while i < n:
        i += (yield i)


def main():
    g = gensend(10)
    # prime it
    print("gensend()", next(g))
    print("gensend() + 0:", g.send(0))
    print("gensend() + 5:", g.send(5))
    print("gensend() - 3:", g.send(-3))
    try:
        print("gensend() + 10", g.send(10))
    except StopIteration:
        print("Stopped iteration.")
    g.close()

    print("")

    # let's break it
    g = gensend(4)
    print("exception", next(g))
    print("exception", g.send(2))
    g.throw(Exception("Broke everything!"))


if __name__ == "__main__":
    main()
