"""
Utility functions
"""
import random
import string


def get_soup(tag):
    t = tag
    while t.parent is not None:
        t = t.parent
    return t


def generate_random_string(size=12, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
