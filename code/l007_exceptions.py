def gen2(i):
    print("INNER YIELD")
    val = yield i
    return val ** 2


def gen1(x):
    print("MIDDLE YIELD FROM")
    result = yield from gen2(x)
    print("MIDDLE YIELD FROM DONE", result)
    yield result
    print("MIDDLE DONE")


def main():
    g = gen1(3)
    print("OUTER", next(g))
    g.throw(Exception("Breaking it!"))


if __name__ == "__main__":
    main()
