import time
import copy
import pandas as pd
from collections import deque
import ai

# InfiniteArray class
# Simulates an infinite array of the next jellies array repeating
class InfiniteArray:
    def __init__(self, arr):
        self.arr = arr.copy()
        self.cur = arr.copy()
        
    def append(self, value):
        self.cur.append(value)
        self.arr.append(copy.deepcopy(value))
        
    # when a jelly is popped, it is checked if it is the second to last jelly
    # if it is we add to the array with the last jelly a repeated copy of the original next jellies
    # the reason why it is the second to last is because at a given time there are always at least two jellies in the next jellies array
    def pop(self, index=-1):
        self.cur.pop(index)
        if len(self.cur) <= 1:
            if(index == 1): 
                self.cur = self.cur + self.arr.copy()
            else:
                self.cur = [self.arr.copy()[0]] + self.cur + self.arr.copy()[1:]
            
    def __getitem__(self, index):
        return self.cur[index]

    def __len__(self):
        return len(self.cur)
        
        
# Jelly class
# Represents a 2x2 jelly piece
# Each jelly can be normal, empty, or not applicable (na)
# The jelly can be expanded to fill adjacent empty spaces
class Jelly:
    def __init__(self, array, type = "normal"):
        if len(array) != 2 or any(len(row) != 2 for row in array):
            print("Each Jelly must be a 2x2 matrix.")
            return
        self.array = array  # 2x2 color matrix
        if( type == "normal" or type == "na" or type == "empty"):
            self.type = type
        else:
            print("Invalid Jelly Type")
            return
        
    def expand(self, boardState):
        if self.type == "empty" or self.type == "na":
            return
        
        new_board = [row.copy() for row in self.array]
        non_empty_count = sum(1 for i in range(2) for j in range(2) if self.array[i][j] != 'E')
        
        # Check the occurrence of each color
        color_counts = {}
        for i in range(2):
            for j in range(2):
                color = self.array[i][j]
                if color != 'E':
                    color_counts[color] = color_counts.get(color, 0) + 1
        
        for i in range(2):
            for j in range(2):
                if self.array[i][j] != 'E':
                    current_color = self.array[i][j]
                    
                    # If the color has more than one occurrence, we expand only when it is the only color in the jelly
                    if color_counts[current_color] > 1 and len(color_counts) > 1:
                        continue
                    
                    new_board[i][j] = self.array[i][j]
                    
                    if non_empty_count == 1:
                        directions = [(-1, -1), (-1, 0), (-1, 1),
                                      ( 0, -1),          ( 0, 1),
                                      ( 1, -1), ( 1, 0), ( 1, 1)]
                    else:
                        directions = [          (-1, 0), 
                                      ( 0, -1),          ( 0, 1),
                                                ( 1, 0)         ]
                    
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < 2 and 0 <= nj < 2:
                            if self.array[ni][nj] == 'E':
                                new_board[ni][nj] = self.array[i][j]
        
        self.array = new_board
        if all(cell == 'E' for row in self.array for cell in row):
            self.type = "empty"
            boardState.nonEmptyJellyCount -= 1

    def is_empty(self):
        return self.type == "empty"           
    def is_na(self):
        return self.type == "na"   

    def erase(self, color):
        for i in range(2):
            for j in range(2):
                if self.array[i][j] == color:
                    self.array[i][j] = 'E'
    def __str__(self):
        return str(self.array)

    def __eq__(self, other):
        return isinstance(other, Jelly) and self.array == other.array

    def __hash__(self):
        return hash(tuple(map(tuple, self.array)))

