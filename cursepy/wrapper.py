"""
cursepy wrapper classes.

These classes are designed to work with specific games,
and make getting information about them much easier.
The class you probably want to work with is the CurseClient.
"""

from typing import Tuple

from cursepy.handlers.base import HandlerCollection
from cursepy.classes import base
from cursepy.classes.search import SearchParam
from cursepy.handlers.maps import DEFAULT_MAP


class CurseClient(HandlerCollection):
    """
    CurseClient - the client class most people will use!

    We implement the handler management and callback features outlined in the HandlerCollection.
    We do some extra things here and there to make life much easier for the end user. 

    We define some entry points for calling handlers.
    These functions will be called by the users actually using these handlers.
    We define some arguments that should be defined,
    as well as what we expect the functions to return.

    This class also provides some entry points into the loaded handlers.
    This provides a standardized way of interacting with handlers.
    """

    def load_default(self):
        """
        We simply load the cursepy default handler map.
        """
        
        self.load_handlers(DEFAULT_MAP)

    def games(self) -> Tuple[base.CurseGame]:
        """
        Returns a tuple of all games supported on curseforge.

        This call can be somewhat intensive,
        so it's a good idea to not call it often.
        Make a note of the relevant game's information!

        :raises NotImplementedError: Must be overridden in child class!
        :return: Tuple of CurseGame instances
        :rtype: Tuple[base.CurseGame]
        """

        return self.handle(0)

    def game(self, id: int) -> base.CurseGame:
        """
        Returns information on a specific game.

        You will need to provide the game ID.
        Game information will be returned in a CurseGame instance.

        :param id: ID of the game to get
        :type id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: CurseGame instance representing the game
        :rtype: base.CurseGame
        """

        return self.handle(1, id)

    def catagories(self) -> Tuple[base.CurseCategory, ...]:
        """
        Gets ALL valid categories on CurseForge.

        This call can get expensive, so call in moderation!

        :return: Tuple of CurseCategory instances
        :rtype: Tuple[base.CurseCategory, ...]
        """

        return self.handle(2)

    def category(self, category_id: int) -> base.CurseCategory:
        """
        Returns information on a category for a specific game.

        You will need to provide a category ID.

        :param game_id: ID of the game
        :type game_id: int
        :param category_id: ID of the category
        :type category_id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: CurseCategory instance representing the category
        :rtype: base.CurseCategory
        """

        return self.handle(3, category_id)

    def sub_category(self, category_id: int) -> Tuple[base.CurseCategory, ...]:
        """
        Gets the sub-categories of the given category.

        We return a tuple of CurseCategory instances
        representing the sub-categories

        :param category_id: ID of category to get sub-catagories for
        :type category_id: int
        :return: Tuple of CurseCategories representing the sub-categories
        :rtype: Tuple[base.CurseCategory, ...]
        """

        return self.handle(4, category_id)

    def iter_search(self, game_id: int, category_id: int, search: SearchParam=None) -> base.CurseAddon:
        """
        Iterates over all results from the search operation.

        We automatically bump the SearchParam by one after
        each call. We will keep yielding until
        we receive a tuple that has a length of zero,
        which at that point we will raise a 'StopIteration' exception.

        Because we only bump the index value,
        we will start on the index that was provided by the
        SearchParam object. For example,
        if the index starts at one, then we will return
        each addon from that page on.

        We use the 'search' method under the hood.

        This method is best used in for loops/situations
        where iterators are used!
        Because we are a generator,
        calling this method on it's own is not recommended!
        If you want a list of values,
        use the 'list()' method on us.

        :param game_id: Game ID to search under
        :type game_id: int
        :param category_id: Category ID to search under
        :type cat_id: int
        :param search: Search Parameter to use
        :type search: SearchParam
        :return: Each CurseAddon that returned during the search operation.
        :rtype: base.CurseAddon
        :raises: StopIteration: When we have run out of search content
        """

        # Check if we should generate a SearchParam:

        if search is None:

            # None provided, let's create one:

            search = self.get_search()

        while True:

            # Get the current page of results:

            results = self.search(game_id, category_id, search)

            # Check to see if the page is empty:

            if not results:

                # No results! Raise 'StopIteration'!

                raise StopIteration()

            # Iterate over the result:

            for item in results:

                # Yield the result:

                yield item

            # Bump the index and continue:

            search.index =+ 1

    def addon(self, addon_id: int) -> base.CurseAddon:
        """
        Gets information on a specific addon.

        You will need to provide an addon ID,
        which can be found by searching a game category.

        :param addon_id: Addon ID
        :type addon_id: int
        :raises NotImplementedError: Must be overridden in child class
        :return: CurseCategory instance representing the addon
        :rtype: base.CurseAddon
        """

        return self.handle(5, addon_id)

    def search(self, game_id: int, category_id: int, search: SearchParam=None) -> Tuple[base.CurseAddon, ...]:
        """
        Searches the given game and category for addons.

        The game_id and category_id parameters are required for searching,
        but the search parameter can optionally be provided to fine-tune to search.

        Each implementation has diffrent search backends,
        so it is important to pass the correct search instance!

        The wrappers will implement search checking,
        to ensure only the correct search parameters are used. 

        :param game_id: ID of the game to search under
        :type game_id: int
        :param category_id: Category to search under
        :type category_id: int
        :param search: Search options to fine tune the search, optional
        :type search: Any
        :return: Tuple of addons that matched the search parameters
        :rtype: Tuple[base.CurseAddon, ...]
        :raises: TypeError: If the search object fails the search check
        """ 

        # Check if we should generate a dummy SearchParam:

        if search is None:

            # Create dummy search param:

            search = SearchParam()

        return self.handle(6, game_id, category_id, search)

    def addon_description(self, addon_id: int) -> base.CurseDescription:
        """
        Gets the description of a specific addon.

        You will need to provide an addon ID,
        which can be found by searching a game category.

        :param addon_id: Addon ID
        :type addon_id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: CurseDescription instance representing the addon's description
        :rtype: base.CurseDescription
        """

        return self.handle(7, addon_id)

    def addon_files(self, addon_id: int) -> Tuple[base.CurseFile]:
        """
        Gets a list of files associated with the addon.

        You will need to provide an addon ID,
        which can be found by searching a game category.

        :param addon_id: Addon ID
        :type addon_id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: Tuple of CurseFile instances representing the addon's files
        :rtype: Tuple[base.CurseFile]
        """

        return self.handle(8, addon_id)

    def addon_file(self, addon_id: int, file_id:int) -> base.CurseFile:
        """
        Gets information on a specific file associated with an addon.

        You will need to provide an addon ID,
        as well as a file ID, which can be found by getting a list of all files

        :param addon_id: Addon ID
        :type addon_id: int
        :param file_id: File ID
        :type file_id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: CurseFile instance representing the addon file
        :rtype: base.CurseFile
        """

        return self.handle(9, addon_id, file_id)

    def file_description(self, addon_id: int, file_id: int) -> base.CurseDescription:
        """
        Gets a description of an addon file.

        You will need to provide a addon ID and a file ID.
        We return a CurseDesciprion object representing the description.

        :param addon_id: Addon ID
        :type addon_id: int
        :param file_id: File ID
        :type file_id: int
        :return: CurseDescription representing the description
        :rtype: base.CurseDescription
        """

        return self.handle(10, addon_id, file_id)


