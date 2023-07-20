from matplotlib import pyplot as plt

import json

data = json.load(open("data.json"))

fig, axs = plt.subplots(2, 2, layout="constrained")


def rotate_data(data, metric, f):
    output = {}
    for mode, dataset in data.items():
        output[mode] = f(dataset[metric])
    return output


def barchart(ax, name, dataset):
    xs = list(range(len(dataset)))
    ax.bar(
        xs, dataset.values(), color=[f"C{x}" for x in xs], label=list(dataset.keys())
    )


def plot(ax, metric, scale, f):
    dataset = rotate_data(data, metric, f)
    barchart(ax, metric, dataset)
    ax.set_title(metric)
    ax.set_ylabel(scale)


plot(axs[0, 0], "gilknocker", "% GIL contention", lambda x: x * 100)
plot(
    axs[0, 1],
    "wall_clock",
    "time (vs. sequential)",
    lambda x: x / data["sequential"]["wall_clock"],
)
plot(axs[1, 0], "cpu", "% CPU util / all cores", lambda x: (x / 1600) * 100)
plot(axs[1, 1], "vmpeak", "peak mem, all processes (mb)", lambda x: x / 1024)

axs[0, 0].legend()

plt.suptitle("Running 16 workers on 8 core / 16 virtual core machine")

plt.savefig("results.png")