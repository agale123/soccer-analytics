# Data Model
 
For each game, we need to generate a list of the progression of the
scores. Each tuple will be of the form (minute, home goals, away
goals). For example, it will look like: 

```
home, away, scores
RGN, ORL, [(0, 0, 0), (23, 1, 0), (47, 2, 0), (78, 2, 1)]
```

Then we will process this list of games to group them by team and
flip the goals if necessary. So for example:

```
[
  [(0, 0, 0), (23, 0, 1), (47, 0, 2), (78, 1, 2)],
  [(0, 0, 0), (65, 1, 0)]
]
```

When plotting, we will need to know the number of goals at each node
of the tree to see how wide we will need to spread the lines. Lines
at each node can be sorted by the end game goal differential.

For color scheme, the gradient is calculated based on a 90 minute
game duration and the colors at the nodes are determined by the 
minutes of the goals. Colors between are extrapolated based on
those minutes.
