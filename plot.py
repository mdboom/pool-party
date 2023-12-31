import json
import sys

from matplotlib import pyplot as plt

benchmark = sys.argv[-1]

data = json.load(open(f"{benchmark}.json"))

fig, axs = plt.subplots(2, 2, layout="constrained")


def rotate_data(data, metric, f):
    output = {}
    for mode, dataset in data.items():
        output[mode] = f(dataset.get(metric, 0))
    return output


def barchart(ax, name, dataset):
    xs = list(range(len(dataset)))
    ax.bar(
        xs, dataset.values(), color=[f"C{x}" for x in xs], label=list(dataset.keys())
    )


def plot(ax, metric, scale, f):
    dataset = rotate_data(data, metric, f)
    barchart(ax, metric, dataset)
    if metric == "wall_clock":
        metric = "speedup"
    ax.set_title(metric)
    ax.set_ylabel(scale)
    ax.set_xticks([])


plot(axs[0, 0], "gilknocker", "% GIL contention", lambda x: x * 100)
plot(
    axs[0, 1],
    "wall_clock",
    "speedup (vs. sequential)",
    lambda x: data["sequential"]["wall_clock"] / x,
)
plot(axs[1, 0], "cpu", "% CPU util / all cores", lambda x: (x / 1600) * 100)
plot(axs[1, 1], "vmpeak", "peak mem, all processes (mb)", lambda x: x / 1024)

axs[0, 1].legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

plt.suptitle(f"{benchmark} benchmark (16 cores)")

plt.savefig(f"{benchmark}.png")
