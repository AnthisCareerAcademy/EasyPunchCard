from User import User

pin = input("give pin: ")

# check if pin exists
try:
    current_user = User(pin)
except ValueError:
    print(f"{pin} isn't in the database")
    quit()

# if user exists and IS admin
if current_user.access.admin_status == 1:
    print("Admin Panel:")

    action = input("add user ('add') or see all users ('see'): ")

    if action == "add":
        student_id = input("student_id: ")
        username = input("username: ")
        admin_status = int(input("admin_status: "))
        current_user.access.add_user(student_id, username, admin_status)

    if action == "see":
        view_what = input("all users ('all') or single user ('single'): ")

        if view_what == 'all':
            print(current_user.access.admin_read_all_users())

        elif view_what == 'single':
            student_id = int(input("student_id: "))
            print(current_user.access.admin_read_self_table(student_id))

    # option to somehow log out

# this user is NON admin
else:
    print("Student Panel:")
    working_status = current_user.access.get_data_all_users("working_status")

    action = input("clock in ('in') or clock out ('out'): ")

    if action == "in":
        current_user.clock.clock_in()

    if action == "out":
        current_user.clock.clock_out()
        
    # option to somehow log out

