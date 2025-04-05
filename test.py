from ai import AIAgent
from jelly_field_state import JellyFieldState
import signal
import time
import os


def run_test(algorithm, level, weight):
    try:
        jellyState = JellyFieldState(level)
        myagent = AIAgent(jellyState)
        def timeout_handler(signum, frame):
            raise TimeoutError("Algorithm execution timed out after 5 minutes")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(300) 
        
        start_time = time.time()
        
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
            solution = myagent.a_star_search(myagent.heuristic_non_empty_jellies, weight)
        elif(algorithm == 'a_star_minimize_goal'):
            solution = myagent.a_star_search(myagent.heuristic_goal_vals, weight)
        elif(algorithm == 'a_star_collapse_count'):
            solution = myagent.a_star_search(myagent.heuristic_collapse_count, weight)
            
        if solution:
            score, steps, solution_time = myagent.get_solution_stats(solution)
        else:
            score, steps, solution_time = 0, 0, 0
        
        # Cancel the alarm
        signal.alarm(0)
        solution.state.stats = {'time': solution_time, 'level': solution.state.stats['level'], 'player': solution.state.player, 'score': score, 'steps': steps, 'memory': myagent.memory}
        
        execution_time = time.time() - start_time
        print(f"Algorithm: {algorithm}, Execution time: {execution_time:.2f} seconds")
        return solution
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        
def run_tests():
    levels = ['leveleasiest', 'leveleasy', 'levelmedium', 'levelhard', 'levelhardest']
    levels = [os.path.join('.', 'levels', f'{level}.txt') for level in levels]
    algorithms = ['depth_first', 'breadth_first', 'greedy_maximize_empty', 'greedy_minimize_goal','greedy_collapse_count', 'a_star_maximize_empty', 'a_star_minimize_goal', 'a_star_collapse_count']
    weight_vals = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    for level in levels:
        for algorithm in algorithms:
            if(algorithm == 'depth_first'):
                solution = run_test(algorithm, level, None)
                write_to_csv(algorithm, level, solution)
            elif(algorithm == 'breadth_first'):
                solution =  run_test(algorithm, level, None)
                write_to_csv(algorithm, level, solution)
            elif(algorithm == 'greedy_maximize_empty'):
                solution = run_test(algorithm, level, None)
                write_to_csv(algorithm, level, solution)
            elif(algorithm == 'greedy_minimize_goal'):
                solution = run_test(algorithm, level, None)    
                write_to_csv(algorithm, level, solution)
            elif(algorithm == 'greedy_collapse_count'):
                solution = run_test(algorithm, level, None)
                write_to_csv(algorithm, level, solution)
            elif(algorithm == 'a_star_maximize_empty'):
                for weight in weight_vals:
                    solution = run_test(algorithm, level, weight)
                    write_to_csv(algorithm, level, solution)
            elif(algorithm == 'a_star_minimize_goal'):
                for weight in weight_vals:
                    solution = run_test(algorithm, level, weight)
                    write_to_csv(algorithm, level, solution)
            elif(algorithm == 'a_star_collapse_count'):
                for weight in weight_vals:
                    solution = run_test(algorithm, level, weight)
                    write_to_csv(algorithm, level, solution)
                    
def write_to_csv(algorithm, level, solution):
    with open('test_results.csv', 'a') as file:
        if solution:
            file.write(f"{algorithm},{level},{solution.state.stats['time']},{solution.state.stats['memory']},{solution.state.stats['score']},{solution.state.stats['steps']}\n")
        else:
            file.write(f"{algorithm},{level},None,None,None,None\n")
run_tests()