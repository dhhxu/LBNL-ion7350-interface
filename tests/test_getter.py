"""
Unit tests for getter.py
"""

import pytest
from LbnlIon7350Interface.LbnlIon7350Interface import getter

def test_is_valid_interval():
    """
    Check that is_valid_interval works correctly for legal interval values
    """
    assert getter.is_valid_interval(1)
    assert getter.is_valid_interval(2)
    assert getter.is_valid_interval(12)

def test_invalid_interval():
    """
    Check that is_valid_interval works correctly for illegal interval values
    """
    assert not getter.is_valid_interval(0)
    assert not getter.is_valid_interval(13)
    assert not getter.is_valid_interval(5.0)
    assert not getter.is_valid_interval(-4)

def test_valid_index():
    """
    Check that is_valid_index works correctly for non-negative integers
    """
    assert getter.is_valid_index(1)
    assert getter.is_valid_index(100)

def test_invalid_index():
    """
    Check that is_valid_index works correctly for negative integers and
    floats
    """
    assert not getter.is_valid_interval(-4)
    assert not getter.is_valid_interval(5.0)

def test_get_date():
    """
    Check that get_date works correctly for valid datetime.
    """
    valid = getter.get_date('2012-01-01T23:59:59')
    assert valid

def test_get_date_bad():
    """
    Check that get_date raises error for only date input.
    """
    invalid = getter.get_date('2012-01-01')
    assert not invalid

def test_get_date_bad2():
    """
    Check that get_date raises error for datetime missing 'T' between the
    date and time.
    """
    invalid2 = getter.get_date('2012-01-01 23:59:59')
    assert not invalid2

def test_get_date_bad3():
    """
    Check that get_date raises error for datetime containing erroneous hour.
    """
    invalid3 = getter.get_date('2012-01-01T24:59:59')
    assert not invalid3

def test_run_batch_bad_date():
    """
    Check that run_batch raises error for an invalid start date argument
    """
    date = '2015-20-01T00:00:00'
    root = '~/'
    end = '2015-01-02T00:00:00'
    with pytest.raises(ValueError) as bad_date:
        getter.run_batch(root, date, end)

    assert bad_date.value.message == 'Invalid/missing dates'

def test_run_batch_bad_date2():
    """
    Check that run_batch raises error for an invalid end date argument
    """
    date = '2015-20-01T00:00:00'
    root = '/'
    start = '2015-01-01T00:00:00'
    with pytest.raises(ValueError) as bad_date:
        getter.run_batch(root, start, date)

    assert bad_date.value.message == 'Invalid/missing dates'

def test_run_batch_bad_date_order():
    """
    Check that run_batch raises error when end date comes before start date
    """
    root = '/'
    start = '2015-01-01T00:00:00'
    end = '2015-01-02T00:00:00'
    with pytest.raises(ValueError) as bad_order:
        getter.run_batch(root, end, start)

    assert bad_order.value.message == 'Start date must come before end date'

def test_run_batch_bad_root():
    """
    Check that run_batch raises error for non-existent root path argument
    """
    root = 'blahasdfjadksx'
    start = '2015-01-01T00:00:00'
    end = '2015-01-02T00:00:00'
    with pytest.raises(ValueError) as bad_root:
        getter.run_batch(root, start, end)

    assert bad_root.value.message == 'Root directory not found'

def test_run_update_bad_interval():
    """
    Check that run_update raises error for illegal interval argument
    """
    root = '~'
    interval = -1
    with pytest.raises(ValueError) as bad_interval:
        getter.run_update(root, interval)

    assert bad_interval.value.message == 'Invalid interval'

