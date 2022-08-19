"""
ForgeSVC - Handlers for getting info via ForgeSVC.net
"""

from __future__ import annotations

import json
from typing import Any, Tuple

from cursepy.classes.search import SearchParam, url_convert
from cursepy.handlers.base import URLHandler
from cursepy.classes import base


class BaseSVCHandler(URLHandler):
    """
    BaseSVCHandler - Base handler all classes must inherit!

    We define some useful functionality that is relevant to child handlers,
    specifically setting our base URL, and using JSON for pre-processing.
    """

    def __init__(self):

        super().__init__('ForgeSVC', 'https://addons-ecs.forgesvc.net', extra='/api/v2/', path='')

        self.raw: Any  # Raw data before formatting and post-processing

    def pre_process(self, data: bytes) -> dict:
        """
        Decodes the bytes from the protocol object
        into JSON format.

        :param data: Bytes from the protocol object
        :type data: bytes
        :return: Dictionary representing raw data
        :rtype: dict
        """

        # Decode the data:

        self.raw = json.loads(data)
    
        # Return the raw data:

        return self.raw

    def post_process(self, data: Any, raw: dict=None, meta:dict=None) -> Any:
        """
        Post-process the packet.

        We add the raw data from the request,
        and we add on the metadata generated by URLHandler.

        The user can optionally provide raw data and metadata to attach to 
        the instance. This will override any instances of the data we currently have.

        :param data: CurseInstance to be post-processed
        :type data: base.BaseCurseInstance
        :param raw: Raw data to be added
        :type raw: dict
        :param meta: Metadata to be added
        :type meta: dict
        :return: Processed curse instance
        :rtype: BaseCurseInstance
        """

        # Add the raw data to the instance:

        data.raw = self.raw if raw is None else raw

        # Add the metadata:

        data.meta = self.make_meta() if meta is None else meta

        # Return the final packet:

        return data


class SVCListGame(BaseSVCHandler):
    """
    Handler for getting a list of games.
    """

    ID: int = 1

    def build_url(self) -> str:
        """
        Builds a valid URL for getting game info.

        :return: URL for list of games
        :rtype: str
        """

        return self.proto.url_build('game')

    @staticmethod
    def format(data: dict) -> Tuple[base.CurseGame, ...]:
        
        # Iterate over the games:

        final = [SVCGame.format(game) for game in data]

        # Return the final game:

        return tuple(final)


class SVCGame(BaseSVCHandler):

    """
    Handler for getting and representing a curseforge game,
    whatever that may be.

    We convert the incoming data to a CurseInstance,
    as well as the function for creating a the valid URL.
    """

    ID: int = 2

    def build_url(self, game_id: int) -> str:
        """
        Returns a URL to fetch game information

        :param game_id: ID of the game to search for
        :type game_id: int
        :return: URL of the game info
        :rtype: str
        """

        return self.proto.url_build(f'game/{game_id}')

    @staticmethod
    def format(data: dict) -> base.CurseGame:
        """
        Formats the given data into a CurseGame.

        :param data: Decoded data to convert
        :type data: dict
        :return: CurseGame instance representing the game
        :rtype: CurseGame
        """
        
        # Create list of game categories:

        final = [cat['gameCategoryId'] for cat in data['categorySections']]

        # Create CurseGame:

        return base.CurseGame(data['name'], data['slug'], data['id'], data['supportsAddons'], tuple(final))


class SVCListCategory(BaseSVCHandler):
    """
    Handler for getting all valid categories on CurseForge.

    We convert the given data into a tuple of CurseCategory instances.
    """

    def build_url(self) -> str:
        """
        Returns a valid URL for fetching category information

        :return: URL for getting all catagories
        :rtype: str
        """

        return self.proto.url_build('category')

    def format(self, data: dict) -> Tuple[base.CurseCategory, ...]:
        """
        Formats the given data into a tuple of CurseCatagories

        :param data: Data to be formatted
        :type data: dict
        :return: Tuple of CurseCatagories
        :rtype: Tuple[CurseCatagories, ...]
        """

        # Iterate over the catagories:

        final = [SVCCategory.format(cat) for cat in data]

        # Return the final tuple:

        return tuple(final)


