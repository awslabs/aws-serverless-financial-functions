# make sure we can find the app code
import sys, os
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../../financial_functions/')

import lambda_handlers as handlers

REQUIRED_PROPERTY_ERR = "'{}' is a required property"
INCORRECT_TYPE_ERR = "'{}' is not of type '{}'"


def test_fv_handler():
    # TODO test data types
    # rate, nper, pmt
    response = handlers.fv_handler({
        "rate": 0.004166666666667,
        "nper": 120,
        "pmt": -100
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 15528.227945

    # rate, nper, pv
    response = handlers.fv_handler({
        "rate": 0.004166666666667,
        "nper": 120,
        "pv": -100
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 164.700950

    # rate, nper, pmt, pv
    response = handlers.fv_handler({
        "rate": 0.004166666666667,
        "nper": 120,
        "pmt": -100,
        "pv": -100
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 15692.928894

    # rate, nper, pmt, pv
    response = handlers.fv_handler({
        "rate": 0.004166666666667,
        "nper": 120,
        "pmt": -100,
        "pv": -100,
        "type": 1
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 15757.629844


def test_fv_missing_rate():
    response = handlers.fv_handler({
        "nper": 120,
        "pmt": -100,
        "pv": -100
    }, None)

    assert 'error' in response


def test_fv_missing_nper():
    response = handlers.fv_handler({
        "rate": 0.004166666666667,
        "pmt": -100,
        "pv": -100
    }, None)

    assert 'error' in response


def test_fvschedule_handler():
    response = handlers.fvschedule_handler({
        "principal": 10000,
        "schedule": [0.05, 0.05, 0.035, 0.035, 0.035]
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 12223.614572


def test_fvschedule_missing_principal():
    response = handlers.fvschedule_handler({}, None)

    assert 'error' in response


def test_fvschedule_missing_schedule():
    response = handlers.fvschedule_handler({
        "principal": 10000
    }, None)

    assert 'error' in response


def test_pv_handler():
    # TODO test data types
    response = handlers.pv_handler({
        "rate": 0.004166666666666666,
        "nper": 120,
        "pmt": -100
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 9428.135033

    response = handlers.pv_handler({
        "rate": 0.004166666666666666,
        "nper": 120,
        "fv": 15692.93
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -9528.135704

    response = handlers.pv_handler({
        "rate": 0.004166666666666666,
        "nper": 120,
        "pmt": -100,
        "fv": 15692.93
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -100.000671

    response = handlers.pv_handler({
        "rate": 0.004166666666666666,
        "nper": 120,
        "pmt": -100,
        "fv": 15692.93,
        "type": 1
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -60.716775


def test_pv_missing_rate():
    response = handlers.pv_handler({
        "nper": 120,
        "pmt": -100,
        "fv": 15692.93
    }, None)

    assert 'error' in response


def test_pv_missing_nper():
    response = handlers.pv_handler({
        "rate": 0.004166666666666666,
        "pmt": -100,
        "fv": 15692.93
    }, None)

    assert 'error' in response


def test_irr_handler():
    # TODO test data types & empty values array
    response = handlers.irr_handler({
        "values": [-100, 39, 59, 55, 20]
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == 0.28095


def test_irr_missing_values():
    response = handlers.irr_handler({}, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("values")


def test_irr_values_wrong_type():
    response = handlers.irr_handler({
        "values": ["test1", "test2"]
    }, None)

    assert 'error' in response
    assert response.get('error') == INCORRECT_TYPE_ERR.format("test1", "number")


def test_irr_values_too_few():
    response = handlers.irr_handler({
        "values": [100]
    }, None)

    assert 'error' in response
    assert "is too short" in response.get('error')


def test_irr_values_missing_pos():
    response = handlers.irr_handler({
        "values": [-100, -200]
    }, None)

    assert 'error' in response
    assert response.get('error') == "IRR requires at least one positive and one negative value"


def test_irr_values_missing_neg():
    response = handlers.irr_handler({
        "values": [100, 200]
    }, None)

    assert 'error' in response
    assert response.get('error') == "IRR requires at least one positive and one negative value"


def test_mirr_handler():
    # TODO test data types & empty values array
    response = handlers.mirr_handler({
        "values": [-1000, 300, 400, 400, 300],
        "finance_rate": 0.12,
        "reinvest_rate": 0.10
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == 0.12876


def test_mirr_missing_values():
    response = handlers.mirr_handler({
        "finance_rate": 0.12,
        "reinvest_rate": 0.10
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("values")


def test_mirr_missing_finance_rate():
    response = handlers.mirr_handler({
        "values": [-1000, 300, 400, 400, 300],
        "reinvest_rate": 0.10
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("finance_rate")


def test_mirr_missing_reinvest_rate():
    response = handlers.mirr_handler({
        "values": [-1000, 300, 400, 400, 300],
        "finance_rate": 0.12,
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("reinvest_rate")


def test_mirr_values_too_few():
    response = handlers.mirr_handler({
        "values": [100],
        "reinvest_rate": 0.10,
        "finance_rate": 0.12
    }, None)

    assert 'error' in response
    assert "is too short" in response.get('error')


def test_mirr_values_missing_pos():
    response = handlers.mirr_handler({
        "values": [-100, -200],
        "reinvest_rate": 0.10,
        "finance_rate": 0.12
    }, None)

    assert 'error' in response
    assert response.get('error') == "MIRR requires at least one positive and one negative value"


def test_mirr_values_missing_neg():
    response = handlers.mirr_handler({
        "values": [100, 200],
        "reinvest_rate": 0.10,
        "finance_rate": 0.12
    }, None)

    assert 'error' in response
    assert response.get('error') == "MIRR requires at least one positive and one negative value"


def test_xirr_handler():
    response = handlers.xirr_handler({
        "values": [-100, 20, 40, 25],
        "dates": ['2016-01-01', '2016-4-1', '2016-10-1', '2017-2-1'],
        "guess": 0.1
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == -0.19674


def test_xirr_missing_values():
    response = handlers.xirr_handler({
        "dates": ['2016-01-01', '2016-4-1', '2016-10-1', '2017-2-1'],
        "guess": 0.1
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("values")


def test_xirr_missing_dates():
    response = handlers.xirr_handler({
        "values": [-100, 20, 40, 25],
        "guess": 0.1
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("dates")


def test_xirr_missing_guess():
    response = handlers.xirr_handler({
        "values": [-100, 20, 40, 25],
        "dates": ['2016-01-01', '2016-4-1', '2016-10-1', '2017-2-1']
    }, None)

    assert 'result' in response
    assert round(response.get('result'), 5) == -0.19674


def test_xirr_values_dates_different_length():
    response = handlers.xirr_handler({
        "values": [-100, 20, 40],
        "dates": ['2016-01-01', '2016-4-1', '2016-10-1', '2017-2-1']
    }, None)

    assert 'error' in response


def test_xirr_no_negative_value():
    response = handlers.xirr_handler({
        "values": [100, 20, 40, 25],
        "dates": ['2016-01-01', '2016-4-1', '2016-10-1', '2017-2-1']
    }, None)

    assert 'error' in response


def test_nper_handler():
    # TODO test data types
    response = handlers.nper_handler({
        "rate": 0.005833333333333,
        "pmt": -150,
        "pv": 8000
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == 64.07335

    # TODO Excel docs claim this isn't supported but Excel produces a value...
    response = handlers.nper_handler({
        "rate": 0.005833333333333,
        "pv": 8000,
        "fv": -100
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == -753.39346

    response = handlers.nper_handler({
        "rate": 0.005833333333333,
        "pmt": -150,
        "pv": 8000,
        "fv": -100
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == 63.40344

    response = handlers.nper_handler({
        "rate": 0.005833333333333,
        "pmt": -150,
        "pv": 8000,
        "fv": -100,
        "type": 1
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == 62.95762


def test_nper_missing_rate():
    response = handlers.nper_handler({
        "pmt": -150,
        "pv": 8000
    }, None)

    assert 'error' in response


def test_nper_missing_pmt():
    response = handlers.nper_handler({
        "rate": 0.005833333333333,
        "pv": 8000
    }, None)

    assert 'error' in response


def test_nper_missing_pv():
    response = handlers.nper_handler({
        "rate": 0.005833333333333,
        "pmt": -150,
    }, None)

    assert 'error' in response


def test_npv_handler():
    # TODO test data types

    response = handlers.npv_handler({
        "rate": 0.1,
        "values": [-10000, 3000, 4200, 6800]
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == 1188.44341


def test_npv_missing_rate():
    response = handlers.npv_handler({
        "values": [-100, 39, 59, 55, 20]
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("rate")


def test_npv_missing_values():
    response = handlers.npv_handler({
        "rate": 0.281,
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("values")



def test_xnpv_handler():
    response = handlers.xnpv_handler({
        "rate": 0.05,
        "values": [-10000, 2000, 2400, 2900, 3500, 4100],
        "dates": ['2016-1-1', '2016-2-1', '2016-5-1', '2016-7-1', '2016-9-1', '2017-1-1']
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 5) == 4475.44879


def test_xnpv_missing_rate():
    response = handlers.xnpv_handler({
        "values": [-10000, 2000, 2400, 2900, 3500, 4100],
        "dates": ['2016-1-1', '2016-2-1', '2016-5-1', '2016-7-1', '2016-9-1', '2017-1-1']
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("rate")


def test_xnpv_missing_values():
    response = handlers.xnpv_handler({
        "rate": 0.05,
        "dates": ['2016-01-01', '2016-2-1', '2016-5-1', '2016-7-1', '2016-9-1', '2017-1-1']
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("values")


def test_xnpv_missing_dates():
    response = handlers.xnpv_handler({
        "rate": 0.05,
        "values": [-10000, 2000, 2400, 2900, 3500, 4100]
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("dates")


def test_xnpv_values_dates_different_lengths():
    response = handlers.xnpv_handler({
        "rate": 0.05,
        "values": [-10000, 2000],
        "dates": ['2016-1-1', '2016-2-1', '2016-5-1']
    }, None)

    assert 'error' in response


def test_xnpv_invalid_date():
    response = handlers.xnpv_handler({
        "rate": 0.05,
        "values": [-10000],
        "dates": ['bogus']
    }, None)

    assert 'error' in response


def test_pmt_handler():
    # TODO test data types
    response = handlers.pmt_handler({
        "rate": 0.00625,
        "nper": 180,
        "pv": 200000
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -1854.02472

    response = handlers.pmt_handler({
        "rate": 0.00625,
        "nper": 180,
        "pv": 200000,
        "fv": 300000
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -2760.06180

    response = handlers.pmt_handler({
        "rate": 0.00625,
        "nper": 180,
        "pv": 200000,
        "fv": 300000,
        "type": 1
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -2742.918559


def test_pmt_missing_rate():
    response = handlers.pmt_handler({
        "nper": 180,
        "pv": 200000
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("rate")


def test_pmt_missing_nper():
    response = handlers.pmt_handler({
        "rate": 0.00625,
        "pv": 200000
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("nper")


def test_pmt_missing_pv():
    response = handlers.pmt_handler({
        "rate": 0.00625,
        "nper": 180,
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("pv")


def test_ppmt_handler():
    # TODO test data types
    response = handlers.ppmt_handler({
        "rate": 0.10,
        "per": 1,
        "nper": 3,
        "pv": 1000
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -302.114804

    response = handlers.ppmt_handler({
        "rate": 0.10,
        "per": 1,
        "nper": 3,
        "pv": 1000,
        "fv": 2000
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -906.344411

    response = handlers.ppmt_handler({
        "rate": 0.10,
        "per": 1,
        "nper": 3,
        "pv": 1000,
        "fv": 2000,
        "type": 1
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -914.858555


def test_ppmt_missing_rate():
    response = handlers.ppmt_handler({
        "per": 1,
        "nper": 3,
        "pv": 1000
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("rate")


def test_ppmt_missing_per():
    response = handlers.ppmt_handler({
        "rate": 0.10,
        "nper": 3,
        "pv": 1000
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("per")


def test_ppmt_missing_nper():
    response = handlers.ppmt_handler({
        "rate": 0.10,
        "per": 1,
        "pv": 1000
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("nper")


def test_ppmt_missing_pv():
    response = handlers.ppmt_handler({
        "rate": 0.10,
        "per": 1,
        "nper": 3,
    }, None)

    assert 'error' in response
    assert response.get('error') == REQUIRED_PROPERTY_ERR.format("pv")


def test_rate_handler():
    # TODO test data types
    response = handlers.rate_handler({
        "nper": 6,
        "pmt": -200,
        "pv": 1000
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 0.054718

    response = handlers.rate_handler({
        "nper": 6,
        "pv": 1000,
        "fv": -100
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == -0.318708

    response = handlers.rate_handler({
        "nper": 6,
        "pmt": -200,
        "pv": 1000,
        "fv": 0.10
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 0.054695

    response = handlers.rate_handler({
        "nper": 6,
        "pmt": -200,
        "pv": 1000,
        "fv": 0.10,
        "type": 1
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 0.079278


def test_rate_missing_nper():
    response = handlers.rate_handler({
        "pmt": -200,
        "pv": 1000,
        "fv": 0.10
    }, None)

    assert 'error' in response


def test_rate_missing_pv():
    response = handlers.rate_handler({
        "nper": 6,
        "pmt": -200,
        "fv": 0.10
    }, None)

    assert 'error' in response


def test_effect_handler():
    response = handlers.effect_handler({
        "nominal_rate": 0.12,
        "npery": 12
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 0.126825


def test_effect_handler_non_int_npery():
    response = handlers.effect_handler({
        "nominal_rate": 0.12,
        "npery": 12.7
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 0.126825


def test_effect_missing_nominal_rate():
    response = handlers.effect_handler({
        "npery": 12
    }, None)

    assert 'error' in response


def test_effect_missing_npery():
    response = handlers.effect_handler({
        "nominal_rate": 0.12
    }, None)

    assert 'error' in response


def test_nominal_handler():
    response = handlers.nominal_handler({
        "effect_rate": 0.12,
        "npery": 12
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 0.113866


def test_nominal_handler_non_int_npery():
    response = handlers.nominal_handler({
        "effect_rate": 0.12,
        "npery": 12.7
    }, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 0.113866


def test_nominal_missing_effect_rate():
    response = handlers.nominal_handler({
        "npery": 12
    }, None)

    assert 'error' in response


def test_nominal_missing_npery():
    response = handlers.nominal_handler({
        "effect_rate": 0.12
    }, None)

    assert 'error' in response


def test_sln_handler():
    response = handlers.sln_handler({
        "cost": 5000,
        "salvage": 300,
        "life": 10
    }, None)
    assert 'result' in response
    assert response.get('result') == 470


def test_sln_handler_missing_cost():
    response = handlers.sln_handler({
        "salvage": 300,
        "life": 10
    }, None)
    
    assert 'error' in response


def test_sln_handler_missing_salvage():
    response = handlers.sln_handler({
        "cost": 5000,
        "life": 10
    }, None)
    
    assert 'error' in response


def test_sln_handler_missing_life():
    response = handlers.sln_handler({
        "cost": 5000,
        "salvage": 300
    }, None)
    
    assert 'error' in response


def test_sln_handler_zero_life():
    response = handlers.sln_handler({
        "cost": 5000,
        "salvage": 300,
        "life": 0
    }, None)
    
    assert 'error' in response
