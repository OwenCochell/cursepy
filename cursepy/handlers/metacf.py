"""
This file contains handlers that can communicate to APIs
that work in the same way as the official API.

These handlers only implement parsing and decoding data using the CHF.
Any feature can be subclassed and worked with as necessary.

CurseForge-like APIs use HTTP(s), utilize similar ULRs (with a differing base),
return data in JSON (with a few exceptions), and formats data in roughly the same way.
If your API is similar to curseforge but not exactly the same,
then you can override any features as necessary.
"""

import json

from typing import Any, Tuple

from cursepy.handlers.base import URLHandler
from cursepy.classes import base
from cursepy.classes.search import SearchParam, url_convert
from cursepy.errors import HandlerNotSupported


class BaseMetaCFHandler(URLHandler):
    """
    BaseMetaCFHandler - Base class all curseforge-like handlers should inherit!

    We define some basic features that curseforge-like APIs should inherit.
    """

    def pre_process(self, data: bytes) -> dict:
        """
        Decodes the JSON data into a python dictionary.

        :param data: Data to be decoded
        :type data: bytes
        :return: Python dictionary
        :rtype: dict
        """

        self.raw = json.loads(data)

        # Extract the data and return it:

        return self.raw['data']

    def post_process(self, data: Any) -> Any:
        """
        Post-processes the outgoing CurseInstance.

        We attach metadata and raw data to the given event.

        :param data: Event to process
        :type data: Any
        :return: Processed event
        :rtype: Any
        """

        # Add raw data:

        data.raw = self.raw

        # Attach meta data:

        data.meta = self.make_meta()

        # Return final data:

        return data


class MetaCFListGame(BaseMetaCFHandler):
    """
    Gets a list of all games.
    """

    ID: int = 1

    def build_url(self) -> str:
        """
        Returns a valid URL for getting game data.

        :return: URL to get game data
        :rtype: str
        """

        return self.proto.url_build("games")

    def format(self, data: dict) -> Tuple[base.CurseGame, ...]:
        """
        Formats the data into a CurseGame object.

        :param data: Data to format
        :type data: dict
        """

        # Iterate over games and create them:

        final = [MetaCFGame.format(self, game) for game in data]

        return tuple(final)


class MetaCFGame(BaseMetaCFHandler):
    """
    Gets info on a specific game.
    """

    ID: int = 2

    def build_url(self, game_id: int) -> str:
        """
        Returns a valid URL for getting game data.

        :param game_id: Game ID 
        :type game_id: int
        :return: URL for getting game data
        :rtype: str
        """

        return self.proto.url_build("games/{}".format(game_id))

    def format(self, data: dict) -> base.CurseGame:
        """
        Formats the given data into a CurseGame.

        :param data: Data to format
        :type data: dict
        :return: CurseGame
        :rtype: base.CurseGame
        """

        # Figure out categories:

        return base.CurseGame(data['name'], data['slug'], data['id'], True, 
                              data['assets']['iconUrl'], data['assets']['tileUrl'], data['assets']['coverUrl'], 
                              data['status'], data['apiStatus'])


class MetaCFListCategory(BaseMetaCFHandler):
    """
    Gets a list of all catagories for a given game.
    """

    ID: int = 4

    def build_url(self, game_id: int) -> str:
        """
        Gets a valid URL for getting game catagories.

        :param game_id: Game ID
        :type game_id: int
        :return: URL for getting category data
        :rtype: str
        """

        return self.proto.url_build("categories?gameId={}".format(game_id))

    @staticmethod
    def format(data: dict) -> Tuple[base.CurseCategory, ...]:
        """
        Formats the given data.

        :param data: Data to format
        :type data: dict
        :return: Tuple of CurseCategory objects
        :rtype: Tuple[base.CurseCategory, ...]
        """

        temp = [MetaCFCategory.format(cat) for cat in data]

        return tuple(temp)


class MetaCFSubCategory(BaseMetaCFHandler):
    """
    Gets sub catagories for a given category.
    """

    ID: int = 5

    def build_url(self, game_id: int, category_id: int) -> str:
        """
        Creates a URL for getting sub catagories.

        :param game_id: Game ID to get catagories for
        :type game_id: int
        :param category_id: Category ID to get sub catagories for
        :type category_id: int
        :return: Valid URL for getting sub catagories.
        :rtype: str
        """

        return self.proto.url_build("categories?gameId={}&classId={}".format(game_id, category_id))

    @staticmethod
    def format(data: dict) -> Tuple[base.CurseCategory, ...]:
        """
        Formats the given data.

        :param data: Data to format
        :type data: dict
        :return: Tuple of CurseCategory objects
        :rtype: Tuple[base.CurseCategory, ...]
        """

        temp = [MetaCFCategory.format(cat) for cat in data]

        return tuple(temp)


