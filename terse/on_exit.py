def on_raised(callback, *args):
    """Invoke callback if exception within args occurs. Reraise exception."""
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            try:
                return main_function(*wargs, **kwargs)
            except Exception as e:
                if len(args) == 0 or isinstance(e, args):
                    callback(main_function, e)
                raise e
        return wrapper
    return decorator


def on_returned(callback, *args):
    """Invoke callback if return is in args. Returns value."""
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
                returned = main_function(*wargs, **kwargs)
                if len(args) == 0:
                    callback(main_function, returned)
                elif returned in (args):
                    callback(main_function, returned)
                return returned
        return wrapper
    return decorator


def no_raise(callback=lambda f, e: 0, instead_return=None):
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            try:
                return main_function(*wargs, **kwargs)
            except Exception as e:
                callback(main_function, e)
                return instead_return
        return wrapper
    return decorator
