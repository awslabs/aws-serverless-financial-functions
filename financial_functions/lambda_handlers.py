from __future__ import print_function
import sys
import log_helper
sys.path.append('lib')
import numpy_financial as numpy
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import validation_json_schemas as schemas
import core as ff
from datetime import datetime

logger = log_helper.getLogger(__name__)


def __validate_arguments(function_name, arguments_json, json_schema):
    """
    Validate the arguments in the provided JSON against the provided json schema
    :param function_name:
    :param arguments_json:
    :param json_schema:
    :return: Dict containing whether the provided json is valid and an error message if validation failed.
    """
    try:
        validate(arguments_json, json_schema)
        return {'isValid': True}
    except ValidationError as err:
        logger.error("Invalid {} request with args: {}. Exception: {}".format(function_name, arguments_json, err))
        return {'isValid': False, 'error': err.message}


def __call_numpy(method, args):
    """
    Call a NumPy method with a given set of arguments
    :param method: NumPy method to call
    :param args: Arguments for the provided NumPy method
    :return: Result from NumPy
    """
    logger.info("Calling numpy.{} with args: {}".format(method, args))
    return {'result': getattr(numpy, method)(*args)}

def __call_ff(method, args):
    """
    Call a core financial function method with a given set of arguments
    :param method: Method to call
    :param args: Arguments for the provided method
    :return: Calculation result
    """
    logger.info("Calling ff.{} with args: {}".format(method, args))
    return {'result': getattr(ff, method)(*args)}


def fv_handler(request, context):
    """
    Future Value calculation
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("FV request: {}".format(request))

    validation_result = __validate_arguments('FV', request, schemas.fv_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['rate'], request['nper'], request.get('pmt', 0), request.get('pv', 0), request.get('type', 0)]
    return __call_numpy('fv', args)

def fvschedule_handler(request, context):
    """
    Returns the future value of an initial principal after applying a series of compound interest rates.
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("FVSCHEDULE request: {}".format(request))

    validation_result = __validate_arguments('FVSCHEDULE', request, schemas.fvschedule_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['principal'], request.get('schedule', [])]
    return __call_ff('fvschedule', args)

