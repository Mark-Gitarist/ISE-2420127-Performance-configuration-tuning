import os
import pandas as pd


def random_search_baseline(data, budget):

    best_performance = float('inf')
    budget_since_best = 0

    for i in range(budget):
        random_solution = data.sample(1).iloc[0].tolist()
        random_config = random_solution[:-1]
        config_perfomance = random_solution[-1]
        
        if config_perfomance < best_performance:
            best_performance = config_perfomance
            best_config = random_config
            budget_since_best = 0
        else:
            budget_since_best += 1

    return best_config, best_performance, budget_since_best




def main():
    datasets_folder = "datasets" 
    output_folder = "search_results"
    os.makedirs(output_folder, exist_ok=True)
    
    budget = 100
    results = {}
    
    for file_name in os.listdir(datasets_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(datasets_folder, file_name)
            
            data = pd.read_csv(file_path)
            
            best_solution, best_performance, budget_since_best = random_search_baseline(data, budget)
            
            results[file_name] = {
                "Best Solution": best_solution,
                "Best Performance": best_performance,
                "Budget Since Best": budget_since_best
            }

    for system, result in results.items():
        print(f"System: {system}")
        print(f"  Best Solution:    [{', '.join(map(str, result['Best Solution']))}]")
        print(f"  Best Performance: {result['Best Performance']}")
        print(f"  Budget Since Best: {result['Budget Since Best']}")

if __name__ == "__main__":
    main()