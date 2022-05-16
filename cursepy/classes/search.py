"""
Search objects for representing search parameters.

We also provide methods for conveting these values
into something handlers can understand.
"""

from dataclasses import dataclass, asdict, field
from typing import Any, Optional
from urllib.parse import urlencode


@dataclass
class SearchParam:
    """
    SearchParam - Providing search options for efficient searching.

    We define the following values:

        * filter - Term to search for(i.e, 'Inventory Mods')
        * index - Addon index to start on
        * pageSize - Number of items to display per page
        * gameVersion - Game version to search under
        * sort - Sorting method to use

    If any of these parameters are unnecessary,
    then the handler can ignore them.
    We use camel case for the parameter names.

    Users should probably use the setter methods for 
    configuring this class!
    Users can also use the 'set' method to configure
    all search parameters in only one call.
    """

    searchFilter: Optional[str] = field(default=None) # Term to search for
    index: Optional[int] = field(default=0)  # Index of addon to start on
    pageSize: Optional[int] = field(default=20)  # Number of items to display per page
    gameVersion: Optional[int] = field(default=None)  # Game version to use
    sort: Optional[int] = field(default=None) # Sort method to use

    # Some sort options defined here:

    FEATURED = 0
    POPULARITY = 1
    LAST_UPDATE = 2
    NAME = 3
    AUTHOR = 4
    TOTAL_DOWNLOADS = 5


    def asdict(self) -> dict:
        """
        Converts ourselves into a dictionary.

        :return: Dictionary of SearchParam values
        :rtype: dict
        """

        return asdict(self)

    def set_page(self, num: int):
        """
        Changes the page we are on.
        
        We change the index to reach the next page, 
        we use this equation to determine this:
        
        index = num * pageSize
        
        This will set the index to the given page.
        For example, if we set the page number to two,
        have a page size of five, and an index of three,
        then the resulting index after the operation will be 10.

        :param page: Page number to set the index to
        :type page: int
        """
        
        self.index = num * self.pageSize
        
    def bump_page(self, num: int=1):
        """
        Bumps the page up or down.
        
        We add the page change to the current index using this equation:
        
        index += num * pageSize
        
        This will change the page in relation with the current index.
        For example, if you bump the page up twice, have a page size of five
        and an index of three, the resulting index after the operation will be 13.

        You can supply a negative number to bump the page downward.
        If the index ends up below zero, then we will set the index to zero.

        :param num: Number of pages to bump
        :type num: int
        """
        
        self.index += num * self.pageSize
        
        if self.index < 0:
            
            self.index = 0

def url_convert(search: SearchParam, url: str='') -> str:
    """
    Converts the given search object into valid URL parameters.
    If the 'base_url' is provided,
    then we will append the converted values to the base_url.

    :param search: The SearchParam to convert
    :type search: SearchParam
    :param url: URL to build off of
    :type url: str
    :return: Converted SearchParameter value
    :rtype: str
    """

    # Get a dictionary of parameters:

    params = search.asdict()
    final = {}

    # Iterate over the parameters:

    for key in params:

        # Check to ensure value is not None:

        if params[key] is not None:

            # Add this to the final:

            final[key] = params[key]

    # Encode and return the values:

    return url + urlencode(final)
