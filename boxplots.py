import pandas as pd
import matplotlib.pyplot as plt
import os

def create_simple_boxplots(results_folder, visualization_folder):
    os.makedirs(visualization_folder, exist_ok=True)

    for file in os.listdir(results_folder):
        if file.endswith("_raw_30_runs.csv"):
            system_name = file.replace("_raw_30_runs.csv", "")
            df = pd.read_csv(os.path.join(results_folder, file))
            
            plt.figure(figsize=(7, 5))
            plt.boxplot([df['Baseline'], df['Tool']], labels=['Random Baseline', 'Proposed Tool'])
            
            plt.title(f"Performance over 30 Runs: {system_name}")
            plt.ylabel("Performance (Lower is Better)")
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            
            plt.savefig(os.path.join(visualization_folder, f"{system_name}_boxplot.png"))
            plt.close()
            print(f"Done: {system_name}")

if __name__ == "__main__":
    create_simple_boxplots("search_results", "visualization_results")