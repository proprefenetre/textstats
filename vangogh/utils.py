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


def remove_diacritics(self, text):
    " Remove accented or otherwise decorated characters "
    import unicodedata

    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    )


# flatten nested dictonaries
def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        # new_key = parent_key + sep + k if parent_key else k
        new_key = k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
