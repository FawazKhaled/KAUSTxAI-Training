# Rung 1: Exploratory Data Analysis with pandas

Rung 1 explores the Students Performance in Exams dataset using pandas, Matplotlib, and Seaborn. The notebook walks through loading and validating data, creating features, summarizing and comparing scores, and visualizing distributions and correlations.

## Learning goals

- Load a local CSV with `pathlib` and pandas.
- Inspect a dataset's structure, data types, categories, and descriptive statistics.
- Check for missing values, duplicate records, whitespace, and invalid score ranges.
- Create and validate row-level features with pandas.
- Compare score summaries across categorical groups without making causal claims.
- Visualize distributions, potential outliers, and pairwise correlations.

## Dataset and setup

The analysis uses the Students Performance in Exams dataset published on Kaggle:

[Students Performance in Exams dataset](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)

The CSV is not included in this repository because its redistribution permission has not been independently verified. Download it from Kaggle and follow the instructions in [Data/README.md](Data/README.md). The expected local file is:

```text
Rung_1/Data/StudentsPerformance.csv
```

From the repository root, prepare the environment and install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r Rung_1/requirements.txt
```

If PowerShell does not allow the activation script to run, use the Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r Rung_1/requirements.txt
```

Open the notebook from the `Rung_1` directory so its relative dataset and image paths resolve correctly:

```powershell
Set-Location Rung_1
jupyter notebook eda.ipynb
```

Run the notebook cells from top to bottom. It validates the expected dataset columns and reports a clear error if the local CSV is missing or has a different schema. The plots are saved in `Rung_1/Images/`.

## Analysis

The notebook includes:

1. Dataset loading, structure inspection, and data-quality checks.
2. An equal-weight average score feature, verified against an independent sum-and-divide calculation.
3. A configurable pass-status feature. The current threshold is 60 in every subject and is an assumption for this exercise, not an official rule.
4. Descriptive statistics and ranking by average score.
5. Histograms and box plots for score distributions, with potential outliers identified by the 1.5-times-IQR rule.
6. Group score summaries across the categories provided by the dataset.
7. A Pearson correlation matrix for the three original exam scores.
8. Findings and limitations, including why group differences and correlations do not establish causality.

## Findings from the dataset

The locally analyzed file contains 1,000 records and eight original columns. The checks found no missing values, exact duplicate rows, invalid scores outside 0 to 100, or leading and trailing whitespace in categorical values.

- The mean mathematics, reading, and writing scores were 66.09, 69.17, and 68.05, respectively.
- The mean of the equal-weight average score was 67.77.
- With the project's assumed threshold of 60 in all three subjects, 603 students (60.3%) passed.
- The strongest pairwise score correlation was between reading and writing (Pearson's *r* = 0.955).

These are descriptive results for this dataset. They are not causal findings, and they should not be generalized beyond the data without further evidence.

## Generated plots

- [Score distributions](Images/score_distributions.png)
- [Score box plots](Images/score_boxplots.png)
- [Average scores by group](Images/average_scores_by_group.png)
- [Score correlations](Images/score_correlations.png)

The CSV remains the work of its original creator or publisher. This project does not claim ownership of the dataset.
