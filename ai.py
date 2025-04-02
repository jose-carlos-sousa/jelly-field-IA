from collections import deque
import copy
import heapq

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = 0

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        child_node.depth = self.depth + 1

    def __lt__(self, other):
        return False  # or any other logic to compare TreeNode instances

class AIAgent:
    def __init__(self, state):
        self.initial_state = state

    def goal_state(self, state):
        return all(value == 0 for value in state.goal.values())

    def get_child_states(self, state):
        states = []
        rows, cols = len(state.board), len(state.board[0])
        for row in range(rows):
            for col in range(cols):
                if state.board[row][col].is_empty():
                    for seqNum in range(min(2, len(state.next_jellies))):
                        jellyState = copy.deepcopy(state)
                        jellyState.move(seqNum, col, row)
                        jellyState.collapse()
                        states.append(jellyState)

        return states
    
    def depth_first_search(self):
        root = TreeNode(self.initial_state)
        stack = [root]
        visited = [root]

        while stack:
            node = stack.pop()
            if self.goal_state(node.state):
                return node
            for state in self.get_child_states(node.state):
                if state not in visited:
                    visited.append(state)
                    new_state = TreeNode(state)
                    node.add_child(new_state)
                    stack.append(new_state)

        return None

    def bfs_search(self):
        root = TreeNode(self.initial_state)
        queue = deque([root])
        visited = [root]
        while queue:
            node = queue.popleft()
            if self.goal_state(node.state):
                return node
            for state in self.get_child_states(node.state):
                if state not in visited:
                    visited.append(state)
                    child = TreeNode(state)
                    node.add_child(child)
                    queue.append(child)
        return None
    
    def iterative_deepening(self, max_depth=10):
        depth = 1
        while depth < max_depth:
            node = TreeNode(self.initial_state)
            stack = [node]
            visited = [node]

            while stack:
                node = stack.pop()
                if self.goal_state(node.state):
                    return node
                for state in self.get_child_states(node.state):
                    if state not in visited and node.depth < depth:
                        visited.append(state)
                        new_state = TreeNode(state)
                        node.add_child(new_state)
                        stack.append(new_state)
            
            depth += 1

        return None

    def heuristic_goal_vals(self, state):
        return sum(state.goal.values())
    def heuristic_non_empty_jellies(self, state):
        return state.nonEmptyJellyCount
    def heuristic_collapse_count(self, state):
        return 1000 / (state.collapseCount + 1)
    
    def a_star_search(self, heuristic, weight=1):
        root = TreeNode(self.initial_state)
        queue = [(0, root)]
        
        visited = set()
        while queue:
            _, node = heapq.heappop(queue)
            if self.goal_state(node.state):
                return node
            visited.add(node.state)
            for state in self.get_child_states(node.state):
                if state not in visited:
                    visited.add(state)
                    child = TreeNode(state)
                    node.add_child(child)
                    cost = node.depth + weight * heuristic(state)
                    heapq.heappush(queue, (cost, child))
        return None
    
    def greedy_search(self, heuristic):
        stack = []
        initial_node = TreeNode(self.initial_state)
        stack.append(initial_node)
        visited = set()

        while stack:
            node = stack.pop()
            if self.goal_state(node.state):
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

        return None
    
    def print_solution(self, node):

        steps = 0
        if (not node):
            print("NO SOLUTION FOUND MENDES!")
            return

        while (node.parent):
            node.state.printBoard()
            steps += 1
            node = node.parent
            
   
        print(f"Solution found in {steps} steps\n")
        return  

