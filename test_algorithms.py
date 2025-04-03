import csv
import time
import signal
from ai import AIAgent
from main import JellyFieldState

# Define timeout exception
class TimeoutException(Exception):
    pass

# Timeout handler
def timeout_handler(signum, frame):
    raise TimeoutException("Algorithm timed out")

def test_algorithm(algorithm, heuristic=None, weight=1):
    results = []
    board_sizes = ["init.txt", "mendes.txt"]  # Add more board sizes if needed
    timeout_seconds = 300  # 5 minutes

    for board_size in board_sizes:
        jellyState = JellyFieldState(board_size)
        agent = AIAgent(jellyState)

        # Set up the timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)
        
        try:
            start_time = time.time()
            if algorithm == "dfs":
                solution = agent.depth_first_search()
            elif algorithm == "bfs":
                solution = agent.bfs_search()
            elif algorithm == "a_star":
                print(heuristic)
                agent = AIAgent(jellyState)
                if heuristic == "heuristic_goal_vals":
                    solution = agent.a_star_search(agent.heuristic_goal_vals, float(weight))
                elif heuristic == "heuristic_non_empty_jellies":
                    solution = agent.a_star_search(agent.heuristic_non_empty_jellies, float(weight))
            elif algorithm == "iterative_deepening":
                solution = agent.iterative_deepening()
            end_time = time.time()
            
            # Turn off the alarm
            signal.alarm(0)

            if solution:
                steps = 0
                node = solution
                while node.parent:
                    steps += 1
                    node = node.parent
                results.append((board_size, algorithm, heuristic, weight, steps, end_time - start_time))
            else:
                results.append((board_size, algorithm, heuristic, weight, "NA", end_time - start_time))
                
        except TimeoutException:
            # Algorithm exceeded time limit
            signal.alarm(0)  # Turn off the alarm
            end_time = time.time()
            results.append((board_size, algorithm, heuristic, weight, "NA", timeout_seconds))

    return results

def write_results_to_csv(results, filename="results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Board Size", "Algorithm", "Heuristic", "Weight", "Steps to Solution", "Time Taken (s)"])
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    algorithms = ["a_star", "bfs", "dfs", "iterative_deepening"]
    heuristics = [None, "heuristic_goal_vals", "heuristic_non_empty_jellies"]
    weights = [0.5 , 1, 1.5, 2, 2.5, 3]

    all_results = []
    for algorithm in algorithms:
        if algorithm == "a_star":
            for heuristic in heuristics:
                if heuristic:
                    for weight in weights:
                        results = test_algorithm(algorithm, heuristic, weight)
                        all_results.extend(results)
        else:
            results = test_algorithm(algorithm)
            all_results.extend(results)

    write_results_to_csv(all_results)
