from terse import main
from .test_invoke_helper import FILENAME
from .test_invoke_helper import main_impl
import os

def test_helper_did_not_create_file():
    assert not os.path.exists(FILENAME)
