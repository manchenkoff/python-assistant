import asyncio
import functools


def async_function(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    return inner
