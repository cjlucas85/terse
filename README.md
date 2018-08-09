# Python terse Library
This module provides a collection of function decorators to handle common procedures done on the entry and exit points.

## Installation
This library can be installed using pip with the following command.

```bash
pip install terse
```

## Directory

### In Directory
Before the function is executed, the current working directory is saved and the directory is changed to the provided **path**. After the function has completed, the directory is changed to the saved working directory. *Caution: This is intended for single threaded usage. Threads should use absolute paths.*

```python
from terse import in_dir
from glob import glob
import os

# Returns all files and directories at file system's root.
@in_dir('/')
def root_files():
    return glob('*')

# Prints current working directory.
print(os.getcwd())
# Prints fils gathered from root.
print(root_files())
# Demonstrates current working directory is preserved.
print(os.getcwd())
```

## Invoke

### Main
Sets the function up to be the file's main function. If the file is __main__, 
then the function is executed. The return value will attempt to be converted 
to a value that can be passed to sys.exit; however if no value can be 
converted, it's assumed the function exited successfully.

Traditionally in Python you do the following to create the main entry point 
in the file.
```python
def main():
    print("Hello World!")


if __name__ == '__main__':
    main()
```

This can be replaced by the following.
```python
from terse import main

@main
def main_impl():
    print("Hello World!")
```



## On Exit

### No Raise
Decorator will catch all exceptions leaked or produced by callee. If provided
with **callback** function, then the callback will only be invoked when an
exception occurs. If provided with **instead_return**, then the value will be 
returned when an exception occurs.

```python
from terse import no_except

def log(function, exception):
    print('LOG: %s' % exception)

# If exception is given, raise given exception.
# Otherwise, return True
@no_raise(instead_return=False, callback=log)
def example(exception=None):
    if exception:
        raise exception
    return True

# Example with no parameters raises no exceptions,
# makes no calls to log, returns True.
assert example() == True

# Example with parameter raises given exception,
# makes a call to log, surpresses exception and
# returns False.
assert example(False) == False
```

### On Returned
Decorator will invoke **callback** whenever a value in **args** is returned by 
function.

```python
from terse import on_returned
from enum import Enum

class Status(Enum):
    SUCCESS = 0
    FAILED = 1
    CONNECTION_FAILED = 2
    DISK_FAILED = 3

def log(function, returned):
    print("LOG: %s" % returned)

# The following are examples for two uses of on_returned.
# First is for any return value and the second is for a 
# set of return values.



# ANY RETURN VALUE

# Function example_any returns any value passed in.
# on_returned will invoke log for any return value.
@on_returned(log)
def example_any(val):
    return val
    
# Log invoked: prints "LOG: Status.SUCCESS"
assert example_any(Status.SUCCESS) == Status.SUCCESS

# Log invoked: prints "LOG: Status.FAILED"
assert example_any(Status.FAILED) == Status.FAILED

# Log invoked: prints "LOG: None"
assert example_any(None) == None

# Log invoked: prints "LOG:1"
assert example_any(1) == 1



# SET OF RETURN VALUES

# Function example_set returns any value passed in.
# on_returned will invoke log whenever values FAILED, 
# CONNECTION_FAILED or DISK_FAILED from enum Status are
# returned by example.
@on_returned(log, Status.FAILED, Status.CONNECTION_FAILED, Status.DISK_FAILED)
def example_set(val):
    return val
    
# log is not invoked.
assert example_set(Status.SUCCESS) == Status.SUCCESS

# Log invoked: prints "LOG: Status.FAILED"
assert example_set(Status.FAILED) == Status.FAILED

# Log invoked: prints "LOG: Status.CONNECTION_FAILURE"
assert example_set(Status.CONNECTION_FAILED) == Status.CONNECTION_FAILED

# Log invoked: prints "LOG: Status.DISK_FAILURE"
assert example_set(Status.DISK_FAILED) == Status.DISK_FAILED
```

### On Raised
Decorator will invoke **callback** whenever exception of type in **args** is 
raised by function.

```python
from terse import on_exception

def log(function, exception):
    print(returned)

# The following are examples for two uses of on_raised.
# First is for any exception and the second is a set of
# exceptions.



# ANY EXCEPTION EXAMPLE

# If exception is given, raise given exception.
# Otherwise, return True
# on_raised will invoke log for all exceptions
# raised by example_any.
@on_raised(log)
def example_any(exception=None)
    if exception:
        raise exception
    return True

# example_any is given no exceptions to throw.
# Therefore, it will raise nothing and return True.
assert example_any() == True

# example_any is given ZeroDivisionError exception.
# It will raise ZeroDivisionError instance.
# on_raised detects exception raised and invokes log.
try:
    example_any(ZeroDivisionError())
    assert False
except ZeroDivisionError:
    pass

# example_any is given ValueError exception.
# It will raise ValueError instance.
# on_raised detects exception raised and invokes log.
try:
    example_any(ValueError())
    assert False
except ValueError:
    pass

# example_any is given KeyError exception.
# It will raise KeyError instance.
# on_raised detects exception raised and invokes log.
try:
    example_any(KeyError())
    assert False
except ValueError:
    pass



# SET OF EXCEPTIONS EXAMPLE

# If exception is given, raise given exception.
# Otherwise, return True.
# on_raised will only invoke log for ZeroDivisionError
# and ValueError. All other exceptions are ignored by
# on_raised.
@on_raised(log, ZeroDivisionError, ValueError)
def example_set(exception=None)
    if exception:
        raise exception
    return True

# example_set is given no exceptions to throw.
# Therefore, it will raise nothing and return True.
assert example_set() == True

# example_set is given ZeroDivisionError exception.
# It will raise ZeroDivisionError instance.
# on_raised detects exception raised and invokes log.
try:
    example_set(ZeroDivisionError())
    assert False
except ZeroDivisionError:
    pass

# example_set is given ValueError exception.
# It will raise ValueError instance.
# on_raised detects exception raised and invokes log.
try:
    example_set(ValueError())
    assert False
except ValueError:
    pass

# example_set is given KeyError exception.
# It will raise KeyError instance.
# example_set detects exception, but it will not
# invoke log because KeyError is not in the set of
# exceptions to be tracked.
try:
    example_set(KeyError())
    assert False
except ValueError:
    pass

```
