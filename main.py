import pygameGUI, time
import copy
#For convertion E means empty space, N means Non playable space
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
        
    def expand(self):
        if(self.type == "empty"):
            return
        if(self.type == "na"):
            return
        newBoard = [row.copy() for row in self.array]
        for i in range(2):
            for j in range(2):
                if self.array[i][j] != 'E':
                    newBoard[i][j] = self.array[i][j]
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    for ni, nj in neighbors:
                        if 0 <= ni < 2 and 0 <= nj < 2:
                            if self.array[ni][nj] == 'E':
                                newBoard[ni][nj] = self.array[i][j]
                            
        self.array = newBoard
        if all(self.array[i][j] == 'E' for i in range(2) for j in range(2)):
            self.type = "empty"
                                

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
            print("Loading from file")
            self.load_from_file(file)
        else:
            self.c1 = 0
            self.c2 = 0
            self.board = []
            self.next_jellies = []
            self.goal = {}
            self.colors = {}
        self.score = 0

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
                print(goal_def)
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
        self.next_jellies = []
        if lines[i].strip() == "//DEF SEQ":
            i += 1
            while i < len(lines):
                if lines[i].strip():
                    jelly_array = [list(lines[i].strip()), list(lines[i+1].strip())]
                    self.next_jellies.append(Jelly(jelly_array))
                    i += 2
                i += 1
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
    def collapse(self):
        changes = True
        while changes:
            changes = False
            oldBoard = copy.deepcopy(self.board)
            for i in range(self.c1):
                for j in range(self.c2):
                    print(f"Checking {i},{j}")
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    globalCollisionColors = set()
                    for ni, nj in neighbors:
                        if 0 <= ni < self.c1 and 0 <= nj < self.c2:
                            print(f"Checking neighbor {ni},{nj}")
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
                                        if (color in self.goal):
                                            self.goal[color] = max(self.goal[color] - 1, 0)
                                        self.board[ni][nj].erase(color)
                                        self.board[ni][nj].expand()
                                        
                    for color in globalCollisionColors:
                        self.board[i][j].erase(color)
                        if (color in self.goal):
                            self.goal[color] = max(self.goal[color] - 1, 0)
                        self.board[i][j].expand()
        
                                
    def move(self, seqNum, x, y):
        if ((self.board[y][x].type == "empty") and (seqNum == 0 or seqNum == 1)):
            self.board[y][x] = self.next_jellies[seqNum]
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
    def printBoard(self): #depois fica a logica das cenas do ricardo aqui
        for row in self.board:
            for i in range(2):
                for jelly in row:
                    print("".join(jelly.array[i]), end=" ")
                print()
        print()
        print("Next Jellies:")
        for jelly in self.next_jellies:
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
            
            

    



def play():
    gui = pygameGUI.pygameGUI()
    jellyState = None
    while( not jellyState):
        file = input("Enter the file name: ")
        try:
            jellyState = JellyFieldState(file)
        except Exception as e:
            print(f"Error loading file: {e}")
            jellyState = None
    print("Initial Board State:")
    
    jellyState.printBoard()
    
    end = False
    
    while not end:
        move, seqNum, x, y = gui.handle_events(jellyState)
        gui.display(jellyState)
        if move:
            jellyState.move(seqNum, x, y)
            jellyState.collapse()
        if jellyState.isGoal():
            end = True
            print("You have won!")
            break
        
        elif jellyState.isBoardFull():
            end = True
            print("You have lost!")
            break


play()
