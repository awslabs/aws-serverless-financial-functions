import wrapper_handler as wrapper

def test_wrapper_handler():
    request = {
        "function_name": "fv",
        'args': {
            "rate": 0.004166666666667,
            "nper": 120,
            "pmt": -100
        }
    }

    response = wrapper.financial_functions_handler(request, None)
    assert 'result' in response
    assert round(response.get('result'), 6) == 15528.227945

def test_wrapper_handler_invalid_function_name():
    response = wrapper.financial_functions_handler({"function_name":"not_available", 'args': {'foo': 'bar'}}, None)
    assert 'error' in response

def test_wrapper_handler_invalid_function_args():
    response = wrapper.financial_functions_handler({"function_name":"fv", 'args': {}}, None)
    assert 'error' in response

