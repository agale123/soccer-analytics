from common import Fonts, Images, Colors, add_twitter_handle
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def interpolate(x1, y1, x2, y2, cubic_p):
    steps = np.linspace(0, cubic_p, 7)
    x = list(map(lambda i: x1 + i, steps)) + list(map(lambda i: x2 - i, steps[::-1]))
    y = [y1] * len(steps) + [y2] * len(steps)
    f = interp1d(x, y, kind="quadratic")
    xs = np.linspace(x1, x2, num=40)
    ys = f(xs)

    return (xs, ys)


def plot_standings_v2(
    df_original,
    df_table_original,
    folder,
    names,
    colors,
    text_colors,
    title,
    label_width=0.37,
    twitter_x=0.88,
    cubic_p=0.1,
    plot_ratio=0.8,
):
    # Make deep copy to avoid changing the input
    df = df_original.copy()
    df_table = df_table_original.copy()

    # Get the week number
    week = int(df.columns[-1])

    # Sort so top teams have lines drawn on top
    df = df.sort_values(by=[str(week)], ascending=False)

    # Set up the plot and axes
    plt.clf()
    fig = plt.figure(dpi=100, figsize=(20 + 4 * (week - 5) / 15, 13.5), facecolor=Colors.WHITE)
    ax0 = fig.add_axes([0, 0, plot_ratio, 0.85])
    ax1 = fig.add_axes([plot_ratio-0.06, 0, 1-(plot_ratio-0.06), 0.85])
    axs = [ax0, ax1]
    
    for ax in axs:
        ax.set_facecolor(Colors.WHITE)

    # Plot scatterplot
    ax = axs[0]

    # Background lines for each team's progress
    for team in df.index:
        x = list(map(lambda j: int(j) - 1, list(df.columns)))
        y = df.loc[team].to_numpy()

        # Interpolate data to get smooth lines
        x2, y2 = [], []
        for xi, yi in zip(x, y):
            if len(x2) == 0:
                x2.append(xi)
                y2.append(yi)
            else:
                xs, ys = interpolate(x2[-1], y2[-1], xi, yi, cubic_p)
                x2.extend(xs)
                y2.extend(ys)
        ax.plot(x2, y2, linewidth=5, color=colors[team], solid_capstyle="round")

    # Circles for each week
    for team in df.index:
        ax.scatter(df.columns, df.loc[team], s=800, color=colors[team], zorder=10)

    # General
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # y-axis
    ax.set_yticks([])
    ax.set_ylim([12.5, 0.5])
    ax.yaxis.grid(False)

    # x-axis
    ax.set_xticks(range(0, week))
    ax.set_xlim([-0.25, week-0.75])
    ax.xaxis.grid(True, color=Colors.LIGHT_GRAY)
    ax.tick_params(
        axis="x", which="major", labelsize=20, color=Colors.GRAY, bottom=False
    )
    ax.set_xlabel(
        "Week", fontproperties=Fonts.BARLOW, size=32, color=Colors.BLACK, ha="center"
    )
    ax.xaxis.set_label_coords(0.5, -0.05)

    # Table plot
    ax = axs[1]

    for team in df.index:
        # Background behind team
        ax.plot(
            [0, label_width],
            [df.at[team, str(week)], df.at[team, str(week)]],
            linewidth=30,
            color=colors[team],
            solid_capstyle="round",
            clip_on=False,
        )
        # Team label
        ax.text(
            0,
            df.at[team, str(week)],
            names[team],
            color=text_colors[team],
            fontsize=20,
            fontproperties=Fonts.BARLOW,
            va="center",
            ha="left",
        )

        # Team stats
        for i, col in enumerate(df_table.columns):
            ax.text(
                label_width + 0.11 + i * 0.12,
                df.at[team, str(week)],
                df_table.at[team, col],
                color=Colors.BLACK,
                fontsize=20,
                fontproperties=Fonts.BARLOW,
                va="center",
                ha="center",
            )

    # Stat headers
    ax.text(
        0,
        0,
        "Team",
        color=Colors.BLACK,
        fontsize=20,
        fontproperties=Fonts.BARLOW_BOLD,
        va="center",
        ha="left",
    )
    for i, col in enumerate(df_table.columns):
        ax.text(
            label_width + 0.11 + i * 0.12,
            0,
            col,
            color=Colors.BLACK,
            fontsize=20,
            fontproperties=Fonts.BARLOW_BOLD,
            va="center",
            ha="center",
        )

    # Set axes to match line chart
    ax.set_ylim([12.5, 0.5])
    ax.set_xlim([0, 0.9])
    ax.axis("off")

    # Title
    plt.suptitle(
        title, fontproperties=Fonts.BARLOW_BOLD, size=48, color=Colors.BLACK, y=0.98, x=0.5+0.08
    )

    # Twitter logo and username
    add_twitter_handle(fig, x=twitter_x, y=-0.065, fs=24, w=0.03)

    # Save image
    fig.tight_layout()
    plt.savefig(
        folder + "/week" + str(week) + ".png", bbox_inches="tight", pad_inches=0.5
    )

def plot_standings(df, folder, playoff_cutoff, names, colors, text_colors, title, extra_cols=5):
    # Add extra columns as backdrop for team names
    week = int(df.columns[-1])
    for i in range(1, extra_cols + 1):
        df[str(week + i)] = df[str(week)]

    # Sort so top teams have lines drawn on top
    df = df.sort_values(by=[str(week)], ascending=False)

    # Start plotting

    plt.clf()
    plt.rcParams["figure.figsize"] = (24, 13.5)
    plt.figure(dpi=1200, facecolor="white")
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("white")

    # Playoff line
    if playoff_cutoff:
        plt.hlines(y=6.5, xmin=0, xmax=week + 1.5, linestyle="--", color="black")
        ax.text(
            week + extra_cols - 1,
            playoff_cutoff + 0.5,
            "Playoff line",
            color="black",
            fontsize=18,
            fontproperties=Fonts.BARLOW,
            va="center",
            ha="right",
        )

    # Plot lines
    for team in df.index:
        ax.plot(
            df.columns,
            df.loc[team],
            linewidth=40,
            color=colors[team],
            alpha=0.9,
            solid_capstyle="round",
        )

        ax.text(
            week + extra_cols - 1,
            df.at[team, str(week)],
            names[team] + " " + str(df.at[team, str(week)]),
            color=text_colors[team],
            fontsize=28,
            fontproperties=Fonts.BARLOW,
            fontweight="bold",
            va="center",
            ha="right",
        )

    # Title
    plt.title(title, fontproperties=Fonts.BARLOW, size=48)

    # General
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)

    # y-axis
    fig.gca().invert_yaxis()
    ax.set_yticks([])
    ax.yaxis.grid(False)

    # x-axis
    ax.set_xticks(range(0, week))
    ax.xaxis.grid(True, color="lightgray")
    ax.tick_params(axis="x", which="major", labelsize=24)
    plt.xlabel("Week", fontproperties=Fonts.BARLOW, size=36)
    ax.xaxis.set_label_coords(
        (week * 0.5) / (week + extra_cols), -0.05, transform=ax.transAxes
    )

    # Twitter logo and username
    add_twitter_handle(fig, x=0.79, y=0.06, fs=26, w=0.03)

    # Save image
    plt.savefig(folder + "/week" + str(week) + ".png", bbox_inches="tight", pad_inches=0.5)