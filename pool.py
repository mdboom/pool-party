try:
    from multiprocessing.pool import (
        SubinterpreterPool,
        SubinterpreterPool2,
        SubinterpreterPool3,
    )
except ImportError:
    pass
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool

try:
    import gilknocker
except ImportError:
    gilknocker = None

import sys
import time

import defs

# TODO: Import __main__ into the subinterpreter so it can access f and it
# doesn't have to be defined in a separate module.

if __name__ == "__main__":
    single = False
    match sys.argv[-1]:
        case "interp":
            Pool = SubinterpreterPool
        case "interp2":
            Pool = SubinterpreterPool2
        case "interp3":
            Pool = SubinterpreterPool3
        case "thread":
            Pool = ThreadPool
        case "subprocess":
            pass
        case "sequential":
            single = True

    if gilknocker is not None:
        knocker = gilknocker.KnockKnock(1_000)
        knocker.start()

    if single:
        result = list(map(defs.bench_nbody, [10] * 64))
    else:
        with Pool() as p:
            result = list(p.map(defs.bench_nbody, [10] * 64))

    assert len(result) == 64
    assert all(len(x) == 100 for x in result)

    if gilknocker is not None:
        knocker.stop()
        print(f"gilknocker: {knocker.contention_metric}")
