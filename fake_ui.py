from User import User

# these would be user inputs
data = {"username": "Admin", "admin_status": 1}
admin = User("1234", data=data)

# these would be buttons
fake_button = int(input("(1 to clock in or 0 to clock out): "))
if fake_button == 1:
    admin.clock.clock_in()

if fake_button == 0:
    admin.clock.clock_out()

# you would work with this to extract data you want
print(admin.access.read_user_table("1234"))