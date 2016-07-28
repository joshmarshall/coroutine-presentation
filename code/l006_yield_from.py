def gen2(i):
    print("INNER YIELD")
    val = yield i
    print("INNER YIELD DONE", val)
    return val ** 2


def gen1(x):
    for i in range(x):
        print("MIDDLE YIELD FROM")
        result = yield from gen2(i)
        print("MIDDLE YIELD FROM DONE", result)
        print("---------------------")
    print("MIDDLE DONE")


def main():
    g = gen1(5)
    print("OUTER", next(g))
    print("OUTER", g.send(3))
    print("OUTER", g.send(4))
    print("OUTER", g.send(5))
    print("OUTER", g.send(6))
    try:
        print("OUTER", g.send(7))
    except StopIteration:
        g.close()


if __name__ == "__main__":
    main()