class MinecraftWrapper(CurseClient):
    """
    MinecraftWrap - Wrapper for working with Minecraft data!

    Minecraft is one of the most popular games on CurseForge.
    Because of this, we think it is appropriate to include a wrapper
    for solely working with Minecraft data.

    We offer a lot of convince methods,
    most notably are the methods for searching/getting addons in a specific category.
    This will automate the search operation,
    filling in the necessary info when necessary.
    This means that you as the user will not have to work(as much) with IDs! 
    """

    # Game ID:

    GAME_ID = 432

    # Category IDs:

    RESOURCE_PACKS = 12
    MODPACKS = 4471
    MODS = 6
    WORLDS = 17

    def search_resource_packs(self, search: SearchParam=None) -> Tuple[base.CurseAddon, ...]:
        """
        Searches the Resource Packs category for addons.
        We use the given SearchParam for the search operation.

        :param search: SearchParam to use, default to None
        :type search: SearchParam, optional
        :return: Tuple of CurseAddons
        :rtype: Tuple[base.CurseAddon, ...]
        """

        # Search the resource packs:

        return self.search(MinecraftWrapper.GAME_ID, MinecraftWrapper.RESOURCE_PACKS, search)

    def search_modpacks(self, search: SearchParam=None) -> Tuple[base.CurseAddon, ...]:
        """
        Searches the Modpacks category for addons.
        Again, we use the SearchParam for the search operation.

        :param search: SearchParameters to use, defaults to None
        :type search: SearchParam, optional
        :return: Tuple of CurseAddons
        :rtype: Tuple[base.CurseAddon, ...]
        """

        # Search the modpacks:

        return self.search(MinecraftWrapper.GAME_ID, MinecraftWrapper.MODPACKS, search)

    def search_mods(self, search: SearchParam=None) -> Tuple[base.CurseAddon, ...]:
        """
        Searches the Mods category for addons.
        Again, we use the SearchParam for the search operation.

        :param search: SearchParam to use, defaults to None
        :type search: SearchParam, optional
        :return: Tuple of CurseAddons
        :rtype: Tuple[base.CurseAddon]
        """

        # Search the mods:

        return self.search(MinecraftWrapper.GAME_ID, MinecraftWrapper.MODS, search)

    def search_worlds(self, search: SearchParam=None) -> Tuple[base.CurseAddon, ...]:
        """
        Searches the Worlds category for addons.
        Again, we use the SearchParam for the search operation.

        :param search: SearchParam to use, defaults to None
        :type search: SearchParam, optional
        :return: Tuple of CurseAddons, optional
        :rtype: Tuple[base.CurseAddon, ...]
        """

        # Search the worlds:

        return self.search(MinecraftWrapper.GAME_ID, MinecraftWrapper.WORLDS, search)
