// State Definition
Board of Jellies -> Matrix
Array with the next jellies [Jelly1, Jelly2]
[C1-NUM, C2-NUM ...]

Note: each Jelly is a 2 by 2 matrix

// Victory condition
for each (color, num) in [C1-NUM, C2-NUM ...] num is 0

// Losing condition
// no space left to place the piece / board filled

// Operators
Choose First Jelly and place it at (X,Y)
If (X,Y) is empty and (X,Y) is part of the map

Choose Second Jelly and place it at (X,Y)
If (X,Y) is empty and (X,Y) is part of the map

Hammer move in (X,Y)
If (X,Y) not empty and is part of the map

// State Update

after placing a new jelly, for all neighbouring jellies: the jellies that border jellies of the same color are deleted and the jelly expands. 

after the first state update, we must check for chained state updates in case that a jelly color expansion causes new jelly deletion

// Score

Number of moves to win the game
