import string
import sys


def cleaner(x):
    """
    cleaning function required for neural model
    """
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]


setattr(sys.modules["__main__"], "cleaner", cleaner)
