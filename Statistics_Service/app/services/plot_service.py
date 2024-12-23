import matplotlib.pyplot as plt
import os

from Statistics_Service.app.repository.event_repository import get_yearly_trends, get_monthly_trends
from Statistics_Service.app.repository.group_repository import get_groups_by_target_type


def plot_yearly_trends(output_file="static/plot/yearly_trends.png"):
    """
    Generate and save a yearly trends plot.
    """
    yearly_df = get_yearly_trends()
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure the directory exists
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_df["year"], yearly_df["event_count"], marker="o", linestyle="-", label="Yearly Trends")
    plt.title("Yearly Attack Trends")
    plt.xlabel("Year")
    plt.ylabel("Event Frequency")
    plt.grid(True)
    plt.legend()
    plt.savefig(output_file, bbox_inches="tight")
    plt.close()  # Close the figure to free memory
    return output_file


def plot_monthly_trends(year_id):
    """
    Generate and save a monthly trends plot for a specific year.
    """
    monthly_df = get_monthly_trends(year_id)
    save_dir = os.path.join("static", "plot")

    os.makedirs(os.path.dirname(save_dir), exist_ok=True)  # Ensure the directory exists
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_df["month"], monthly_df["event_count"], color="skyblue")
    plt.title(f"Monthly Attack Trends for Year {year_id}")
    plt.xlabel("Month")
    plt.ylabel("Event Frequency")
    plt.xticks(range(1, 13))
    plt.grid(axis="y")
    path = os.path.join(save_dir, f'{year_id}_monthly_trends.png')
    plt.savefig(path, bbox_inches="tight")
    plt.close()  # Close the figure to free memory


    return path




def plot_groups_by_target_type(target_type_id=None, output_folder="static/plots"):
    data = get_groups_by_target_type(target_type_id)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for target in data:
        target_type = target["target_type"]
        groups = target["groups"]

        # Extract group names and event counts
        group_names = [group["group_name"] for group in groups]
        event_counts = [group["event_count"] for group in groups]

        # Limit to top 10 groups and group others
        top_n = 10
        if len(groups) > top_n:
            group_names = group_names[:top_n] + ["Others"]
            event_counts = event_counts[:top_n] + [sum(event_counts[top_n:])]

        # Create horizontal bar chart
        plt.figure(figsize=(12, 8))
        plt.barh(group_names, event_counts, color="skyblue")
        plt.title(f"Top {top_n} Groups by Attack Counts for Target Type: {target_type}")
        plt.xlabel("Number of Attacks")
        plt.ylabel("Groups")
        plt.gca().invert_yaxis()  # Invert y-axis for better readability
        plt.tight_layout()

        # Save the plot as an image
        output_file = os.path.join(output_folder, f"{target_type_id}_groups_plot.png")

        plt.savefig(output_file)
        plt.close()  # Close the figure to free memory

        # Normalize path for cross-platform compatibility
        return os.path.normpath(output_file)

