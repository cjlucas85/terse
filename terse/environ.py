import os
from contextlib import contextmanager


@contextmanager
def template_environ(set_func, **kwargs):
    old_values = {}
    for key, val in kwargs.items():
        try:
            old_values[key] = os.environ[key]
        except KeyError:
            old_values[key] = None
        os.environ[key] = str(set_func(key, val))
    try:
        yield
    finally:
        for key, val in old_values.items():
            if val is not None:
                os.environ[key] = val
            else:
                os.environ[key] = ""
                del os.environ[key]


@contextmanager
def set_environ(**kwargs):
    with template_environ(lambda k, v: v, **kwargs):
        yield


@contextmanager
def postfix_environ(**kwargs):
    with template_environ(lambda k, v: os.environ[k] + v, **kwargs):
        yield


@contextmanager
def prefix_environ(**kwargs):
    with template_environ(lambda k, v: v + os.environ[k], **kwargs):
        yield


def set_env(**kwargs):
    def decorator(fn):
        def wrapper(*fn_args, **fn_kwargs):
            with set_environ(**kwargs):
                return fn(*fn_args, **fn_kwargs)
        return wrapper
    return decorator


def prefix_env(**kwargs):
    def decorator(fn):
        def wrapper(*fn_args, **fn_kwargs):
            with prefix_environ(**kwargs):
                return fn(*fn_args, **fn_kwargs)
        return wrapper
    return decorator


def postfix_env(**kwargs):
    def decorator(fn):
        def wrapper(*fn_args, **fn_kwargs):
            with postfix_environ(**kwargs):
                return fn(*fn_args, **fn_kwargs)
        return wrapper
    return decorator