class MetaCFCategory(BaseMetaCFHandler):
    """
    In a perfect world, we get info on a specific category.

    Unfortunately, this is not a perfect world we live in.
    The CF API only allows us to list categories,
    not grab info on a specific one.

    Because of this, this addon raises 'HandlerNotSupported'
    when the handle method is called.

    We are only here to do category formatting for other
    handlers that may work with categories.
    """

    ID: int = 4

    def handle(self, *args) -> Any:
        """
        Because CurseForge does not support getting info on a specific addon,
        we raise a HandlerNotSupported exception. 

        :raises: HandlerNotSupported
        """

        raise HandlerNotSupported("CurseForge does not support individual handler lookup!")

    @staticmethod
    def format(data: dict) -> base.CurseCategory:
        """
        Formats the given data.

        :param data: Data to format
        :type data: dict
        :return: CurseCategory object representing the data
        :rtype: base.CurseCategory
        """

        # Convert all keys to lowercase

        data = {k.lower():v
            for k, v in
            data.items()
        }


        # Figure out attachment:

        attach = base.CurseAttachment('Category Icon', -1, data['iconurl'], data['iconurl'], True, -1, 'Icon of the category')

        # Determine if this is a class:

        return base.CurseCategory(data['id'], data['gameid'], data['name'], data['classid'] if 'classid' in data.keys() else data['id'], 
                                  data['parentcategoryid'] if 'parentcategorycd' in data.keys() else data['id'], attach, data['url'], data['datemodified'], data['slug'])


class MetaCFAddon(BaseMetaCFHandler):
    """
    Gets a specific addon.
    """

    ID: int = 6

    def build_url(self, addon_id: int) -> str:
        """
        Creates a valid URL for getting addon info.

        :param addon_id: ID of the addon
        :type addon_id: int
        :return: URL for getting addon data
        :rtype: str
        """

        return self.proto.url_build("mods/{}".format(addon_id))

    @staticmethod
    def format(data: dict) -> base.CurseAddon:
        """
        Creates a CurseAddon instance from the given data.

        :param data: Data to work with
        :type data: dict
        :return: CurseAddon instance
        :rtype: base.CurseAddon
        """

        # Convert all data to lowercase:

        data = {k.lower():v
            for k, v in
            data.items()
        }

        # Convert the authors:

        authors = [
            base.CurseAuthor(auth['id'], auth['name'], auth['url'])
            for auth in data['authors']
        ]

        # Create the logo attachment:

        logoa = data['logo']

        logo = base.CurseAttachment(logoa['title'], logoa['id'], logoa['thumbnailUrl'] if 'thumbnailUrl' in logoa.keys() else logoa['thumbnailurl'], logoa['url'], True, data['id'], logoa['description'])

        # Create other attachments, named screenshots by CF:

        attach = [
            base.CurseAttachment(att['title'], att['id'], att['thumbnailUrl'], att['url'], False, data['id'], att['description'])
            for att in data['screenshots']
        ]

        attach.insert(0, logo)

        # Create catagories:

        cats = [MetaCFCategory.format(cat) for cat in data['categories']]

        # Convert links to lowercase:
        
        data['links'] = {k.lower():v
            for k, v in
            data['links'].items()
        }

        return base.CurseAddon(data['name'], data['slug'], data['summary'],
                               data['links']['websiteurl'], 'EN', data['datecreated'], data['datemodified'], data['datereleased'], data['id'], data['downloadcount'], data['gameid'], data['isavailable'] if 'isavailable' in data.keys() else True, False,
                               tuple(authors), tuple(attach), data['primarycategoryid'], data['classid'] if 'classid' in data.keys() else cats[0].root_id, tuple(cats), data['isfeatured'], data['thumbsupcount'] if 'thumbsupcount' in data.keys() else None, 
                               data['gamepopularityrank'] if 'gamepopularityrank' in data.keys() else None, data['allowmoddistribution'], data['mainfileid'], data['status'], data['links']['wikiurl'], data['links']['issuesurl'], data['links']['sourceurl'])


class MetaCFAddonDescription(BaseMetaCFHandler):
    """
    Gets the description for a specific addon.
    """

    ID: int = 8

    def pre_process(self, data: bytes) -> str:
        """
        We do not decode the info via JSON,
        as CurseForge gives us strings.

        :param data: Data to decode
        :type data: bytes
        :return: Decoded response data
        :rtype: str
        """
        
        # Set the raw data:
        
        self.raw = data
        
        temp = json.loads(data)
        
        return temp['data']

    def build_url(self, addon_id: int) -> str:
        """
        Builds a valid URL for getting addon descriptions.

        :param addon_id: Addon ID
        :type addon_id: int
        :return: URL for getting addon descriptions
        :rtype: str
        """

        return self.proto.url_build("mods/{}/description".format(addon_id))
    
    @staticmethod
    def format(data: str) -> base.CurseDescription:
        """
        Creates a CurseDescription instance with the given data.

        :param data: Data to process
        :type data: str
        :return: CurseDescription object
        :rtype: base.CurseDescription
        """

        return base.CurseDescription(data)


