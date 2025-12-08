import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

# Fixing random state for reproducibility
np.random.seed(19680801)


def plot_scatter(ax, prng, nb_samples=100):
    """Scatter plot."""
    for mu, sigma, marker in [(-0.5, 0.75, "o"), (0.75, 1.0, "s")]:
        x, y = prng.normal(loc=mu, scale=sigma, size=(2, nb_samples))
        ax.plot(x, y, ls="none", marker=marker)
    ax.set_xlabel("X-label")
    ax.set_ylabel("Y-label")
    ax.set_title("Axes title")
    return ax


def plot_colored_lines(ax):
    """Plot lines with colors following the style color cycle."""
    t = np.linspace(-10, 10, 100)

    def sigmoid(t, t0):
        return 1 / (1 + np.exp(-(t - t0)))

    nb_colors = min(len(plt.rcParams["axes.prop_cycle"]), 4)
    shifts = np.linspace(-5, 5, nb_colors)
    amplitudes = np.linspace(1, 1.5, nb_colors)
    for t0, a in zip(shifts, amplitudes):
        ax.plot(t, a * sigmoid(t, t0), label=f"$t_0$ = {t0:.1f}", markevery=10)
    ax.set_xlim(-10, 10)
    ax.legend(title="Legend title")
    return ax


def plot_bar_graphs(ax, prng, min_value=5, max_value=25, nb_samples=4):
    """Plot two bar graphs side by side, with letters as x-tick labels."""
    x = np.arange(nb_samples)
    ya, yb = prng.randint(min_value, max_value, size=(2, nb_samples))
    width = 0.35
    ax.bar(x + width / 2, ya, width, hatch=r"//")
    ax.bar(x + width * 3 / 2, yb, width, color="C2", hatch=r"\\")
    ax.set_xticks(x + width, labels=["a", "b", "c", "d"])
    return ax


def plot_colored_circles(ax, prng, nb_samples=15):
    """
    Plot circle patches.

    NB: draws a fixed amount of samples, rather than using the length of
    the color cycle, because different styles may have different numbers
    of colors.
    """
    for sty_dict, _ in zip(plt.rcParams["axes.prop_cycle"](), range(nb_samples)):
        ax.add_patch(
            plt.Circle(  # type: ignore
                prng.normal(scale=3, size=2),
                radius=1.0,
                color=sty_dict["color"],
            )
        )
    ax.grid(visible=True)

    # Add title for enabling grid
    plt.title("ax.grid(True)", family="monospace", fontsize="small")

    ax.set_xlim([-4, 8])
    ax.set_ylim([-5, 6])
    ax.set_aspect("equal", adjustable="box")  # to plot circles as circles
    return ax


def plot_image_and_patch(ax, prng, size=(20, 20)):
    """Plot an image with random values and superimpose a circular patch."""
    values = prng.random_sample(size=size)
    ax.imshow(values)
    c = plt.Circle((5, 5), radius=5, label="patch", linewidth=2)  # type: ignore
    ax.add_patch(c)
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])


def plot_histograms(ax, prng, nb_samples=10000):
    """Plot 4 histograms and a text annotation."""
    params = ((10, 10), (4, 12), (50, 12), (6, 55))
    for a, b in params:
        values = prng.beta(a, b, size=nb_samples)
        ax.hist(values, histtype="stepfilled", bins=30, alpha=0.8, density=True)

    # Add a small annotation.
    ax.annotate(
        "Annotation",
        xy=(0.25, 4.25),
        xytext=(0.9, 0.9),
        textcoords=ax.transAxes,
        va="top",
        ha="right",
        bbox=dict(boxstyle="round", alpha=0.2),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="angle,angleA=-95,angleB=35,rad=10"
        ),
    )
    return ax


def plot_figure() -> Figure:
    """Setup and plot the demonstration figure with a given style."""
    # Use a dedicated RandomState instance to draw the same "random" values
    # across the different figures.
    prng = np.random.RandomState(96917002)

    fig, axs = plt.subplots(
        ncols=3,
        nrows=2,
        figsize=(7.4, 5.8),
        layout="constrained",
    )
    axs = axs.flatten()

    fig.suptitle("Figure Title", x=0.01, ha="left")

    plot_scatter(axs[0], prng)
    plot_image_and_patch(axs[1], prng)
    plot_bar_graphs(axs[2], prng)
    plot_colored_lines(axs[3])
    plot_histograms(axs[4], prng)
    plot_colored_circles(axs[5], prng)

    # add divider
    rec = Rectangle((0.025, 12.5), 0.9, 1, clip_on=False, linewidth=2)

    axs[4].add_artist(rec)

    fig.suptitle("Figure Title | 中文 | にほんご | 한글 ")
    fig.set(linewidth=2)

    return fig
