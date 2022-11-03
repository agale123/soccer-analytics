# NWSL Analytics

This repository contains different NWSL-related analytics projects.

* `goal-assist-combos`: Players who have combined for the most goals
* `golden-boot`: Goals scored over the course of the season by contenders for the golden boot
* `moving-window-points`: Shows 5-game moving average of points for each team
* `nwsl-rank`: Python visualizations of teams' relative ranking in 2022
* `nwsl-standings`: Used d3 to build a webapp highlighting teams' rankings in 2021
* `playoff-odds`: Visualization of playoff odds over the 2022 season
* `playoff-possibilities`: Enumerates all possible standings outcomes and shows the distribution
* `reign-quilt`: Visualization of Reign match results as a quilt pattern
* `schedule-distribution`: How rest duration for different teams is distributed

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