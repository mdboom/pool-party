def bench(_indata):
    return [1000.0] * (1 << 16)


def get_data():
    return [1000.0] * (1 << 10)


def assert_result(result):
    assert len(result) == (1 << 10)
    assert all(len(x) == (1 << 16) for x in result)
