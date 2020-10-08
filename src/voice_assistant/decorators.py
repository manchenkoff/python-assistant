import asyncio
from functools import partial, wraps


def async_function(func):
    @wraps(func)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, partial(func, *args, **kwargs))

    return inner
