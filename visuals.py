import matplotlib.pyplot as plt
import pandas as pd
import os

def visualize_comparison(results_folder, dataset_name, visualization_folder):

    baseline_file = os.path.join(results_folder, f"{dataset_name}_baseline.csv")
    tool_file = os.path.join(results_folder, f"{dataset_name}_tool.csv")

    if not os.path.exists(baseline_file) or not os.path.exists(tool_file):
        return

    baseline_df = pd.read_csv(baseline_file)
    tool_df = pd.read_csv(tool_file)

    baseline_df['Best_So_Far'] = baseline_df['Performance'].cummin()
    tool_df['Best_So_Far'] = tool_df['Performance'].cummin()

    plt.figure(figsize=(10, 6))

    plt.plot(baseline_df.index, baseline_df['Best_So_Far'], label="Random Search (Baseline)", color='green', linestyle='--')
    plt.plot(tool_df.index, tool_df['Best_So_Far'], label="Evolutionary Tool (Proposed)", color='blue', linewidth=2)

    plt.xlabel("Search Iteration (Measurement Budget)", fontsize=12)
    plt.ylabel("Best Performance Found", fontsize=12)
    plt.title(f"Convergence Comparison: {dataset_name}", fontsize=14)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)

    os.makedirs(visualization_folder, exist_ok=True)
    plt.savefig(os.path.join(visualization_folder, f"{dataset_name}_comparison.png"))
    plt.close()

def main():
    """
    Main function to generate visualizations for all datasets in the results folder.
    """
    results_folder = "search_results"
    visualization_folder = "visualization_results"

    if not os.path.exists(results_folder):
        print(f"Error: The folder {results_folder} does not exist.")
        return

    for file_name in os.listdir(results_folder):
        if file_name.endswith("_search_results.csv"):
            dataset_name = file_name.replace("_search_results.csv", "")
            visualize_comparison(results_folder, dataset_name, visualization_folder)


if __name__ == "__main__":
    main()