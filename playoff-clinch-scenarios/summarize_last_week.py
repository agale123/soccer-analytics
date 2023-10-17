import pandas as pd
import numpy as np
import itertools

TEAMS = [
    "ORL",
    "HOU",
    "NJY",
    "KCC",
    "WAS",
    "NC",
    "CHI",
    "RGN",
    "SD",
    "LOU",
    "LA",
    "POR",
]

df = pd.read_csv("week_22_2.csv")
for team in TEAMS:
    for sub in ["Playoff", "Host", "Bye", "Shield"]:
        df[team + "_" + sub] = np.where(df[team + "_" + sub], team, "")

df["clinched"] = [list(filter(None, l)) for l in df[[t + "_Playoff" for t in TEAMS]].values.tolist()]
df["host"] = [list(filter(None, l)) for l in df[[t + "_Host" for t in TEAMS]].values.tolist()]
df["bye"] = [list(filter(None, l)) for l in df[[t + "_Bye" for t in TEAMS]].values.tolist()]
df["shield"] = [list(filter(None, l)) for l in df[[t + "_Shield" for t in TEAMS]].values.tolist()]

drop = list(filter(lambda x: "_" in x, df.columns))
df = df.drop(columns=drop)

ALREADY_CLINCHED = {"SD", "POR"}
TEAMS_CLINCHED = set()
ALREADY_HOST = {"SD", "POR"}
TEAMS_HOST = set()
ALREADY_BYE = {"SD", "POR"}
TEAMS_BYE = set()
ALREADY_SHIELD = set()
TEAMS_SHIELD = set()

for team in TEAMS:
    if df["clinched"].str.contains(team, regex=False).any():
        TEAMS_CLINCHED.add(team)
    if df["host"].str.contains(team, regex=False).any():
        TEAMS_HOST.add(team)
    if df["bye"].str.contains(team, regex=False).any():
        TEAMS_BYE.add(team)
    if df["shield"].str.contains(team, regex=False).any():
        TEAMS_SHIELD.add(team)
        
GAMES = list(filter(lambda x: "-" in x, df.columns))

def evaluate(teams, metric):
    output = {}
    for team in teams:

        # As we identify matching criteria, remove those rows
        subset = df.copy()

        # Store all the matches
        results = []

        # Check if all entries of a previous result are fully contained in values.
        def results_contains(values):
            for result in results:
                match = True
                for r in result:
                    if r not in values:
                        match = False
                if match:
                    return True
            return False

        # Evaluate n game criteria
        for n in range(1, 7):
            options = []
            for game in GAMES:
                for outcome in subset[game].unique():
                    if (
                        subset[subset[game] == outcome][metric]
                        .str.contains(team, regex=False)
                        .any()
                    ):
                        options.append((game, outcome))

            for combo in itertools.combinations(options, n):
                gs = list(map(lambda x: x[0], combo))
                os = list(map(lambda x: x[0], combo))
                masks = [subset[g] == o for (g, o) in combo]
                if len(gs) != len(set(gs)):
                    continue
                if results_contains(combo):
                    continue
                if (
                    subset[np.logical_and.reduce(masks)][metric]
                    .str.contains(team, regex=False)
                    .all()
                ):
                    subset = subset[~(np.logical_and.reduce(masks))]
                    results.append(list(combo))
        
        output[team] = results
    return output

WIN = ["(1, 0)", "(8, 0)"]
TIE = ["(0, 0)", "(1, 1)", "(8, 8)"]
LOSS = ["(0, 1)", "(0, 8)"]


def compare(r1, r2):
    for x, y in zip(r1, r2):
        if x[0] != y[0]:
            return False
        elif x[1] in WIN and not y[1] in WIN:
            return False
        elif x[1] in TIE and not y[1] in TIE:
            return False
        elif x[1] in LOSS and not y[1] in LOSS:
            return False
    return True


def count_matches(rs):
    val = 1
    for r in rs:
        if r[1] in WIN or r[1] in LOSS:
            val *= 2
        else:
            val *= 3
    return val


def to_string(rs):
    val = []
    for r in rs:
        if r[1] in WIN:
            val += [r[0].split("-")[0] + " win"]
        elif r[1] in LOSS:
            val += [r[0].split("-")[0] + " loss"]
        else:
            val += [r[0].split("-")[0] + " draw"]
    return " + ".join(val)

def to_special_string(next_result, matches):
    games = list(map(lambda x: x[0], next_result))
    matches = list(map(lambda x: [y[1] for y in x], matches))
    matches = list(map(list, zip(*matches)))
    val = []
    for g, m in zip(games, matches):
        if m[0] in WIN:
            prefix = ""
            if len(set(m)) != len(WIN):
                if "(1, 0)" in m:
                    prefix = " small"
                elif "(8, 0)" in m:
                    prefix = " big"
            val += [g.split("-")[0] + prefix + " win"]
        elif m[0] in LOSS:
            prefix = ""
            if len(set(m)) != len(LOSS):
                if "(0, 1)" in m:
                    prefix = " small"
                elif "(0, 8)" in m:
                    prefix = " big"
            val += [g.split("-")[0] + prefix + " loss"]
        else:
            prefix = ""
            if len(set(m)) != len(TIE):
                if "(0, 0)" in m or "(1, 1)" in m:
                    prefix = " small"
                elif "(8, 8)" in m:
                    prefix = " big"
            val += [g.split("-")[0] + prefix + " draw"]
    return " + ".join(val)


def to_english(results):
    output = {}
    for team in results:
        output[team] = []
        team_results = results[team]

        for n in range(1, 7):
            team_results_n = list(filter(lambda x: len(x) == n, team_results))
            while len(team_results_n) > 0:
                next_result = team_results_n[0]
                matches = list(
                    filter(lambda x: compare(x, next_result), team_results_n[1:])
                )
                if len(matches) + 1 == count_matches(next_result):
                    output[team].append(to_string(next_result))
                else:
                    output[team].append(to_special_string(next_result, matches + [next_result]))
                
                team_results_n.remove(next_result)
                for m in matches:
                    team_results_n.remove(m)

                

    return output

print("Shield:")
init = {x: [] for x in ALREADY_SHIELD}
init.update(evaluate(TEAMS_SHIELD-ALREADY_SHIELD, "shield"))
results = to_english(init)
for key in results:
    print(key)
    for r in results[key]:
        print("  " + r)
    
print("Bye:")
init = {x: [] for x in ALREADY_BYE}
init.update(evaluate(TEAMS_BYE-ALREADY_BYE, "bye"))
results = to_english(init)
for key in results:
    print(key)
    for r in results[key]:
        print("  " + r)

print("Host:")
init = {x: [] for x in ALREADY_HOST}
init.update(evaluate(TEAMS_HOST-ALREADY_HOST, "host"))
results = to_english(init)
for key in results:
    print(key)
    for r in results[key]:
        print("  " + r)
        
print("Clinch:")
init = {x: [] for x in ALREADY_CLINCHED}
init.update(evaluate(TEAMS_CLINCHED - ALREADY_CLINCHED, "clinched"))
results = to_english(init)
for key in results:
    print(key)
    for r in results[key]:
        print("  " + r)