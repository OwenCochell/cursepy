"""
We outline objects used for defining search parameters.

We provide a few implementations for diffrent protocols,
and even some search options for specific games.
"""

from dataclasses import dataclass, asdict, field
from typing import Any, Optional
from urllib.parse import urlencode


@dataclass
class BaseSearch(object):
    """
    BaseSearch - Class all child search options should inherit!

    We define some parameters and features that should be used
    and overloaded by child classes.

    We remain ambiguous, and specific implementations will be used 
    for specific games.
    """

    def convert(self) -> dict:
        """
        Converts the parameters of this class into something
        the handlers will understand.

        By default, we just return a dictionary
        representing this object. 
        """

        return self.to_dict()

    def to_dict(self) -> dict:
        """
        Converts this dataclass into a dictionary.

        :return: Dictionary of this dataclass
        :rtype: dict
        """

        return asdict(self)


@dataclass
class URLSearch(BaseSearch):
    """
    URLSearch - Class for generating URL parameters.

    We automatically iterate over our search attributes,
    and use urllib to encode the attributes into a URL valid string.
    """

    def convert(self) -> str:
        """
        Converts the attributes in this class
        into valid URL parameters.

        This can be appended to the end of a URL
        for a valid URL search.
        
        If any parameters are 'None',
        then they will not be included.

        :return: Encoded URL variables
        :rtype: str
        """

        # Get a dictionary of parameters:

        params = self.to_dict()
        final = {}

        # Iterate over the parameters:

        for key in params:

            # Check to ensure value is not None:

            if params[key] is not None:

                # Add this to the final:

                final[key] = params[key]

        # Encode and return the values:

        return urlencode(final)


@dataclass
class ForgeSVCSearch(URLSearch):
    """
    Search class for ForgeSVC handlers.

    We define the needed attributes,
    as well as some constants that can be used
    to fine tune the search options.
    """

    filter: Optional[str] = field(default=None) # Term to search for
    index: Optional[int] = field(default=None)  # Page of search results to view
    pageSize: Optional[int] = field(default=None)  # Number of items to display per page
    gameVersion: Optional[int] = field(default=None)  # Game version to use
    sort: Optional[int] = field(default=None) # Sort method to use

    # Sort options:

    FEATURED = 0
    POPULARITY = 1
    LAST_UPDATE = 2
    NAME = 3
    AUTHOR = 4
    TOTAL_DOWNLOADS = 5
