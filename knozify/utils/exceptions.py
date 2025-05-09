from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled

def show_time_exception_handler(exc, context):
    # let DRF cook first and get the original exception
    response = exception_handler(exc, context)

    # Now get the wait time from throttle and add it to response, simple right :) (took me 1-2 hour to get here)
    if isinstance(exc, Throttled) and response is not None:
        response.data['time_left'] = exc.wait
    return response