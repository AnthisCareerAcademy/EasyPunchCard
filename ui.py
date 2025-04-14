import tkinter as tk

from tkinter import ttk, messagebox

from tkcalendar import Calendar
from datetime import datetime, timedelta


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
        self.reports_selection_frame = ttk.Frame(self.root)
        self.class_reports_frame: ttk.Frame = ttk.Frame(self.root)
        self.individual_reports_frame: ttk.Frame = ttk.Frame(self.root)
        self.student_management_frame: ttk.Frame = ttk.Frame(self.root)

        # Admin Windows
        self.select_student_frame: None | ttk.Frame = None
        self.edit_student_frame: None | ttk.Frame = None
        self.add_student_frame: None | ttk.Frame = ttk.Frame(self.root)

        # A list of the current frames
        self.frames: list[str: ttk.Frame] = {
            "log_in_frame": self.log_in_frame,
            "clock_in_frame": self.clock_in_frame,
            "admin_frame": self.admin_frame,
            'reports_selection_frame': self.reports_selection_frame,
            "class_reports_frame": self.class_reports_frame,
            "individual_reports_frame": self.individual_reports_frame,
            "student_management_frame": self.student_management_frame,
            "add_student_frame": self.add_student_frame,
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
        fname = self.current_user.access.get_data_all_users("first_name").title()
        lname = self.current_user.access.get_data_all_users("last_name").title()
        username = fname + " " + lname
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
        fname = self.current_user.access.get_data_all_users("first_name").title()
        lname = self.current_user.access.get_data_all_users("last_name").title()
        username = fname + " " + lname
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

        # Set the columns and initializing the student table ---------------------------------------------
        columns: tuple[str, str, str, str, str, str, str, str] = (
            "Student ID", "First Name", "Last Name", "Start Time", "Working", "Total Minutes", "Graduation Year")

        students_table: ttk.Treeview = ttk.Treeview(self.admin_frame, columns=columns, show="headings")

        for column in columns:
            students_table.heading(column, text=column)
        students_table.pack()
        # --------------------------------------------------------------------------------------------------

        # Insert students below -----------------------------------------------------------------------
        all_students = self.current_user.access.admin_read_all_users()

        # Group by grad year and then sorted by last name
        sorted_all_students = sort_list(all_students)

        for student in sorted_all_students:
            del student["end_time"]
            del student["admin_status"]
            students_table.insert("", "end", values=list(student.values()))
        # ----------------------------------------------------------------------------------------------

        # Configure and pack the edit button ------------
        manage_student_button: tk.Button = tk.Button(
            self.admin_frame,
            text="Student Management",
            command=lambda: self.show(self.student_management_frame,
                                      "student_management_frame",
                                      self.create_student_management_screen),
            bg="#00796B",
            fg="white",
            font=("Roboto", 36, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        manage_student_button.pack(anchor="center", pady=10)
        # ------------------------------------------------

        # Configure and pack the reports button ------------
        report_button: tk.Button = tk.Button(
            self.admin_frame,
            text="Reports",
            command=lambda: self.show(self.reports_selection_frame, "reports_selection_frame", self.create_reports_selection_screen),
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

    def create_add_student_screen(self):
        """
        Creates and configures the elements needed
        to add students (students) to the database
        """

        # Configuring the rows of the parent window
        self.add_student_frame.rowconfigure(0, weight=6)  # Top space
        self.add_student_frame.rowconfigure(1, weight=6)  # Center Space
        self.add_student_frame.rowconfigure(2, weight=2)  # Footer space

        # Configuring the columns of the parent window
        self.add_student_frame.columnconfigure(0, weight=1)  # Left space
        self.add_student_frame.columnconfigure(1, weight=2)  # Center space
        self.add_student_frame.columnconfigure(2, weight=1)  # Right space

        # Frame that will be on the higher side of the screen
        top_frame: ttk.Frame = ttk.Frame(
            self.add_student_frame,
            # borderwidth=5,
            # relief="solid"

        )
        top_frame.grid(row=0, column=1, sticky="nsew")
        top_frame.grid_propagate(False)

        # Configuring the columns of the top child window
        top_frame.columnconfigure(0, weight=3)
        top_frame.columnconfigure(1, weight=3)
        top_frame.columnconfigure(2, weight=3)

        # Configuring the rows of the top child window
        top_frame.rowconfigure(0, weight=2)
        top_frame.rowconfigure(1, weight=1)
        top_frame.rowconfigure(2, weight=8)
        top_frame.rowconfigure(6, weight=2)

        # title label
        title_label: ttk.Label = ttk.Label(
            top_frame,
            text="New student",
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
        pin_entry.insert(0, "Student ID")  # Prepopulate with "PIN"
        pin_entry.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)
        pin_entry.bind("<FocusIn>", lambda clicked: pin_entry.delete(0, tk.END))

        # Textbox in which the student's graduation year will be hosted
        grad_entry = ttk.Entry(
            top_frame,
            font=("Roboto", 20),
        )

        grad_entry.insert(0, "Grad Year - YYYY")  # Prepopulate with "PIN"
        grad_entry.grid(row=1, column=3, sticky="nsew", pady=5, padx=5)
        grad_entry.bind("<FocusIn>", lambda clicked: grad_entry.delete(0, tk.END))

        # Textbox in which the student's username will be hosted
        fname_entry = ttk.Entry(
            top_frame,
            font=("Roboto", 20)
        )
        fname_entry.insert(0, "First Name")  # Prepopulate with "first name"
        fname_entry.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)
        fname_entry.bind("<FocusIn>", lambda clicked: fname_entry.delete(0, tk.END))

        # last name
        lname_entry = ttk.Entry(
            top_frame,
            font=("Roboto", 20)
        )
        lname_entry.insert(0, "Last Name")  # Prepopulate with "last name"
        lname_entry.grid(row=1, column=2, sticky="nsew", pady=5, padx=5)
        lname_entry.bind("<FocusIn>", lambda clicked: lname_entry.delete(0, tk.END))

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
            cursor="hand2",
            command=lambda: self.add_student_request(pin_entry.get(), fname_entry.get(), lname_entry.get(), grad_entry.get())
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
            command=lambda: self.show(self.add_student_frame, "add_student_frame", self.create_add_student_screen)
        )

        reset_button.grid(row=2, column=1, sticky="ew")

        # Frame that will host the back button
        back_button_frame: ttk.Frame = ttk.Frame(
            self.add_student_frame,
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
            command=lambda: self.show(self.student_management_frame, "student_management_frame", self.create_student_management_screen),
            fg="white",
            font=("Roboto", 24, "bold"),
            relief="flat",
            cursor="hand2"
        )

        back_button.grid(row=1, column=0, sticky="nsew")

    def create_student_management_screen(self):
        """
        Creates and configures the elements needed for the window
        :return None
        """

        # Configuring the rows of the parent window
        self.student_management_frame.rowconfigure(0, weight=6)  # Top space
        self.student_management_frame.rowconfigure(1, weight=6)  # Center Space
        self.student_management_frame.rowconfigure(2, weight=2)  # Footer space

        # Configuring the columns of the parent window
        self.student_management_frame.columnconfigure(0, weight=1)  # Left space
        self.student_management_frame.columnconfigure(1, weight=2)  # Center space
        self.student_management_frame.columnconfigure(2, weight=1)  # Right space

        # Frame that will be on the higher side of the screen
        top_frame: ttk.Frame = ttk.Frame(
            self.student_management_frame,
            # borderwidth=5,
            # relief="solid"

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
            text="student Management",
            font=("Roboto", 50, "bold"),
            foreground="#00796B"
        )

        title_label.grid(row=0, column=0, columnspan=6)

        students = {}
        for student in self.current_user.access.admin_read_all_users():
            # Skips the admin user
            if student["admin_status"] == 1:
                continue
            username = student["first_name"] + " " + student["last_name"]
            students.update({username: student['student_id']})

        # Dropdown of the available students
        select_student_dropdown: ttk.Combobox = ttk.Combobox(
            top_frame,
            values=list(sorted(students.keys())),
            font=("Roboto", 25, "bold")
        )

        select_student_dropdown.grid(
            row=2, column=0,
            sticky="new",
            columnspan=6
        )

        # Button used to select an student
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

        # Button used to delete an student from the database
        delete_student_button: tk.Button = tk.Button(
            top_frame,
            text="Delete student",
            bg="#8B0000",
            fg="white",
            font=("Roboto", 30, "bold"),
            relief="flat",
            command=lambda: self.delete_student_request(select_student_dropdown.get(), students),
            bd=0,
            cursor="hand2"
        )
        delete_student_button.grid(row=4, column=1, columnspan=4, sticky="ew")

        # Frame that will be on the lower side of the screen
        bottom_frame: ttk.Frame = ttk.Frame(
            self.student_management_frame,
            # borderwidth=5,
            # relief="solid"
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

        # Frame that will host the back button
        back_button_frame: ttk.Frame = ttk.Frame(
            self.student_management_frame,
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
            command=lambda: self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen),
            fg="white",
            font=("Roboto", 24, "bold"),
            relief="flat",
            cursor="hand2"
        )

        back_button.grid(row=1, column=0, sticky="nsew")

        # Frame that will host the Add student button
        add_student_button_frame: ttk.Frame = ttk.Frame(
            self.student_management_frame,
            # borderwidth=5,
            # relief="solid"
        )
        add_student_button_frame.grid(row=2, column=2, sticky="nsew")
        add_student_button_frame.grid_propagate(False)

        # configures the rows of the add_student_button_frame
        add_student_button_frame.rowconfigure(0, weight=1)
        add_student_button_frame.rowconfigure(1, weight=1)

        # configures the columns of the add_student_button_frame
        add_student_button_frame.columnconfigure(0, weight=1)
        add_student_button_frame.columnconfigure(1, weight=1)

        # Button that takes the add student window
        add_student_button: tk.Button = tk.Button(
            add_student_button_frame,
            text="Add student",
            bg="#06402B",
            # command=lambda: self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen),
            fg="white",
            font=("Roboto", 24, "bold"),
            relief="flat",
            cursor="hand2",
            command=lambda: self.show(self.add_student_frame, "add_student_frame", self.create_add_student_screen)
        )

        add_student_button.grid(row=1, column=1, sticky="nsew")

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
    def add_student_request(self, pin: str, first_name: str, last_name: str, grad_year: str):

        # Creates a list to store the active PINs in the database
        active_pins: list[str] = []
        active_usernames: list[str] = []
        username = first_name + " " + last_name

        # Goes through the list of users and extracts their PINs
        for user in self.current_user.access.admin_read_all_users():
            active_pins.append(user['student_id'])
            active_usernames.append(user["first_name"] + " " + user["last_name"])

        # Checks for possible PIN errors from the user
        if len(pin) < 7:
            messagebox.showwarning("PIN Error", "Your Student ID needs to be at least 7 digits")
            return
        elif not pin.isdigit():
            messagebox.showwarning("PIN Error", "Your PIN cannot have letters only numbers are allowed")
            return
        elif pin in active_pins:
            messagebox.showwarning("PIN Error", f"Another user exists with the same PIN: {pin}")
            return

        # Checks for possible username errors from the user
        if not first_name or not last_name:
            messagebox.showwarning("USERNAME Error", "Your firstname or lastname cannot be empty")
            return
        elif username in active_usernames:
            messagebox.showwarning("USERNAME Error", f"Another user exists with the same NAME: {username}")
            return

        try:
            grad_year_int = int(grad_year)
        except ValueError:
            messagebox.showwarning("Graduation Year Error", "Your Graduation year needs to be a number")
            return

        if not grad_year_int:
            messagebox.showwarning("Graduation Year Error", "Your Graduation year cannot be empty")
        elif grad_year_int < datetime.today().year:
            messagebox.showwarning("Graduation Year Error", f"Your Graduation year cannot be less than {datetime.today().year}")
            return

        self.current_user.access.add_user(pin, first_name, last_name, 0, grad_year_int)
        messagebox.showinfo("User Addition", f"{username} Has been added to the database")
        self.show(self.add_student_frame, "add_student_frame", self.create_add_student_screen)

    def delete_student_request(self, username: str, students: dict[str, str]):

       try:
           student_pin = students[username]
           self.current_user.access.remove_user(student_pin)
           messagebox.showinfo("User Deletion", f"{username} has been deleted from the database")
           self.show(self.student_management_frame, "student_management_frame", self.create_student_management_screen)
       except KeyError:
           messagebox.showwarning("User Error", "Please select a valid user")

    def create_reports_selection_screen(self):
        page_title = ttk.Label(
            self.reports_selection_frame, text="Reports",font=("Roboto", 36, 'underline')
        )
        page_title.pack(pady=20)

        class_reports_button = tk.Button(
            self.reports_selection_frame,
            text="Make a class report",
            command=lambda: self.show(self.class_reports_frame, "class_reports_frame", self.create_class_reports_screen),
            bg="#00796B",
            fg="white", font=("Roboto", 28, "bold"),
            relief="flat", bd=0
        )
        class_reports_button.pack(pady=10)

        individual_reports_button = tk.Button(
            self.reports_selection_frame,
            text="Make an individual report",
            command=lambda: self.show(self.individual_reports_frame, "individual_reports_frame", self.create_individual_reports_screen),
            bg="#00796B",
            fg="white", font=("Roboto", 28, "bold"),
            relief="flat", bd=0
        )
        individual_reports_button.pack(pady=10)

    def create_class_reports_screen(self):
        # file name text input
        class_file_name_label: ttk.Label = ttk.Label(self.class_reports_frame, text="File Name",font=("Roboto", 24))
        class_file_name_label.pack(pady=5)
        class_file_name: tk.Entry = tk.Entry(self.class_reports_frame, width=20, font=20)
        class_file_name.pack(pady=5)

        # company name text input
        class_company_name_label: ttk.Label = ttk.Label(self.class_reports_frame, text="Class Name",font=("Roboto", 24))
        class_company_name_label.pack(pady=5)
        class_company_name: tk.Entry = tk.Entry(self.class_reports_frame, width=20, font=20)
        class_company_name.pack(pady=5)

        # title text input
        class_title_label: ttk.Label = ttk.Label(self.class_reports_frame, text="Title Name",font=("Roboto", 24))
        class_title_label.pack(pady=5)
        class_title_name: tk.Entry = tk.Entry(self.class_reports_frame, width=20, font=20)
        class_title_name.pack(pady=5)

        # Print class report button
        print_class_button: tk.Button = tk.Button(
            self.class_reports_frame,
            text="Print All Users Report",
            command=lambda: self.print_class_report(class_file_name.get(), class_company_name.get(), class_title_name.get()),
            bg="#00796B",
            fg="white", font=("Roboto", 20, "bold"),
            relief="flat", bd=0)
        print_class_button.pack(pady=20)
        # --------------------------------------------------------------
    
    def create_individual_reports_screen(self):
        # file name text input
        file_name_label: ttk.Label = ttk.Label(self.individual_reports_frame, text="File Name",font=("Roboto", 20))
        file_name_label.pack(pady=5)

        file_name: tk.Entry = tk.Entry(self.individual_reports_frame, width=20, font=18)
        file_name.pack(pady=5)

        # company name text input
        company_name_label: ttk.Label = ttk.Label(self.individual_reports_frame, text="Class Name",font=("Roboto", 20))
        company_name_label.pack(pady=5)
        company_name: tk.Entry = tk.Entry(self.individual_reports_frame, width=20, font=18)
        company_name.pack(pady=5)

        # title text input
        title_label: ttk.Label = ttk.Label(self.individual_reports_frame, text="Title Name",font=("Roboto", 20))
        title_label.pack(pady=5)
        title_name: tk.Entry = tk.Entry(self.individual_reports_frame, width=20, font=18)
        title_name.pack(pady=5)

        # student dropdown
        student_label: ttk.Label = ttk.Label(self.individual_reports_frame, text="Select student", font=("Roboto", 20))
        student_label.pack(pady=10)

        all_users = self.current_user.access.admin_read_all_users()
        values = {}
        for user in all_users:
            fname = user["first_name"]
            lname = user["last_name"]
            username = fname + " " + lname
            values[username] = user["student_id"]

        student_combobox: ttk.Combobox = ttk.Combobox(
            self.individual_reports_frame,
            values=list(values),
            font=20)
        
        student_combobox.pack(pady=5)

        # date range selection
        self.cal = Calendar(self.individual_reports_frame, selectmode='day', year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, font=("Roboto", 12))
        self.cal.pack(pady=15)

        self.start_date = None
        self.end_date = None
        
        self.feedback_label = ttk.Label(self.individual_reports_frame, text="")
        self.feedback_label.pack(pady=10)

        # start date button
        start_date_button: tk.Button = tk.Button(
            self.individual_reports_frame, 
            text="Set Start Date", 
            command=self.set_start_date,
            bg = "#00796B",
            fg = "white",
            font = ("Roboto", 16, "bold"),
            relief = "flat",
            bd = 0,
            height = 1,
            width = 15,
            )
        start_date_button.pack(pady=10)
        
        # end date button
        end_date_button: tk.Button = tk.Button(
            self.individual_reports_frame, 
            text="Set End Date", 
            command=self.set_end_date,
            bg="#00796B",
            fg="white",
            font=("Roboto", 16, "bold"),
            relief="flat",
            bd=0,
            height=1,
            width=15,
            )
        end_date_button.pack(pady=15)

        # print specific user report button
        print_specific_user_button: tk.Button = tk.Button(
            self.individual_reports_frame,
            text="Print Specific User Report",
            command=lambda: self.print_specific_user_report(file_name.get(), company_name.get(), title_name.get(), self.start_date.strftime('%m/%d/%Y'), self.end_date.strftime('%m/%d/%Y'), student_combobox.get(), str(values[student_combobox.get()])),
            bg="#00796B",
            fg="white", font=("Roboto", 20, "bold"),
            relief="flat", bd=0)
        print_specific_user_button.pack(pady=20)

    def print_class_report(self, file_name, company_name, title):
        """creates class report in a folder called Reports"""
        self.current_user.report.create_class_pdf(file_name, company_name, title)
        self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen)

    def print_specific_user_report(self, file_name, company_name, title, start_date, end_date, name, student_id):
        """creates a user report in the same Reports folder"""
        self.current_user.report.create_user_specific_pdf(file_name, company_name, title, start_date, end_date, name, student_id)
        self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen)

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

    def student_selected(self, emp_id: str, window=0, constructor=0):
        """
        Makes a call to the database, using a specific user credentials
        :param emp_id: credential connected to the student in the database (4-digits)
        :param window: parent window
        :param constructor: Method used to create the screen
        :return: None
        """

        student = self.current_user.access.admin_get_row_all_users(emp_id)
    # ----------------------------------------------------

    # Backend functions
    def log_in(self):
        """
        Checks if the user has the right credentials to log in
        :return:
        """

        # Check if the username and PIN fields are fulfilled
        if self.pin.get():
            try:
                user = User(self.pin.get())
            except ValueError:
                    messagebox.showwarning("User Error", "User does not exist")
                    self.pin.set("")
                    return

            admin_status = user.access.admin_status
            if admin_status == 1:
                self.current_user = User(self.pin.get())
                self.show(self.admin_frame, "admin_frame", self.create_admin_panel_screen)
            elif admin_status == 0:
                # Checks if the credentials are in the database
                self.current_user = User(self.pin.get())
                if self.current_user.access.get_data_all_users("working_status") == 1:
                    self.show(self.clock_in_frame, "clock_in_frame", self.create_clock_out_screen)
                else:
                    self.show(self.clock_in_frame, "clock_in_frame", self.create_clock_in_screen)

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

    # # Extra functions
    # def exit_fullscreen(self):
    #     self.root.attributes("-fullscreen", False)

def sort_list(list):
    """
    Args:
        list: list of dicts. This data would come from the return of the function admin_read_all_users
    Return:
        Returns a list grouped by graduation year and sorted by last name within those groupings
    """
    list_sorted_grad_year = sorted(list, key=lambda x: x['graduation_year'])
    grad_years = {}
    for student in list_sorted_grad_year:
        year = student['graduation_year']
        if year not in grad_years:
            grad_years[year] = []
        grad_years[year].append(student)
    for year in grad_years:
        grad_years[year] = sorted(grad_years[year], key=lambda x: x['last_name'])
    flattened_list = [student for year in grad_years.values() for student in year]
    return flattened_list


gui = GUI()
gui.root.mainloop()
