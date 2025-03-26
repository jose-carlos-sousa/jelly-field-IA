# Jelly Field Puzzle

## State Definition
- Board of Jellies -> Matrix
- Array with the next jellies [Jelly1, Jelly2]
- [C1-NUM, C2-NUM ...]

Note: each Jelly is a 2 by 2 matrix

## Victory condition
- For each (color, num) in [C1-NUM, C2-NUM ...] num is 0

## Losing condition
- No space left to place the piece / board filled

## Operators
- Choose First Jelly and place it at (X,Y)
  - If (X,Y) is empty and (X,Y) is part of the map
- Choose Second Jelly and place it at (X,Y)
  - If (X,Y) is empty and (X,Y) is part of the map
- Hammer move in (X,Y)
  - If (X,Y) not empty and is part of the map

## State Update
- After placing a new jelly, for all neighbouring jellies: the jellies that border jellies of the same color are deleted and the jelly expands.
- After the first state update, we must check for chained state updates in case that a jelly color expansion causes new jelly deletion

## Score
- Number of moves to win the game

## Testing Algorithms

A script `test_algorithms.py` is provided to test various algorithms for different board sizes and write the results to a CSV file.

### Usage

1. Ensure you have the necessary files (`init.txt`, `mendes.txt`, etc.) in the same directory.
2. Run the script using the command:
   ```sh
   python test_algorithms.py
   ```
3. The results will be written to `results.csv` in the same directory.
