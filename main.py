import sys, pygame, time

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#For convertion E means empty space, N means Non playable space
class Jelly:
    def __init__(self, array, type = "normal"):
        if len(array) != 2 or any(len(row) != 2 for row in array):
            raise ValueError("Each Jelly must be a 2x2 matrix.")
        self.array = array  # 2x2 color matrix
        if( type == "normal" or type == "na" or type == "empty"):
            self.type = type
        else:
            raise ValueError("Invalid Jelly Type")
        
    def expand(self):
        if(self.type == "empty"):
            return
        if(self.type == "na"):
            return
        for i in range(2):
            for j in range(2):
                if self.array[i][j] != 'E':
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    for ni, nj in neighbors:
                        if 0 <= ni < 2 and 0 <= nj < 2:
                            if self.array[ni][nj] == 'E':
                                self.array[ni][nj] = self.array[i][j]
                                

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

    def load_from_file(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
        # Parse colors
        self.colors = {}
        i = 0
        if( lines[i] == "//DEF COLORS\n"):
            i += 1
            while not  lines[i].startswith("//DEF GOAL\n"):
                color_def = lines[i].strip().split('=')
                color_name = color_def[0].strip()
                color_value = tuple(map(int, color_def[1].strip()[1:-1].split(',')))
                self.colors[color_name] = color_value
                i += 1
        
        # Parse goal
        self.goal = {}
        if( lines[i] == "//DEF GOAL\n"):
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
            if lines[i] == "//DEF BOARD\n":
                i += 1
                while not lines[i].startswith("//DEF SEQ"):
                    if lines[i].strip():
                        row = []
                        for j in range(0, len(lines[i].strip()), 2):
                            jelly_array = [
                                [lines[i][j], lines[i][j+1]],
                                [lines[i+1][j], lines[i+1][j+1]]
                            ]
                            row.append(Jelly(jelly_array))
                        self.board.append(row)
                        i += 2
                self.c1 = len(self.board)
                self.c2 = len(self.board[0])

        # Parse sequence
        self.next_jellies = []
        if( lines[i] == "//DEF SEQ\n"):
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
            raise ValueError("Invalid direction")

        for color1, color2 in pairs:
            if color1 == color2:
                collisionColors.append(color1)

        return collisionColors if collisionColors else None
    def collapse(self):
        changes = True
        while changes:
            changes = False
            for i in range(self.c1):
                for j in range(self.c2):
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
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
                            collisionColors = self.checkCollision(self.board[i][j], self.board[ni][nj], direction)
                            if collisionColors:
                                changes = True
                                for color in collisionColors:
                                    self.board[i][j].erase(color)
                                    self.board[ni][nj].erase(color)
                                self.board[i][j].expand()
                                self.board[ni][nj].expand()

    def display(self):
        for i in range(self.c1):
            for j in range(self.c2):
                square = self.board[i][j].array
                left = j * (width // self.c2)
                top = i * (height // self.c1)
                for r in range(len(square)):
                    for c in range(len(square[r])):
                        rect = pygame.Rect(left + c * (width // (self.c2 * 2)), top + r * (height // (self.c1 * 2)), width // (self.c2 * 2), height // (self.c1 * 2)) 
                        pygame.draw.rect(screen, self.colors[square[r][c]], rect)


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

# Define a 2x2 Jelly (Color 1)
jelly1 = Jelly([['E', 'A'], ['E', 'B']], "normal")
jelly1.expand()
print(jelly1)

jellyState = JellyFieldState("init.txt")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0, 0, 0))
    jellyState.display()
    time.sleep(2)
    jellyState.collapse()
    pygame.display.flip()
    clock.tick(60)
