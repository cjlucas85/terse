# Python terse Library
This module provides a collection of function decorators to handle common procedures done on the entry and exit points.

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

### No Exception
Decorator will catch all exceptions leaked or produced by callee. If provided with **callback** function, then the callback will only be invoked when an exception occurs. If provided with **instead_return**, then the value will be returned when an exception occurs.

```python
from terse import no_except

def simple_log(function, exception):
  print(exception)

@no_except(instead_return=False)
def example(raise_exception=False):
  if raise_exception:
    raise Exception("exception from example")
  return True

assert example()
assert example(False) == False
```
