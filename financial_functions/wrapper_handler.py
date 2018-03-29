import lambda_handlers as handlers
import log_helper
import sys

logger = log_helper.getLogger(__name__)

def financial_functions_handler(request, context):
    """
    This function takes in an arbritary financial function and its parameters as inputs and returns the result of that calculation
    :param request: Dict containing the financial function name and its parameters
    :param context: Lambda execution context
    :return: Dict with a 'result' entry containing the result of the calculation
    """
    logger.info("financial function request: {}".format(request))

    function_name = request.get("function_name")
    if function_name is None: 
        return {"error": "Please provide a function name using the function_name parameter"}
        
    function_handler_name = function_name + "_handler"
    if hasattr(handlers, function_handler_name):
        request.pop('function_name', None) #to ensure that the schema validation doesn't fail
        return getattr(handlers, function_handler_name)(request, context)
    else:
        return {"error": "Invalid function name: "+ function_name+". Please see documentation for help on supported functions" }