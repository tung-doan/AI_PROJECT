#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configure plot styling
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def analyze_execution_times():
    """
    Analyze and visualize the average execution times
    for each algorithm across different maze sizes.
    """
    # Check if the results file exists
    filepath = 'results/execution_times.csv'
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        print("Please run the benchmarks first using data.py")
        return

    # Read the CSV file
    try:
        # First row contains headers
        df = pd.read_csv(filepath)
        
        # Rename columns for clarity if needed
        if len(df.columns) >= 5:  # Expected number of columns
            df.columns = ['Maze Size', 'Generation Algorithm', 'DFS Time', 'BFS Time', 
                          'A* Time']
        elif len(df.columns) >= 4:  # Expected number of columns when only using prim algorithm
            df.columns = ['Maze Size', 'DFS Time', 'BFS Time', 'A* Time']
        
        # Skip the header row if it was already in the CSV
        if df.iloc[0, 0] == 'Maze Size' or str(df.iloc[0, 0]).lower() == 'maze size':
            print("Found header row in data, skipping it.")
            df = df.iloc[1:].copy()
            
        # Convert numeric columns to appropriate types
        df['Maze Size'] = pd.to_numeric(df['Maze Size'], errors='coerce')
        for col in ['DFS Time', 'BFS Time', 'A* Time']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # Remove any rows with NaN values
        df = df.dropna()
        
        # Group by maze size to calculate average execution times
        grouped_by_size = df.groupby('Maze Size').mean(numeric_only=True).reset_index()
        
        # Create Bar Chart visualization
        plt.figure(figsize=(12, 8))
        width = 0.25  # width of the bars
        x = np.arange(len(grouped_by_size['Maze Size']))
        
        plt.bar(x - width, grouped_by_size['DFS Time'], width, label='DFS', color='#1f77b4')
        plt.bar(x, grouped_by_size['BFS Time'], width, label='BFS', color='#ff7f0e')
        plt.bar(x + width, grouped_by_size['A* Time'], width, label='A*', color='#2ca02c')
        
        plt.xlabel('Maze Size')
        plt.ylabel('Average Execution Time (seconds)')
        plt.title('Thời gian thực thi trung bình')
        plt.xticks(x, grouped_by_size['Maze Size'])
        plt.grid(True, axis='y', alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('results/execution_times_bar_chart.png', dpi=300)
        plt.show()
        
        print("Visualizations created and saved to results directory.")
        print("\nAverage execution time (s) by maze size:")
        print(grouped_by_size[['Maze Size', 'DFS Time', 'BFS Time', 'A* Time']])
        
    except Exception as e:
        print(f"Error analyzing execution times: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if not os.path.exists('results'):
        os.makedirs('results')
    analyze_execution_times()