class SVCCategory(BaseSVCHandler):
    """
    Handler for getting and representing a curseforge category via ForgeSVC.
    """

    ID: int = 4

    def build_url(self, category_id: int) -> str:
        """
        Returns a valid URL to fetch category information

        :param category_id: ID of the category
        :type category_id: int
        :return: URL of the category info
        :rtype: str
        """

        return self.proto.url_build(f'category/{category_id}')

    @staticmethod
    def format(data: dict) -> base.CurseCategory:
        """
        Formats the decoded data into a CurseCategory instance

        :param data: Data to be formatted
        :type data: dict
        :return: CurseCategory instance
        :rtype: base.CurseCategory
        """

        return base.CurseCategory(data['id'], data['gameId'], data['name'], data['rootGameCategoryId'], 
                                  data['parentGameCategoryId'], data['avatarUrl'], data['dateModified'])


class SVCSubCategory(BaseSVCHandler):
    """
    Handler for getting sub-categories
    for a given category.
    """

    ID: int = 5

    def build_url(self, category_id) -> str:
        """
        Builds a valid URL for getting a list of sub-categories.

        :param category_id: ID of the category
        :type category_id: int
        :return: URL for list of sub-categories
        :rtype: str
        """

        return self.proto.url_build(f'category/section/{category_id}')

    @staticmethod
    def format(data: dict) -> Tuple[base.CurseCategory, ...]:
        """
        Formats the decoded data into a CurseCategory instance

        :param data: Data to be formatted
        :type data: dict
        :return: Tuple of CurseCategory instances
        :rtype: Tuple[CurseCategory, ...]
        """

        # Iterate over the catagories:

        final = [SVCCategory.format(cat) for cat in data]

        # Return the final tuple:

        return tuple(final)


class SVCAddon(BaseSVCHandler):
    """
    Handler for getting addon information.
    """

    ID: int = 6

    def build_url(self, addon_id: int) -> str:
        """
        Builds a valid URL for getting addon information.

        :param addon_id: ID of the addon
        :type addon_id: int
        :return: URL for getting addon info
        :rtype: str
        """

        return self.proto.url_build(f'addon/{addon_id}')

    @staticmethod
    def format(data: dict) -> base.CurseAddon:
        """
        Formats decoded data into CurseAddon instances

        :param data: Data to be formatted
        :type data: dict
        :return: CurseAddon instance representing the addon
        :rtype: base.CurseAddon
        """
        
        # Convert the authors:

        authors = [
            base.CurseAuthor(auth['id'], auth['name'], auth['url'])
            for auth in data['authors']
        ]


        # Convert the attachments:

        attach = [
            base.CurseAttachment(
                attachment['title'],
                attachment['id'],
                attachment['thumbnailUrl'],
                attachment['url'],
                attachment['isDefault'],
                attachment['projectId'],
                attachment['description'],
            )
            for attachment in data['attachments']
        ]


        # Create the instance:

        return base.CurseAddon(data['name'], data['slug'], data['summary'], data['websiteUrl'],
                               data['primaryLanguage'], data['dateCreated'], data['dateModified'], data['dateReleased'],
                               data['id'], data['downloadCount'], data['gameId'], data['isAvailable'], data['isExperiemental'],
                               tuple(authors), tuple(attach), data['primaryCategoryId'], data['isFeatured'], data['popularityScore'],
                               data['gamePopularityRank'], data['gameName'])


class SVCSearch(BaseSVCHandler):
    """
    Handler for searching for addon information.
    """

    def build_url(self, game_id: int, section_id: int, search: SearchParam) -> str:
        """
        Generates a valid URL with the given search parameter.

        :return: Valid URL for searching
        :rtype: str
        """

        # Create and return the URL:

        return self.proto.url_build(
            url_convert(
                search,
                url=f'addon/search?gameId={game_id}&sectionId={section_id}&',
            )
        )

    def format(self, data: dict) -> Tuple[base.CurseAddon, ...]:
        """
        Formats the given search results.

        :param data: Data to be formatted
        :type data: dict
        :return: Tuple of CurseAddon instances
        :rtype: Tuple[base.CurseAddon, ...]
        """

        # Iterate over the instances:

        final = [SVCAddon.format(addon) for addon in data]

        # Return the final tuple:

        return tuple(final)


class SVCAddonDescription(BaseSVCHandler):
    """
    Handler for getting an addon description.
    """

    ID: int = 8

    def build_url(self, addon_id: int) -> str:
        """
        Builds a valid URL for getting addon descriptions.

        :param addon_id: Addon ID
        :type addon_id: int
        :return: URL for addon descriptions
        :rtype: str
        """
        
        return self.proto.url_build(f'addon/{addon_id}/description')

    def pre_process(self, data: bytes) -> str:
        """
        We do NOT decode the info via JSON,
        as ForgeSVC gives us HTML strings.

        :param data: Data to be converted into string
        :type data: bytes
        :return: String representing the HTML data
        :rtype: str
        """

        # Set the raw data:

        self.raw = data

        return data.decode()

    @staticmethod
    def format(data: str) -> base.CurseDescription:
        """
        Formats decoded data into a CurseDescription

        :param data: Data to be decoded
        :type data: dict
        :return: CurseDescription representing the addon description
        :rtype: base.CurseDescription
        """
        
        return base.CurseDescription(data)


