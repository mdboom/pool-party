def bench(n):
    if n < 2:
        return 1
    return bench(n - 1) + bench(n - 2)


def get_data():
    return [34] * 64


def assert_result(result):
    assert len(result) == 64
    assert all(x == 9227465 for x in result)