def pv_handler(request, context):
    """
    Present Value calculation
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("PV request: {}".format(request))

    validation_result = __validate_arguments('PV', request, schemas.pv_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['rate'], request['nper'], request.get('pmt', 0), request.get('fv', 0), request.get('type', 0)]
    return __call_numpy('pv', args)


def npv_handler(request, context):
    """
    Net Present Value of a cash flow series
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("NPV request: {}".format(request))

    validation_result = __validate_arguments('NPV', request, schemas.npv_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    # Need to append a 0 entry to the beginning of the values list for NumPy NPV to align with Excel
    # Excel assumes the investment begins one period before the first value cash flow whereas
    # NumPy assumes they begin at the same time.
    args = [request['rate'], [0] + request['values']]
    return __call_numpy('npv', args)


def xnpv_handler(request, context):
    """
    Net Present Value of a cash flow series that's not necessarily periodic.
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("XNPV request: {}".format(request))

    validation_result = __validate_arguments('XNPV', request, schemas.xnpv_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    if len(request['values']) != len(request['dates']):
        return {'error': 'values and dates must have the same length'}

    dates = list(map(lambda s: datetime.strptime(s, '%Y-%m-%d'), request['dates']))
    args = [request['rate'], request['values'], dates]
    return __call_ff('xnpv', args)


def pmt_handler(request, context):
    """
    Compute the payment against loan principal plus interest
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("PMT request: {}".format(request))

    validation_result = __validate_arguments('PMT', request, schemas.pmt_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['rate'], request['nper'], request['pv'], request.get('fv', 0), request.get('type', 0)]
    return __call_numpy('pmt', args)


def ppmt_handler(request, context):
    """
    Compute the payment against loan principal
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("PPMT request: {}".format(request))

    validation_result = __validate_arguments('PPMT', request, schemas.ppmt_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['rate'], request['per'], request['nper'], request['pv'], request.get('fv', 0), request.get('type', 0)]
    return __call_numpy('ppmt', args)


def irr_handler(request, context):
    """
    Internal Rate of Return calculation.
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("IRR request: {}".format(request))

    validation_result = __validate_arguments('IRR', request, schemas.irr_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    # IRR requires at least one positive and one negative value
    sorted_values = sorted(request.get('values'))
    values_length = len(request.get('values'))
    if sorted_values[0] > 0 or sorted_values[values_length - 1] <= 0:
        return {'error': "IRR requires at least one positive and one negative value"}

    args = [request['values']]
    return __call_numpy('irr', args)


def mirr_handler(request, context):
    """
    Modified Internal Rate of Return calculation.
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("MIRR request: {}".format(request))

    validation_result = __validate_arguments('MIRR', request, schemas.mirr_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    # MIRR requires at least one positive and one negative value
    sorted_values = sorted(request.get('values'))
    values_length = len(request.get('values'))
    if sorted_values[0] > 0 or sorted_values[values_length - 1] <= 0:
        return {'error': "MIRR requires at least one positive and one negative value"}

    args = [request['values'], request['finance_rate'], request['reinvest_rate']]
    return __call_numpy('mirr', args)


def xirr_handler(request, context):
    """
    Returns the internal rate of return for a schedule of cash flows that is not necessarily periodic.
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("XIRR request: {}".format(request))

    validation_result = __validate_arguments('XIRR', request, schemas.xirr_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    # XIRR requires at least one positive and one negative value
    sorted_values = sorted(request.get('values'))
    values_length = len(request.get('values'))
    if sorted_values[0] > 0 or sorted_values[values_length - 1] <= 0:
        return {'error': "XIRR requires at least one positive and one negative value"}

    if len(request['values']) != len(request['dates']):
        return {'error': 'values and dates must have the same length'}

    dates = list(map(lambda s: datetime.strptime(s, '%Y-%m-%d'), request['dates']))
    args = [request['values'], dates, request.get('guess', 0.1)]
    return __call_ff('xirr', args)


def nper_handler(request, context):
    """
    Number of periodic payments required to pay off a loan.
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("NPER request: {}".format(request))

    validation_result = __validate_arguments('NPER', request, schemas.nper_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['rate'], request.get('pmt', 0), request['pv'], request.get('fv', 0), request.get('type', 0)]
    result = __call_numpy('nper', args)
    # numpy.nper returns a numpy.ndarray object with the result in it . Need to unwrap the result.
    return dict(map(lambda entry: (entry[0], entry[1].item(0)), result.items()))


def rate_handler(request, context):
    """
    Rate of interest period.
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("Rate request: {}".format(request))

    validation_result = __validate_arguments('Rate', request, schemas.rate_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['nper'], request.get('pmt', 0), request['pv'], request.get('fv', 0), request.get('type', 0), request.get('guess', 0.10)]
    return __call_numpy('rate', args)


def effect_handler(request, context):
    """
    Effective annual interest rate
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("Effect request: {}".format(request))

    validation_result = __validate_arguments('Effect', request, schemas.effect_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['nominal_rate'], int(request['npery'])]
    return __call_ff('effect', args)


def nominal_handler(request, context):
    """
    Nominal annual interest rate
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("Nominal request: {}".format(request))

    validation_result = __validate_arguments('nominal', request, schemas.nominal_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}

    args = [request['effect_rate'], int(request['npery'])]
    return __call_ff('nominal', args)


def sln_handler(request, context):
    """
    Straight line depreciation of an asset for one period
    :param request: Dict containing the parameters to pass to the formula.
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("SLN request: {}".format(request))

    validation_result = __validate_arguments('sln', request, schemas.sln_schema)
    if not validation_result.get('isValid'):
        return {'error': validation_result.get('error')}
    if request['life'] == 0:
        return {'error': 'life cannot be zero'}

    args = [request['cost'], request['salvage'], request['life']]
    return __call_ff('sln', args)

