import itertools

def flatten_args(*args):
    items = []
    for arg in args:
        if not isinstance(arg, type) and callable(arg):
            items.append(flatten_args(arg()))
        else:
            items.append(arg)
    return items


def on_exception(callback, *args):
    """Invoke callback if exception within args occurs. Reraise exception."""
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            try:
                return main_function(*wargs, **kwargs)
            except Exception as e:
                # Extract from function if provided one.
                if len(args) and not isinstance(args[0], type) and callable(args[0]):
                    exceptions = args[0]()
                else:
                    exceptions = args
                # Determine action
                if len(exceptions) == 0 or isinstance(e, exceptions):
                    callback()
                raise e
        return wrapper
    return decorator


def on_returned(callback, *args):
    """Invoke callback if return is in args. Returns value."""
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
                returned = main_function(*wargs, **kwargs)
                # Extract from function if provided one.
                if len(args) and not isinstance(args[0], type) and callable(args[0]):
                    exceptions = args[0]()
                else:
                    exceptions = args
                # Determine action
                if len(exceptions) == 0 and returned is None:
                    callback()
                elif returned in (exceptions):
                    callback()
                return returned
        return wrapper
    return decorator



"""
    Filter Exception
If exception occurs, invoke callback and return value or allow exception 
to rise.

    Filter Return
If function returns value within args, invoke callback and return value or 
allow exception to rise.

    Filter
Allows for either exception or return to be the trigger for the callback.
"""

def filter_returned(callback, default=None, return_map={}):
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            returned = main_function(*wargs, **kwargs)
            if returned in return_map.keys():
                return return_map[returned]
            else:
                return default
        return wrapper
    return decorator


def filter_exception(callback, default=None, exception_map={}):
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            try:
                return main_function(*wargs, **kwargs)
            except Exception as e:
                if type(e) in exception_map.keys():
                    raise exception_map[type(e)]
                elif default is not None:
                    raise default
                else:
                    raise e
        return wrapper
    return decorator


"""
    Ensure Return
Ensures that the function returns a value of some kind.
"""
def default_return(default=None):
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            returned = main_function(*wargs, **kwargs)
            return default if returned is None else returned
        return wrapper
    return decorator


def ensure_type(default=None, return_type=None):
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            returned = main_function(*wargs, **kwargs)
            if return_type is None:
                return default if returned is None else returned
            return default if type(returned) == return_type else returned
        return wrapper
    return decorator


"""
Check return
"""
def check_return_type(types=[]):
    def decorator(main_function):
        def wrapper(*wargs, **kwargs):
            returned = main_function(*wargs, **kwargs)
            if type(returned) not in types:
                raise TypeError()
            return returned
        return wrapper
    return decorator
