import sys

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

import concurrent.futures

gilknocker = None
try:
    if "nogil" not in sys.version:
        import gilknocker
except ImportError:
    pass

import argparse
import sys

import defs
import raytrace


BENCHMARKS = {
    "nbody": (defs.bench_nbody, defs.get_nbody_data, defs.assert_nbody_results),
    "nbody_no_share": (defs.bench_nbody_no_share, defs.get_nbody_data, defs.assert_nbody_results),
    "data_pass": (
        defs.bench_data_pass,
        defs.get_data_pass_data,
        defs.assert_data_pass_results,
    ),
    "balance": (defs.bench_balance, defs.get_balance_data, defs.assert_balance_results),
    "raytrace": (
        raytrace.bench_raytrace,
        raytrace.get_raytrace_data,
        raytrace.assert_raytrace_results,
    ),
    "fib": (defs.bench_fib, defs.get_fib_data, defs.assert_fib_results),
}


def get_multiprocessing_runner(pool_type):
    def multiprocessing_runner(nworkers, func, data):
        with pool_type(nworkers) as p:
            return list(p.map(func, data))

    return multiprocessing_runner


def get_sequential_runner():
    def sequential_runner(nworkers, func, data):
        return list(map(func, data))

    return sequential_runner


def get_threadpool_executor_runner():
    def threadpool_executor_runner(nworkers, func, data):
        with concurrent.futures.ThreadPoolExecutor(max_workers=nworkers) as executor:
            futures = [executor.submit(func, elem) for elem in data]
            concurrent.futures.wait(futures)
            return [x.result() for x in futures]

    return threadpool_executor_runner


# TODO: Import __main__ into the subinterpreter so it can access f and it
# doesn't have to be defined in a separate module.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark multiprocessing pools in various modes"
    )
    parser.add_argument(
        "mode",
        choices=["interp", "interp2", "thread", "subprocess", "sequential", "futures"],
        help="Type of pool to use",
    )
    parser.add_argument(
        "benchmark", choices=list(BENCHMARKS.keys()), help="The benchmark to run"
    )
    parser.add_argument(
        "--workers",
        type=int,
        nargs="?",
        help="The number of workers to run",
        default=16,
    )
    args = parser.parse_args()

    single = False
    match args.mode:
        case "interp":
            runner = get_multiprocessing_runner(SubinterpreterPool)
        case "interp2":
            runner = get_multiprocessing_runner(SubinterpreterPool2)
        case "thread":
            runner = get_multiprocessing_runner(ThreadPool)
        case "subprocess":
            runner = get_multiprocessing_runner(Pool)
        case "sequential":
            runner = get_sequential_runner()
        case "futures":
            runner = get_threadpool_executor_runner()

    bench_func, bench_data, bench_assert = BENCHMARKS[args.benchmark]

    if gilknocker is not None:
        knocker = gilknocker.KnockKnock(1_000)
        knocker.start()

    result = runner(args.workers, bench_func, bench_data())
    bench_assert(result)

    if gilknocker is not None:
        knocker.stop()
        print(f"gilknocker: {knocker.contention_metric}")
    elif "nogil" in sys.version:
        print(f"gilknocker: 0")
