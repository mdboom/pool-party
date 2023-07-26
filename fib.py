def bench(n):
    if n < 2:
        return 1
    return bench(n - 1) + bench(n - 2)


def get_data():
    return [28] * 64


def assert_result(result):
    assert len(result) == 64
    assert all(x == 514229 for x in result)
