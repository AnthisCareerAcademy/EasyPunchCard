import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Admin Panel Layout")
root.geometry("600x400")  # Set initial window size

# Configure the main frame with a grid layout
main_frame = ttk.Frame(root)
main_frame.pack()

# Dropdown at the top
dropdown = ttk.Combobox(main_frame, values=["Option 1", "Option 2", "Option 3"])
dropdown.set("Select")  # Prepopulate with "Select"
dropdown.grid(row=0, column=0, columnspan=2, sticky="new", pady=(0, 20))
# main_frame.columnconfigure(0, weight=1)

# Left Sidebar for Buttons
sidebar = ttk.Frame(main_frame)
sidebar.grid(row=1, column=0, sticky="nsw", padx=(0, 20))
sidebar.columnconfigure(0, weight=1)

reset_button = ttk.Button(sidebar, text="Reset")
remove_button = ttk.Button(sidebar, text="Remove")
admin_status_button = ttk.Button(sidebar, text="Admin Status")
add_button = ttk.Button(main_frame, text="Add")

reset_button.grid(row=0, column=0, sticky="ew", pady=5)
remove_button.grid(row=1, column=0, sticky="ew", pady=5)
admin_status_button.grid(row=2, column=0, sticky="ew", pady=5)
add_button.grid(row=3, column=0, sticky="ew", pady=5)

# Central area for text boxes
center_frame = ttk.Frame(main_frame)
center_frame.grid(row=1, column=1, sticky="nsew")
main_frame.columnconfigure(1, weight=3)  # Central area expands more

# Text boxes for PIN and Username
pin_entry = ttk.Entry(center_frame)
pin_entry.insert(0, "PIN")  # Prepopulate with "PIN"
pin_entry.grid(row=0, column=0, sticky="ew", padx=(0, 20), pady=5)

username_entry = ttk.Entry(center_frame)
username_entry.insert(0, "Username")  # Prepopulate with "Username"
username_entry.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=5)

# Run the application
root.mainloop()
