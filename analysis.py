import pandas as pd
import matplotlib.pyplot as plt
import warnings
import os
import shutil

# Create analysis folder (delete if exists)
if os.path.exists("analysis"):
    shutil.rmtree("analysis")
os.makedirs("analysis")

# Optional: Suppress Axes3D warning if not using 3D plots
warnings.filterwarnings("ignore", message=".*Unable to import Axes3D.*")

# Load the CSV file
df = pd.read_csv("test_results.csv")

# Drop rows with missing values for key metrics
df_clean = df.dropna(subset=["Time", "Memory", "Score", "Steps"])

# Simplify level names (remove path and extension)
df_clean["Level"] = df_clean["Level"].str.replace("./levels/", "", regex=False).str.replace(".txt", "", regex=False)


# Define algorithm categories
uninformed_algorithms = ["depth_first", "breadth_first", "iterative_deepening"]
df_uninformed = df_clean[df_clean["Algorithm"].isin(uninformed_algorithms)]
df_informed = df_clean[~df_clean["Algorithm"].isin(uninformed_algorithms)]
def plot_metrics(metric: str, ylabel: str, base_filename: str):
    for df_group, group_name, cmap in [
        (df_uninformed, "Uninformed", "Blues"),
        (df_informed, "Informed", "Reds")
    ]:
        pivot = df_group.pivot_table(
            index="Algorithm", 
            columns="Level", 
            values=metric,
            aggfunc="mean"
        )
        ax = pivot.plot(kind="bar", colormap=cmap, figsize=(12, 8))
        ax.set_title(f"Average {ylabel} by {group_name} Algorithm and Level")
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Algorithm")
        ax.grid(axis='y', linestyle="--", alpha=0.7)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        
        # Set integer y-ticks for Steps metric
        if metric == "Steps":
            import matplotlib.ticker as ticker
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            
        ax.legend(title="Level")
        plt.tight_layout()
        plt.savefig(os.path.join("analysis", f"{group_name.lower()}_{base_filename}"))
        plt.close()

# Example usage:
plot_metrics("Time", "Execution Time (ms)", "time.png")
plot_metrics("Memory", "Memory Usage (MB)", "memory.png")
plot_metrics("Score", "Score", "score.png")
plot_metrics("Steps", "Steps Taken", "steps.png")
