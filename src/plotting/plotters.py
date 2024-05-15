from dataclasses import dataclass

import matplotlib.pyplot as plt
import scienceplots as _
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from helpers import PathLike


class PlotterBuilder:
    def __init__(self):
        self.base_value: list[float] = []
        self.experimental: list[float] = []
        self.theoretical: list[float] = []


@dataclass
class Plotter:
    base_value: list[float]
    experimental: list[float]
    theoretical: list[float]


def plot(
    x: list[float] | list[int],
    experimental_y: list[float],
    theoretical_y: list[float],
    xlabel: str,
    ylabel: str,
    fig_path: PathLike,
) -> None:
    plt.style.use(["science", "notebook", "grid"])

    subplots: tuple[Figure, Axes] = plt.subplots()
    fig, ax = subplots

    ax.plot(x, experimental_y, "--o", label="Experimental")
    ax.plot(x, theoretical_y, ":o", label="Teórico")
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.savefig(fig_path, dpi=200)
