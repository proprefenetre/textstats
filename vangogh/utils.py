""" Utility snippets """


def timethis(func):
    """ timing decorator """
    from functools import wraps
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__module__}.{func.__name__} : {end-start:.3}")
        return r

    return wrapper


def _rm_diacritics(self, text):
    " Remove accented or otherwise decorated characters "
    import unicodedata

    return "".join(
        c
        for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )
