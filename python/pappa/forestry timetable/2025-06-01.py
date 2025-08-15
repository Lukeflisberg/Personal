#Notes:
# None of the event constraints are implemented yet.
# Thinking to doing it by when the user updates the event constrains, the block will jump to a valid position. e.g. if 1 must be after 2 but 2 is after 1, then 1 will jump behind 2
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

FILE_PATH = 'timetable.csv'

# Default data
DEFAULT_GROUPS = ['G1', 'G2', 'G3']
DEFAULT_PERIODS = ['T1', 'T2', 'T3', 'T4', 'T5']

blocks = []

# Custom data
# Format: (group, start period) after period constraint, before period constraint, description, color, before entry constraint, after entry constraint, duration
CUSTOM_ENTRIES = {
    ('G1', 'T1'): {'before_p_constraint': None, 'after_p_constraint': None, 'description': 'Mathematics', 'color': 'blue', 'before_e_constraint': None, 'after_e_constraint': None, 'duration': 3},
    ('G2', 'T2'): {'before_p_constraint': None, 'after_p_constraint': None, 'description': 'Physics', 'color': 'green','before_e_constraint': None, 'after_e_constraint': None, 'duration': 2},
    ('G3', 'T3'): {'before_p_constraint': None, 'after_p_constraint': None, 'description': 'Chemistry', 'color': 'red', 'before_e_constraint': None, 'after_e_constraint': None, 'duration': 1},
    ('G1', 'T4'): {'before_p_constraint': None, 'after_p_constraint': None, 'description': 'Biology', 'color': 'yellow', 'before_e_constraint': None, 'after_e_constraint': None, 'duration': 2},
    ('G2', 'T5'): {'before_p_constraint': None, 'after_p_constraint': None, 'description': 'History', 'color': 'purple', 'before_e_constraint': None, 'after_e_constraint': None, 'duration': 1}
}

def custom_timetable(custom_entries=CUSTOM_ENTRIES, periods=DEFAULT_PERIODS, groups=DEFAULT_GROUPS):
    """ Creates a custom timetable based on predefined entries. """
    timetable = pd.DataFrame('', index=groups, columns=periods)

    for (group, start_period), entry in custom_entries.items():
        start_index = periods.index(start_period)
        timetable.at[group, periods[start_index]] = entry
        
    return timetable

def load_timetable(file_path=FILE_PATH, default_groups=DEFAULT_GROUPS, time_periods=DEFAULT_PERIODS):
    """ Initializes a timetable for groups and time periods if none is found. Otherwise it loads the existing timetable."""
    if not os.path.exists(file_path):
        print("No existing timetable found. Creating a new one.")
        return custom_timetable()
    
    timetable = pd.read_csv(file_path, index_col=0)

    for group in timetable.index:
        for period in timetable.columns:
            entry = timetable.at[group, period]
            try:
                # Try to load JSON, if fails, leave as is
                timetable.at[group, period] = json.loads(entry)
            except (TypeError, json.JSONDecodeError):
                pass

    print("Timetable loaded successfully.")
    return timetable

def save_timetable(timetable, file_path=FILE_PATH):
    """ Saves the current timetable to a file."""
    timetable_copy = timetable.copy()

    for group in timetable_copy.index:
        for period in timetable_copy.columns:
            entry = timetable_copy.at[group, period]

            if isinstance(entry, dict):
                # Convert dict to JSON string for saving
                timetable_copy.at[group, period] = json.dumps(entry)
    timetable_copy.to_csv(file_path)
    print("Timetable saved successfully.")

