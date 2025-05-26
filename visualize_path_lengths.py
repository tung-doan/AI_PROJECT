#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configure plot styling
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def analyze_path_lengths():
    """
    Analyze and visualize the average path lengths found
    by each algorithm across different maze sizes.
    """
    # Check if the results file exists
    filepath = 'results/path_lengths.csv'
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
            df.columns = ['Maze Size', 'Generation Algorithm', 'DFS Length', 'BFS Length', 
                          'A* Length']
        elif len(df.columns) >= 4:  # Expected number of columns when only using prim algorithm
            df.columns = ['Maze Size', 'DFS Length', 'BFS Length', 'A* Length']
        
        # Skip the header row if it was already in the CSV
        if df.iloc[0, 0] == 'Maze Size' or str(df.iloc[0, 0]).lower() == 'maze size':
            print("Found header row in data, skipping it.")
            df = df.iloc[1:].copy()
            
        # Convert numeric columns to appropriate types
        df['Maze Size'] = pd.to_numeric(df['Maze Size'], errors='coerce')
        for col in ['DFS Length', 'BFS Length', 'A* Length']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # Remove any rows with NaN values
        df = df.dropna()
        
        # Group by maze size to calculate average path lengths
        grouped_by_size = df.groupby('Maze Size').mean(numeric_only=True).reset_index()
        
        # Plot average path length by maze size
        plt.figure(figsize=(12, 8))
        width = 0.25  # width of the bars
        x = np.arange(len(grouped_by_size['Maze Size']))
        
        plt.bar(x - width, grouped_by_size['DFS Length'], width, label='DFS')
        plt.bar(x, grouped_by_size['BFS Length'], width, label='BFS')
        plt.bar(x + width, grouped_by_size['A* Length'], width, label='A*')
        
        plt.xlabel('Maze Size')
        plt.ylabel('Average Path Length (steps)')
        plt.title('Độ dài đường đi trung bình')
        plt.xticks(x, grouped_by_size['Maze Size'])
        plt.legend()
        plt.tight_layout()
        plt.savefig('results/path_lengths_visualization.png', dpi=300)
        plt.show()
        
        print("Visualization created and saved to results directory.")
        print("\nAverage path length by maze size:")
        print(grouped_by_size[['Maze Size', 'DFS Length', 'BFS Length', 'A* Length']])
        
    except Exception as e:
        print(f"Error analyzing path lengths: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if not os.path.exists('results'):
        os.makedirs('results')
    analyze_path_lengths()