import importlib
import os
import json
import logging

from typing import Callable, Any

logger = logging.getLogger()

FUNCTION_NAME = os.getenv("FUNCTION_NAME")


def lambda_handler(event, context):
    if not FUNCTION_NAME:
        raise ValueError("Please specify the environment variable `FUNCTION_NAME`")

    m = importlib.import_module(name='lambda_functions.%s' % FUNCTION_NAME)
    if not hasattr(m, 'lambda_handler'):
        raise Exception(f'function `{FUNCTION_NAME}` has no `lambda_handler` function')

    handler: Callable[[Any, Any], Any] = getattr(m, 'lambda_handler')
    if not callable(handler):
        raise Exception(f'lambda handler for function `{FUNCTION_NAME}` is not callable!')

    try:
        return handler(event, context)

    except ValueError as e:
        logger.error(e)
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': "application/json",
            },
            'body': json.dumps({
                "message": str(e)
            })
        }

    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': "application/json",
            },
            'body': json.dumps({
                "message": "Sorry, there was an error whilst processing your request, please try again"
            })
        }
