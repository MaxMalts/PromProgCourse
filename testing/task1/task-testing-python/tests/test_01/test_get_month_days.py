import pytest
from simple_library_01.functions import get_month_days


def test_get_month_days_year_1930():
    assert 30 == get_month_days(1930, 3)

def test_get_month_days_is_leap():
    assert 29 == get_month_days(800, 2)

def test_get_month_days_month_2():
    assert 28 == get_month_days(33, 2)
    
def test_get_month_days_wrong_month():
    with pytest.raises(AttributeError):
        get_month_days(33, 13)

def test_get_month_days_30():
    assert 30 == get_month_days(33, 6)
    
def test_get_month_days_31():
    assert 31 == get_month_days(33, 7)