# Python terse Library
This module provides a collection of function decorators to handle common procedures done on the entry and exit points.

## Installation
This library can be installed using pip with the following command.

```bash
pip install terse
```

## Directory

### In Directory
Before the function is executed, the current working directory is saved and the directory is changed to the provided **path**. After the function has completed, the directory is changed to the saved working directory.

```python
from terse import in_dir
from glob import glob
import os

@in_dir('/sys/class/net')
def interfaces():
    return glob('*')

print(os.getcwd())
print(interfaces())
print(os.getcwd())
```

## On Exit

### No Raise
Decorator will catch all exceptions leaked or produced by callee. If provided with **callback** function, then the callback will only be invoked when an exception occurs. If provided with **instead_return**, then the value will be returned when an exception occurs.

```python
from terse import no_except

def simple_log(function, exception):
    print(exception)

@no_raise(instead_return=False)
def example(raise_exception=False):
    if raise_exception:
        raise Exception("exception from example")
    return True

assert example()
assert example(False) == False
```

### On Returned
Decorator will invoke **callback** whenever a value in **args** is returned by function.

```python
from terse import on_returned
from enum import Enum


class Status(Enum):
    SUCCESS = 0
    FAILED = 1
    CONNECTION_FAILURE = 2
    DISK_FAILURE = 3


def log(function, returned):
    print("LOG: %s" % returned)


@on_returned(log, Status.FAILED, Status.CONNECTION_FAILURE, Status.DISK_FAILURE)
def example1(val):
    return val

assert example1(Status.SUCCESS) == Status.SUCCESS
# prints "LOG: Status.FAILED"
assert example1(Status.FAILED) == Status.FAILED
# prints "LOG: Status.CONNECTION_FAILURE"
assert example1(Status.CONNECTION_FAILURE) == Status.CONNECTION_FAILURE
# prints "LOG: Status.DISK_FAILURE"
assert example1(Status.DISK_FAILURE) == Status.DISK_FAILURE
```

### On Raised
Decorator will invoke **callback** whenever exception of type in **args** is raised by function.

```python
from terse import on_exception

def simple_log(function, returned):
    print(returned)

@on_raised(simple_log, ZeroDivisionError)
def divide(a, b):
    return a / b

assert divide(1, 0) == 0.0
try:
    divide(1, 0)
except ZeroDivisionError:
    print("Caught exception")
```
