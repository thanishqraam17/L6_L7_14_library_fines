import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------
def test_returned_on_time():
    assert late_fine("student", 10, False) == 0

def test_unknown_member():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("alien", 5, False)

def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)

def test_zero_days_is_valid():
    # boundary: days_kept == 0 must NOT raise
    assert late_fine("student", 0, False) == 0

def test_faculty_overdue():
    assert late_fine("faculty", 35, False) == 5

def test_faculty_loan_period_is_30():
    # 20 days is overdue for a student but not for faculty
    assert late_fine("faculty", 20, False) == 0

def test_student_overdue():
    assert late_fine("student", 18, False) == 8

def test_exactly_at_loan_limit_no_fine():
    # boundary: overdue == 0 -> `overdue > 0` is False
    assert late_fine("student", 14, False) == 0

def test_one_day_overdue():
    # boundary: overdue == 1 -> `overdue > 0` is True
    assert late_fine("student", 15, False) == 2

def test_fine_capped_at_200():
    assert late_fine("guest", 64, False) == 200

def test_fine_exactly_200_not_capped():
    # boundary: fine == 200 -> `fine > 200` is False (guest: 40 * 5)
    assert late_fine("guest", 54, False) == 200

def test_fine_just_under_cap():
    assert late_fine("guest", 53, False) == 195

def test_damaged_book_surcharge():
    assert late_fine("student", 10, True) == 150

def test_damaged_and_overdue():
    assert late_fine("student", 18, True) == 158

def test_damaged_and_capped():
    assert late_fine("guest", 64, True) == 350


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

def test_cannot_borrow_high_fine():
    assert can_borrow(0, 101, "student") is False

def test_fine_exactly_100_still_allowed():
    # boundary: pending_fine == 100 -> `> 100` is False
    assert can_borrow(0, 100, "student") is True

def test_student_at_book_limit():
    assert can_borrow(3, 0, "student") is False

def test_student_just_under_limit():
    assert can_borrow(2, 0, "guest") is True

def test_faculty_can_borrow():
    assert can_borrow(9, 0, "faculty") is True

def test_faculty_at_book_limit():
    assert can_borrow(10, 0, "faculty") is False

def test_faculty_high_fine_blocked():
    assert can_borrow(0, 150, "faculty") is False


# ---------- renewal_status ----------
def test_renewal_denied_reservation():
    assert renewal_status(0, True, 5) == "denied"

def test_reservation_beats_limit():
    assert renewal_status(5, True, -3) == "denied"

def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"

def test_renewal_one_renewal_left():
    assert renewal_status(1, False, 5) == "renewed"

def test_renewal_overdue():
    assert renewal_status(0, False, -1) == "overdue"

def test_renewal_due_today_ok():
    # boundary: days_left == 0 -> `< 0` is False
    assert renewal_status(0, False, 0) == "renewed"

def test_renewal_ok():
    assert renewal_status(0, False, 5) == "renewed"
