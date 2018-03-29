import lambda_handlers as handlers
import validation_json_schemas as schemas
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import log_helper
import sys

logger = log_helper.getLogger(__name__)

def financial_functions_handler(request, context):
    """
    This function takes in an arbritary financial function and its parameters as inputs and returns the result of that calculation
    :param request: Dict containing the financial function name (function_name) and its parameters (args)
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("financial function request: {}".format(request))

    try:
        validate(request, schemas.wrapper_schema)
    except ValidationError as err:
        logger.info("Invalid request: {}. Exception: {}".format(request, err))
        return {'error': err.message}

    function_name = request['function_name']
    function_handler_name = function_name + "_handler"
    if hasattr(handlers, function_handler_name):
        return getattr(handlers, function_handler_name)(request['args'], context)
    else:
        return {"error": "Invalid function name: " + function_name + ". Please see documentation for help on supported functions"}
