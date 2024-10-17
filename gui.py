import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import time
import random
import os


class CosmetologyClockInSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Cosmetology Business Management")
        self.root.geometry("1000x700")
        self.root.config(bg='#F0F0F5')

        self.username = tk.StringVar()
        self.pin = tk.StringVar()
        self.start_time = None
        self.total_hours = 0
        self.dark_mode = False

        # Create side navigation bar
        self.create_side_nav()

        # Create frames for different sections
        self.log_in_frame = ttk.Frame(self.root)
        self.clock_in_frame = ttk.Frame(self.root)
        self.admin_frame = ttk.Frame(self.root)
        self.reports_frame = ttk.Frame(self.root)

        # Initially show the clock-in frame
        self.clock_in_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.admin_frame.pack_forget()
        self.reports_frame.pack_forget()
        self.log_in_frame.pack_forget()

        # Create screens for each section
        self.create_clock_in_screen()
        self.create_admin_panel_screen()
        self.create_reports_screen()
        self.create_log_in_screen()

    def create_side_nav(self):
        """Creates a sidebar for navigation"""
        nav_frame = tk.Frame(self.root, bg="#333", width=200)
        nav_frame.pack(side="left", fill="y")

        # Clock in Button
        clockin_button = tk.Button(nav_frame, text="Clock In", command=self.show_clock_in_frame,
                                   bg="#444", fg="white", font=("Roboto", 12), bd=0, height=2)
        clockin_button.pack(fill="x", pady=(50, 5))

        # Admin Panel Button
        admin_button = tk.Button(nav_frame, text="Admin Panel", command=self.show_admin_frame,
                                 bg="#444", fg="white", font=("Roboto", 12), bd=0, height=2)
        admin_button.pack(fill="x", pady=5)

    def show_clock_in_frame(self):
        """Show the clock-in frame and hide others."""
        self.clock_in_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.admin_frame.pack_forget()
        self.reports_frame.pack_forget()
        self.log_in_frame.pack_forget()

    def show_log_in_frame(self):
        """Show the clock-in frame and hide others."""
        self.log_in_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.clock_in_frame.pack_forget()
        self.admin_frame.pack_forget()
        self.reports_frame.pack_forget()

    def show_admin_frame(self):
        """Show the admin frame and hide others."""
        self.admin_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.clock_in_frame.pack_forget()
        self.reports_frame.pack_forget()
        self.log_in_frame.pack_forget()

    def show_reports_frame(self):
        """Show the reports frame and hide others."""
        self.reports_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.clock_in_frame.pack_forget()
        self.admin_frame.pack_forget()
        self.log_in_frame.pack_forget()

    def create_clock_in_screen(self):
        # Title
        title_label = ttk.Label(self.clock_in_frame, text="Log In",
                                font=("Roboto", 20, "bold"), foreground="#00796B")
        title_label.pack(pady=20)

        # Username and PIN input
        self.create_floating_entry(self.clock_in_frame, "Username", self.username)
        self.create_floating_entry(self.clock_in_frame, "PIN", self.pin, show="*")

        self.log_in_button = tk.Button(self.clock_in_frame, text="Continue", command=self.show_log_in_frame,
                                         bg="#00796B", fg="white", font=("Roboto", 12, "bold"),
                                         relief="flat", bd=0, height=2, width=20, cursor="hand2")
        self.log_in_button.pack(anchor="center", pady=20)

    def create_floating_entry(self, parent, placeholder, text_var, show=None):
        """Creates an entry with a floating label effect."""
        entry_frame = ttk.Frame(parent)
        entry_frame.pack(anchor="center", pady=(10, 15))

        entry_label = ttk.Label(entry_frame, text=placeholder, font=("Roboto", 12))
        entry_label.grid(row=0, column=0, sticky="w")

        entry = ttk.Entry(entry_frame, textvariable=text_var, font=("Roboto", 12), width=30, show=show)
        entry.grid(row=1, column=0)
        return entry

    def create_admin_panel_screen(self):
        # Admin title
        admin_title = ttk.Label(self.admin_frame, text="Admin Panel",
                                font=("Roboto", 20, "bold"), foreground="#00796B")
        admin_title.pack(pady=20)

        # Admin table
        columns = ('Username', 'Clock-In Time', 'Clock-Out Time', 'Hours Worked')
        self.tree = ttk.Treeview(self.admin_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20)

        # Insert mock data
        self.tree.insert("", "end", values=("johndoe", "9:00 AM", "5:00 PM", 8))
        self.tree.insert("", "end", values=("janedoe", "8:00 AM", "4:00 PM", 8))

        # Add buttons for Edit Employee and Reports
        edit_button = tk.Button(self.admin_frame, text="Edit Employee", command=self.open_edit_employee_window,
                                bg="#00796B", fg="white", font=("Roboto", 12, "bold"), relief="flat", bd=0)
        edit_button.pack(anchor="center", pady=10)

        report_button = tk.Button(self.admin_frame, text="Reports", command=self.open_reports_window,
                                  bg="#00796B", fg="white", font=("Roboto", 12, "bold"), relief="flat", bd=0)
        report_button.pack(anchor="center", pady=10)

    def create_reports_screen(self):
        # Title for reports
        reports_title = ttk.Label(self.reports_frame, text="Reports",
                                  font=("Roboto", 20, "bold"), foreground="#00796B")
        reports_title.pack(pady=20)

        # Placeholder for future report content
        report_label = ttk.Label(self.reports_frame, text="Reports will be displayed here.", font=("Roboto", 12))
        report_label.pack(pady=20)

    def create_log_in_screen(self):
        title_label = ttk.Label(self.log_in_frame, text=f"{self.username.get()} is logged in",
                                font=("Roboto", 20, "bold"), foreground="#00796B")
        title_label.pack(pady=20)
        # Clock in/out button
        self.clock_in_button = tk.Button(self.log_in_frame, text="Clock in", command=self.clock_in,
                                         bg="#00796B", fg="white", font=("Roboto", 12, "bold"),
                                         relief="flat", bd=0, height=2, width=20, cursor="hand2")
        self.clock_in_button.pack(anchor="center", pady=20)



        # Total hours worked
        self.total_hours_label = ttk.Label(self.log_in_frame, text="Total hours: 0", font=("Roboto", 12))
        self.total_hours_label.pack(anchor="center", pady=10)

    def open_edit_employee_window(self):
        """Opens a new window to edit employee details."""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Employee")
        edit_window.geometry("400x300")

        # Example in-line editable employee table (simple example)
        edit_label = ttk.Label(edit_window, text="Edit employee data here.")
        edit_label.pack(pady=20)

    def open_reports_window(self):
        """Opens a new window to view and print reports."""
        # if self.logged_in_user.is _admin()== False:
            # return with an error message

        report_window = tk.Toplevel(self.root)
        report_window.title("Reports")
        report_window.geometry("500x400")

        # Range of dates and employee selection
        range_label = ttk.Label(report_window, text="Specify Date Range", font=("Roboto", 12))
        range_label.pack(pady=10)
        start_date = tk.Entry(report_window, width=20)
        start_date.pack(pady=5)
        end_date = tk.Entry(report_window, width=20)
        end_date.pack(pady=5)

        employee_label = ttk.Label(report_window, text="Select Employee", font=("Roboto", 12))
        employee_label.pack(pady=10)
        employee_combobox = ttk.Combobox(report_window, values=["All Employees", "johndoe", "janedoe"])
        employee_combobox.pack(pady=5)

        # Print button
        print_button = tk.Button(report_window, text="Print Report", command=self.print_report,
                                 bg="#00796B", fg="white", font=("Roboto", 12, "bold"), relief="flat", bd=0)
        print_button.pack(pady=20)

    def print_report(self):
        """Sends the report to the default printer."""
        # Print functionality
        report_text = "This is a sample report. \nTitle: Business Report \nDate Range: xx/xx/xxxx - xx/xx/xxxx \nAdmin: Admin Name"

        # Use os module to open the default print dialog (platform-specific)
        if os.name == "nt":  # For Windows
            file_name = "report.txt"
            with open(file_name, "w") as f:
                f.write(report_text)
            os.startfile(file_name, "print")
        else:
            messagebox.showinfo("Print Report", "Printing is not supported on this OS.")

    def clock_in(self):
        """Handles the clock-in process."""
        username = self.username.get()
        pin = self.pin.get()

        if username and pin:
            if self.start_time is None:  # Not clocked in
                self.start_time = time.time()  # Set start time
                self.clock_in_button.config(text="Clock Out")
                messagebox.showinfo("Clock In", "You are now clocked in.")
            else:  # Already clocked in
                clock_out_time = time.time()
                hours_worked = (clock_out_time - self.start_time) / 3600  # Convert seconds to hours
                self.total_hours += hours_worked
                self.total_hours_label.config(text=f"Total hours: {self.total_hours:.2f}")
                self.start_time = None  # Reset start time
                self.clock_in_button.config(text="Clock In")
                messagebox.showinfo("Clock Out", f"You clocked out. Total hours worked: {hours_worked:.2f}.")

        else:
            messagebox.showwarning("Input Error", "Please enter both username and PIN.")

        # log user out after doing anything to the clock


# Create main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = CosmetologyClockInSystem(root)
    root.mainloop()
