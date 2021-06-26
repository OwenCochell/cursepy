"""
General classes for representing curseforge information.
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Tuple

from capy.classes.search import BaseSearch

# Set the number of instances:

NUM_INST = 7


@dataclass
class BaseCurseInstance(object):

    """
    BaseCurseInstance - Class all child instances must inherit!

    A curses instance is a class representing information from curseforge.
    This allows developers to work with this information in a connivent way.

    Some classes might even do operations on the data if needed,
    or might be able to fetch data themselves(?).

    We seek to standardize curseforge information,
    allowing developers to work with with only one packet type,
    regardless of backend/method/source of information.

    We also provide a field for supplying metadata about the instance.
    THis can really be anything the backend thinks is helpful,
    although we recommend keeping it to connection details and statistics.

    You can use the INST_ID field to identify instances.

    We have the following parameters:

        * raw - Raw data from the backend(Does not have to be provided!)
        * meta - Meta data on this instance. See the backend in question for information on metadata
        * hands - HandlerCollection instance
    """

    raw: Any = field(init=False, repr=False)  # RAW packet data
    meta: Any = field(init=False, repr=False)  # Metadata on this packet
    hands: Any = field(init=False, repr=False, compare=False)  # Handler Collection instance
    INST_ID: int = field(default=0, init=False)


@dataclass
class CurseAuthor(BaseCurseInstance):

    """
    CurseAuthor - Represents an author for a curses addon.

    An 'author' is an account that published a curses addon.

    This class only contains metadata on a author.
    The information in this class is not necessary for 
    getting addon information.
    Instead, it is extra info for those interested.

    Completely disregard this info if it is not relevant to you!

    We contain the following parameters:

        * id - ID of this author
        * name - Name of the author
        * url - URL to author's page
    """

    id: int
    name: str
    url: str

    INST_ID = 3


@dataclass
class CurseDescription(BaseCurseInstance):

    """
    CurseDescription - Represents a decritpion of a addon.

    A 'description' is HTML code that the addon author can provide
    that describes the addon in detail.
    We also count file changelogs as a description!

    Again, this description is in HTML,
    so some formatting may be necessary!

    We offer the ability to attach custom 'formatters' to this object.
    A 'formatter' wll convert the HTML code into something.
    The implementation of formatters is left ambiguous,
    as users may have diffrent use cases.
    Check out the formatter documentation for more info.

    A formatter can be attached to us manually, 
    or it can automatically be added upon each call by the CursesAPI
    or wrapper.

    We also offer the ability to save the description to an external file
    for later usage.

    We contain the following parameters:

        * description_raw - Raw, unformatted description
        * formatter - Formatter instance attached to this object 
    """

    description: str
    formatter: Any = field(init=False)

    INST_ID = 7


@dataclass
class CurseAttachment(BaseCurseInstance):

    """
    CurseAttachment - Represents an attachment

    An 'attachment' is a piece of media,
    usually an image of thumbnail,
    that is shown on the addon page.

    These attachments can be the icon of the addon,
    as well as bonus images of the addon provided by the author.

    We contain useful metadata on said images,
    and we also offer tools to download and save these images.

    We contain the following parameters:

        * title - Title of the attachment
        * id - ID of the attachment
        * thumb_url - URL of the thumbnail image(If attachment is image, then thumbnail is smaller image)
        * url - URL of the attachment
        * is_thumbnail - Boolean determining if this attachment is the thumbnail of the addon
        * addon_id - ID of the addon this attachment is a part of
    """

    title: str
    id: int
    thumb_url: str
    url: str
    is_thumbnail: bool
    addon_id: int

    INST_ID = 4


@dataclass
class CurseFile(BaseCurseInstance):

    """
    CurseFile - Represents an addon file.

    An 'addon file' is a specific file available in an addon.
    Because multiple versions for an addon can exist,
    most addons have multiple files that can be downloaded.

    We contain useful metadata on each file,
    and offer the ability to download said file,
    as well as retrieve the changelog.

    We contain the following parameters:

        * id - ID of the file
        * addon_id - ID of the addon this file is apart of
        * display_name - Display name of the file
        * file_name - File name of the file
        * date - Date the file was uploaded
        * download_url - Download URL of the file
        * length - Length in bytes of the file
        * version - Version of the game needed to work with this file
        * dependencies - List dependency addons ID's
    """

    id: int
    addon_id: int
    display_name: str
    file_name: str
    date: str
    download_url: str
    length: int
    version: Tuple[str, ...]
    dependencies: Tuple[int,...]

    INST_ID = 6

    @property
    def changelog(self) -> CurseDescription:
        """
        Gets the changelog of this file,
        and returns it as a CurseDescription object.

        Whatever handler is registered to the HandlerCollection for 
        getting game descriptions will be used!

        :return: CurseDescription representing the description of this file
        :rtype: CurseDescription
        """

        return self.hands.handel(7, self.addon_id, self.id)


@dataclass
class CurseAddon(BaseCurseInstance):

    """
    CurseAddon - Represents a addon for a specific game.

    An 'addon' is something(mod, modpack, skin) that is added onto a game
    to change or add certain features and aspects.

    The definition of a generic addon is purposefly left ambiguous,
    as it can be anything from a resource pack in minecraft to a mod in Kerbal Space Program.
    If you want something a bit more helpful and specific to a game,
    then the game wrappers might be helpful!

    This class contains useful metadata on a addon.
    We do NOT contain a detailed description information,
    and file information is converted into a CurseFile instance.

    We contain the following parameters:

        * name - Name of the addon
        * slug - Slug of the addon
        * summary - Short summary of the addon
        * url - URL of the addon page
        * lang - Language of the addon
        * date_created - Date of creation
        * date_modified - Date of last modification
        * date_release - Date of the latest release
        * id - ID of this addon
        * download_count - Number of downloads
        * game_id - ID of the game this addon is in
        * available - Boolean determining if the addon is available
        * experimental - Boolean determining if the addon is expiremental
        * authors - Tuple of authors for this addon
    """

    name: str
    slug: str
    summary: str
    url: str
    lang: str
    date_created: str
    date_modified: str
    date_release: str
    id: int
    download_count: int
    game_id: int
    available: bool
    experimental: bool
    authors: Tuple[CurseAuthor,...]
    attachments: Tuple[CurseAttachment,...]

    INS_ID = 5

    @property
    def description(self) -> CurseDescription:
        """
        Gets the description for this CurseAddon.

        Whatever handler is assigned to addon descriptions will be
        used to generate a CurseDescription.

        :return: CurseDescription representing this addon
        :rtype: CurseDescription
        """

        return self.hands.addon_description(self.id)

    def files(self) -> Tuple[CurseFile, ...]:
        """
        Gets a tuple of files associated with this addon.

        :return: Tuple of CurseFile instances
        :rtype: Tuple[CurseFile, ...]
        """
        
        return self.hands.addon_files(self.id)

    def file(self, file_id: int) -> CurseFile:
        """
        Gets a file associated with this addon.
        We use this addon ID to get the file.

        :param file_id: ID of the file to find
        :type file_id: int
        :return: CurseFile representing the file
        :rtype: CurseFile
        """

        return self.hands.addon_file(self.id, file_id)


@dataclass
class CurseCategory(BaseCurseInstance):

    """
    CurseCategory - Represents a category for a specific game. 

    A 'category' is a collection of addons for a specific game.
    Lets use Minecraft as an example, Minecraft has the following catagories:

        * Resource Packs
        * Modpacks
        * Mods
        * Worlds

    If you wanted to get info on a mod, then you would search in the 'Mods' category.
    This allows addons to be organized by type.

    This class contains identifying info on catagories,
    most important being the category ID,
    which is needed to search for projects in that specific category.

    Categories can be nested,
    meaning that each category can have a variable number of child categories.
    We contain references to the root_id, 
    which is the ID of the root category for all nested categories.
    The parent_id is the ID of the category one level up from ours.

    We contain the following parameters:

        * id - ID of the category
        * game_id - ID of the game this category is under
        * name - Name of the category
        * root_id - ID of the root category
        * parent_id - ID of the parent category
        * icon - CurseAttachment of this catagories icon
        * date - Date this category was created 
    """

    id: int
    game_id: int
    name: str
    root_id: int
    parent_id: int
    icon: CurseAttachment
    date: str

    INST_ID = 1

    def sub_categroies(self) -> Tuple[CurseAddon, ...]:
        """
        Gets all sub-catagories for this category.

        :return: Tuple of sub-categories for this category
        :rtype: Tuple[CurseCategory, ...]
        """

        return self.hands.sub_category(self.id)

    def search(self, search_param: Optional[BaseSearch]=None) -> Tuple[int]:
        """
        Searches this category with the given search parameters.

        :param search_param: Search parameter object to use, defaults to None
        :type search_param: Optional[BaseSearch], optional
        :return: Tuple of curse addons found in the search
        :rtype: Tuple[CurseAddon, ...]
        """

        return self.hands.search(self.game_id, self.id, search_param)


@dataclass
class CurseGame(BaseCurseInstance):

    """
    CurseGame - Represents a game on curseforge.

    A game is a collection of addons/catagories
    that are relevant to a specific title, 
    such as World of Warcraft or Minecraft.

    Game instances can have useful meta info for a particular title,
    but the most important are the game ID and catagories info,
    as you will need these values to get more precise project information.

    Not all games support addons!
    Some games are listed for reasons unknown,
    and do not have addon support.
    You can determine if a game has addon support by checking the 'support_addons' parameter.

    Some values are not loaded and interpreted by this class!
    These include game detection hints(Used for determining where a game is),
    and game file information(What files are necessary for modding and where they can be found).
    If this information is important to you, then the raw data can be found under the 'raw' parameter. 

    We contain the following parameters:

        * name - Name of the game
        * slug - Slug of the game
        * id - ID of the game
        * support_addons - Boolean determining if this game supports addons
        * catagories - ID's of the root categories associated with this game,
            use the 'categories' method to get CategoryInstances for these ID's
    """

    name: str
    slug: str
    id: int
    support_addons: float
    cat_ids: Tuple[int,...]

    INST_ID = 2

    def categories(self) -> Tuple[CurseCategory, ...]:
        """
        Gets a tuple of all root categories for this game.

        :return: [description]
        :rtype: Tuple[CurseCategory, ...]
        """

        # Get all categories for this game:

        final = []

        for cat_id in self.cat_ids:

            # Retrieve category info for this ID:

            final.append(self.hands.category(cat_id))

        # Return the final tuple:

        return tuple(final)
