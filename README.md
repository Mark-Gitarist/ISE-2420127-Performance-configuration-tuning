# ISE Assignment

This project compares a proposed evolutionary search tool against a random search baseline on multiple software configuration datasets. Each dataset contains configuration options as columns and a final performance column. The scripts search for low-performing configurations, compare the methods over repeated runs, and generate summary tables and boxplot visualizations.

## Project Structure

```text
.
|-- baseline.py                  # Random search baseline
|-- tool.py                      # Proposed evolutionary search tool
|-- comparison.py                # Runs 30 repeated comparisons and writes summary results
|-- boxplots.py                  # Creates boxplot images from the 30-run results
|-- final_results.csv            # Final comparison summary table
|-- datasets/                    # Input datasets used by the experiments
|-- search_results/              # Generated CSV outputs from searches and repeated runs
|-- visualization_results/       # Generated boxplot PNG files
|-- requirements.pdf             # version requirements
|-- manual.pdf                   # user manual
`-- replication.pdf              # document on how to replicate the results
```

## Important Files

### `baseline.py`

Implements the random search baseline. For each CSV in `datasets/`, it randomly samples configurations up to a fixed budget of 100 valid configurations, tracks the best performance found, and writes one result file per dataset to `search_results/`.

Run it with:

```bash
python baseline.py
```

This produces files such as:

```text
search_results/7z_baseline.csv
search_results/Apache_baseline.csv
```

### `tool.py`

Implements the proposed evolutionary search approach. It starts from an initial random population, mutates the current best configuration, restarts after repeated non-improvements, and records the configurations it evaluates.

Run it with:

```bash
python tool.py
```

This produces files such as:

```text
search_results/7z_tool.csv
search_results/Apache_tool.csv
```

### `comparison.py`

Runs the main experiment. For each dataset, it runs both the proposed tool and the random baseline 30 times using a search budget of 100. It then calculates averages, improvement percentage, Mann-Whitney U test p-values, and average budget since the best configuration was found.

Run it with:

```bash
python comparison.py
```

This produces:

```text
final_results.csv
search_results/*_raw_30_runs.csv
search_results/*_tool.csv
search_results/*_baseline.csv
```

`final_results.csv` is the main summary file for reporting the experiment results.

### `boxplots.py`

Generates boxplot visualizations comparing the proposed tool against the random baseline using the raw 30-run result files.

Run it after `comparison.py`:

```bash
python boxplots.py
```

This produces PNG files in:

```text
visualization_results/
```

## Data Folders

### `datasets/`

Contains the input CSV datasets:

```text
7z.csv
Apache.csv
LLVM.csv
PostgreSQL.csv
brotli.csv
spear.csv
storm.csv
x264.csv
```

Each dataset has configuration columns followed by a final performance column.

### `search_results/`

Contains generated CSV files from the search scripts:

- `*_baseline.csv`: configurations evaluated by the random search baseline.
- `*_tool.csv`: configurations evaluated by the proposed evolutionary tool.
- `*_raw_30_runs.csv`: paired tool and baseline scores from 30 repeated runs.

### `visualization_results/`

Contains generated boxplot images for each dataset. These are created by `boxplots.py`.

## Setup

The documented environment uses Python 3.13.2 and the following package versions:

```bash
pip install pandas==2.3.3 numpy==2.2.4 scipy==1.15.2 matplotlib==3.10.1
```

If you prefer using a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas==2.3.3 numpy==2.2.4 scipy==1.15.2 matplotlib==3.10.1
```

## Recommended Workflow

From the project root, run:

```bash
python comparison.py
python boxplots.py
```

Use `comparison.py` to regenerate the main numerical results and `boxplots.py` to regenerate the visualizations.

## Outputs to Check

After running the main workflow, check:

- `final_results.csv` for the overall comparison table.
- `search_results/*_raw_30_runs.csv` for the raw repeated-run data.
- `visualization_results/*_boxplot.png` for the generated boxplots.

## Notes

- The experiment uses a search budget of 100 evaluations.
- `comparison.py` performs 30 repetitions per dataset.
- `comparison.py` sets random seeds for reproducibility.
- The scripts currently treat lower performance values as better.
