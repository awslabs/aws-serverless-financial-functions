import pytest

from datetime import date
import core as ff

def test_fvschedule():
    assert ff.fvschedule(10000, [0.05, 0.05, 0.035, 0.035, 0.035]) == 12223.614571875
    assert ff.fvschedule(100, [0.04, 0.06, 0.05]) == 115.752
    
def test_xnpv():
    assert ff.xnpv(
        0.05,
        [-10000, 2000, 2400, 2900, 3500, 4100],
        [date(2016, 1, 1), date(2016, 2, 1), date(2016, 5, 1), date(2016, 7, 1), date(2016, 9, 1), date(2017, 1, 1)]
    ) == 4475.448794482614
    
    assert ff.xnpv(
        0.05,
        [-10000, 2000, 2400, 2900, 3500, 4100, 5300],
        [date(2016, 1, 1), date(2016, 2, 1), date(2016, 5, 1), date(2016, 7, 1), date(2016, 9, 1), date(2017, 1, 1), date(2017, 2, 3)]
    ) == 9500.179287007002
    
    assert ff.xnpv(
        0.05,
        [-1000, 300, 400, 400, 300],
        [date(2011, 12, 1), date(2012, 1, 1), date(2013, 2, 1), date(2014, 3, 1), date(2015, 4, 1)]
    ) == 289.90172260419456
    
def test_xnpv_mismatched_lists():
    with pytest.raises(ValueError):
        ff.xnpv(0.05, [-100], [])
    
def test_xnpv_dates_not_chronological_order():
    with pytest.raises(ValueError):
        ff.xnpv(
            0.05,
            [-10000, 2000],
            [date(2016, 2, 1), date(2016, 1, 1)])
    
def test_xirr():
    assert ff.xirr(
        [-100, 20, 40, 25],
        [date(2016, 1, 1), date(2016, 4, 1), date(2016, 10, 1), date(2017, 2, 1)]
    ) == -0.19674386129832788
    
    assert ff.xirr(
        [-100, 20, 40, 25, 8, 15],
        [date(2016, 1, 1), date(2016, 4, 1), date(2016, 10, 1), date(2017, 2, 1), date(2017, 3, 1), date(2017, 6, 1)]
    ) == 0.0944390744445201
    
    assert ff.xirr(
        [-1000, 300, 400, 400, 300],
        [date(2011, 12, 1), date(2012, 1, 1), date(2013, 2, 1), date(2014, 3, 1), date(2015, 4, 1)],
        0.1
    ) == 0.23860325587217
    
def test_xirr_mismatched_lists():
    with pytest.raises(ValueError):
        ff.xirr([-100], [])
    
def test_xirr_dates_not_chronological_order():
    with pytest.raises(ValueError):
        ff.xirr(
            [-100, 20],
            [date(2016, 4, 1), date(2016, 1, 1)])

def test_effect():
    assert ff.effect(.12, 12) == 0.12682503013196977
    assert ff.effect(.10, 4) == 0.10381289062499954
    assert ff.effect(.10, 2) == 0.10250000000000004
    assert ff.effect(.025, 2) == 0.02515624999999999

def test_nominal():
    assert ff.nominal(.12, 12) == 0.11386551521499655
    assert ff.nominal(.10, 4) == 0.09645475633778045
    assert ff.nominal(.10, 2) == 0.09761769634030326
    assert ff.nominal(.025, 12) == 0.02471803523811289

def test_sln():
    assert ff.sln(5000, 300, 10) == 470
    assert ff.sln(10000, 1000, 5) == 1800
    assert ff.sln(500, 100, 8) == 50
    assert ff.sln(1200, 200, 6) == 166.66666666666666
