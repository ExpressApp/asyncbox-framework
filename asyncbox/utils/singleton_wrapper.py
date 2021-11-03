"""Wrapper to ensure that singleton building function invoked only once."""

from functools import wraps
from typing import Any, Callable


def singleton_wrapper(global_name: str) -> Callable:
    """Wrap singleton building function to ensure is is invoked exactly once."""

    def wrapper(building_function: Callable) -> Callable:  # noqa: WPS430
        @wraps(building_function)
        def wrapped(*args: Any, **kwargs: Any) -> Any:  # noqa: WPS430
            if global_name in globals():  # noqa: WPS421
                return globals().get(global_name)  # noqa: WPS421
            application = building_function(*args, **kwargs)
            globals()[global_name] = application  # noqa: WPS421
            return application

        return wrapped

    return wrapper
