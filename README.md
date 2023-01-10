# NWSL Analytics

This repository contains different NWSL-related analytics projects.

* [`asa`](asa/README.md): Plots using xG data from ASA, including performance relative to xG and xGA
* [`fawsl-rank`](fawsl-rank/README.md): Show changes in rankings over the FAWSL season
* [`goal-assist-combos`](goal-assist-combos/README.md): Players who have combined for the most goals
* [`goal-heatmap`](goal-heatmap/README.md): Heatmap of scored goals
* [`golden-boot`](golden-boot/README.md): Goals scored over the course of the season by contenders for the golden boot
* [`moving-window-points`](moving-window-points/README.md): Shows 5-game moving average of points for each team
* [`nwsl-rank`](nwsl-rank/README.md): Python visualizations of teams' relative ranking in 2022
* [`nwsl-standings`](nwsl-standings/README.md): Used d3 to build a webapp highlighting teams' rankings in 2021
* [`playoff-odds`](playoff-odds/README.md): Visualization of playoff odds over the 2022 season
* [`playoff-possibilities`](playoff-possibilities/README.md): Enumerates all possible standings outcomes and shows the distribution
* [`reign-quilt`](reign-quilt/README.md): Visualization of Reign match results as a quilt pattern
* [`schedule-infographic`](schedule-infographic/README.md): How rest duration for different teams is distributed
* [`score-waterfall`](score-waterfall/README.md): Visualization of how the scores for each team's games evolved over the game
* [`search-trends`](search-trends/README.md): Visualization of how each teams Google Search trends varied over the year

## Development

### Package management

Requirements for the Python libraries and notebooks in this project are
defined in `requirements.txt`. The versions supported by these notebooks is
defined in `requirements.lock.txt`. To update this file, run:

```
 pip3 freeze > requirements.lock.txt
 ```

To install the package containing shared code between notebooks:

```
pip3 install --editable .
```