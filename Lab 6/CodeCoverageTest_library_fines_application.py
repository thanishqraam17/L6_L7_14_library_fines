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

def test_faculty_overdue():
    # faculty loan = 30 days, 5 days overdue * Rs.1
    assert late_fine("faculty", 35, False) == 5

def test_student_overdue():
    # student loan = 14 days, 4 days overdue * Rs.2
    assert late_fine("student", 18, False) == 8

def test_fine_capped_at_200():
    # guest: 50 overdue * 5 = 250 -> capped at 200
    assert late_fine("guest", 64, False) == 200

def test_damaged_book_surcharge():
    assert late_fine("student", 10, True) == 150


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

def test_cannot_borrow_high_fine():
    assert can_borrow(0, 101, "student") is False

def test_faculty_can_borrow():
    assert can_borrow(9, 0, "faculty") is True


# ---------- renewal_status ----------
def test_renewal_denied_reservation():
    assert renewal_status(0, True, 5) == "denied"

def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"

def test_renewal_overdue():
    assert renewal_status(0, False, -1) == "overdue"

def test_renewal_ok():
    assert renewal_status(0, False, 5) == "renewed"
