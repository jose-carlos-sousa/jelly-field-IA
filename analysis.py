import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil

if os.path.exists("analysis"):
    shutil.rmtree("analysis")
os.makedirs("analysis")

df = pd.read_csv("test_results.csv")

# Create a copy instead of a view to avoid SettingWithCopyWarning
df_clean = df.dropna(subset=["Time", "Memory", "Score", "Steps"]).copy()


df_clean.loc[:, "Memory"] = df_clean["Memory"].astype(float) / (1024 * 1024)

df_clean.loc[:, "Level"] = df_clean["Level"].str.replace("./levels/", "", regex=False).str.replace(".txt", "", regex=False)

df_clean = df_clean.copy()  

a_star_mask = df_clean["Algorithm"].str.contains("a_star", na=False)

def process_a_star(row):
    if "a_star" in str(row["Algorithm"]):
        weight = float(row.get("Weight", 1.0))
        if weight == 1.0:
            return row["Algorithm"] 
        elif weight == 1.5:

            return "weighted_" + row["Algorithm"]
        else:
            return None
    return row["Algorithm"]
df_clean["Algorithm"] = df_clean.apply(process_a_star, axis=1)
df_clean = df_clean[df_clean["Algorithm"].notna()]
print(df_clean)
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
        
        if metric == "Steps":
            import matplotlib.ticker as ticker
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            
        # Position legend in top right corner
        ax.legend(title="Level", loc='upper right')
        
        plt.tight_layout()
        plt.savefig(os.path.join("analysis", f"{group_name.lower()}_{base_filename}"))
        plt.close()

plot_metrics("Time", "Execution Time (s)", "time.png")
plot_metrics("Memory", "Memory Usage (MB)", "memory.png")
plot_metrics("Score", "Score", "score.png")
plot_metrics("Steps", "Steps Taken", "steps.png")
