"""
Backend componets for communicating with curseforge.
"""


from http.client import TEMPORARY_REDIRECT
import json
from typing import Any, Tuple, Callable, Union
from functools import wraps

from capy.classes import base
from capy.proto import URLProtocol


class BaseBackend(object):

    """
    BaseBackend - All child backends must inherit this class!

    A backend is a component that interacts with curseforge in some way.
    The way the user interacts with the backend is standardized,
    and the same information should be returned regardless of backend implementation.
    Other backends may add functionality,
    but they will at the very least have the features defined here.

    Again, backends interact with curseforge using protocol objects.
    We handle the decoding and conversion into objects that can be worked with.

    We attempt to be modular, allowing developers to swap components in and out.
    This allows a developer to make the backend do something if they want it too.
    """

    def __init__(self, name) -> None:
        
        name = name  # Name of this backend

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

        raise NotImplementedError("Must be overridden in child class!")

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

        raise NotImplementedError("Must be overridden in child class!")

    def categories(self) -> Tuple[base.CurseCategory]:
        """
        Gets a list of all valid categories on curseforge.

        This call can be quite expensive,
        so use it sparingly!

        :return: Tuple of CurseCategory instances
        :raises NotImplimentedError: Must be overridden in child class!
        :rtype: Tuple[base.CurseCategory]
        """

        raise NotImplementedError("Must be overridden in child class!")

    def game_catagories(self, id: int) -> Tuple[base.CurseCategory]:
        """
        Returns a tuple of all root catagories for a given game.

        You will need to provide a game ID.
        These catagories can be used to lookup addons! 

        :param id: ID of the game get catagories
        :type id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: Tuple of CurseCategory instances for each category the game has
        :rtype: Tuple[base.CurseCategory]
        """

        raise NotImplementedError("Must be overridden in child class!")

    def sub_categories(self, category_id: int) -> Tuple[base.CurseCategory]:
        """
        Gets all sub-categories of a given category.

        You will need to provide a category ID.

        :param category_id: ID of the category to get sub-category
        :type category_id: int
        :raises: NotImplimentedError: Must be overridden in child class!
        :return: Tuple of CurseCategory instances
        :rtype: Tuple[base.CurseCategory]
        """

        raise NotImplementedError("Must be overridden in child class!")

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

        raise NotImplementedError("Must be overridden in child class!")

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

        raise NotImplementedError("Must be overridden in child class!")

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

        raise NotImplementedError("Must be overridden in child class!")

    def addon_files(self, addon_id: int) -> Tuple[base.CurseFile]:
        """
        Gets a list of files associated with the addon.

        YOu will need to provide an addon ID,
        which can be found by searching a game category.

        :param addon_id: Addon ID
        :type addon_id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: Tuple of CurseFile instances representing the addon's files
        :rtype: Tuple[base.CurseFile]
        """

        raise NotImplementedError("Must be overridden in child class!")

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

        raise NotImplementedError("Must be overridden in child class!")

    def file_description(self, addon_id: int, file_id: int) -> base.CurseDescription:
        """
        Gets the description of the file.

        You will need to provide the addon ID, and the file ID.

        :param addon_id: ID of the addon
        :type addon_id: int
        :param file_id: ID of the game
        :type file_id: int
        :raises NotImplementedError: Must be overridden in child class!
        :return: CurseDescription instance representing the file description
        :rtype: base.CurseDescription
        """

        raise NotImplementedError("Must be overridden in child class!")

    def search(self, game_id: int, category_id: int, search: Any) -> Tuple[base.CurseAddon, ...]:
        """
        Searches the given category using the search parameters.

        The search parameters can really be anything,
        so we keep there implementation ambiguous!

        :param game_id: ID of the game to search under
        :type game_id: int
        :param category_id: ID of the category to search
        :type category_id: int
        :param search: Search parameters to use 
        :type search: Any
        :raises NotImplementedError: Must be overridden in child class!
        :return: Tuple of CurseAddon instances representing the matched addons
        :rtype: Tuple[base.CurseAddon, ...]
        """

        raise NotImplementedError("Must be overridden in child class!")

    def load_json(self, text: bytes) -> dict:
        """
        Converts the given bytes into a dictionary using JSON.

        The data must comply to JSON formatting guidelines!

        :param text: Text to convert
        :type text: str
        :return: Dictionary from text
        :rtype: dict
        """

        # Convert and return:

        return json.load(text)


