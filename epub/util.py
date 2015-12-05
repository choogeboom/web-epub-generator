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


class SetGet:
    """
    Defines an interface for setting/getting multiple attributes with keyword arguments
    """
    def set(self, **kwargs):
        for prop_name in kwargs:
            self.__dict__[prop_name] = kwargs[prop_name]

    def get(self, *args):
        prop_values = []
        for prop_name in args:
            prop_values.append(self.__dict__[prop_name])
        return prop_values
