from rest_framework.exceptions import Throttled


# I actually changed the approach from last commit because I didn't feel right to declare whole new global exception, just to add time in one class
class TimeThrottleMix:
    """
    To Inject time left (in integer), Now if the rate limit of API occurs this will help
    """
    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, Throttled) and response is not None:
            response.data['time_left'] = exc.wait
            response.data['detail_for_user'] = f"Too many request, please wait for {exc.wait} seconds"
            
        return response

        