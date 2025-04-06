from collections import deque
import copy, time
import heapq
import tracemalloc
import os

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = 0
        self.move = []
        
    def add_move(self, move):
        self.move = move  #Move is [x,y,seqNum]

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        child_node.depth = self.depth + 1

    def __lt__(self, other):
        return False  # or any other logic to compare TreeNode instances

class AIAgent:
    def __init__(self, state):
        self.initial_state = state
        self.time = 0
        self.memory = 0

    def goal_state(self, state):
        return all(value == 0 for value in state.goal.values())

    def get_child_states(self, state):
        stateDict = {}
        rows, cols = len(state.board), len(state.board[0])
        for row in range(rows):
            for col in range(cols):
                if state.board[row][col].is_empty():
                    for seqNum in range(min(2, len(state.next_jellies))):
                        jellyState = copy.deepcopy(state)
                        jellyState.move(seqNum, col, row)
                        jellyState.collapse()
                        stateDict[(row, col, seqNum)] = jellyState

        return stateDict
    
    def depth_first_search(self):
        tracemalloc.start()
        start = time.time()
        root = TreeNode(self.initial_state)
        stack = [root]
        visited = [root]

        while stack:
            node = stack.pop()
            if self.goal_state(node.state):
                self.time = time.time() - start
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                self.memory = peak
                return node
            for moveArr, state in self.get_child_states(node.state).items():
                if state not in visited:
                    visited.append(state)
                    new_state = TreeNode(state)
                    new_state.add_move(moveArr)
                    node.add_child(new_state)
                    stack.append(new_state)

        self.time = time.time() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.memory = peak 
        return None

    def bfs_search(self):
        tracemalloc.start()
        start = time.time()
        root = TreeNode(self.initial_state)
        queue = deque([root])
        visited = [root]
        while queue:
            node = queue.popleft()
            if self.goal_state(node.state):
                self.time = time.time() - start
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                self.memory = peak
                return node
            for moveArr, state in self.get_child_states(node.state).items():
                if state not in visited:
                    visited.append(state)
                    child = TreeNode(state)
                    child.add_move(moveArr)
                    node.add_child(child)
                    queue.append(child)
        
        self.time = time.time() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.memory = peak 
        return None
    
    def iterative_deepening(self, max_depth=10):
        tracemalloc.start()
        start = time.time()
        depth = 1
        while depth < max_depth:
            node = TreeNode(self.initial_state)
            stack = [node]
            visited = [node]

            while stack:
                node = stack.pop()
                if self.goal_state(node.state):
                    self.time = time.time() - start
                    _, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    self.memory = peak
                    return node
                for moveArr, state in self.get_child_states(node.state).items():
                    if node.depth < depth:
                        visited.append(state)
                        new_state = TreeNode(state)
                        new_state.add_move(moveArr)
                        node.add_child(new_state)
                        stack.append(new_state)
            depth += 1

        self.time = time.time() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.memory = peak
        return None

    def heuristic_goal_vals(self, state):
        return sum(state.goal.values())
    def heuristic_non_empty_jellies(self, state):
        return state.nonEmptyJellyCount
    def heuristic_collapse_count(self, state):
        return 1000 / (state.collapseCount + 1)
    
    def a_star_search(self, heuristic, weight=1):
        tracemalloc.start()
        start = time.time()
        root = TreeNode(self.initial_state)
        queue = [(0, root)]
        
        visited = set()
        while queue:
            _, node = heapq.heappop(queue)
            if self.goal_state(node.state):
                self.time = time.time() - start
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                self.memory = peak
                return node
            visited.add(node.state)
            for moveArr, state in self.get_child_states(node.state).items():
                if state not in visited:
                    visited.add(state)
                    child = TreeNode(state)
                    child.add_move(moveArr)
                    node.add_child(child)
                    cost = node.depth + weight * heuristic(state)
                    heapq.heappush(queue, (cost, child))

        self.time = time.time() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.memory = peak
        return None
    
    def greedy_search(self, heuristic):
        tracemalloc.start()
        start = time.time()
        stack = []
        initial_node = TreeNode(self.initial_state)
        stack.append(initial_node)
        visited = set()

        while stack:
            node = stack.pop()
            if self.goal_state(node.state):
                self.time = time.time() - start
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                self.memory = peak
                return node

            visited.add(node.state)
            best_child = None
            best_heuristic = float('inf')
            for state in self.get_child_states(node.state):
                if state not in visited:
                    h_value = heuristic(state)
                    if h_value < best_heuristic:
                        best_heuristic = h_value
                        best_child = TreeNode(state)
            
            if best_child:
                node.add_child(best_child)
                stack.append(best_child)

        self.time = time.time() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.memory = peak
        return None
    
    def get_solution_stats(self, node):
        steps = 0
        move_sequence = []
        if (not node):
            return None
        player = node.state.player
        print(f"Player: {player}")
        print(f"stats: {node.state.stats}")
        level = node.state.stats['level']
        cur_timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
        file_name = f"solution_{player}_{level}_{cur_timestamp}.txt"
        while (node.parent):
            steps += 1
            move_sequence.append(node.move)
            node = node.parent
        move_sequence.reverse()
            
        board_size = len(node.state.board) * len(node.state.board[0])

        score = (1000 * board_size) / (steps + self.time)
        solution_dir = "solutions"
        if not os.path.exists(solution_dir):
            os.makedirs(solution_dir)
        random_num = os.urandom(4).hex()
        filename = f"{solution_dir}/{file_name}"
        with open(filename, "w") as f:
            f.write(f"Score: {round(score, 2)}\n")
            f.write(f"Steps: {steps}\n")
            f.write(f"Time: {round(self.time, 5)} seconds\n")
            f.write(f"Memory: {self.memory} bytes\n")
            for move in move_sequence:
                if (move[2] == 0):
                    f.write(f"Move: left piece moved to ({move[0]}, {move[1]})\n")
                else:
                    f.write(f"Move: right piece moved to ({move[0]}, {move[1]})\n")
            
        return round(score, 2), steps, self.time

