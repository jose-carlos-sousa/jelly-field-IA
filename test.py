from ai import AIAgent
from main import State
from jelly_field_state import JellyFieldState

def run_test():
    levels = ['leveleasiet.txt','leveleasy.txt','levelmedium.txt','levelhard.txt', 'levelhardest.txt']
    algorithms = ['depth_first', 'breadth_first', 'greedy_maximize_empty', 'greedy_minimize_goal','greedy_collapse_count', 'a_star_maximize_empty', 'a_star_minimize_goal', 'a_star_collapse_count']
    weight_vals = [0.5, 1 ,1.5,2,2.5,3, 3.5,4,4.5,5]
    for level in levels:
        jellyState = JellyFieldState(level)
        myagent = AIAgent(jellyState)
        for algorithm in algorithms:
            if(algorithm == 'depth_first'):
                solution = myagent.depth_first_search()
            elif(algorithm == 'breadth_first'):
                solution = myagent.bfs_search()
            elif(algorithm == 'greedy_maximize_empty'):
                solution = myagent.greedy_search(myagent.heuristic_non_empty_jellies)
            elif(algorithm == 'greedy_minimize_goal'):
                solution = myagent.greedy_search(myagent.heuristic_goal_vals)
            elif(algorithm == 'greedy_collapse_count'):
                solution = myagent.greedy_search(myagent.heuristic_collapse_count)
            elif(algorithm == 'a_star_maximize_empty'):
                for weight in weight_vals:
                    solution = myagent.a_star_search(myagent.heuristic_non_empty_jellies, weight)
            elif(algorithm == 'a_star_minimize_goal'):
                for weight in weight_vals:
                    solution = myagent.a_star_search(myagent.heuristic_goal_vals, weight)
            elif(algorithm == 'a_star_collapse_count'):
                for weight in weight_vals:
                    solution = myagent.a_star_search(myagent.heuristic_collapse_count, weight)
        