import importlib
import os

from typing import Callable, Any

FUNCTION_NAME = os.getenv("FUNCTION_NAME")


def lambda_handler(event, context):
    if not FUNCTION_NAME:
        raise ValueError("Please specify the environment variable `FUNCTION_NAME`")

    m = importlib.import_module(name='app.%s' % FUNCTION_NAME)
    if not hasattr(m, 'lambda_handler'):
        raise Exception(f'function `{FUNCTION_NAME}` has no `lambda_handler` function')

    handler: Callable[[Any, Any], Any] = getattr(m, 'lambda_handler')
    if not callable(handler):
        raise Exception(f'lambda handler for function `{FUNCTION_NAME}` is not callable!')
    
    return handler(event, context)