def draw_table(timetable, ax):
    global blocks
    # def meets_criteria():
    #     """ Checks if the current entry meets certain criteria. """
    #     _start_p = int(period.replace('T', ''))
    #     _before_p_constraint = int(entry['before_p_constraint'].replace('T', '')) if entry['before_p_constraint'] is not None else None
    #     _after_p_constraint = int(entry['after_p_constraint'].replace('T', '')) if entry['after_p_constraint'] is not None else None
    #     # Here
    #     _before_e_constraint = int(entry['before_e_constraint'].replace('T', '')) if entry['before_e_constraint'] is not None else None
    #     _after_e_constraint = int(entry['after_e_constraint'].replace('T', '')) if entry['after_e_constraint'] is not None else None

    #     if ((_after_p_constraint is None or _after_p_constraint < _start_p) and
    #         (_before_p_constraint is None or _start_p < _before_p_constraint + entry['duration'])):
    #         return True

    #     return False
    
    # def force_criteria():
    #     return None
    
    """ Updates the graph with the current timetable data. """
    for group_idx, group in enumerate(timetable.index):
        plot_row = group_idx * 2 + 1
        
        for period_idx, period in enumerate(timetable.columns):
            entry = timetable.at[group, period]
            
            if isinstance(entry, dict):
                # Draw a filled rectangle 
                rect = plt.Rectangle(
                    (period_idx - 0.5, plot_row - 0.5), 
                    entry['duration'], 
                    1, 
                    facecolor=entry['color'], 
                    edgecolor='black', 
                    label=entry['description']
                    )
                
                ax.add_patch(rect)

                ax.text(
                    period_idx - 0.5 + entry['duration']/2,
                    plot_row,
                    entry['description'],
                    ha='center', va='center', fontsize=9, color='black', fontweight='bold'
                )         

                blocks.append({
                    'patch': rect,
                    'group': group,
                    'period': period,
                    'duration': entry['duration'],
                    'description': entry['description'],
                    'color': entry['color'],
                    'before_p_constraint': entry['before_p_constraint'],
                    'after_p_constraint': entry['after_p_constraint'],
                    'before_e_constraint': entry['before_e_constraint'],
                    'after_e_constraint': entry['after_e_constraint']
                })          

def update_table():
    """ Updates the timetable entries based on user input. """
    return None

def snap_to_grid():
    """ Snaps the timetable entries to a grid based on the defined periods. """
    return None

def update_timetable():
    return None

# Initialize or load the timetable
timetable = load_timetable()

print('*'*60)
print(timetable)
print('*'*60)

# Intialize the graph
x = timetable.columns
y = timetable.index

num_groups = len(y)
num_periods = len(x)
plot_rows = num_groups * 2 + 1

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(10, 4))    

# Create the table grid
ax.set_xticks(range(num_periods))
ax.set_xticklabels(x)
ax.set_yticks([i*2 + 1 for i in range(num_groups)])
ax.set_yticklabels(y)

# Turn on the grid lines
ax.set_xlim(-0.5, num_periods - 0.5)
ax.set_ylim(-0.5, plot_rows - 1.5)
ax.invert_yaxis() 
# ax.grid(True)
ax.tick_params(axis='both', which='both', length=0)  # Hide ticks

# Draw timetable entries before showing the plot
draw_table(timetable, ax)

# Event handling
def on_click(event):
    """ Handles click events on the plot. """
    if event.inaxes != ax:
        return
    
    for block in blocks:
        contains, _ = block['patch'].contains(event)

        if contains:
            print(f"Clicked Block Info:")
            print(f"Group: {block['group']}")
            print(f"Period: {block['period']}")
            print(f"Duration: {block['duration']}")
            print(f"Description: {block['description']}")
            print(f"Color: {block['color']}")
            print(f"Before Period Constraint: {block['before_p_constraint']}")
            print(f"After Period Constraint: {block['after_p_constraint']}")
            print(f"Before Entry Constraint: {block['before_e_constraint']}")
            print(f"After Entry Constraint: {block['after_e_constraint']}")
            break

# Connect the click event to the handler
fig.canvas.mpl_connect('button_press_event', on_click)

# Show the plot
plt.title("Timetable")
plt.tight_layout()
plt.show()

save_timetable(timetable)