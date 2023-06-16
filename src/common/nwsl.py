class NWSL:
    NAMES = {
        "NJNY": "NJ/NY Gotham",
        "POR": "Portland Thorns",
        "LA": "Angel City",
        "CHI": "Chicago Red Stars",
        "WAS": "Washington Spirit",
        "SD": "San Diego Wave",
        "NC": "NC Courage",
        "RGN": "OL Reign",
        "LOU": "Racing Louisville",
        "HOU": "Houston Dash",
        "ORL": "Orlando Pride",
        "KCC": "KC Current",
        "KC": "FC Kansas City",
        "BOS": "Boston Breakers",
        "UTA": "Utah Royals",
        "WNY": "Western NY Flash",
    }
    COLORS = {
        "BOS": "#234B8D",
        "CHI": "#3cb5e4", # or #C8102E
        "HOU": "#ff6a01",
        "KC": "#0082B9",
        "KCC": "#62cac9", # or #cf3339
        "LA": "#f8d5ce",
        "LOU": "#c5b4e1",
        "NC": "#d7c38b", # or #00416b
        "NJNY": "#a9f1f5", # or #000000
        "ORL": "#60269e",
        "POR": "#97262c",
        "RGN": "#002f87",
        "SD": "#fc1896", # or #011e40
        "UTA": "#fdb71a",
        "WAS": "#000000", 
        "WNY": "#d12121",
    }
    TEXT_COLORS = {
        "NJNY": "#000000",
        "POR": "#ffffff",
        "LA": "#000000",
        "CHI": "#000000",
        "WAS": "#ffffff",
        "SD": "#000000",
        "NC": "#000000",
        "RGN": "#ffffff",
        "LOU": "#000000",
        "HOU": "#000000",
        "ORL": "#ffffff",
        "KCC": "#000000",
    }
    MAPPING = {
        "NJ/NY Gotham": "NJNY",
        "NJ/NY Gotham FC": "NJNY",
        "NJY": "NJNY",
        "Sky Blue FC": "NJNY",
        "Portland Thorns": "POR",
        "Angel City": "LA",
        "Angel City FC": "LA",
        "Chicago Red Stars": "CHI",
        "Washington Spirit": "WAS",
        "San Diego Wave": "SD",
        "San Diego Wave FC": "SD",
        "NC Courage": "NC",
        "North Carolina Courage": "NC",
        "OL Reign": "RGN",
        "Reign FC": "RGN",
        "Racing Louisville": "LOU",
        "Racing Louisville FC": "LOU",
        "Houston Dash": "HOU",
        "Orlando Pride": "ORL",
        "KC Current": "KCC",
        "Kansas City Current": "KCC",
        "Utah Royals": "UTA",
    }

    def map_team(t):
        if t in NWSL.MAPPING:
            return NWSL.MAPPING[t]
        else:
            return t

    def color(t, old = False):
        team = NWSL.map_team(t) if not (old and t == "KC") else t
        if team in NWSL.COLORS:
            return NWSL.COLORS[team]
        else:
            return "#808080"

    def text_color(t):
        team = NWSL.map_team(t)

        if team in NWSL.TEXT_COLORS:
            return NWSL.TEXT_COLORS[team]
        else:
            return "black"

    def name(t):
        team = NWSL.map_team(t)

        if team in NWSL.NAMES:
            return NWSL.NAMES[team]
        else:
            return t
