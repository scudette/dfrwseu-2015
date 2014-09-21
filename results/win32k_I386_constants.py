import os
from matplotlib import rc
rc('pgf', texsystem='pdflatex')
rc('font', size=8)

import matplotlib
matplotlib.use("pgf")

import matplotlib.pyplot as plt

import yaml

STYLES = ["ko", "k+", "kx", "ks"]
CONSTANTS = ["gptiCurrent", "grpWinStaList", "gpepCSRSS", "xxxCapture"]

# Plot struct offsets against kernel version.
def DrawData(arch):
    data = yaml.load(open("win32_data.json").read())

    # First filter for architecture and sort by version.
    data = sorted([x for x in data if x["arch"] == arch],
                  key=lambda x: x["version"])

    data = [x for i, x in enumerate(data) if (i % 1 == 0) or x['version'] >= '6']

    x_axis = range(len(data))

    plt.figure()

    # Only care about struct now.
    labels = []
    i = 0

    for k in CONSTANTS:
        print k

        label = k
        style = STYLES[i % len(STYLES)]
        i += 1
        plt.plot(x_axis, [r.get(k, 0) for r in data],
                 style, markerfacecolor="none",
                 label=label, markeredgewidth=1.5, markersize=5)

        plt.plot(x_axis, [r.get(k, 0) for r in data],
                 "k-", linewidth=0.5, label="_nolegend_")

        labels.append(label)

    plt.legend(loc='upper left', shadow=True)

    plt.xticks(x_axis, [r['version'] for r in data], rotation='vertical')

    plt.title("Win32k.sys constants variations with Version (%s)" % arch)
    plt.xlabel("Version")
    plt.ylabel("Constants offset")
    plt.tight_layout()

    output_file = os.path.splitext(__file__)[0]
    plt.savefig('%s.pdf' % output_file, dpi=500)

DrawData("I386")
