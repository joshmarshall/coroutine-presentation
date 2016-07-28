class Iter(object):

    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == self.n:
            raise StopIteration()

        i = self.i
        self.i += 1
        return i


def main():
    i = Iter(10)
    print("<Iter>", next(i))
    print("<Iter>", next(i))
    print("<Iter>", next(i))
    # etc

    for i in Iter(3):
        print("<for>", i)

    print("<sum>", sum(Iter(5)))

    lambda x: x ** 2
    print("<n^2>", [x for x in map(lambda x: x**2, Iter(5))])


if __name__ == "__main__":
    main()