class MetaCFAddonSearch(BaseMetaCFHandler):
    """
    Searches for a specific addon.
    """

    ID: int = 6

    def build_url(self, game_id: int, search: SearchParam) -> str:
        """
        Creates a valid URL for searching addons.

        :param game_id: ID of the game to search under
        :type game_id: int
        :param search: CFSearch object that contains search parameters
        :type search: CFSearch
        :return: URL for searching
        :rtype: str
        """

        # Add the game ID to the search object:

        search.gameId = game_id

        # Create the params dict:

        params = search.asdict()

        # Switch some keys around:

        params['classId'] = params.pop('rootCategoryId')

        thing =  self.proto.url_build(
            url_convert(
                params,
                url='mods/search'
            )
        )

        return thing

    def format(self, data: dict) -> Tuple[base.CurseAddon, ...]:
        """
        Formats the given data.

        :param data: Data to format
        :type data: dict
        :return: Formatted data
        :rtype: Tuple[base.CurseAddon, ...]
        """

        # Iterate over instances:

        final = [MetaCFAddon.format(addon) for addon in data]

        return tuple(final)


class MetaCFAddonFiles(BaseMetaCFHandler):
    """
    Gets all files for a specific addon.
    """

    ID: int = 9

    def build_url(self, addon_id: int, search: SearchParam) -> str:
        """
        Builds a valid URL for getting all files associated with an addon.

        :param addon_id: Addon ID
        :type addon_id: int
        :return: URL for getting all files
        :rtype: str
        """

        # Create a dict:

        params = search.asdict()

        # Swap some keys around:

        # Switch some keys around:

        params['classId'] = params.pop('rootCategoryId')

        return self.proto.url_build(
            url_convert(
                search.asdict(),
                url='mods/{}/files'.format(addon_id)
            )
        )

    @staticmethod
    def format(data: dict) -> Tuple[base.CurseFile, ...]:
        """
        Converts the given data into a tuple of CurseFile instances.

        :param data: Data to format
        :type data: dict
        :return: Tuple of all files
        :rtype: Tuple[base.CurseFile, ...]
        """

        temp = [MetaCFAddonFile.format(file) for file in data]

        return tuple(temp)


class MetaCFAddonFile(BaseMetaCFHandler):
    """
    Gets a specific file from an addon.
    """

    ID: int = 10

    def build_url(self, addon_id: int, file_id: int) -> str:
        """
        Builds a valid URL for getting all files associated with an addon.

        :param addon_id: Addon ID
        :type addon_id: int
        :param file_id: File ID
        :type file_id: int
        :return: URL for getting a file
        :rtype: str
        """

        return self.proto.url_build("mods/{}/files/{}".format(addon_id, file_id))

    @staticmethod
    def format(data: dict) -> base.CurseFile:
        """
        Converts the given data into a curse file.

        :param data: Data to format
        :type data: dict
        :return: Curse file representing the given data
        :rtype: base.CurseFile
        """

        # We fill in None for the dependency ID and the File ID, as that info is not available

        depends = [base.CurseDependency(None, dep['modId'], data['id'], dep['relationType']) for dep in data['dependencies']]

        # Figure out hashes:

        hashes = [base.CurseHash(hsh['value'], hsh['algo']) for hsh in data['hashes']]

        return base.CurseFile(data['id'], data['modId'], data['displayName'], data['fileName'], data['fileDate'], data['downloadUrl'],
                              data['fileLength'], tuple(data['gameVersions']), tuple(depends), data['gameId'], data['isAvailable'], data['releaseType'], 
                              data['fileStatus'], tuple(hashes), data['downloadCount'])


class MetaCFFileDescription(BaseMetaCFHandler):
    """
    Gets the description for a given file.
    """

    ID: int = 11

    def pre_process(self, data: bytes) -> str:
        """
        We do NOT decode the data via JSON,
        as we are working with HTML.

        :param data: Data to be decoded
        :type data: bytes
        :return: String representing the description
        :rtype: str
        """

        self.raw = data
        
        temp = json.loads(data)

        return temp['data']

    def build_url(self, addon_id: int, file_id: int) -> str:
        """
        Returns a valid URL for getting a file description.

        :param addon_id: Addon ID
        :type addon_id: int
        :param file_id: File ID
        :type file_id: int
        :return: URL for getting a file description
        :rtype: str
        """

        return self.proto.url_build('mods/{}/files/{}/changelog'.format(addon_id, file_id))

    @staticmethod
    def format(data: str) -> base.CurseDescription:
        """
        Formats the given data into a CurseDescription instance.

        :param data: Data to format
        :type data: str
        :return: CurseDescription containing the file description
        :rtype: base.CurseDescription
        """

        return base.CurseDescription(data)
