import pandas as pd
import random
import os


def evolutionary_search(data, budget, initial_percentage, output_file):

    initial_population = data.sample(int(budget* initial_percentage)).sort_values(data.columns[-1])

    current_best = initial_population.iloc[0].tolist()

    remaining_budget = budget - len(initial_population)

    current_best_config = current_best[:-1]
    current_best_performance = current_best[-1]

    final_config = current_best_config.copy()
    final_performance = current_best_performance

    mutation_rate = 0.35

    restart_count = 0
    budget_since_best_final = 0

    history = []

    for _, row in initial_population.iterrows():
            history.append(row.tolist())

    while remaining_budget > 0:

        restart_limit = max(10, int(0.20 * remaining_budget))
        
        new_config = current_best_config.copy()

        for column in range(len(new_config)):
            if random.random() < mutation_rate:
                column_name = data.columns[column]
                new_config[column] = random.choice(data[column_name].unique())

        config_check = (data[data.columns[:-1]]== new_config).all(1)
        config_exists = data[config_check]

        if len(config_exists) > 0:
            remaining_budget -= 1
            budget_since_best_final += 1
            new_performance = config_exists.iloc[0, -1]

            history.append(new_config + [new_performance])

            if new_performance < current_best_performance:

                restart_count = 0
                current_best_config = new_config
                current_best_performance = new_performance

                if current_best_performance < final_performance:
                    final_config = current_best_config
                    final_performance = current_best_performance
                    budget_since_best_final = 0

            else:
                restart_count += 1

                if restart_count >= restart_limit:
                    new_restart_config =data.sample(1).iloc[0].tolist()
                    current_best_config = new_restart_config[:-1]
                    current_best_performance = new_restart_config[-1]
                    restart_count = 0
                    remaining_budget -= 1
                    budget_since_best_final += 1

                    history.append(new_restart_config)

    history_df = pd.DataFrame(history, columns=data.columns)
    history_df.to_csv(output_file, index=False)

    return final_config, final_performance, budget_since_best_final


def main():
    datasets_folder = "datasets" 
    output_folder = "search_results"
    os.makedirs(output_folder, exist_ok=True)
    
    budget = 100
    initial_percentage = 0.2 
    results = {}
    
    for file_name in os.listdir(datasets_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(datasets_folder, file_name)
            data = pd.read_csv(file_path)
            output_file = os.path.join(output_folder, f"{file_name.split('.')[0]}_tool.csv")
            final_config, final_performance, budget_since_best_final = evolutionary_search(data, budget, initial_percentage, output_file)
            results[file_name] = {
                "Final config": final_config,
                "Final Performance": final_performance,
                "Budget Since Best Final": budget_since_best_final
            }

    for system, result in results.items():
        print(f"System: {system}")
        print(f"  Final config:    [{', '.join(map(str, result['Final config']))}]")
        print(f"  Best Performance: {result['Final Performance']}")
        print(f"  Budget Since Best Final: {result['Budget Since Best Final']}")

if __name__ == "__main__":
    main()