from collections import defaultdict
import itertools
import random
import numpy as np
import pandas as pd

df = pd.read_csv("schedule.csv", index_col=0)

full_tiebreak = True

def calc_table(matches):
    m = matches.copy().dropna()

    # Calculate home/away wins
    m["home_wins"] = np.where(m["home_goals"] > m["away_goals"], 1, 0)
    m["away_wins"] = np.where(m["home_goals"] < m["away_goals"], 1, 0)

    # Calculate home/away points
    m["home_points"] = 3 * m["home_wins"] + np.where(
        m["home_goals"] == m["away_goals"], 1, 0
    )
    m["away_points"] = 3 * m["away_wins"] + np.where(
        m["home_goals"] == m["away_goals"], 1, 0
    )

    # Combine home/away results
    results = pd.concat(
        [
            m[["home", "home_points", "home_goals", "away_goals", "home_wins"]].rename(
                columns={
                    "home": "team",
                    "home_points": "points",
                    "home_goals": "goals_for",
                    "away_goals": "goals_against",
                    "home_wins": "wins",
                }
            ),
            m[["away", "away_points", "away_goals", "home_goals", "away_wins"]].rename(
                columns={
                    "away": "team",
                    "away_points": "points",
                    "away_goals": "goals_for",
                    "home_goals": "goals_against",
                    "away_wins": "wins",
                }
            ),
        ]
    )

    # Calculate the table
    table = results.groupby(["team"]).agg(
        {"points": "sum", "goals_for": "sum", "goals_against": "sum", "wins": "sum"}
    ).reset_index()
    table["goals_diff"] = table["goals_for"] - table["goals_against"]

    if full_tiebreak:
        # Calculate tiebreakers for teams tied on points/goal differential/wins
        # - Goal differential
        # - Total wins
        # - Goals scored
        # - Head to head points
        # - Head to head goals scored
        table["tie_points"] = 0
        table["tie_goals"] = 0
        for index, row in table.iterrows():
            team = row["team"]
            tied = table[
                (table["team"] != team)
                & (table["points"] == row["points"])
                & (table["goals_diff"] == row["goals_diff"])
                & (table["wins"] == row["wins"])
            ].reset_index(drop=True)
            if len(tied.index) > 1:
                table.at[index, "tie_points"] = random.randint(0, 10)
            elif len(tied.index) == 1:
                opp = tied.iloc[0]["team"]
                subset = m[m["home"].isin([team, opp]) & m["away"].isin([team, opp])]
                for _, game in subset.iterrows():
                    game = game.fillna(0)
                    game[["home_goals", "away_goals"]] = game[
                        ["home_goals", "away_goals"]
                    ].apply(pd.to_numeric)
                    if game["home"] == team:
                        table.at[index, "tie_points"] += game["home_points"]
                        table.at[index, "tie_goals"] += game["home_goals"]
                    else:
                        table.at[index, "tie_points"] += game["away_points"]
                        table.at[index, "tie_goals"] += game["away_goals"]

        # Sort final table
        table = table.sort_values(
            by=["points", "goals_diff", "wins", "goals_for", "tie_points", "tie_goals"],
            ascending=False,
        ).reset_index(drop=True)
        table.index = table.index + 1
    else:
        # Sort final table
        table = table.sort_values(
            by=["points", "goals_diff", "wins", "goals_for"],
            ascending=False,
        ).reset_index()
        table.index = table.index + 1

        prev = table.iloc[0][["points", "goals_diff", "wins", "goals_for"]]
        for i in range(1, len(table.index)):
            cur = table.iloc[i][["points", "goals_diff", "wins", "goals_for"]]
            if (prev == cur).all():
                idx_list = table.index.tolist()
                idx_list[i] = idx_list[i-1]
                table.index = idx_list
            prev = cur

    return table

# Calculate the current table to test the script
table = calc_table(df.dropna())

# Generate a list of all possible scores
scores =  [(0, 0)]
for i in [1, 8]:
    scores.append((i, 0))
    scores.append((0, i))
    scores.append((i, i))

# GD (normalized to 0.01 to 0.99)
def scale_GD(gd):
    return (gd + 50) / 100


# W (normalized to 0.0001 to 0.0099)
def scale_W(w):
    return w / 24 / 100


# GF (normalized to 0.000001 to 0.000099)
def scale_GF(gf):
    return gf / 60 / 10000


REMAINING = 6
POSS = pd.DataFrame(itertools.product(scores, repeat=REMAINING))

