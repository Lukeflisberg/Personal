import tkinter as tk

list_units = ['mm', 'cm', 'dm', 'm', 'km', 'inch', 'feet', 'yard', 'mile']

def convert_units():
    try:
        value = float(entry_value.get())
        from_unit = from_var.get()
        to_unit = to_var.get()
        
        conversion_factors = {
            'mm': 0.1,
            'cm': 1,
            'dm': 10,
            'm': 100,
            'km': 100000,
            'inch': 2.54,
            'feet': 30.48,
            'yard': 91.44,
            'mile': 160934.4
        }

        if from_unit not in conversion_factors or to_unit not in conversion_factors:
            raise ValueError("Invalid unit provided.")
        
        value_in_cm = value * conversion_factors[from_unit]
        converted_value = value_in_cm / conversion_factors[to_unit]
        result_label.config(text=f"{value} {from_unit} = {converted_value:.4f} {to_unit}")

    except Exception as e:
        result_label.config(text=f"Error: {e}")

root = tk.Tk()
root.geometry("600x300")
root.title("Metric Converter")

label = tk.Label(root, text="Enter value to convert:")
label.pack(pady=10)

entry_value = tk.Entry(root)
entry_value.pack(pady=5)

dropdown_frame = tk.Frame(root)
dropdown_frame.pack(pady=5)

from_var = tk.StringVar(value=list_units[0])
to_var = tk.StringVar(value=list_units[1])

from_dropdown = tk.OptionMenu(dropdown_frame, from_var, *list_units)
from_dropdown.pack(side=tk.LEFT, padx=10)
to_dropdown = tk.OptionMenu(dropdown_frame, to_var, *list_units)
to_dropdown.pack(side=tk.LEFT, padx=10)

convert_btn = tk.Button(root, text="Convert", command=convert_units)
convert_btn.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()