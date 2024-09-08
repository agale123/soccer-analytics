# Playoff constraints

## Introduction

The problem of calculating which teams have clinched playoff spots in the NWSL can be complex, especially when teams clinch playoff spots early in the season when it is not sensible to enumerate all possible outcomes. Instead I use **CP-SAT** solver from [Google's OR-Tools](https://developers.google.com/optimization/cp/cp_solver) to solve an integer programming problem. Using this solver, I calculate both the highest possible ranking and lowest possible ranking for each team to determine if they have clinched a playoff spot or been eliminated. Those results can then be used to calculate the set of scenarios from the upcoming weekends games that would result in a team clinching a playoff spot.

## Model

### Initial state
* $p^0_i$: points team *i* currently has
* $g_{ij}$: games remaining between team *i* and team *j*
* $k$: team for whom we are calculating if they have clinched a playoff spot
* $T$: the set of all teams

### Variables
* $w_{ij}$: future wins of team *i* over team *j*  
* $t_{ij}$: future ties between team *i* and team *j*  
* $p_i$: final points of team *i*
* $b_i$: boolean with value 1 if team *i* has the same or more points than team *k*

### Constraints

The number of wins, losses, and ties between two teams must equal the total number of games remaining between them:
```math
\forall i,j\in T, w_{ij} + w_{ji} + t_{ij} = g_{ij}
```

Ties between team *i* and *j* must be the same as the number of ties between team *j* and *i*:
```math
\forall i,j\in T, t_{ij} = t_{ji}
```
  
We can make a simplifying assumption that the worst case for team *k* is that they lose all future matches. If they still clinch a playoff spot, then we know there is no way they won't make the playoffs. So total points is the current number of points plus 3 for each win and 1 for each draw. Team *k* gets no additional points:
```math
p_i= \begin{cases}
  p^0_k & \text{if $i=k$} \\
  p^0_i + 3 \sum_{j\in T} w_{ij} + \sum_{j\in T} t_{ij} & \text{otherwise}
\end{cases}
```
 
Finally, we know that team *i* could potentially beat team *k* in the standings if it has at least as many points as team *k*:
```math
b_i = 1 \implies  p_i \geq p_k
```

### Objective

Subject to these constaints, we seek to maximize the number of teams that have more points than team *k*:

$$ \sum_{i\in T, i\neq k} b_i$$ 

If this sum is 8 or less then team *k* has clinched a playoff spot. Otherwise, there is a chance that they are eliminated.

## Scenarios
This model can be utilized to quickly calculate all scenarios that would lead to a team clinching a playoff spot in a subsequent weekend. To do this, enumerate all possible outcomes (win/loss/draw) for all 7 matches in the following weekend. For each set of outcomes, calculate if a team has clinched a playoff spot.

If all scenarios results in a team clinching a playoff spot, then they have already clinched a playoff spot. Otherwise, to summarize these results, iteratively look at sets of one, two, three, etc sets of game outcomes (e.g. game 1 results in a win). For each set of outcomes, if all games result in a team clinching then print out that set of outcomes and remove all matching games from the list of scenarios. Continue until no games where a team clinching a playoff spot remain. The set of printed scenarios are the set of outcomes which guarentee a team clinches a playoff spot.

## References

Russell, T., van Beek, P. (2008). Mathematically Clinching a Playoff Spot in the NHL and the Effect of Scoring Systems. In: Bergler, S. (eds) Advances in Artificial Intelligence. Canadian AI 2008. Lecture Notes in Computer Science(), vol 5032. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-540-68825-9_23
