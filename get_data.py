import argparse
import json
import shutil
import subprocess

py = "venv/bin/python"
pip = [py, "-m", "pip"]

shutil.rmtree("venv")
subprocess.check_call(["../cpython/python", "-m", "venv", "venv"])
subprocess.check_call(
    pip
    + [
        "install",
        "git+https://github.com/mdboom/extrainterpreters@main#egg-info=extrainterpreters",
    ]
)
subprocess.check_call(pip + ["install", "gilknocker"])

data = {}

parser = argparse.ArgumentParser(
    description="Benchmark multiprocessing pools in various modes"
)
parser.add_argument(
    "benchmark", type=str, nargs='?', help="The benchmark to run", default="nbody"
)
args = parser.parse_args()
benchmark = args.benchmark


for mode in ["interp", "interp2", "interp3", "thread", "sequential", "subprocess"]:
    print(f"{mode=}")

    if benchmark in ("data_pass", "balance") and mode == "interp3":
        print(f"Skipping: {benchmark} doesn't work with interp3")
        continue

    output = subprocess.run(
        [
            "./memusg",
            "/usr/bin/time",
            "-f",
            "'wall_clock: %e\ncpu: %P\n'",
            py,
            "pool.py",
            mode,
            benchmark
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout

    data[mode] = {}

    for line in output.splitlines():
        if b":" not in line:
            continue
        parts = line.split(b":")
        if len(parts) != 2:
            continue
        key, val = parts
        match key:
            case b"gilknocker":
                val = float(val)
            case b"wall_clock":
                val = float(val)
            case b"vmpeak":
                val = int(val.split()[0])
            case b"cpu":
                val = int(val[:-1])
            case _:
                continue

        data[mode][key.decode("utf-8")] = val

json.dump(data, open(f"{benchmark}.json", "w"))
