import csv
import time
from ai import AIAgent
from main import JellyFieldState

def test_algorithm(algorithm, heuristic=None, weight=1):
    results = []
    board_sizes = ["init.txt", "mendes.txt"]  # Add more board sizes if needed

    for board_size in board_sizes:
        jellyState = JellyFieldState(board_size)
        agent = AIAgent(jellyState)

        start_time = time.time()
        if algorithm == "dfs":
            solution = agent.depth_first_search()
        elif algorithm == "bfs":
            solution = agent.bfs_search()
        elif algorithm == "a_star":
            solution = agent.a_star_search(heuristic, weight)
        elif algorithm == "iterative_deepening":
            solution = agent.iterative_deepening()
        end_time = time.time()

        if solution:
            steps = 0
            node = solution
            while node.parent:
                steps += 1
                node = node.parent
            results.append((board_size, steps, end_time - start_time))
        else:
            results.append((board_size, "No solution", end_time - start_time))

    return results

def write_results_to_csv(results, filename="results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Board Size", "Steps to Solution", "Time Taken (s)"])
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    algorithms = ["dfs", "bfs", "a_star", "iterative_deepening"]
    heuristics = [None, "heuristic_goal_vals", "heuristic_non_empty_jellies"]
    weights = [1, 1.5, 2]

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
