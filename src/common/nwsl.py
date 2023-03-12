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
        "KC": "KC Current",
    }
    COLORS = {
        "NJNY": "#a9f1f5", # or #000000
        "POR": "#97262c",
        "LA": "#f8d5ce",
        "CHI": "#3cb5e4", # or #C8102E
        "WAS": "#000000",
        "SD": "#fc1896", # or #011e40
        "NC": "#d7c38b", # or #00416b
        "RGN": "#002f87",
        "LOU": "#c5b4e1",
        "HOU": "#ff6a01",
        "ORL": "#60269e",
        "KC": "#62cac9", # or #cf3339
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
        "KC": "#000000",
    }
    MAPPING = {
        "NJ/NY Gotham": "NJNY",
        "NJ/NY Gotham FC": "NJNY",
        "NJY": "NJNY",
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
        "Racing Louisville": "LOU",
        "Racing Louisville FC": "LOU",
        "Houston Dash": "HOU",
        "Orlando Pride": "ORL",
        "KC Current": "KC",
        "Kansas City Current": "KC",
        "KCC": "KC",
    }

    def map_team(t):
        if t in NWSL.MAPPING:
            return NWSL.MAPPING[t]
        else:
            return t

    def color(t):
        team = NWSL.map_team(t)
        if team in NWSL.COLORS:
            return NWSL.COLORS[team]
        else:
            return "gray"

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
