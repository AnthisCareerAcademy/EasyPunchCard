from Clock import Clock


def test_clock_in_pushing(setup_user):
    """
    Test that clocking in correctly updates the database.
    """
    lock = Clock(student_id="5678")

    # Mock initial database state
    conn = setup_user.get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO all_users (student_id, total_minutes, start_time, working_status) VALUES (?, ?, ?, ?)",
                   ("5678", 50, None, 0))
    conn.commit()

    # Perform the clock-in action
    Clock.clock_in()

    # Verify working_status and start_time are updated
    cursor.execute("SELECT working_status, start_time FROM all_users WHERE student_id = ?", ("5678",))
    working_status, start_time = cursor.fetchone()
    assert working_status == 1, f"Expected working_status to be 1, but got {working_status}"
    assert start_time is not None, "Expected start_time to be set, but got None"

    cursor.close()
    conn.close()