class JellyFieldState:
    def __init__(self, file=None):
        if file:
            print("Loading from file...")
            self.load_from_file(file)
        else:
            self.c1 = 0
            self.c2 = 0
            self.board = []
            self.next_jellies = InfiniteArray([])
            self.goal = {}
            self.colors = {}
            self.nonEmptyJellyCount = 0
            self.collapseCount = 0
        self.stats = {'time': 0, 'steps': 0, 'level': "", 'player': "", 'score': 0, 'memory': 0}
        self.player = None
                        
    def load_from_file(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
        # Parse colors
        self.colors = {}
        i = 0
        if lines[i].strip() == "//DEF COLORS":
            i += 1
            while not  lines[i].startswith("//DEF GOAL\n"):
                color_def = lines[i].strip().split('=')
                color_name = color_def[0].strip()
                color_value = tuple(map(int, color_def[1].strip()[1:-1].split(',')))
                self.colors[color_name] = color_value
                i += 1
        
        # Parse goal
        self.goal = {}
        if lines[i].strip() == "//DEF GOAL":
            i+=1
            while not lines[i].startswith("//DEF BOARD\n"):
                goal_def = lines[i].strip().split('=')
                color_name = goal_def[0].strip()
                goal_value = int(goal_def[1].strip())
                self.goal[color_name] = goal_value
                i += 1
        # Parse board
            self.board = []
            if lines[i].strip() == "//DEF BOARD":
                i += 1
                while not lines[i].startswith("//DEF SEQ"):
                    if lines[i].strip():
                        row = []
                        for j in range(0, len(lines[i].strip()), 2):
                            jelly_array = [
                                [lines[i][j], lines[i][j+1]],
                                [lines[i+1][j], lines[i+1][j+1]]
                            ]
                            jellyType = 'normal'
                            if(lines[i][j] == 'E' ):
                                jellyType = "empty"
                            if(lines[i][j] == 'N' ):
                                jellyType = "na"
                                
                            row.append(Jelly(jelly_array, jellyType))
                        self.board.append(row)
                        i += 2
                self.c1 = len(self.board)
                self.c2 = len(self.board[0])

        # Parse sequence
        self.next_jellies = InfiniteArray([])
        if lines[i].strip() == "//DEF SEQ":
            i += 1
            while i < len(lines):
                if lines[i].strip():
                    jelly_array = [list(lines[i].strip()), list(lines[i+1].strip())]
                    self.next_jellies.append(Jelly(jelly_array))
                    i += 2
                i += 1

        self.nonEmptyJellyCount = 0
        for row in range(self.c1):
            for col in range(self.c2):
                if self.board[row][col].type != "empty" and self.board[row][col].type != "na":
                    self.nonEmptyJellyCount += 1

        self.collapseCount = 0

    # Check for collision between two jellies
    # Returns a list of colors that are the same in both jellies
    # If no colors match, returns None
    def checkCollision(self, jelly1, jelly2, direction):
        if jelly1.type == "na" or jelly2.type == "na":
            return None

        collisionColors = []
        if direction == 'up':
            pairs = [(jelly1.array[0][0], jelly2.array[1][0]), (jelly1.array[0][1], jelly2.array[1][1])]
        elif direction == 'down':
            pairs = [(jelly1.array[1][0], jelly2.array[0][0]), (jelly1.array[1][1], jelly2.array[0][1])]
        elif direction == 'left':
            pairs = [(jelly1.array[0][0], jelly2.array[0][1]), (jelly1.array[1][0], jelly2.array[1][1])]
        elif direction == 'right':
            pairs = [(jelly1.array[0][1], jelly2.array[0][0]), (jelly1.array[1][1], jelly2.array[1][0])]
        else:
            print("Invalid direction")
            return None

        for color1, color2 in pairs:
            if color1 == color2:
                collisionColors.append(color1)

        return collisionColors if collisionColors else None

    
    # Collapse the board
    # Check for collisions and update the board accordingly until no more changes occur
    def collapse(self):
        changes = True
        while changes:
            changes = False
            oldBoard = copy.deepcopy(self.board)
            for i in range(self.c1):
                for j in range(self.c2):
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    globalCollisionColors = set()
                    for ni, nj in neighbors:
                        if 0 <= ni < self.c1 and 0 <= nj < self.c2:
                    
                            if ni == i - 1:
                                direction = 'up'
                            elif ni == i + 1:
                                direction = 'down'
                            elif nj == j - 1:
                                direction = 'left'
                            elif nj == j + 1:
                                direction = 'right'
                            collisionColors = self.checkCollision(oldBoard[i][j], oldBoard[ni][nj], direction)
                            if collisionColors:
                                for color in collisionColors:
                                    if color not in ['E', 'N']:
                                        changes = True
                                        globalCollisionColors.add(color)
                                        
                    for color in globalCollisionColors:
                        self.board[i][j].erase(color)
                        self.collapseCount += 1
                        if (color in self.goal):
                            self.goal[color] = max(self.goal[color] - 1, 0)
                        self.board[i][j].expand(self)
        
    # Move a jelly to a new position                   
    def move(self, seqNum, x, y):
        if ((self.board[y][x].type == "empty") and (seqNum == 0 or seqNum == 1)):
            self.board[y][x] = self.next_jellies[seqNum]
            self.nonEmptyJellyCount += 1
            self.next_jellies.pop(seqNum)
        else :
            print("Invalid Jelly Move")

    def __eq__(self, other):
        return (
            isinstance(other, JellyFieldState)
            and self.board == other.board
            and self.next_jellies == other.next_jellies
            and self.goal == other.goal
        )

    def __hash__(self):
        return hash((tuple(map(tuple, self.board)), tuple(self.next_jellies), frozenset(self.goal.items())))

    def __str__(self):
        return f"Colors {self.colors} Board: {self.board}, Next Jellies: {self.next_jellies}, Goal: {self.goal}"
    
    def printBoard(self):
        for row in self.board:
            for i in range(2):
                for jelly in row:
                    print("".join(jelly.array[i]), end=" ")
                print()
        print()
        print("Next Jellies:")
        for jelly in self.next_jellies.cur:
            for i in range(2):
                print("".join(jelly.array[i]))
            print()
        print()
        print("Goal:")
        for color, goal in self.goal.items():
            print(f"{color}: {goal}")
        print()
    
    def isGoal(self):
        for _, goal in self.goal.items():
            if goal != 0:
                return False
        return True
        
    def isBoardFull(self):
        for row in self.board:
            for jelly in row:
                if jelly.type == "empty":
                    return False
        return True
    
    # Used in hints to determine the next best move
    def get_next_best_move(self):
        aiAgent = ai.AIAgent(self)
        node = aiAgent.a_star_search(aiAgent.heuristic_collapse_count, 1.5)

        move = None

        while node.parent:
            move = node.move
            node = node.parent
        return move
