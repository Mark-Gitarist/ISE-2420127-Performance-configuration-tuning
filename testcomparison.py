import pandas as pd
import numpy as np
import random
import os
from scipy import stats
from tool import evolutionary_search
from baseline import random_search



def run_experiments():
    datasets_folder = "datasets"
    budget = 100
    initial_percentage  = 0.2
    repetitions = 30 
    np.random.seed(42)
    random.seed(42)

    summary = []

    for file_name in sorted(os.listdir(datasets_folder)):
        if file_name.endswith(".csv"):
            print(f"Testing {file_name}...")
            df = pd.read_csv(os.path.join(datasets_folder, file_name))

            file_path = os.path.join(datasets_folder, file_name)
            output_file = os.path.join("search_results", f"{file_name}_baseline.csv")
            
            tool_scores = []
            baseline_scores = []

            for i in range(repetitions):
                _, tool_performance, _ = evolutionary_search(df, budget, initial_percentage)
                tool_scores.append(tool_performance)

                _, baseline_performance = random_search(file_path, budget, output_file)
                baseline_scores.append(baseline_performance)

            avg_tool = np.mean(tool_scores)
            avg_baseline = np.mean(baseline_scores)
            std_tool = np.std(tool_scores)

            _, p_val = stats.mannwhitneyu(tool_scores, baseline_scores, alternative='less')

            summary.append({
                "System": file_name,
                "Baseline_Avg": round(avg_baseline, 5),
                "Tool_Avg": round(avg_tool, 5),
                "Tool_Std": round(std_tool, 5),
                "Improvement %": round(((avg_baseline - avg_tool) / avg_baseline) * 100, 2),
                "P-Value": round(p_val, 4),
            })

    summary_df = pd.DataFrame(summary)
    print("Comparison of Tool and Random Baseline (Average of 30 Runs)")
    print(summary_df.to_string(index=False))
    summary_df.to_csv("final_results.csv", index=False)

if __name__ == "__main__":
    run_experiments()