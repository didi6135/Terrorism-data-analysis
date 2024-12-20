import matplotlib.pyplot as plt
import os

def plot_yearly_trends(yearly_df, output_file="static/yearly_trends.png"):
    """
    Generate and save a yearly trends plot.
    """
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


def plot_monthly_trends(monthly_df, year, output_file="static/monthly_trends.png"):
    """
    Generate and save a monthly trends plot for a specific year.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_df["month"], monthly_df["event_count"], color="skyblue")
    plt.title(f"Monthly Attack Trends for Year {year}")
    plt.xlabel("Month")
    plt.ylabel("Event Frequency")
    plt.xticks(range(1, 13))
    plt.grid(axis="y")
    plt.savefig(output_file, bbox_inches="tight")
    plt.close()  # Close the figure to free memory
    return output_file
