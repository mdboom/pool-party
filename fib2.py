class Fibonacci:
    def __init__(self, x):
        self.x = x

    def calculate(self, n):
        # This line doesn't actually matter for the calculation, but this is what
        # causes the nogil threaded performance to drop precipitously.
        #
        # While this may be silly for computing fibonacci, it is pretty
        # idiomatic for an instance to have some state that is updated on a
        # method call (we see this in the raytrace benchmark, for example).
        # Note there is no actual sharing of Fibonacci instances between
        # threads here. This is a thread having lock contention with itself,
        # apparently.
        #
        # Linux perf reports a spike of about 10% of runtime in
        # _PyObject_GetInstanceAttribute when this line is present, vs 0.00% without.
        self.x += 1

        if n < 2:
            return 1
        return self.calculate(n - 1) + self.calculate(n - 2)


def bench(n):
    f = Fibonacci(1)
    return f.calculate(n)


def get_data():
    return [28] * 64


def assert_result(result):
    assert len(result) == 64
    assert all(x == 514229 for x in result)
