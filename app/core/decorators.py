from functools import wraps
from typing import Type

from fastapi import HTTPException

from app.core.exceptions import WeatherAppBaseException


def custom_exceptions_to_http_error(
    exceptions_to_handle: list[Type[WeatherAppBaseException]],
):
    def wrapper(router_function):
        @wraps(router_function)
        async def wrapped(*args, **kwargs):
            try:
                return await router_function(*args, **kwargs)
            except WeatherAppBaseException as err:
                if type(err) in exceptions_to_handle:
                    raise HTTPException(
                        status_code=err.http_status_code, detail=str(err)
                    ) from err
                raise err

        return wrapped

    return wrapper
