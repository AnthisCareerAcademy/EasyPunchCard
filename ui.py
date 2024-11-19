import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk, messagebox
from User import User
from datetime import datetime, timedelta

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

        # Create frames for different sections
        self.nav_frame: ttk.Frame = ttk.Frame(self.root)

        self.log_in_frame: ttk.Frame = ttk.Frame(self.root)
        self.clock_in_frame: ttk.Frame = ttk.Frame(self.root)
        self.admin_frame: ttk.Frame = ttk.Frame(self.root)
        self.reports_frame: ttk.Frame = ttk.Frame(self.root)
        self.employee_management_frame: ttk.Frame = ttk.Frame(self.root)

        # A list of the current frames
        self.frames: list[str: ttk.Frame] = {
            "log_in_frame": self.log_in_frame,
            "clock_in_frame": self.clock_in_frame,
            "admin_frame": self.admin_frame,
            "reports_frame": self.reports_frame,
            "employee_management_frame": self.employee_management_frame
        }

        # Admin Windows
        self.select_employee_window: None | tk.Toplevel = None
        self.edit_employee_window: None | tk.Toplevel = None
        self.add_employee_window: None | tk.Toplevel = None

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

    def create_employee_management_screen(self):
        """
        Creates and configures the elements needed for the window
        :return None
        """

        # Title -------------------------------
        title_label: ttk.Label = ttk.Label(
            self.employee_management_frame,
            text="Employee Management",
            font=("Roboto", 60, "bold"),
            foreground="#00796B"
        )
        title_label.pack()
        # -------------------------------------

        # Management buttons -----------------------------------------------
        edit_employee_button: tk.Button = tk.Button(
            self.employee_management_frame,
            text="Edit Employee",
            command=lambda: self.open_select_employee_window(),
            bg="#00796B",
            fg="white",
            font=("Roboto", 36, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
        )

        edit_employee_button.pack(anchor="center", pady=50)

        add_employee_button: tk.Button = tk.Button(
            self.employee_management_frame,
            text="Add Employee",
            command=lambda: self.open_select_employee_window(),
            bg="#00796B",
            fg="white",
            font=("Roboto", 36, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        add_employee_button.pack(anchor="center", pady=10)

        remove_employee_button: tk.Button = tk.Button(
            self.employee_management_frame,
            text="Remove Employee",
            command=lambda: self.open_select_employee_window(),
            # Needs to be edited
            bg="#8B0000",
            fg="white",
            font=("Roboto", 36, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        remove_employee_button.pack(anchor="center", pady=50)

    # --------------------------------------------------------------------------

        # Log out button -----------------------------------------
        back_button: tk.Button = tk.Button(
            self.employee_management_frame,
            text="Back",
            command=lambda: self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen),
            bg="#8B0000",
            fg="white",
            font=("Roboto", 30, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2", )

        back_button.pack(side="bottom", anchor="sw")
        # ----------------------------------------------------------

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
    def open_edit_employee_window(self):
        """
        Opens a new window to edit employee details
        :return None:
        """

    def open_add_employee_window(self):
        """Creates the elements and the pop-up window needed
        to add a new employee to the database"""

        if self.add_employee_window is None:
            # Configures the initial pop-up window
            self.add_employee_window = tk.Toplevel(self.employee_management_frame)
            self.add_employee_window.title("Add Employee")
            self.add_employee_window.geometry("600x400")

    def open_select_employee_window(self):
        """
        Opens a new window to select an employee before editing it
        :return None:
        """
        if self.select_employee_window is None:
            self.select_employee_window = tk.Toplevel(self.admin_frame)
            self.select_employee_window.title("Choose Employee")
            self.select_employee_window.geometry("600x400")

            # Title label
            employee_label = ttk.Label(self.select_employee_window,
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
                self.select_employee_window,
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
                self.select_employee_window,
                text="Select",
                command=handle_selection,  # Causes an error
                bg="#00796B",
                fg="white",
                font=("Roboto", 36, "bold"),
                cursor="hand2"
            )

            select_button.pack(pady=30)
        else:
            self.select_employee_window.destroy()
            self.select_employee_window = None
            self.open_select_employee_window()

    def open_reports_window(self):
        """
        Opens a new window to view and print reports
        :return None:
        """
        # Create the pop-up window for class reports------------------------------------
        class_report_window: tk.Toplevel = tk.Toplevel(self.admin_frame)
        class_report_window.title("Class Reports")
        class_report_window.geometry("500x400")

        # file name text input
        class_file_name_label: ttk.Label = ttk.Label(class_report_window, text="File Name",font=("Roboto", 12))
        class_file_name_label.pack(pady=5)
        class_file_name: tk.Entry = tk.Entry(class_report_window, width=20)
        class_file_name.pack(pady=5)

        # company name text input
        class_company_name_label: ttk.Label = ttk.Label(class_report_window, text="Company Name",font=("Roboto", 12))
        class_company_name_label.pack(pady=5)
        class_company_name: tk.Entry = tk.Entry(class_report_window, width=20)
        class_company_name.pack(pady=5)

        # title text input
        class_title_label: ttk.Label = ttk.Label(class_report_window, text="Title Name",font=("Roboto", 12))
        class_title_label.pack(pady=5)
        class_title_name: tk.Entry = tk.Entry(class_report_window, width=20)
        class_title_name.pack(pady=5)

        # Print class report button
        print_class_button: tk.Button = tk.Button(
            class_report_window,
            text="Print All Users Report",
            command=lambda: self.print_class_report(class_file_name.get(), class_company_name.get(), class_title_name.get()),
            bg="#00796B",
            fg="white", font=("Roboto", 12, "bold"),
            relief="flat", bd=0)
        print_class_button.pack(pady=20)
        # --------------------------------------------------------------


        # Create the pop-up window for small reports------------------------------------
        report_window: tk.Toplevel = tk.Toplevel(self.admin_frame)
        report_window.title("User Reports")
        report_window.geometry("500x750")

        # file name text input
        file_name_label: ttk.Label = ttk.Label(report_window, text="File Name",font=("Roboto", 12))
        file_name_label.pack(pady=5)

        file_name: tk.Entry = tk.Entry(report_window, width=20)
        file_name.pack(pady=5)

        # company name text input
        company_name_label: ttk.Label = ttk.Label(report_window, text="Company Name",font=("Roboto", 12))
        company_name_label.pack(pady=5)
        company_name: tk.Entry = tk.Entry(report_window, width=20)
        company_name.pack(pady=5)

        # title text input
        title_label: ttk.Label = ttk.Label(report_window, text="Title Name",font=("Roboto", 12))
        title_label.pack(pady=5)
        title_name: tk.Entry = tk.Entry(report_window, width=20)
        title_name.pack(pady=5)

        # student dropdown
        employee_label: ttk.Label = ttk.Label(report_window, text="Select Employee", font=("Roboto", 12))
        employee_label.pack(pady=10)

        all_users = self.current_user.access.admin_read_all_users()
        values = {}
        for user in all_users:
            values[user[1]] = user[0]

        employee_combobox: ttk.Combobox = ttk.Combobox(
            report_window,
            values=list(values))
        
        employee_combobox.pack(pady=5)

        # date range selection
        self.cal = Calendar(report_window, selectmode='day', year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, font=("Roboto", 12))
        self.cal.pack(pady=20)

        self.start_date = None
        self.end_date = None
        
        self.feedback_label = ttk.Label(report_window, text="")
        self.feedback_label.pack(pady=10)

        # start date button
        start_date_button: tk.Button = tk.Button(
            report_window, 
            text="Set Start Date", 
            command=self.set_start_date,
            bg = "#00796B",
            fg = "white",
            font = ("Roboto", 12, "bold"),
            relief = "flat",
            bd = 0,
            height = 1,
            width = 15,
            )
        start_date_button.pack(pady=10)
        
        # end date button
        end_date_button: tk.Button = tk.Button(
            report_window, 
            text="Set End Date", 
            command=self.set_end_date,
            bg="#00796B",
            fg="white",
            font=("Roboto", 12, "bold"),
            relief="flat",
            bd=0,
            height=1,
            width=15,
            )
        end_date_button.pack(pady=10)

        # print specific user report button
        print_specific_user_button: tk.Button = tk.Button(
            report_window,
            text="Print Specific User Report",
            command=lambda: self.print_specific_user_report(file_name.get(), company_name.get(), title_name.get(), self.start_date.strftime('%m-%d-%Y'), self.end_date.strftime('%m-%d-%Y'), employee_combobox.get(), str(values[employee_combobox.get()])),
            bg="#00796B",
            fg="white", font=("Roboto", 12, "bold"),
            relief="flat", bd=0)
        print_specific_user_button.pack(pady=20)

        # --------------------------------------------------------------

    def print_class_report(self, file_name, company_name, title):
        """creates class report in a folder called Reports"""
        self.current_user.report.create_class_pdf(file_name, company_name, title)

    def print_specific_user_report(self, file_name, company_name, title, start_date, end_date, name, student_id):
        """creates a user report in the same Reports folder"""
        self.current_user.report.create_user_specific_pdf(file_name, company_name, title, start_date, end_date, name, student_id)

    def set_start_date(self):
        self.start_date = datetime.strptime(self.cal.get_date(), "%m/%d/%y")
        self.feedback_label.config(text=f"Start Date Set: {self.start_date.strftime('%Y-%m-%d')}")

    # Function to update the end date
    def set_end_date(self):
        self.end_date = datetime.strptime(self.cal.get_date(), "%m/%d/%y")
        self.feedback_label.config(text=f"End Date Set: {self.end_date.strftime('%Y-%m-%d')}")
        if self.start_date and self.end_date:
            self.highlight_range()

    # Function to highlight the date range
    def highlight_range(self):
        try:
            # Validate date range
            if self.start_date > self.end_date:
                raise ValueError("Start date must be before or equal to the end date!")
            # Clear previous highlights
            self.cal.calevent_remove('all')
            # Highlight the new date range
            current_date = self.start_date
            while current_date <= self.end_date:
                self.cal.calevent_create(current_date, "Range Highlight", "highlight")
                current_date += timedelta(days=1)
            # Configure the highlight appearance
            self.cal.tag_config("highlight", background="lightblue", foreground="black")
            self.feedback_label.config(text=f"Highlighted: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        except ValueError as e:
            self.feedback_label.config(text=f"Error: {e}")

    def employee_selected(self, emp_id: str, window=0, constructor=0):
        """
        Makes a call to the database, using a specific user credentials
        :param emp_id: credential connected to the employee in the database (4-digits)
        :param window: parent window
        :param constructor: Method used to create the screen
        :return: None
        """

        employee = self.current_user.access.admin_get_row_all_users(emp_id)
        self.open_edit_employee_window()
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
                except TypeError:
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
