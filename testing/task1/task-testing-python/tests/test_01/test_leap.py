import pytest
from simple_library_01.functions import is_leap


def test_is_leap_wrong_year():
    with pytest.raises(AttributeError):
        is_leap(-1)

def test_is_leap_mod_400():
    assert True == is_leap(800)
    
def test_is_leap_mod_100():
    assert False == is_leap(300)

def test_is_leap_mod_4():
    assert True == is_leap(8)
    
def test_is_not_leap():
    assert False == is_leap(55)
    