"""
Search objects for representing search parameters.

We also provide methods for converting these values
into something handlers can understand.
"""

from dataclasses import dataclass, asdict, field
from typing import Any, Optional
from urllib.parse import urlencode


@dataclass
class SearchParam(object):
    """
    SearchParam - Object that contains various parameters for searching.

    This object is used for both addon searching, and file sorting.
    It is up to the handler receiving this object to use and interpret these values!
    The handler can ignore any values they see fit.

    We define the following values:

        * gameId - ID of the game to search addons for
        * rootCategoryId - Filter by section ID
        * categoryId - Filter by category ID
        * gameVersion - Filter by game version string
        * searchFilter - Filter by free text search, just like a search bar
        * sortField - Filter mods in a certain way (featured, popularity, total_downloads, ect.), use constants for defining this!
        * sortOrder - Order of search results (ascending or descending), use constants for defining this!
        * modLoaderType - Filter mods associated with a specific mod loader
        * gameVersionTypeId - Only show files tagged with a specific version ID
        * slug - Filter by slug
        * index - Index of the first item to include in the results
        * pageSize - Number of items to show in each page
    """

    gameId: int = field(default=None)
    rootCategoryId: int = field(default=None)
    categoryId: int = field(default=None)
    gameVersion: str = field(default=None)
    searchFilter: str = field(default=None)
    sortField: int = field(default=None)
    sortOrder: str = field(default=None)
    modLoaderType: int = field(default=None)
    gameVersionTypeId: int = field(default=None)
    slug: str = field(default=None)
    index: int = field(default=0)
    pageSize: int = field(default=20)

    # Constants for defining sort filters:

    FEATURED = 1
    POPULARITY = 2
    LAST_UPDATE = 3
    NAME = 4
    AUTHOR = 5
    TOTAL_DOWNLOADS = 6
    CATEGORY = 7
    GAME_VERSION = 8

    # Constants for defining sort order:

    ASCENDING = 'asc'
    DESCENDING = 'desc'

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

        self.index = max(self.index, 0)


def url_convert(search: dict, url: str='') -> str:
    """
    Converts the given dictionary into valid URL parameters.
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

    final = {key: search[key] for key in search if search[key] is not None}

    # Encode and return the values:

    return url + '?' + urlencode(final)