class ForgeSVCBackend(BaseBackend):
    """
    ForgeSVCBackend - Gets curseforge information via 'forgesvc.net'.

    We support all features defined in BaseBackend.
    """

    def __init__(self) -> None:

        super().__init__("ForgeSVC")

        self.proto = URLProtocol("https://addons-ecs.forgesvc.net") # Protocol object to use

        # Configure the protocol object:

        self.proto.extra = '/api/v2/'
        self.raw = {}  # Raw data of the last request

    def post_process(self, pack) -> Any:
        """
        Post-processes the given instance.

        :param pack: Instance to post-format
        :type pack: BaseCurseInstance
        """

        if type(pack) == tuple:

            # Do the operation on each item in the tuple:

            for item in pack:

                item.raw = self.raw

                item.meta = self.proto.make_meta()

            return pack

        # Attach raw data:

        pack.raw = self.raw

        # Attach metadata:

        pack.meta = self.proto.make_meta()

        # Return the pack:

        return pack

    def games(self) -> Tuple[base.CurseGame,...]:
        """
        Returns a tuple of all valid curse games.

        Again, this function is very expensive to call!
        You should not use this often in production environments!

        :return: Tuple of CurseGame objects
        :rtype: Tuple[base.CurseGame]
        """

        # Get and raw game data:

        data = self._proto_call('game')

        # Iterate over each game:

        final = []

        for game in data:

            final.append(self._create_game(game))

        # Return the tuple:

        return self.post_process(tuple(final))

    def game(self, id: int) -> base.CurseGame:
        """
        Gets a game via the game ID.

        :param id: Game ID to search
        :type id: int
        :return: CurseGame instance representing the game
        :rtype: base.CurseGame
        """

        # Get raw game data:

        data = self._proto_call('game/{}'.format(id))

        # Create the game:

        game = self._create_game(data)

        # Return the game:

        return self.post_process(game)

    def game_catagories(self, id: int) -> Tuple[base.CurseCategory]:
        """
        Returns a tuple of CurseCategory instances for each category of the game.

        :param id: ID of the game to get categories from
        :type id: int
        :return: Tuple of CurseCategory instances
        :rtype: Tuple[base.CurseCategory]
        """

        # Get and return the tuple of categories:

        game = self.game(id)

        # Iterate and get all root categoires for the game:

        final = []

        for id in game.cat_ids:

            final.append(self.category(id))

        # Post-process and return the instances:

        return self.post_process(tuple(final))

    def category(self, category_id: int) -> base.CurseCategory:
        """
        Returns a CurseCategory instance representing the given category.

        :param category_id: ID of the category
        :type category_id: int
        :return: CurseCategory instance
        :rtype: base.CurseCategory
        """

        # Get the raw data:

        data = self._proto_call('category/{}'.format(category_id))

        # Create and return the category:

        return self.post_process(self._create_category(data))
 
    def sub_catagories(self, category_id: int) -> Tuple[base.CurseCategory]:
        """
        Gets the sub-categories of the given category.

        We return a tuple of CurseCategory instances
        representing the sub-categories.

        :param category_id: ID of the category to get sub-categories for 
        :type category_id: int
        :return: Tuple of CurseCategories representing the sub-categories
        :rtype: Tuple[base.CurseCategory]
        """

        # Get the raw data:

        data = self._proto_call('category/section/{}'.format(category_id))

        # Iterate over the data:

        final = []

        for cat in data:

            # Create a category:

            final.append(self._create_category(cat))

        # Post-process the data and return:

        return self.post_process(tuple(final))

    def addon(self, addon_id: int) -> base.CurseAddon:
        """
        Creates a CurseAddon instance representing the given addon.

        :param addon_id: ID of the addon
        :type addon_id: int
        :return: CurseAddon object representing the addon
        :rtype: base.CurseAddon
        """

        # Get the raw data:

        data = self._proto_call('addon/{}'.format(addon_id))

        # Convert the authors:

        authors = []

        for author in data['authors']:

            # Create and add the author:

            authors.append(base.CurseAuthor(author['id'], author['name'], author['url']))

        # Convert the attachments:

        attach = []

        for attachment in data['attachments']:

            attach.append(base.CurseAttachment(attachment['title'], attachment['id'], attachment['thumbnailUrl'],
                          attachment['url'], attachment['isDefault'], attachment['projectId']))

        # Create the packet:

        addon = base.CurseAddon(data['name'], data['slug'], data['summary'], data['websiteUrl'],
                                data['primaryLanguage'], data['dateCreated'], data['dateModified'], data['dateRelease'],
                                data['id'], data['downloadCount'], data['gameId'], data['isAvailable'], data['isExperimental'],
                                tuple(authors), tuple(attach))

        # Return the packet:

        return self.post_process(addon)

    def addon_description(self, addon_id: int) -> base.CurseDescription:
        """
        Returns a CurseDescription instance representing the description of an addon.

        :param addon_id: ID of the addon
        :type addon_id: int
        :return: CureDescription representing the addon
        :rtype: base.CurseDescription
        """

        # Get raw data:

        data = self._proto_call('{}/description', raw=True)

        # Create the packet:

        desc = base.CurseDescription(data)

        # Process and return the pack:

        return self.post_process(desc)

    def addon_files(self, addon_id: int) -> Tuple[base.CurseFile, ...]:
        """
        Gets a list of all files associated with the addon.

        :param addon_id: ID of the addon to get files for
        :type addon_id: int
        :return: Tuple of CurseFile instances associated with the addon
        :rtype: Tuple[base.CurseFile, ...]
        """

        # Get raw data:

        data = self._proto_call('addon/{}/files'.format(addon_id))

        # 

    def _proto_call(self, path: str, raw: bool=False) -> Any:
        """
        Calls the underlying protocol,
        and determines if we should decode
        the received data using JSON.

        :param path: Path of the URL to build
        :type path: str
        :param raw: Boolean determining if we should decode via JSON, defaults to False
        :type raw: bool, optional
        :return: Decoded data via JSON or bytes
        :rtype: Union[dict, bytes]
        """

        # Call the protocol object:

        self.raw = self.proto.get_data(self.proto.url_build(path))

        # Determine if we should decode:

        data = self.raw

        if not raw:

            # Decode the data:

            data = json.loads(self.raw)

        # Return the data:

        return data

    def _create_game(self, data: dict) -> base.CurseGame:
        """
        Creates a CurseGame instance using the provided game data.

        We automatically pull the necessary values from the game,
        as well as parse and convert the categories.*

        :param data: Data to create game instance with
        :type data: dict
        :return: CurseGame instance representing the game
        :rtype: base.CurseGame
        """

        # Create list of game categories:

        final = []

        # Create CurseGame:

        game = base.CurseGame(data['name'], data['slug'], data['id'], data['supportsAddons'], None)

        # Return the CurseGame:

        return game

    def _create_category(self, data: dict) -> base.CurseCategory:
        """
        Creates a CurseCategory instance using the provided game data.

        :param data: Data to create category instance with
        :type data: dict
        :return: CurseCategory instance representing the game
        :rtype: base.CurseCategory
        """

        # Create the category:

        cat = base.CurseCategory(data['id'], data['gameId'], data['name'], None, None, None, None)

        # Return the category:

        return cat

    def _create_file(self, data: dict) -> base.CurseFile:
        """
        Creates a CurseFile instance based on raw data.

        :param data: Data to be formatted
        :type data: dict
        :return: CurseFile representing the raw data
        :rtype: base.CurseFile
        """

        