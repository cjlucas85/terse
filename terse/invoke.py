import sys


def main(func=None):
    """Main Decorator"""
    def decorator(main_function):
        if main_function.__module__ == '__main__':
            returned = main_function()
            try:
                sys.exit(int(returned))
            except (TypeError, ValueError):
                sys.exit(0)
    if callable(func):
        return decorator(func)
    else:
        return decorator
