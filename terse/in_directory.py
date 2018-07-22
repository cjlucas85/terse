import os


class InDirectory:
    def __init__(self, path):
        self.old_cwd = os.getcwd()
        self.path = path

    def __enter__(self):
        self.old_cwd = os.getcwd()
        try:
            os.chdir(self.path())
        except TypeError:
            os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)


def in_dir(path):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            with InDirectory(path):
                return fn(*args, **kwargs)
        return wrapper
    return decorator
