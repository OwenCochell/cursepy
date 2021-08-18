"""
Formatters for use with CurseDescriptions.

We offer methods for normalising and formatting descriptions,
which are in HTML.

This can be as simple as striping HTML markups,
or as in-depth as loading said information into a custom class.
"""

import re

from typing import Any


class BaseFormat(object):
    """
    BaseFormat - Base class all formatters must inherit!

    We define some useful functionality for all formatters to implement.
    A 'formatter' is something that changes HTML content into something else.
    What the content gets converted to is up to the formatter!
    """

    def format(self, data: str) -> Any:
        """
        Formats the given string data.

        This is the entry point for the formatter!
        If formatting is enabled,
        then this method will be called with the given string to be formatted.

        :param data: Data to be formatted
        :type data: str
        :return: Formatted data, whatever that may be
        :rtype: Any
        :raises: NotImplementedError: Must be overridden in child class!
        """

        raise NotImplementedError("Must be implemented in child class!")


class NullFormatter(BaseFormat):
    """
    NullFormatter - As the name implies, does nothing!

    We simply return the data that we were provided with.
    """
 
    def format(self, data: str) -> str:
        """
        Returns the given data

        :param data: Data to format
        :type data: str
        :return: Given data
        :rtype: str
        """

        return data


class StripHTML(BaseFormat):
    """
    Strips all HTML tags and metadata using regular expressions.

    This is not a foolproof operation,
    and this could easily fail in many ways!
    """

    PATTERN = '<[^>]*>'

    def format(self, data: str) -> str:
        """
        Strips the given data of all HTML tags and metadata.

        :param data: Data to format
        :type data: str
        :return: Formatted string data
        :rtype: str
        """

        return str(re.sub(StripHTML.PATTERN, '', data))
 

class BSFormatter(BaseFormat):
    """
    Loads the data into the Beautiful Soup parser for further processing.

    The user can specify the parser to use.
    We use python's built in HTML parser by default,
    although another can be selected using class parameters.
    """

    DEFAULT='html.parser'
    LXML='lxml'
    HTML5LIB='html5lib'

    def __init__(self, parser='html.parser'):
        
        self.parser = parser

    def format(self, data: str) -> Any:
        """
        Sends the given data to the Beautiful Soup parser.
        We use the selected parser.

        :param data: HTML Data to parse
        :type data: str
        :return: BeautifulSoup object
        :rtype: Any
        """

        import bs4

        return bs4.BeautifulSoup(data, self.parser)
