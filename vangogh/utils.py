"""
Utilities for testing & timing
"""

from functools import wraps
import time


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__module__}.{func.__name__} : {end-start:.3}")
        return r

    return wrapper