# Calculate all outcomes
def calculate_outcomes(df):
    # Each row represents a possible set of remaining scores for the final games
    poss = POSS.copy()

    # Calculate the current table
    table = calc_table(df.dropna())

    # Fill in points, goal differential, and wins from already played games
    for i, row in table.iterrows():
        poss[row["team"] + "_Pts"] = row["points"]
        poss[row["team"] + "_GD"] = row["goals_diff"]
        poss[row["team"] + "_GF"] = row["goals_for"]
        poss[row["team"] + "_W"] = row["wins"]

    # Calculate points/goal differential/wins from future games
    for i, row in df[df["home_goals"].isna()].reset_index().iterrows():
        poss[row["home"] + "_Pts"] += np.where(
            poss[i].str[0] > poss[i].str[1],
            3,
            np.where(poss[i].str[0] == poss[i].str[1], 1, 0),
        )
        poss[row["away"] + "_Pts"] += np.where(
            poss[i].str[1] > poss[i].str[0],
            3,
            np.where(poss[i].str[1] == poss[i].str[0], 1, 0),
        )

        poss[row["home"] + "_GD"] += poss[i].str[0] - poss[i].str[1]
        poss[row["away"] + "_GD"] += poss[i].str[1] - poss[i].str[0]

        poss[row["home"] + "_GF"] += poss[i].str[0]
        poss[row["away"] + "_GF"] += poss[i].str[1]

        poss[row["home"] + "_W"] += np.where(poss[i].str[0] > poss[i].str[1], 1, 0)
        poss[row["away"] + "_W"] += np.where(poss[i].str[1] > poss[i].str[0], 1, 0)

    # For each team, calculate a playoff score that a team must maximize to be in the playoffs
    # The score is: Pts + GD (normalized to 0.01 to 0.99) + W (normalized to 0.0001 to 0.0099)
    for team in table["team"]:
        poss[team + "_Score"] = (
            poss[team + "_Pts"]
            + scale_GD(poss[team + "_GD"])
            + scale_W(poss[team + "_W"])
            + scale_GF(poss[team + "_GF"])
        )

    cols = [t + "_Score" for t in table["team"]]

    # For each team, calculate if they made the playoffs
    for team in table["team"]:
        poss[team + "_Playoff"] = (
            poss.loc[:, cols].gt(poss.loc[:, team + "_Score"], axis=0).sum(axis=1)
        ) < 6
        poss[team + "_Host"] = (
            poss.loc[:, cols].gt(poss.loc[:, team + "_Score"], axis=0).sum(axis=1)
        ) < 4
        poss[team + "_Bye"] = (
            poss.loc[:, cols].gt(poss.loc[:, team + "_Score"], axis=0).sum(axis=1)
        ) < 2
        poss[team + "_Shield"] = (
            poss.loc[:, cols].gt(poss.loc[:, team + "_Score"], axis=0).sum(axis=1)
        ) < 1

    # Confirm there are no ties impacting standings
    # Check that 1!=2 2!=3 4!=5 6!=7
    for i in range(1, 8):
        poss[str(i) + "_Rank"] = poss.loc[:, cols].apply(lambda x: x.nlargest(i).iloc[-1], axis=1)

    poss["tie"] = (
        (poss["1_Rank"] == poss["2_Rank"])
        | (poss["2_Rank"] == poss["3_Rank"])
        | (poss["4_Rank"] == poss["5_Rank"])
        | (poss["6_Rank"] == poss["7_Rank"])
    )

    return poss

def fill_scores(df, scores):
    temp = df.copy()
    for home, home_score, away, away_score in scores:
        temp.loc[
            (temp["home"] == home) & (temp["away"] == away), ["home_goals", "away_goals"]
        ] = [home_score, away_score]
        
    return temp

# Calculate week 22 options
# TODO(agale): remove these temp scores
temp = fill_scores(
    df,
    [
        ("HOU", 0, "LA", 0),
    ],
)

results = calculate_outcomes(temp)
results = results.rename(
    columns={
        0: "ORL-HOU",
        1: "NJY-KCC",
        2: "WAS-NC",
        3: "CHI-RGN",
        4: "SD-LOU",
        5: "LA-POR",
    }
)

if results["tie"].sum() > 0:
    print("Tied teams")
    print(results[results["tie"]])
drop = (
    [t + "_" + x for t in table["team"] for x in ["W", "Pts", "GF", "GD", "Score"]]
    + ["tie"]
    + [str(i) + "_Rank" for i in range(1, 8)]
)
results = results.drop(columns=drop)

results.to_csv("week_22_2.csv", index=False)
