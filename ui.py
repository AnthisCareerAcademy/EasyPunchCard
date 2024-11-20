import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import Calendar
from datetime import datetime

from User import User

class GUI:
    def __init__(self):

        # Configuring the root screen
        self.root: tk.Tk = tk.Tk()
        self.root.title("Cosmetology Clock-In System")
        self.root.geometry("1000x700")
        self.root.config(bg="#F0F0F5")

        self.root.attributes("-fullscreen", True)  # Enable full-screen mode

        # Creates user credential variables
        # self.username: tk.StringVar = tk.StringVar()
        self.pin: tk.StringVar = tk.StringVar()

        # Create a variable for the current User
        self.current_user: User | None = None

        self.admin_status: tk.IntVar = tk.IntVar(value=0)

        # Create frames for different sections
        self.nav_frame: ttk.Frame = ttk.Frame(self.root)

        self.log_in_frame: ttk.Frame = ttk.Frame(self.root)
        self.clock_in_frame: ttk.Frame = ttk.Frame(self.root)
        self.admin_frame: ttk.Frame = ttk.Frame(self.root)
        self.reports_frame: ttk.Frame = ttk.Frame(self.root)
        self.employee_management_frame: ttk.Frame = ttk.Frame(self.root, borderwidth=5, relief="solid")

        # Admin Windows
        self.select_employee_frame: None | ttk.Frame = None
        self.edit_employee_frame: None | ttk.Frame = None
        self.add_employee_frame: None | ttk.Frame = ttk.Frame(self.root)

        # A list of the current frames
        self.frames: list[str: ttk.Frame] = {
            "log_in_frame": self.log_in_frame,
            "clock_in_frame": self.clock_in_frame,
            "admin_frame": self.admin_frame,
            "reports_frame": self.reports_frame,
            "employee_management_frame": self.employee_management_frame,
            "add_employee_frame": self.add_employee_frame,
        }

        # Start The Program with the log in screen
        self.create_log_in_screen()

        # Initially show the log_in frame
        self.log_in_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Frame creating methods ---------------------------------------------------
    @ staticmethod
    def create_floating_entry(
            parent: ttk.Frame,
            placeholder: str,
            text_var: tk.StringVar,
            show: str = None):
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
            font=("Roboto", 40),
            width=16,
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
            text="Clock-In System",
            font=("Roboto", 60, "bold"),
            foreground="#00796B"
        )

        title_label.pack()
        # --------------------------------------

        # Username and PIN input ---------------
        # self.create_floating_entry(  # USERNAME
        #     parent=self.log_in_frame,
        #     placeholder="USERNAME",
        #     text_var=self.username
        # )

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
            font=("Roboto", 36, "bold"),
            relief="flat",
            bd=0,
            # height=3,
            # width=20,
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
        username = self.current_user.access.get_data_all_users("username").title()
        title_label: ttk.Label = ttk.Label(
            self.clock_in_frame,
            text=f"{username} is logged in",
            font=("Roboto", 60, "bold"),
            foreground="#00796B"
        )

        title_label.pack(pady=20)
        # ------------------------------------------------

        # Clock in button
        clock_in_button: tk.Button = tk.Button(
            self.clock_in_frame,
            text="Clock In",
            command=self.clock_in,
            bg="#00796B",
            fg="white",
            font=("Roboto", 60, "bold"),
            relief="flat",
            bd=0,
            height=2,
            width=15,
            cursor="hand2"
        )

        clock_in_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

        # Log out button -----------------------------------------
        log_out_button: tk.Button = tk.Button(
            self.clock_in_frame,
            text="Log out",
            command=self.log_out,
            bg="#8B0000",
            fg="white",
            font=("Roboto", 40, "bold"),
            relief="flat",
            bd=0,
            height=2,
            width=10,
            cursor="hand2")

        log_out_button.pack(pady=10)
        # ----------------------------------------------------------

        # Gets the user hours and writes them in a label --------------------------------------------
        total_minutes: int = self.current_user.access.get_data_all_users("total_minutes")
        hours: int = total_minutes // 60
        minutes: float = total_minutes % 60
        hours_label: ttk.Label = ttk.Label(
            self.clock_in_frame,
            text=f"Total Time: {hours}h{minutes}m",
            font=("Roboto", 80, "bold"),
            foreground="#000000"
        )
        hours_label.pack(expand=True)
        # --------------------------------------------------------------------------------------------

    def create_clock_out_screen(self):
        """
                Creates and configures the necessary elements
                for the clock_out screen
                :return None:
                """

        # Title ------------------------------------------
        username = self.current_user.access.get_data_all_users("username").title()
        title_label: ttk.Label = ttk.Label(
            self.clock_in_frame,
            text=f"{username.title()} is logged in",
            font=("Roboto", 60, "bold"),
            foreground="#00796B"
        )

        title_label.pack(pady=20)
        # ------------------------------------------------

        # Clock in button
        clock_out_button: tk.Button = tk.Button(
            self.clock_in_frame,
            text="Clock Out",
            command=self.clock_out,
            bg="#00796B",
            fg="white",
            font=("Roboto", 60, "bold"),
            relief="flat",
            bd=0,
            height=2,
            width=15,
            cursor="hand2"
        )

        clock_out_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

        # Log out button -----------------------------------------
        log_out_button: tk.Button = tk.Button(
            self.clock_in_frame,
            text="Log out",
            command=self.log_out,
            bg="#8B0000",
            fg="white",
            font=("Roboto", 40, "bold"),
            relief="flat",
            bd=0,
            height=2,
            width=10,
            cursor="hand2")

        log_out_button.pack(anchor="center", pady=10)
        # ----------------------------------------------------------

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
            font=("Roboto", 60, "bold"),
            foreground="#00796B"
        )

        title_label.pack()
        # ----------------------------------------------

        # Set the columns and initializing the employees table ---------------------------------------------
        columns: tuple[str, str, str, str, str, str] = (
            "Student ID", "Username", "Admin Status", "Start Time", "Working", "Total Minutes")

        employees_table: ttk.Treeview = ttk.Treeview(self.admin_frame, columns=columns, show="headings")

        for column in columns:
            employees_table.heading(column, text=column)
        employees_table.pack()
        # --------------------------------------------------------------------------------------------------

        # Insert Employees below -----------------------------------------------------------------------
        all_employees = self.current_user.access.admin_read_all_users()
        for employee in all_employees:
            employees_table.insert("", "end", values=employee)
        # ----------------------------------------------------------------------------------------------

        # Configure and pack the edit button ------------
        manage_employee_button: tk.Button = tk.Button(
            self.admin_frame,
            text="Employee Management",
            command=lambda: self.show(self.employee_management_frame,
                                      "employee_management_frame",
                                      self.create_employee_management_screen),
            bg="#00796B",
            fg="white",
            font=("Roboto", 36, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        manage_employee_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

        # Configure and pack the reports button ------------
        report_button: tk.Button = tk.Button(
            self.admin_frame,
            text="Reports",
            command=self.open_reports_window,
            bg="#00796B",
            fg="white",
            font=("Roboto", 36, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        report_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

        # Log out button -----------------------------------------
        log_out_button: tk.Button = tk.Button(
            self.admin_frame,
            text="Log out",
            command=self.log_out,
            bg="#8B0000",
            fg="white",
            font=("Roboto", 30, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",)

        log_out_button.pack(anchor="center", pady=10)
        # ----------------------------------------------------------

    def create_add_employee_screen(self):
        """
        Creates and configures the elements needed
        to add employees (students) to the database
        """

        # Configuring the rows of the parent window
        self.add_employee_frame.rowconfigure(0, weight=6)  # Top space
        self.add_employee_frame.rowconfigure(1, weight=6)  # Center Space
        self.add_employee_frame.rowconfigure(2, weight=2)  # Footer space

        # Configuring the columns of the parent window
        self.add_employee_frame.columnconfigure(0, weight=1)  # Left space
        self.add_employee_frame.columnconfigure(1, weight=2)  # Center space
        self.add_employee_frame.columnconfigure(2, weight=1)  # Right space

        # Frame that will be on the higher side of the screen
        top_frame: ttk.Frame = ttk.Frame(
            self.add_employee_frame,
            # borderwidth=5,
            # relief="solid"

        )
        top_frame.grid(row=0, column=1, sticky="nsew")
        top_frame.grid_propagate(False)

        # Configuring the columns of the top child window
        top_frame.columnconfigure(0, weight=3)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=3)

        # Configuring the rows of the top child window
        top_frame.rowconfigure(0, weight=2)
        top_frame.rowconfigure(1, weight=1)
        top_frame.rowconfigure(2, weight=8)
        top_frame.rowconfigure(6, weight=2)

        # title label
        title_label: ttk.Label = ttk.Label(
            top_frame,
            text="New Employee",
            font=("Roboto", 50, "bold"),
            foreground="#00796B"
        )

        title_label.grid(row=0, column=0, columnspan=3)

        # TextBoxes
        pin_entry = ttk.Entry(
            top_frame,
            font=("Roboto", 20),
        )

        # Textbox in which the student's PIN will be hosted
        pin_entry.insert(0, "PIN")  # Prepopulate with "PIN"
        pin_entry.grid(row=1, column=0, sticky="nsew", pady=5)
        pin_entry.bind("<FocusIn>", lambda clicked: pin_entry.delete(0, tk.END))

        # Textbox in which the student's username will be hosted
        username_entry = ttk.Entry(
            top_frame,
            font=("Roboto", 20)
        )
        username_entry.insert(0, "USERNAME")  # Prepopulate with "Username"
        username_entry.grid(row=1, column=2, sticky="nsew", pady=5)
        username_entry.bind("<FocusIn>", lambda clicked: username_entry.delete(0, tk.END))

        # Creates the
        buttons_frame: ttk.Frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        buttons_frame.grid_propagate(False)

        # Configures the frame's columns
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=5)
        buttons_frame.columnconfigure(2, weight=1)

        # Configures the frame's row
        buttons_frame.rowconfigure(0, weight=2)
        buttons_frame.rowconfigure(1, weight=4)
        buttons_frame.rowconfigure(2, weight=4)
        buttons_frame.rowconfigure(3, weight=1)

        add_button: tk.Button = tk.Button(
            buttons_frame,
            text="Add",
            bg="#00796B",
            fg="white",
            font=("Roboto", 30, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        add_button.grid(row=1, column=1, sticky="ew")

        reset_button: tk.Button = tk.Button(
            buttons_frame,
            text="Reset",
            bg="#8B0000",
            fg="white",
            font=("Roboto", 30, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.show(self.add_employee_frame, "add_employee_frame", self.create_add_employee_screen)
        )

        reset_button.grid(row=2, column=1, sticky="ew")

        # Frame that will host the back button
        back_button_frame: ttk.Frame = ttk.Frame(
            self.add_employee_frame,
            # borderwidth=5,
            # relief="solid"
        )
        back_button_frame.grid(row=2, column=0, sticky="nsew")
        back_button_frame.grid_propagate(False)

        # configures the rows of the back button frame
        back_button_frame.rowconfigure(0, weight=1)
        back_button_frame.rowconfigure(1, weight=1)

        # configures the columns of the back button frame
        back_button_frame.columnconfigure(0, weight=1)
        back_button_frame.columnconfigure(1, weight=1)

        # Button that takes the admin back to the admin panel
        back_button: tk.Button = tk.Button(
            back_button_frame,
            text="Back",
            bg="#8B0000",
            command=lambda: self.show(self.employee_management_frame, "employee_management_frame", self.create_employee_management_screen),
            fg="white",
            font=("Roboto", 24, "bold"),
            relief="flat",
            cursor="hand2"
        )

        back_button.grid(row=1, column=0, sticky="nsew")

    def create_employee_management_screen(self):
        """
        Creates and configures the elements needed for the window
        :return None
        """

        # Configuring the rows of the parent window
        self.employee_management_frame.rowconfigure(0, weight=6)  # Top space
        self.employee_management_frame.rowconfigure(1, weight=6)  # Center Space
        self.employee_management_frame.rowconfigure(2, weight=2)  # Footer space

        # Configuring the columns of the parent window
        self.employee_management_frame.columnconfigure(0, weight=1)  # Left space
        self.employee_management_frame.columnconfigure(1, weight=2)  # Center space
        self.employee_management_frame.columnconfigure(2, weight=1)  # Right space

        # Frame that will be on the higher side of the screen
        top_frame: ttk.Frame = ttk.Frame(
            self.employee_management_frame,
            borderwidth=5,
            relief="solid"

        )
        top_frame.grid(row=0, column=1, sticky="nsew")
        top_frame.grid_propagate(False)

        # Configuring the columns of the top child window
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)
        top_frame.columnconfigure(3, weight=1)
        top_frame.columnconfigure(4, weight=1)
        top_frame.columnconfigure(5, weight=1)
        top_frame.columnconfigure(6, weight=1)

        # Configuring the rows of the top child window
        top_frame.rowconfigure(0, weight=2)
        top_frame.rowconfigure(1, weight=1)
        top_frame.rowconfigure(2, weight=1)
        top_frame.rowconfigure(3, weight=1)
        top_frame.rowconfigure(4, weight=1)
        top_frame.rowconfigure(5, weight=1)
        top_frame.rowconfigure(6, weight=5)

        # title label
        title_label: ttk.Label = ttk.Label(
            top_frame,
            text="Employee Management",
            font=("Roboto", 50, "bold"),
            foreground="#00796B"
        )

        title_label.grid(row=0, column=0, columnspan=6)

        # Dropdown of the available employees
        select_employee_dropdown: ttk.Combobox = ttk.Combobox(
            top_frame,
            values=["Luis Velasquez", "Jackson", "Aung"],
            font=("Roboto", 25, "bold")
        )

        select_employee_dropdown.grid(
            row=2, column=0,
            sticky="new",
            columnspan=6
        )

        # Button used to select an employee
        select_button: tk.Button = tk.Button(
            top_frame,
            text="Select",
            bg="#00796B",
            fg="white",
            font=("Roboto", 30, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        select_button.grid(row=3, column=1, columnspan=4, sticky="ew")

        # Frame that will be on the lower side of the screen
        bottom_frame: ttk.Frame = ttk.Frame(
            self.employee_management_frame,
            borderwidth=5,
            relief="solid"
        )

        bottom_frame.grid(row=1, column=1, sticky="nsew")
        bottom_frame.grid_propagate(False)

        # Configures the rows of the bottom child frame
        bottom_frame.rowconfigure(0, weight=3)
        bottom_frame.rowconfigure(1, weight=1)
        bottom_frame.rowconfigure(2, weight=2)

        # Configures the columns of the bottom child frame
        bottom_frame.columnconfigure(0, weight=2)
        bottom_frame.columnconfigure(1, weight=2)
        bottom_frame.columnconfigure(2, weight=2)

        # Creates the calendar that will be used to edit the student's hours
        calendar = Calendar(
            bottom_frame,
            selectmode='day',
            year=datetime.today().year,
            month=datetime.today().month,
            day=datetime.today().day,
            font=("Roboto", 12),
            foreground = "white",
            background="#00796B"
        )
        calendar.grid(row=0, column=0, sticky="nsew")
        print(calendar.get_date())

        # Frame that will host the back button
        back_button_frame: ttk.Frame = ttk.Frame(
            self.employee_management_frame,
            borderwidth=5,
            relief="solid"
        )
        back_button_frame.grid(row=2, column=0, sticky="nsew")
        back_button_frame.grid_propagate(False)

        # configures the rows of the back button frame
        back_button_frame.rowconfigure(0, weight=1)
        back_button_frame.rowconfigure(1, weight=1)

        # configures the columns of the back button frame
        back_button_frame.columnconfigure(0, weight=1)
        back_button_frame.columnconfigure(1, weight=1)

        # Button that takes the admin back to the admin panel
        back_button: tk.Button = tk.Button(
            back_button_frame,
            text="Back",
            bg="#8B0000",
            command=lambda: self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen),
            fg="white",
            font=("Roboto", 24, "bold"),
            relief="flat",
            cursor="hand2"
        )

        back_button.grid(row=1, column=0, sticky="nsew")

        # Frame that will host the Add Employee button
        add_employee_button_frame: ttk.Frame = ttk.Frame(
            self.employee_management_frame,
            borderwidth=5,
            relief="solid"
        )
        add_employee_button_frame.grid(row=2, column=2, sticky="nsew")
        add_employee_button_frame.grid_propagate(False)

        # configures the rows of the add_employee_button_frame
        add_employee_button_frame.rowconfigure(0, weight=1)
        add_employee_button_frame.rowconfigure(1, weight=1)

        # configures the columns of the add_employee_button_frame
        add_employee_button_frame.columnconfigure(0, weight=1)
        add_employee_button_frame.columnconfigure(1, weight=1)

        # Button that takes the add employee window
        add_employee_button: tk.Button = tk.Button(
            add_employee_button_frame,
            text="Add Employee",
            bg="#06402B",
            # command=lambda: self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen),
            fg="white",
            font=("Roboto", 24, "bold"),
            relief="flat",
            cursor="hand2",
            command=lambda: self.show(self.add_employee_frame, "add_employee_frame", self.create_add_employee_screen)
        )

        add_employee_button.grid(row=1, column=1, sticky="nsew")

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

    # Clock Methods ----------------------------------------
    def clock_in(self):
        # messagebox.showinfo("Hours", "You currently have 32hrs")
        self.show(self.clock_in_frame, "clock_in_frame", self.create_clock_out_screen)
        self.current_user.clock.clock_in()

    def clock_out(self):
        self.current_user.clock.clock_out()
        self.show(self.clock_in_frame, "clock_in_frame", self.create_clock_in_screen)
    # -----------------------------------------------------

    # Admin methods --------------------------------------
    def open_select_employee_window(self):
        """
        Opens a new window to select an employee before editing it
        :return None:
        """
        if self.select_employee_frame is None:
            self.select_employee_frame = tk.Toplevel(self.admin_frame)
            self.select_employee_frame.title("Choose Employee")
            self.select_employee_frame.geometry("600x400")

            # Title label
            employee_label = ttk.Label(self.select_employee_frame,
                                       text="Choose an Employee",
                                       font=("Roboto", 20, "bold"))
            employee_label.pack()

            # Gets all the employees
            employees = self.current_user.access.admin_read_all_users()

            # Maps the username to their PIN -----------------------------------
            employees_credentials: dict[str, str] = {}

            for employee in employees:
                employees_credentials.update({employee[1]: employee[0]})
            # ----------------------------------------------------------------------

            # Sets up a dropdown of the employees
            employee_combobox: ttk.Combobox = ttk.Combobox(
                self.select_employee_frame,
                values=[*list(employees_credentials.keys())],
                font=("Roboto", 20),
            )
            employee_combobox.pack(pady=10)

            def handle_selection():
                """
                Makes sure the id selected is valid
                :return None:
                """

                try:
                    emp_id = employees_credentials[employee_combobox.get()]
                    self.employee_selected(emp_id)
                except KeyError:
                    tk.messagebox.showwarning("User Error",
                                              "Please select a valid employee id")

            # Set up the select button
            select_button: tk.Button = tk.Button(
                self.select_employee_frame,
                text="Select",
                command=handle_selection,  # Causes an error
                bg="#00796B",
                fg="white",
                font=("Roboto", 36, "bold"),
                cursor="hand2"
            )

            select_button.pack(pady=30)
        else:
            self.select_employee_frame.destroy()
            self.select_employee_frame = None
            self.open_select_employee_window()

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

    def employee_selected(self, emp_id: str, window=0, constructor=0):
        """
        Makes a call to the database, using a specific user credentials
        :param emp_id: credential connected to the employee in the database (4-digits)
        :param window: parent window
        :param constructor: Method used to create the screen
        :return: None
        """

        employee = self.current_user.access.admin_get_row_all_users(emp_id)
        print(employee)
    # ----------------------------------------------------

    # Backend functions
    def log_in(self):
        """
        Checks if the user has the right credentials to log in
        :return:
        """

        # Check if the username and PIN fields are fulfilled
        if self.pin.get():

            # Temporary access to admin panel
            if self.pin.get() == "0000":
                self.current_user = User(self.pin.get())
                # self.current_user.access.add_user(1010, "luis", 0)
                # self.current_user.access.add_user(2020, "jackson", 0)
                # self.current_user.access.add_user(3030, "aung", 0)
                # self.current_user.access.add_user(4040, "obeth", 0)
                # self.current_user.access.add_user(5050, "martin", 0)
                # self.current_user.access.add_user(6060, "logan", 0)
                self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen)
            else:

                # Checks if the credentials are in the database
                try:
                    self.current_user = User(self.pin.get())
                    if self.current_user.access.get_data_all_users("working_status") == 1:
                        self.show(self.clock_in_frame, "clock_in_frame", self.create_clock_out_screen)
                    else:
                        self.show(self.clock_in_frame, "clock_in_frame", self.create_clock_in_screen)

                # Warns the user if the credentials are incorrect
                except ValueError:
                    messagebox.showwarning("User Error", "User does not exist")
                    self.pin.set("")
        else:
            # Resets the log in screen
            self.pin.set("")
            messagebox.showwarning("Input Error", "Please enter your PIN")

    def log_out(self):
        """
        Logs the current user so the next one can clock in/out
        :return None:
        """

        # Resets the corresponding attributes and drives the user to the log in screen
        self.current_user = None
        self.pin.set("")
        self.show(self.log_in_frame, "log_in_frame", self.create_log_in_screen)

    # Extra functions
    def exit_fullscreen(self):
        self.root.attributes("-fullscreen", False)


gui = GUI()
gui.root.mainloop()
