def gen(n):
    for i in range(n):
        yield i


def main():
    g = gen(10)
    print("gen()", next(g))
    print("gen()", next(g))
    # etc, will raise StopIteration

    for i in gen(5):
        print("<for>", i)

    print("<list>", [i * 2 for i in gen(5)])


if __name__ == "__main__":
    main()
