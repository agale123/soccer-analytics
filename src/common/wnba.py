class WNBA:
    NAMES = {
        "LV": "Las Vegas Aces",
        "CHI": "Chicago Sky",
        "CONN": "Connecticut Sun",
        "DAL": "Dallas Wings",
        "SEA": "Seattle Storm",
        "MIN": "Minnesota Lynx",
        "PHX": "Pheonix Mercury",
        "WSH": "Washington Mystics",
        "NY": "New York Liberty",
        "LA": "Los Angeles Sparks",
        "ATL": "Atlanta Dream",
        "IND": "Indiana Fever",
    }
    COLORS = {
        "LV": "#000000",
        "CHI": "#FFCD00", # "#418FDE",
        "CONN": "#DC4405",
        "DAL": "#C4D600",
        "SEA": "#2C5234",
        "MIN": "#236192",
        "PHX": "#3c286e",
        "WSH": "#C8102E",
        "NY": "#6ECEB2",
        "LA": "#702F8A",
        "ATL": "#418fde", #"#C8102E",
        "IND": "#041E42", # "#C8102E"
    }
    TEXT_COLORS = {
        "LV": "#ffffff",
        "CHI": "#ffffff",
        "CONN": "#ffffff",
        "DAL": "#ffffff",
        "SEA": "#ffffff",
        "MIN": "#ffffff",
        "PHX": "#ffffff",
        "WSH": "#ffffff",
        "NY": "#ffffff",
        "LA": "#ffffff",
        "ATL": "#ffffff",
        "IND": "#ffffff",
    }
    MAPPING = {v: k for k, v in NAMES.items()}

    def map_team(t):
        if t in WNBA.MAPPING:
            return WNBA.MAPPING[t]
        else:
            return t

    def color(t):
        team = WNBA.map_team(t)
        if team in WNBA.COLORS:
            return WNBA.COLORS[team]
        else:
            return "gray"

    def text_color(t):
        team = WNBA.map_team(t)

        if team in WNBA.TEXT_COLORS:
            return WNBA.TEXT_COLORS[team]
        else:
            return "black"

    def name(t):
        team = WNBA.map_team(t)

        if team in WNBA.NAMES:
            return WNBA.NAMES[team]
        else:
            return t
