from LbnlIon7350Interface.LbnlIon7350Interface import getter

def test_is_valid_interval():
    assert getter.is_valid_interval(5)
    assert not getter.is_valid_interval(0)
    assert not getter.is_valid_interval(1)
    assert not getter.is_valid_interval(13)

    assert getter.is_valid_interval(2)
    assert getter.is_valid_interval(12)

def test_get_date():
    valid = getter.get_date('2012-01-01 23:59:59')
    assert valid

    invalid = getter.get_date('2012-01-01')
    assert not invalid

    invalid2 = getter.get_date('2012-13-01 23:59:59')
    assert not invalid2
