import pandas as pd
import matplotlib.pyplot as plt
import json
import os

FILE_PATH  = 'timetable.csv'
COLUMNS = [
    "Time Period Start", "Group", "Duration", "Header", "Description", "Color",
    "Before T Period", "After T Period", "Before Event", "After Event"
]

def add_timeblock(timetable, block):
    """ Add a new time block (as a dict) to the timetable DataFrame. """
    timetable.loc[len(timetable)] = block

def create_empty_timetable():
    """ Creates an empty timetable DataFrame """
    return pd.DataFrame(columns=COLUMNS)

def save_timetable(timetable, file_path=FILE_PATH):
    """ Save the timetable to a CSV file. """
    timetable.to_csv(file_path, index=False)
    print("Timetable saved.")

def load_timetable(file_path=FILE_PATH):
    """ Load the timetable from the CSV file, or create a new one if not found """
    if os.path.exists(file_path):
        timetable = pd.read_csv(file_path)
        print("Timetable loaded.")
    else:
        timetable = create_empty_timetable()
        print("Created a new timetable.")

    return timetable

def plot_timetable(timetable):
    """ Plot the timetable using matplotlib """
    if timetable.empty:
        print("No data to plot.")
        return
    
    print(timetable)
    print(timetable['Group'])
    print(timetable["Group"])
    groups = timetable["Group"].dropna().unique()
    periods = timetable["Time Period Start"].dropna().unique()
    # periods = ["T1", "T2", "T3", "T4", "T5", "T6"]
    fig, ax = plt.subplots(figsize=(10, 4))

    # Map group and period to y and x positions
    group_map = {g: i*2+1 for i, g in enumerate(groups)}
    period_map = {p: i for i, p in enumerate(periods)}

    # Draw blocks
    for _, row in timetable.iterrows():
        x = period_map[row["Time Period Start"]]
        y = group_map[row["Group"]]
        rect = plt.Rectangle(
            (x - 0.5, y - 0.5),
            row["Duration"],
            1,
            facecolor=row["Color"] if pd.notna(row["Color"]) else "gray",
            edgecolor='black'
        )
        ax.add_patch(rect)
        ax.text(
            x - 0.5 + row["Duration"]/2,
            y,
            row["Header"],
            ha='center', va='center', fontsize=9, color='black', fontweight='bold'
        )

    ax.set_xticks([period_map[p] for p in periods])
    ax.set_xticklabels(periods)
    ax.set_yticks([group_map[g] for g in groups])
    ax.set_yticklabels(groups)
    ax.set_xlim(-0.5, len(periods) - 0.5)
    ax.set_ylim(-0.5, len(groups)*2 + 0.5)
    ax.invert_yaxis()
    ax.grid(True)
    plt.title("Timetable")
    plt.tight_layout()
    plt.show()

# Example usage:
if __name__ == "__main__":
    timetable = load_timetable()

    # Example: Add a block if timetable is empty
    if timetable.empty:
        add_timeblock(timetable, [
            "T1", "G1", 2, "Research", "Do research", "blue", None, None, None, None
        ])
        add_timeblock(timetable, [
            "T2", "G2", 1, "Summary", "Write summary", "green", None, "T1", None, "Research"
        ])
        save_timetable(timetable)

    plot_timetable(timetable)