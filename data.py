import sys
import os
import csv
import random
import time
import numpy as np

# Add module paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import maze and algorithm modules
from maze.maze import Maze
from algorithm.a_star_final import find_path as a_star_find_path
from algorithm.bfs_final import find_path as bfs_find_path
from algorithm.dfs_final import find_path as dfs_find_path

def run_benchmarks(num_runs=10, maze_sizes=[15, 25, 50], complexity=0.05):
    """
    Run benchmarks for all pathfinding algorithms using only Prim's maze generation
    
    Parameters:
    - num_runs: Number of runs per configuration
    - maze_sizes: List of maze sizes to test
    - complexity: Maze complexity parameter
    """
    print(f"Starting benchmark with {num_runs} runs per maze size...")
    
    # Initialize result containers
    results_search = []  # Store number of cells explored
    results_time = []    # Store execution times
    results_path = []    # Store path lengths
    
    # Add headers to results
    results_search.append(["Maze Size", "DFS Cells", "BFS Cells", "A* Cells"])
    results_time.append(["Maze Size", "DFS Time", "BFS Time", "A* Time"])
    results_path.append(["Maze Size", "DFS Length", "BFS Length", "A* Length"])
    
    total_configs = len(maze_sizes) * num_runs
    current_config = 0
    
    for size in maze_sizes:
        for run in range(num_runs):
            current_config += 1
            print(f"\nProgress: {current_config}/{total_configs} - Running size={size}, run={run+1}")
            
            # Create maze with specified parameters using only prim algorithm
            try:
                m = Maze(size, complexity=complexity, algorithm="prim")
                
                # Save maze details for results
                search_results = [size]
                time_results = [size]
                path_results = [size]
                
                # Run DFS algorithm
                print("Running DFS algorithm...")
                dfs_search_steps = []
                start_time = time.time()
                dfs_path, dfs_search_steps = dfs_find_path(m, return_search_steps=True)
                end_time = time.time()
                dfs_time = end_time - start_time
                
                # Run BFS algorithm
                print("Running BFS algorithm...")
                bfs_search_steps = []
                start_time = time.time()
                bfs_result = bfs_find_path(m, return_search_steps=True)
            
                if isinstance(bfs_result, tuple) and len(bfs_result) == 3:
                    bfs_path, bfs_search_steps, _ = bfs_result
                else:
                    bfs_path = bfs_result
                    bfs_search_steps = []
                end_time = time.time()
                bfs_time = end_time - start_time
                
                # Run A* algorithm
                print("Running A* algorithm...")
                a_star_search_steps = []
                start_time = time.time()
                a_star_result = a_star_find_path(m, return_search_steps=True)
                # A* also returns 3 values when return_search_steps=True
                if isinstance(a_star_result, tuple) and len(a_star_result) == 3:
                    a_star_path, a_star_search_steps, _ = a_star_result
                else:
                    a_star_path = a_star_result
                    a_star_search_steps = []
                end_time = time.time()
                a_star_time = end_time - start_time
                
                # Store cells explored
                search_results.extend([
                    len(dfs_search_steps) if dfs_search_steps else 0,
                    len(bfs_search_steps) if bfs_search_steps else 0,
                    len(a_star_search_steps) if a_star_search_steps else 0
                ])
                
                # Store execution times
                time_results.extend([dfs_time, bfs_time, a_star_time])
                
                # Store path lengths
                path_results.extend([
                    len(dfs_path) if dfs_path else 0,
                    len(bfs_path) if bfs_path else 0,
                    len(a_star_path) if a_star_path else 0
                ])
                
                # Add results to collection
                results_search.append(search_results)
                results_time.append(time_results)
                results_path.append(path_results)
                
                # Print results for this run
                print("\nResults for this run:")
                print(f"  DFS:     Path length: {len(dfs_path) if dfs_path else 'No path'}, "
                      f"Cells explored: {len(dfs_search_steps) if dfs_search_steps else 0}, "
                      f"Time: {dfs_time:.5f}s")
                print(f"  BFS:     Path length: {len(bfs_path) if bfs_path else 'No path'}, "
                      f"Cells explored: {len(bfs_search_steps) if bfs_search_steps else 0}, "
                      f"Time: {bfs_time:.5f}s")
                print(f"  A*:      Path length: {len(a_star_path) if a_star_path else 'No path'}, "
                      f"Cells explored: {len(a_star_search_steps) if a_star_search_steps else 0}, "
                      f"Time: {a_star_time:.5f}s")
                
            except Exception as e:
                print(f"Error in configuration size={size}, run={run+1}: {e}")
                # Still add the configuration to results but with zeros
                results_search.append([size, 0, 0, 0])
                results_time.append([size, 0, 0, 0])
                results_path.append([size, 0, 0, 0])
    
    # Save results to CSV files
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Save cells explored
    with open('results/cells_explored.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_search)
    
    # Save execution times
    with open('results/execution_times.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_time)
    
    # Save path lengths
    with open('results/path_lengths.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results_path)
    
    print("\nBenchmark completed.")
    print("Results saved to:")
    print("  - results/cells_explored.csv")
    print("  - results/execution_times.csv")
    print("  - results/path_lengths.csv")

def run_single_benchmark(maze_size=25, complexity=0.05):
    """
    Run a single benchmark for all pathfinding algorithms on one maze
    """
    print(f"\nRunning single benchmark test with size={maze_size}, algorithm=prim, complexity={complexity}")
    
    # Create maze using only prim algorithm
    m = Maze(maze_size, complexity=complexity, algorithm="prim")
    
    # Run DFS algorithm
    print("Running DFS algorithm...")
    start_time = time.time()
    dfs_path, dfs_search_steps = dfs_find_path(m, return_search_steps=True)
    dfs_time = time.time() - start_time
    
    # Run BFS algorithm
    print("Running BFS algorithm...")
    start_time = time.time()
    bfs_result = bfs_find_path(m, return_search_steps=True)
    # BFS returns 3 values when return_search_steps=True
    if isinstance(bfs_result, tuple) and len(bfs_result) == 3:
        bfs_path, bfs_search_steps, _ = bfs_result
    else:
        bfs_path = bfs_result
        bfs_search_steps = []
    bfs_time = time.time() - start_time
    
    # Run A* algorithm
    print("Running A* algorithm...")
    start_time = time.time()
    a_star_result = a_star_find_path(m, return_search_steps=True)
    # A* also returns 3 values when return_search_steps=True
    if isinstance(a_star_result, tuple) and len(a_star_result) == 3:
        a_star_path, a_star_search_steps, _ = a_star_result
    else:
        a_star_path = a_star_result
        a_star_search_steps = []
    a_star_time = time.time() - start_time
    
    # Print results
    print("\nResults:")
    print(f"  DFS:     Path length: {len(dfs_path) if dfs_path else 'No path'}, "
          f"Cells explored: {len(dfs_search_steps) if dfs_search_steps else 0}, "
          f"Time: {dfs_time:.5f}s")
    print(f"  BFS:     Path length: {len(bfs_path) if bfs_path else 'No path'}, "
          f"Cells explored: {len(bfs_search_steps) if bfs_search_steps else 0}, "
          f"Time: {bfs_time:.5f}s")
    print(f"  A*:      Path length: {len(a_star_path) if a_star_path else 'No path'}, "
          f"Cells explored: {len(a_star_search_steps) if a_star_search_steps else 0}, "
          f"Time: {a_star_time:.5f}s")
    
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Maze pathfinding algorithm benchmarking tool')
    parser.add_argument('--runs', type=int, default=100, 
                        help='Number of runs per configuration (default: 5)')
    parser.add_argument('--sizes', type=int, nargs='+', default=[15, 25, 50],
                        help='Maze sizes to test (default: 1500 2500 5000)')
    parser.add_argument('--complexity', type=float, default=0.05,
                        help='Maze complexity (default: 0.05)')
    parser.add_argument('--single', action='store_true',
                        help='Run a single benchmark test with default parameters')
    
    args = parser.parse_args()
    
    if args.single:
        run_single_benchmark(maze_size=1000, complexity=args.complexity)
    else:
        run_benchmarks(
            num_runs=args.runs,
            maze_sizes=args.sizes,
            complexity=args.complexity
        )