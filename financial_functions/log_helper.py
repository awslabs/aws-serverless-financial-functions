import os
import sys
import logging

def getLogger(name):
    """
    Initializes logger with given name. Sets log level based on lambda environment variable value.
    """
    # get logger level from function env var and create logger
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    return logger
