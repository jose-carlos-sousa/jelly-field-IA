from collections import deque
import copy

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
    
    def print_solution(self, node):

        steps = 0
        if (not node):
            print("NO SOLUTION FOUND MENDES!")
            return

        while (node.parent):
            steps += 1
            node = node.parent
   
        print(f"Solution found in {steps} steps\n")
        return  

