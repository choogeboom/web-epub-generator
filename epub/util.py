"""
Utility functions
"""
import random
import string
import urllib.request


def get_soup(tag):
    t = tag
    while t.parent is not None:
        t = t.parent
    return t


def generate_random_string(size=12, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def read_html(url: str) -> str:
    """
    Read the html from a URL into a UTF-8 string

    :param url: The URL of the page to load
    :return: A string containing the HTML of the specified page
    :raise urllib.request.URLError: on errors with opening the page
    """
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html.decode('utf-8')


def read_file(file_name: str) -> str:
    with open(file_name, 'r') as file:
        return file.read()


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
