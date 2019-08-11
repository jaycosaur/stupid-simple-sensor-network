import sys


def is_micropython():
    if sys.implementation.name == 'micropython':
        return True
    else:
        return False
