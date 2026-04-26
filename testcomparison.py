import pandas as pd
import numpy as np
import random
import os
from scipy import stats
from tool import evolutionary_search
from baseline import random_search



def run_experiments():
    datasets_folder = "datasets"
    output_folder = "search_results"
    budget = 100
    initial_percentage  = 0.2
    repetitions = 30 

    np.random.seed(42)
    random.seed(42)

    summary = []

    os.makedirs(output_folder, exist_ok=True)

    for file_name in sorted(os.listdir(datasets_folder)):
        if file_name.endswith(".csv"):
            print(f"Testing {file_name}...")
            df = pd.read_csv(os.path.join(datasets_folder, file_name))
            file_path = os.path.join(datasets_folder, file_name)

            tool_output_file = os.path.join(output_folder, f"{file_name}_tool.csv")
            baseline_output_file = os.path.join(output_folder, f"{file_name}_baseline.csv")
            
            tool_scores = []
            baseline_scores = []
            tool_best_budget = []
            baseline_best_budget = []

            for i in range(repetitions):
                _, tool_performance, tool_budget_since_best = evolutionary_search(df, budget, initial_percentage, tool_output_file)
                tool_scores.append(tool_performance)
                tool_best_budget.append(tool_budget_since_best)

                _, baseline_performance, baseline_budget_since_best = random_search(file_path, budget, baseline_output_file)
                baseline_scores.append(baseline_performance)
                baseline_best_budget.append(baseline_budget_since_best)

            avg_tool = np.mean(tool_scores)
            avg_baseline = np.mean(baseline_scores)
            std_tool = np.std(tool_scores)
            avg_tool_budget_since_best = np.mean(tool_best_budget)
            avg_baseline_budget_since_best = np.mean(baseline_best_budget)

            _, p_val = stats.mannwhitneyu(tool_scores, baseline_scores, alternative='less')

            summary.append({
                "System": file_name,
                "Baseline_Avg": round(avg_baseline, 5),
                "Tool_Avg": round(avg_tool, 5),
                "Tool_Std": round(std_tool, 5),
                "Improvement %": round(((avg_baseline - avg_tool) / avg_baseline) * 100, 2),
                "P-Value": round(p_val, 4),
                "Avg Tool_Budget Since Best": round(avg_tool_budget_since_best, 2),
                "Avg Baseline_Budget Since Best": round(avg_baseline_budget_since_best, 2)
            })

    summary_df = pd.DataFrame(summary)
    print("Comparison of Tool and Random Baseline (Average of 30 Runs)")
    print(summary_df.to_string(index=False))
    summary_df.to_csv("final_results.csv", index=False)

if __name__ == "__main__":
    run_experiments()