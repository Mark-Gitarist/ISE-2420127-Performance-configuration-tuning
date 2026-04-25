import pandas as pd
import numpy as np
import os
from scipy import stats
from tool import evolutionary_search
from baselineTest import random_search_baseline



def run_experiments():
    datasets_folder = "datasets"
    budget = 100
    initial_percentage  = 0.2
    repetitions = 30 

    summary = []

    for file_name in sorted(os.listdir(datasets_folder)):
        if file_name.endswith(".csv"):
            print(f"Testing {file_name}...")
            df = pd.read_csv(os.path.join(datasets_folder, file_name))
            
            tool_scores = []
            budget_since_best_tool = []
            baseline_scores = []
            budget_since_best_baseline = []

            for i in range(repetitions):
                _, tool_performance, tool_budget_since_best = evolutionary_search(df, budget, initial_percentage)
                tool_scores.append(tool_performance)
                budget_since_best_tool.append(tool_budget_since_best)

                _, baseline_performance, baseline_budget_since_best = random_search_baseline(df, budget)
                baseline_scores.append(baseline_performance)
                budget_since_best_baseline.append(baseline_budget_since_best)

            avg_tool = np.mean(tool_scores)
            avg_baseline = np.mean(baseline_scores)
            std_tool = np.std(tool_scores)
            avg_tool_budget_since_best = np.mean(budget_since_best_tool)
            avg_baseline_budget_since_best = np.mean(budget_since_best_baseline)

            _, p_val = stats.mannwhitneyu(tool_scores, baseline_scores, alternative='less')

            summary.append({
                "System": file_name,
                "Baseline_Avg": round(avg_baseline, 5),
                "Tool_Avg": round(avg_tool, 5),
                "Tool_Std": round(std_tool, 5),
                "Improvement %": round(((avg_baseline - avg_tool) / avg_baseline) * 100, 2),
                "P-Value": round(p_val, 4),
                "Tool_Budget Since Best": round(avg_tool_budget_since_best, 2),
                "Baseline_Budget Since Best": round(avg_baseline_budget_since_best, 2)
            })

    summary_df = pd.DataFrame(summary)
    print("Comparison of Tool and Random Baseline (Average of 30 Runs)")
    print(summary_df.to_string(index=False))
    summary_df.to_csv("final_results.csv", index=False)

if __name__ == "__main__":
    run_experiments()