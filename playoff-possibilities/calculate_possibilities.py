from collections import defaultdict
import itertools
import math
import random
import numpy as np
import pandas as pd
import multiprocessing

# Max number of possible goals for each game
lim = 3

# Read in schedule
df = pd.read_csv("schedule.csv")

# Convert scores to tuples
df.loc[~df["score"].isnull(), "score"] = (
    df.loc[~df["score"].isnull(), "score"]
    .str.split("-")
    .apply(lambda x: (int(x[0]), int(x[1])))
)

def calc_table(matches):
    m = matches.copy()

    # Calculate home/away goals
    m["home_goals"] = m["score"].str[0]
    m["away_goals"] = m["score"].str[1]

    # Calculate home/away points
    m["home_points"] = np.where(m["home_goals"] > m["away_goals"], 3, 0) + np.where(
        ~m["home_goals"].isnull() * m["home_goals"] == m["away_goals"], 1, 0
    )
    m["away_points"] = np.where(m["home_goals"] < m["away_goals"], 3, 0) + np.where(
        ~m["home_goals"].isnull() * m["home_goals"] == m["away_goals"], 1, 0
    )

    # Calculate home/away wins
    m["home_wins"] = np.where(m["home_goals"] > m["away_goals"], 1, 0)
    m["away_wins"] = np.where(m["home_goals"] < m["away_goals"], 1, 0)

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
    ).fillna(0)
    results[["goals_for", "goals_against"]] = results[
        ["goals_for", "goals_against"]
    ].apply(pd.to_numeric)

    # Calculate the table
    table = results.groupby(["team"]).agg(
        {"points": "sum", "goals_for": "sum", "goals_against": "sum", "wins": "sum"}
    )
    table["goals_diff"] = table["goals_for"] - table["goals_against"]
    table = table.reset_index()

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

    return table

# Calculate all possible score combos
scores = list(
    list(
        map(
            lambda x: (x, 0),
            range(1, lim),
        )
    )
    + [(0, 0)]
    + list(
        map(
            lambda x: (0, x),
            range(1, lim),
        )
    )
)

# Count the number of remaining games
remaining = sum(df["score"].isna())

# Calculate score permutations
empty = pd.DataFrame(
    index=df["home"].unique(), columns=range(1, len(df["home"].unique()) + 1)
).fillna(0)
ranks = empty.copy()

def process_combination(comb):
    temp = empty.copy()
    df2 = df.copy()
    df2.loc[df2["score"].isnull(), "score"] = comb
    rank = calc_table(df2)
    for i, row in rank.iterrows():
        temp.at[rank.at[i, "team"], i] += 1
    return temp

p = multiprocessing.Pool(16)
results = p.imap(process_combination, itertools.combinations_with_replacement(scores, remaining))
for result in results:
    ranks = ranks.add(result)

# Write to csv
ranks.to_csv('possibilities-' + str(lim) + '.csv')