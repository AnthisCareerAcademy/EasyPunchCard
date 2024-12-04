from User import User


def test_clock_in_pushing():
    """
    Test that clocking in correctly updates the database.
    """
    user = User("1010")

    # Mock initial database state
    conn = user.access.get_db()
    cursor = conn.cursor()

    # Perform the clock-in action
    user.clock.clock_in()

    # Verify working_status and start_time are updated
    cursor.execute("SELECT working_status FROM all_users WHERE student_id = ?", ("1010",))
    working_status = cursor.fetchall()[0][0]
    assert working_status == 1, f"Expected working_status to be 1, but got {working_status}"

    # Clocks the user out
    user.clock.clock_out()

    cursor.close()
    conn.close()