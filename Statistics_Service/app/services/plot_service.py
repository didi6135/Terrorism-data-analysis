import matplotlib.pyplot as plt

def plot_event_trends_cleaned(yearly_df, monthly_df, year=None):


    plt.figure(figsize=(10, 6))
    plt.plot(yearly_df["year"], yearly_df["event_count"], marker="o", linestyle="-", label="Yearly Trends")
    plt.title("Yearly Attack Trends")
    plt.xlabel("Year")
    plt.ylabel("Event Frequency")
    plt.grid(True)
    plt.legend()
    plt.show()

    if not monthly_df.empty:
        plt.figure(figsize=(10, 6))
        plt.bar(monthly_df["month"], monthly_df["event_count"], color="skyblue")
        plt.title(f"Monthly Attack Trends for Year {year}")
        plt.xlabel("Month")
        plt.ylabel("Event Frequency")
        plt.xticks(range(1, 13))
        plt.grid(axis="y")
        plt.show()


def plot_yearly_trends(yearly_df):

    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(yearly_df["year"], yearly_df["event_count"], marker="o", linestyle="-", label="Yearly Trends")
    plt.title("Yearly Attack Trends")
    plt.xlabel("Year")
    plt.ylabel("Event Frequency")
    plt.grid(True)
    plt.legend()
    plt.show()



def plot_monthly_trends(monthly_df, year):


    plt.figure(figsize=(10, 6))
    plt.bar(monthly_df["month"], monthly_df["event_count"], color="skyblue")
    plt.title(f"Monthly Attack Trends for Year {year}")
    plt.xlabel("Month")
    plt.ylabel("Event Frequency")
    plt.xticks(range(1, 13))
    plt.grid(axis="y")
    plt.show()
