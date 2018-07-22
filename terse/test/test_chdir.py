import os
from terse import InDirectory
from terse import in_dir

#TODO Test lambda argument
def test_chdir():
    cwd = os.getcwd()
    with InDirectory('..'):
        assert cwd != os.getcwd()
    assert cwd == os.getcwd()
    with InDirectory(lambda: '..'):
        assert cwd != os.getcwd()
    assert cwd == os.getcwd()

#TODO Test lambda argument
def test_in_dir():
    cwd = os.getcwd()
    @in_dir('..')
    def func(ocwd, oval):
        assert ocwd != os.getcwd()
        return oval
    val = 123456789
    assert func(cwd, val) == val
    assert cwd == os.getcwd()
    @in_dir(lambda: '..')
    def func2(ocwd, oval):
        assert ocwd != os.getcwd()
        return oval
    val = 987654321
    assert func2(cwd, val) == val
    assert cwd == os.getcwd()
