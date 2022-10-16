from common import Fonts, Images
import matplotlib.pyplot as plt

def plot_standings(df, folder, playoff_cutoff, names, colors, text_colors, title, extra_cols=5):
    # Add extra columns as backdrop for team names
    week = int(df.columns[-1])
    extra_cols = 5
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

    # Username and Twitter logo
    plt.text(
        0.97,
        -0.07,
        "@agale137",
        transform=ax.transAxes,
        color="black",
        fontsize=20,
        alpha=0.7,
        fontproperties=Fonts.BARLOW,
        va="center",
        ha="right",
    )
    newax = fig.add_axes([0.79, 0.06, 0.03, 0.03], anchor="SE", zorder=1)
    newax.imshow(Images.TWITTER)
    newax.axis("off")

    # Save image
    plt.savefig(folder + "/week" + str(week) + ".png", bbox_inches="tight", pad_inches=0.5)