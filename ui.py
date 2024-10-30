import tkinter as tk
from os.path import expanduser
from tkinter import ttk
from tkinter import messagebox
import time
import os
from turtledemo.penrose import start

from User import User
from better_ui.show_functions import show_clock_in_frame


class GUI:
    def __init__(self):

        # Configuring the root screen
        self.root: tk.Tk = tk.Tk()
        self.root.title("Cosmetology Clock-In System")
        self.root.geometry("1000x700")
        self.root.config(bg="#F0F0F5")

        # Creates user credential variables
        self.username: tk.StringVar = tk.StringVar()
        self.pin: tk.StringVar = tk.StringVar()

        # Create a variable for the current User
        self.current_user: User | None = None

        # Create frames for different sections
        self.nav_frame: ttk.Frame = ttk.Frame(self.root)

        self.log_in_frame: ttk.Frame = ttk.Frame(self.root)
        self.clock_in_frame: ttk.Frame = ttk.Frame(self.root)
        self.admin_frame: ttk.Frame = ttk.Frame(self.root)
        self.reports_frame: ttk.Frame = ttk.Frame(self.root)

        # A list of the current frames
        self.frames: list[str: ttk.Frame] = {
            "log_in_frame": self.log_in_frame,
            "clock_in_frame": self.clock_in_frame,
            "admin_frame": self.admin_frame,
            "reports_frame": self.reports_frame
        }

        # Start The Program with the log in screen
        self.create_log_in_screen()

        # Initially show the log_in frame
        self.log_in_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Frame creating methods -------------------------------------------------------
    @ staticmethod
    def create_floating_entry(
            parent: ttk.Frame,
            placeholder: str,
            text_var: tk.StringVar,
            show: str=None):
        """
        Creates an entry with a floating label effect.
        :param parent: Parent frame widget where the entry should be placed on
        :param placeholder: Text of the Label above the Entry
        :param text_var: `Variable in which the input will be stored
        :param show: Auto-replaces characters to the specified character (If specified)
        :return ttk.Entry:
        """

        # Creates and configures the entry frame -------
        entry_frame: ttk.Frame = ttk.Frame(parent)
        entry_frame.pack(anchor="center", pady=(10,15))
        # ----------------------------------------------

        # Creates and configures placeholder label -----------------------------------------
        entry_label: ttk.Label = ttk.Label(entry_frame, text=placeholder, font=("Roboto", 12))
        entry_label.grid(row=0, column=0, sticky="w")
        # --------------------------------------------------------------------------------------

        # Creates configures and returns the Entry --
        entry: ttk.Entry = ttk.Entry(
            entry_frame,
            textvariable=text_var,
            font=("Roboto", 12),
            width=30,
            show=show
        )

        entry.grid(row=1, column=0)
        # -------------------------------------------

        return entry


    def create_log_in_screen(self):
        """
        Creates and configures the necessary elements
        for the log_in screen
        :return None:
        """

        # Title -------------------------------
        title_label: ttk.Label = ttk.Label(
            self.log_in_frame,
            text="Welcome",
            font=("Roboto", 20, "bold"),
            foreground="#00796B"
        )

        title_label.pack()
        # --------------------------------------

        # Username and PIN input ---------------
        self.create_floating_entry(  # USERNAME
            parent=self.log_in_frame,
            placeholder="USERNAME",
            text_var=self.username
        )

        self.create_floating_entry(  # PIN
            parent=self.log_in_frame,
            placeholder="PIN",
            text_var=self.pin,
            show="*"
        )
        # --------------------------------------

        # Creates and configures the log-in button ---------------------------------------------------------------------
        log_in_button: tk.Button = tk.Button(
            self.log_in_frame,
            text="Log-In",
            command=self.log_in,
            bg="#00796B",
            fg="white",
            font=("Roboto", 12, "bold"),
            relief="flat",
            bd=0,
            height=2,
            width=20,
            cursor="hand2")

        log_in_button.pack(anchor="center", pady=20)
        # --------------------------------------------------------------------------------------------------------------

    def create_clock_in_screen(self):
        """
        Creates and configures the necessary elements
        for the clock_in screen
        :return None:
        """

        # Title ------------------------------------------
        title_label: ttk.Label = ttk.Label(
            self.clock_in_frame,
            text=f"{self.username.get().title()} is logged in",
            font=("Roboto", 20, "bold"),
            foreground="#00796B"
        )

        title_label.pack(pady=20)
        # ------------------------------------------------

        # Clock in button
        clock_in_button: tk.Button = tk.Button(
            self.clock_in_frame,
            text="Clock In",
            command=lambda: self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen),
            bg="#00796B",
            fg="white",
            font=("Roboto", 12, "bold"),
            relief="flat",
            bd=0,
            height=2,
            width=20,
            cursor="hand2"
        )

        clock_in_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

    def create_admin_panel_screen(self):
        """
        Creates and configures the elements
        in the admin panel screen
        :return None:
        """

        # Admin Title ----------------------------------
        title_label: ttk.Label = ttk.Label(
            self.admin_frame,
            text="Admin Panel",
            font=("Roboto", 20, "bold"),
            foreground="#00796B"
        )

        title_label.pack()
        # ----------------------------------------------

        # Set the columns and initializing the employees table ---------------------------------------------
        columns: tuple[str, str, str, str, str, str] = (
            "Student ID", "Username", "Admin Status", "Total Minutes", "Start Time", "Working")

        employees_table: ttk.Treeview = ttk.Treeview(self.admin_frame, columns=columns, show="headings")

        for column in columns:
            employees_table.heading(column, text=column)
        employees_table.pack()
        # --------------------------------------------------------------------------------------------------

        # Insert Employees below -----------------------------------------------------------------------
        employees_table.insert("", "end", values=("johndoe", "9:00 AM", "5:00 PM", 8))
        employees_table.insert("", "end", values=("john", "8:00 AM", "4:00 PM", 8))
        # ----------------------------------------------------------------------------------------------

        # Configure and pack the edit button ------------
        edit_button: tk.Button = tk.Button(
            self.admin_frame,
            text="Edit Employee",
            command=self.open_edit_employee_window,
            bg="#00796B",
            fg="white",
            font=("Roboto", 12, "bold"),
            relief="flat",
            bd=0
        )

        edit_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

        # Configure and pack the reports button ------------
        report_button: tk.Button = tk.Button(
            self.admin_frame,
            text="Reports",
            command=self.open_reports_window,
            bg="#00796B",
            fg="white",
            font=("Roboto", 12, "bold"),
            relief="flat",
            bd=0
        )

        report_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

    # -------------------------------------------------------------------------------

    # Complementary Methods -----------------------------------------------
    def show(self, frame: ttk.Frame, name: str, frame_builder):
        """
        Shows a specific frame and hides the rest
        :param frame: The frame object to be shown
        :param name: The name of the frame to be shown
        :param frame_builder: Method that will recreate the frame
        :return None:
        """

        self.reset(frame, frame_builder)

        # Pack the screen needed to be shown
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Hides every other frame not being used
        for frame_name, frame_object in self.frames.items():
            if frame_name == name:
                continue

            frame_object.pack_forget()

    @staticmethod
    def reset(frame: ttk.Frame, frame_builder):
        """
        Erases everything from the specified frame
        :param frame:
        :param frame_builder: Method that will re-create the frame
        :return None:
        """

        for widget in frame.winfo_children():
            widget.destroy()

        # Rebuilds the frame
        frame_builder()
    # ---------------------------------------------------------------------

    # Mock Methods ----------------------------------------
    def clock_in(self):
        pass
    # ---------------------------------------------------------------------

    # Admin methods --------------------------------------
    def open_edit_employee_window(self):
        """
        Opens a new window to edit employee details
        :return None:
        """

        # Creates a pop-up window to edit employee's details
        edit_window: tk.Toplevel = tk.Toplevel(self.admin_frame)
        edit_window.title("Edit Employee")
        edit_window.geometry("400x300")

    def open_reports_window(self):
        """
        Opens a new window to view and print reports
        :return None:
        """

        # Create the pop-up window ------------------------------------
        report_window: tk.Toplevel = tk.Toplevel(self.admin_frame)
        report_window.title("Reports")
        report_window.geometry("500x400")
        # --------------------------------------------------------------

        # Range of dates ----------------------------------------------
        range_label: ttk.Label = ttk.Label(
            report_window,
            text="Specify Date Range",
            font=("Roboto", 12)
        )

        range_label.pack(pady=10)

        start_date: tk.Entry = tk.Entry(report_window, width=20)
        start_date.pack(pady=5)

        end_date: tk.Entry = tk.Entry(report_window, width=20)
        end_date.pack(pady=5)
        # ---------------------------------------------------------------

        # Employee selection --------------------------------------
        employee_label: ttk.Label = ttk.Label(
            report_window,
            text="Select Employee",
            font=("Roboto", 12))

        employee_label.pack(pady=10)

        employee_combobox: ttk.Combobox = ttk.Combobox(
            report_window,
            values=["All Employees", "johndoe", "Luis"])

        employee_combobox.pack(pady=5)
        # -----------------------------------------------------------

        # Print button
        print_button: tk.Button = tk.Button(
            report_window,
            text="Print Report",
            command=self.print_report,
            bg="#00796B",
            fg="white", font=("Roboto", 12, "bold"),
            relief="flat", bd=0)

        print_button.pack(pady=20)

    def print_report(self):
        pass
    # ----------------------------------------------------

    # Backend functions
    def log_in(self):
        """
        Checks if the user has the right credentials to log in
        :return:
        """

        # Check if the username and PIN fields are fulfilled
        if self.username.get() and self.pin.get():
            self.show(self.clock_in_frame, "clock_in_frame", self.create_clock_in_screen)
        else:
            self.username.set("")
            self.pin.set("")
            self.show(self.log_in_frame, "log_in_frame", self.create_log_in_screen)
            messagebox.showwarning("Input Error", "Please enter both username and PIN")

gui = GUI()
gui.root.mainloop()