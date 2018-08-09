from terse import main

FILENAME = 'made_by_test_invoke_helper.txt'

@main
def main_impl():
    with open(FILENAME) as f:
        f.write('made by test invoke helper.txt')