class SVCAddonFiles(BaseSVCHandler):
    """
    Handler for getting all files for an addon
    """

    ID: int = 9

    def build_url(self, addon_id: int) -> str:
        """
        Builds a valid URL for getting a list of all files associated with an addon

        :param addon_id: ID of the addon
        :type addon_id: int
        :return: URL for getting file info
        :rtype: str
        """

        return self.proto.url_build(f'addon/{addon_id}/files')

    def format(self, data: dict) -> Tuple[base.CurseFile, ...]:
        """
        Formats the decoded data into a tuple of CurseFiles

        :param data: Data to be formatted
        :type data: dict
        :return: Tuple of curse files
        :rtype: Tuple[base.CurseFile, ...]
        """

        # Extract the addon ID from the URL:

        id = int(self.url.split('/')[6])

        # Iterate over the files:

        final = [SVCFile.low_format(file, id, limited=True) for file in data]

        # Return the data:

        return tuple(final)


class SVCFile(BaseSVCHandler):
    """
    Handler for getting addon files
    """

    ID: int = 10

    def build_url(self, addon_id: int, file_id: int) -> str:
        """
        Returns a valid URL for getting an addon file

        :param addon_id: ID of the addon
        :type addon_id: int
        :param file_id: ID of the file
        :type file_id: int
        :return: URL for addon file
        :rtype: str
        """

        return self.proto.url_build(f'addon/{addon_id}/file/{file_id}')

    def format(self, data: dict) -> base.CurseFile:
        """
        Formats the given data into a CurseFile instance

        :param data: Data to be formatted
        :type data: dict
        :return: CurseFile instance
        :rtype: CurseFile
        """

        # Get the addon ID:

        id = int(self.url.split('/')[6])

        # Call the low-level format method:

        return self.low_format(data, id)

    @staticmethod
    def low_format(data: dict, addon_id: int, limited=False) -> base.CurseFile:
        """
        Low-level format method.

        We are static to allow other classes to use us to format data.
        The actual 'format()' method will extract the addon ID from the URL
        and pass it along to us.

        In some cases, we are not given full dependence info,
        for example when all files for a given addon is requested.
        You can use the 'limited' parameter to prevent a key error.

        :param data: Data to be formatted
        :type data: dict
        :param addon_id: ID of the addon
        :type addon_id: int
        :return: CurseFile instance
        :rtype: base.CurseFile
        """

        # Get the dependencies ID's:

        final = []

        for depen in data['dependencies']:

            if limited:

                final.append(base.CurseDependency(None, depen['addonId'], None, depen['type']))

                continue

            # Add the dependency ID's:

            final.append(base.CurseDependency(depen['id'], depen['addonId'], depen['fileId'], depen['type']))

        return base.CurseFile(data['id'], addon_id, data['displayName'], data['fileName'], data['fileDate'], 
        data['downloadUrl'], data['fileLength'], tuple(data['gameVersion']), tuple(final))


class SVCFileDescription(BaseSVCHandler):
    """
    Handler for getting the description of a file
    """

    ID: int = 11

    def build_url(self, addon_id: int, file_id: int) -> str:
        """
        Returns a valid URL for getting file description

        :param addon_id: ID of the addon
        :type addon_id: int
        :param file_id: ID of the file
        :type file_id: int
        :return: URL for getting file description
        :rtype: str
        """

        return self.proto.url_build(f'addon/{addon_id}/file/{file_id}/changelog')

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

        return data.decode()

    def format(self, data: str) -> base.CurseDescription:
        """
        Formats the given data into a CurseDescription instance

        :param data: Data to format
        :type data: str
        :return: CurseDescription representing the data
        :rtype: CurseDescription
        """

        return base.CurseDescription(data)


# Set the handler map:

svc_map = (SVCListGame(),
    SVCGame(),
    SVCListCategory(),
    SVCCategory(),
    SVCSubCategory(),
    SVCAddon(),
    SVCSearch(),
    SVCAddonDescription(),
    SVCAddonFiles(),
    SVCFile(),
    SVCFileDescription())
