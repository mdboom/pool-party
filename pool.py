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

import argparse
import sys

import defs


BENCHMARKS = {
    "nbody": (defs.bench_nbody, defs.get_nbody_data, defs.assert_nbody_results),
    "data_pass": (
        defs.bench_data_pass,
        defs.get_data_pass_data,
        defs.assert_data_pass_results,
    ),
    "balance": (defs.bench_balance, defs.get_balance_data, defs.assert_balance_results),
}


# TODO: Import __main__ into the subinterpreter so it can access f and it
# doesn't have to be defined in a separate module.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark multiprocessing pools in various modes"
    )
    parser.add_argument(
        "mode",
        choices=["interp", "interp2", "interp3", "thread", "subprocess", "sequential"],
        help="Type of pool to use",
    )
    parser.add_argument(
        "benchmark", choices=list(BENCHMARKS.keys()), help="The benchmark to run"
    )
    parser.add_argument(
        "workers", type=int, nargs="?", help="The number of workers to run"
    )
    args = parser.parse_args()

    single = False
    match args.mode:
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

    bench_func, bench_data, bench_assert = BENCHMARKS[args.benchmark]

    if gilknocker is not None:
        knocker = gilknocker.KnockKnock(1_000)
        knocker.start()

    if single:
        result = list(map(bench_func, bench_data()))
    else:
        with Pool(args.workers) as p:
            result = list(p.map(bench_func, bench_data()))

    bench_assert(result)

    if gilknocker is not None:
        knocker.stop()
        print(f"gilknocker: {knocker.contention_metric}")
