#!/usr/bin/python3
import os


def main():
    os.system('rm dist/* -rf')
    os.system('python3 setup.py sdist')
    os.system('python3 setup.py bdist_wheel --universal')
    os.system('twine upload dist/*')


if __name__ == '__main__':
    main()
