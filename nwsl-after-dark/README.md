# nwsl-after-dark

Project to analyze the "NWSL After Dark" phenomenon where late night games
tend to have more chaos.

## Findings

TODO

## Methodology

### scraper.ipynb

Jupyter Notebook file to read data from the NWSL website and merge it with
gametimes from FBRef.

### matches_fbref.csv

Data for NWSL matches downloaded from
[FBRef](https://fbref.com/en/comps/182/schedule/NWSL-Scores-and-Fixtures).

### matches.csv

Merged data from scraping the [NWSL](https://www.nwslsoccer.com/schedule)
website.

### analysis.ipynb

Generates scatterplots and linear regressions between game time and certain
stats like number of goals and fouls.