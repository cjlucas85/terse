import os
from contextlib import contextmanager


@contextmanager
def cwd(path):
    old_path = os.getcwd()
    os.chdir(path() if callable(path) else path)
    try:
        yield
    finally:
        os.chdir(old_path)


def in_dir(path):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            with cwd(path):
                return fn(*args, **kwargs)
        return wrapper
    return decorator

