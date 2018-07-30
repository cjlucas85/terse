from terse import on_raised
from terse import on_returned
from terse import no_raise


on_raised_counter = 0
def test_on_raised_none():
    global on_raised_counter
    # SETUP PREDICTABLE COUNTER FUNCTION
    def increment_counter(f, e):
        global on_raised_counter
        on_raised_counter += 1
    # SETUP PASS THROUGH FUNCTION
    @on_raised(increment_counter)
    def invoke_error(error):
        if isinstance(error, Exception):
            raise error
        else:
            return error
    # TEST PASS THROUGH
    on_raised_counter = 0
    assert invoke_error(0) == 0
    assert on_raised_counter == 0
    assert invoke_error(1) == 1
    assert on_raised_counter == 0
    assert invoke_error(2) == 2
    assert on_raised_counter == 0
    # TEST DEFAULT
    try:
        invoke_error(IOError())
        assert False
    except IOError:
        assert on_raised_counter == 1
    try:
        invoke_error(OSError())
        assert False
    except OSError:
        assert on_raised_counter == 2
    try:
        invoke_error(NotImplementedError())
        assert False
    except NotImplementedError:
        assert on_raised_counter == 3


def test_on_raised_singular():
    global on_raised_counter
    # SETUP PREDICTABLE COUNTER FUNCTION
    def increment_counter(f, r):
        global on_raised_counter
        on_raised_counter += 1
    # SETUP PASS THROUGH FUNCTION
    @on_raised(increment_counter, IndexError)
    def invoke_error_one(error):
        if isinstance(error, Exception):
            raise error
        else:
            return error
    # TEST PASS THROUGH
    on_raised_counter = 0
    assert invoke_error_one(0) == 0
    assert on_raised_counter == 0
    assert invoke_error_one(1) == 1
    assert on_raised_counter == 0
    assert invoke_error_one(2) == 2
    assert on_raised_counter == 0
    # TEST SINGULAR
    try:
        invoke_error_one(IndexError())
        assert False
    except IndexError:
        assert on_raised_counter == 1
    try:
        invoke_error_one(OSError())
        assert False
    except OSError:
        assert on_raised_counter == 1
    try:
        invoke_error_one(NotImplementedError())
        assert False
    except NotImplementedError:
        assert on_raised_counter == 1


def test_on_raised_many():
    global on_raised_counter
    # SETUP PREDICTABLE COUNTER FUNCTION
    def increment_counter(f, r):
        global on_raised_counter
        on_raised_counter += 1
    # SETUP PASS THROUGH FUNCTION
    @on_raised(increment_counter, IndexError, KeyError)
    def invoke_error_many(error):
        if isinstance(error, Exception):
            raise error
        else:
            return error
    # TEST PASS THROUGH
    on_raised_counter = 0
    assert invoke_error_many(0) == 0
    assert on_raised_counter == 0
    assert invoke_error_many(1) == 1
    assert on_raised_counter == 0
    assert invoke_error_many(2) == 2
    assert on_raised_counter == 0
    # TEST MULTIPLE
    try:
        invoke_error_many(IndexError())
        assert False
    except IndexError:
        assert on_raised_counter == 1
    try:
        invoke_error_many(KeyError())
        assert False
    except KeyError:
        assert on_raised_counter == 2
    try:
        invoke_error_many(NotImplementedError())
        assert False
    except NotImplementedError:
        assert on_raised_counter == 2


on_returned_counter = 0
def test_on_returned_empty():
    global on_returned_counter
    def increment_counter(f, r):
        global on_returned_counter
        on_returned_counter += 1
    @on_returned(increment_counter)
    def return_value(returned_value):
        return returned_value
    on_returned_counter = 0
    assert on_returned_counter == 0
    assert return_value(None) == None
    assert on_returned_counter == 1
    assert return_value(1) == 1
    assert on_returned_counter == 2
    assert return_value(2) == 2
    assert on_returned_counter == 3


def test_on_returned_singular():
    global on_returned_counter
    def increment_counter(f, r):
        global on_returned_counter
        on_returned_counter += 1
    @on_returned(increment_counter, 1)
    def return_value_one(returned_value):
        return returned_value
    on_returned_counter = 0
    assert on_returned_counter == 0
    assert return_value_one(1) == 1
    assert on_returned_counter == 1
    assert return_value_one(0) == 0
    assert on_returned_counter == 1
    assert return_value_one(1) == 1
    assert on_returned_counter == 2
    assert return_value_one(0) == 0
    assert on_returned_counter == 2


def test_on_returned_many():
    global on_returned_counter
    def increment_counter(f, r):
        global on_returned_counter
        on_returned_counter += 1
    @on_returned(increment_counter, 1, 2)
    def return_value_many(returned_value):
        return returned_value
    on_returned_counter = 0
    assert on_returned_counter == 0
    assert return_value_many(1) == 1
    assert on_returned_counter == 1
    assert return_value_many(2) == 2
    assert on_returned_counter == 2
    assert return_value_many(3) == 3
    assert on_returned_counter == 2
    assert return_value_many(4) == 4
    assert on_returned_counter == 2


def test_no_raise():
    @no_raise(instead_return=False)
    def f1():
        return True
    @no_raise(instead_return=False)
    def f2():
        raise Exception()
    @no_raise(instead_return=10)
    def f3():
        raise OSError()
    # RUN ALL THREE
    assert f1() == True
    assert f2() == False
    assert f3() == 10
