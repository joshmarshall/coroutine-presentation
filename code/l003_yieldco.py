WAIT = object()
DONE = object()


class F(object):

    def __init__(self, x):
        self.x = x
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1

        if self.i < self.x:
            print("F<{0}> waiting".format(self.x))
            return WAIT

        if self.i == self.x:
            print("F<{0}> done".format(self.x))
            self.value = self.x
            return DONE

        raise StopIteration()


def gen(x):
    f1 = F(x)
    yield f1
    f2 = F(f1.value)
    yield f2
    print("GEN<{0}> DONE".format(x), f2.value)


def main():
    g1 = gen(2)
    g2 = gen(5)
    g3 = gen(8)
    tasks = [(None, g1), (None, g2), (None, g3)]

    # super dumb event loop / trampoline
    while tasks:
        caller, callee = tasks.pop(0)

        try:
            v = next(callee)
        except StopIteration:
            continue

        if v == DONE:
            if caller:
                caller, callee = caller
                tasks.append((caller, callee))
        elif v == WAIT:
            tasks.append((caller, callee))
        elif isinstance(v, F):
            tasks.append(((caller, callee), v))
        else:
            raise Exception("Unknown yield value: {0}".format(v))


if __name__ == "__main__":
    main()
