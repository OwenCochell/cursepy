"""
General classes for representing curseforge information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, TYPE_CHECKING
from os.path import isdir, join

from cursepy.classes.search import SearchParam
from cursepy.formatters import BaseFormat, NullFormatter
from cursepy.proto import URLProtocol

if TYPE_CHECKING:

    # Only import the HandlerCollection when type checking,
    # resolves a circular dependency

    from cursepy.handlers.base import HandlerCollection


@dataclass
class BaseCurseInstance(object):
    """
    BaseCurseInstance - Class all child instances must inherit!

    A curses instance is a class representing information from curseforge.
    This allows developers to work with this information in a connivent way.

    Some classes might even do operations on the data if needed,
    or might be able to fetch data themselves.

    We seek to standardize curseforge information,
    allowing developers to work with with only one packet type,
    regardless of backend/method/source of information.

    We also provide a field for supplying metadata about the instance.
    This can really be anything the backend thinks is helpful,
    although we recommend keeping it to connection details and statistics.

    Packets can also have the raw, unformatted data attached to them.
    This data is NOT standardized,
    meaning that the raw data will most likely be different across different handlers.
    Be aware, that handlers are under no obligation to attach raw data to the packet!

    We have the following parameters:

        * raw - Raw data from the backend(Does not have to be provided!)
        * meta - Meta data on this instance. See the backend in question for information on metadata
        * hands - HandlerCollection instance
    """

    raw: Any = field(init=False, repr=False, default=None)  # RAW packet data
    meta: Any = field(init=False, repr=False, default=None)  # Metadata on this packet
    hands: HandlerCollection = field(init=False, repr=False, compare=False)  # Handler Collection instance


@dataclass
class BaseWriter(BaseCurseInstance):
    """
    Parent class that adds writing functionality to the instance.

    This class provides tools for writing content to external files,
    and offers entry points for child classes to fine-tune and configure these writes.
    """

    def low_write_bytes(self, data: bytes, path: str, append: bool=False) -> int:
        """
        Writes the given data to an external file in bytes.

        By default, we overwrite the file at the given path!
        If this is not something you want, you can pass 'True'
        to the 'append' value. 
        This will append the description to the end of the file provided.

        We use the internal 'open' function built into python.
        Standard exceptions associated with this function will be raised accordingly!

        :param data: Data to write to the file
        :type data: bytes
        :param path: Path to the file to write, must be a path-like-object
        :type path: str
        :param append: Value determining if we are appending to the file, defaults to False
        :type append: bool, optional
        :return: Number of bytes written
        :rtype: int
        """

        # Open the file-like object:

        file = open(path, 'ab' if append else 'wb')

        # Write the content:

        return file.write(bytes(data))

    def low_write_string(self, data: str, path: str, append: bool=False) -> int:
        """
        Similar to low_write_bytes, 
        except we write the content as a string.

        :param data: Data to write to file
        :type data: str
        :param path: Path to file to write
        :type path: str
        :param append: Value determining if we are appending to the file, defaults to False
        :type append: bool, optional
        :return: Number of bytes written
        :rtype: int
        """

        # Open the file-like object:

        file = open(path, 'a' if append else 'wb')

        # Write the content:

        return file.write(data)

    def write(self, path: str, append: bool=False) -> int:
        """
        Write function for this class.

        Child classes should implement this function!
        This allows them to fine-tune the write process automatically,
        and pass the content to be written without the user having to specify it.

        Child classes should use the 'low_write' function to preform the operation.

        :param path: Path to the file to write to
        :type path: str
        :param append: Value determining if we should append instead of overwrite, defaults to False
        :type append: bool, optional
        :raises NotImplementedError: Function should be overridden in child class!
        :return: Number of bytes written
        :rtype: int
        """

        raise NotImplementedError("Should be overloaded in child class!")


@dataclass
class BaseDownloader(BaseWriter):
    """
    Parent class for all instances that download information.

    We offer some helper methods for achieving this.
    We expect the protocol to be HTTP.
    """

    def low_download(self, url: str, path: str=None) -> bytes:
        """
        Downloads the given data and returns it as bytes.

        We use the 'URLProtocol' to get the information.

        We also offer to save the downloaded information
        to an external file.
        You can pass the path to the file using the 'path' parameter.
        If this value is none, then the data will not be saved.
        The data will be returned regardless of weather it is saved or not.

        :param url: URL of the content to download
        :type url: str
        :param path: Path to file to save downloaded data, optional
        :type path: str, optional
        :return: Bytes of the downloaded data
        :rtype: bytes
        """

        # Create the URL protocol:

        url_proto = URLProtocol(url)

        # Get the data:

        data = url_proto.get_data(url)

        # Determine if we should write to a file:

        if path is not None:

            # Save the data to a file:

            self.low_write_bytes(data, path)

        # Finally, return the data:

        return data

    def download(self, path: str=None) -> bytes:
        """
        Download function for this class!

        Child classes should implement this function!
        This allows them to fine-tune the download operation automatically,
        and pass the necessary parameters without the user having to specify them.

        Implementations should use the 'low_download' function for this operation.

        :param path: Path to file to save the downloaded information to, defaults to None
        :type path: str, optional
        :return: Downloaded bytes
        :rtype: bytes
        :raises: NotImplementedError: Must be overridden in child class!
        """

        raise NotImplementedError("Must be overridden in child class!")


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
class CurseDescription(BaseWriter):
    """
    CurseDescription - Represents a description of a addon.

    A 'description' is HTML code that the addon author can provide
    that describes something in detail.
    Addons and file descriptions fall into this category.

    Again, this description is in HTML,
    so some formatting may be necessary!

    We offer the ability to attach custom 'formatters' to this object.
    A 'formatter' will convert the HTML code into something.
    The implementation of formatters is left ambiguous,
    as users may have different use cases.
    Check out the formatter documentation for more info.

    A formatter can be attached to us manually, 
    or it can automatically be added upon each call by the CursesAPI
    or wrapper.

    We also offer the ability to save the description to an external file
    for later usage.

    We contain the following parameters:

        * description - Raw, unformatted description
        * formatter - Formatter instance attached to this object 
    """

    description: str
    formatter: BaseFormat = field(default=NullFormatter(), init=False)

    INST_ID = 7

    def attach_formatter(self, form: BaseFormat):
        """
        Attaches the given formatter to this instance.

        We do a check to make sure that the formatter inherits 'BaseFormat'.

        :param form: Formatter to attach to this description
        :type form: BaseFormat
        :raises: TypeError: If the formatter does NOT inherit 'BaseFormat'
        """

        # Check of the formatter inherits 'BaseFormat':

        if not isinstance(form, BaseFormat):

            # Object does not inherit BaseFormat!

            raise TypeError("Formatter must inherit 'BaseFormat'!")

        # Attach the formatter to ourselves:

        self.formatter = form

    def format(self) -> Any:
        """
        Sends the description through the formatter,
        and returns the formatted content,
        whatever that may be.

        :return: Formatted data
        :rtype: Any
        """

        return self.formatter.format(self.description)

    def write(self, path: str, append: bool=False) -> int:
        """
        Writes the description to an external file.

        We use the CurseWriter 'low_write' method for this operation.

        We write the raw content, as formatters may not return writable components!

        :param path: Path to the file to write, must be a path-like-object
        :type path: str
        :param append: Value determining if we are appending to the file, defaults to False
        :type append: bool, optional
        :return: Number of bytes written
        :rtype: int
        """

        # Use the 'low_write' method:

        return self.low_write_string(self.description, path, append=append)

    def __str__(self) -> str:
        """
        Method called when this object's content is requested as a string.

        We return the raw data, as it may not return string content.

        :return: Formatted description content
        :rtype: str
        """

        return self.description


@dataclass
class CurseAttachment(BaseDownloader):
    """
    CurseAttachment - Represents an attachment.

    An 'attachment' is a piece of media,
    usually an image or thumbnail,
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
        * description - Description of this attachment
    """

    title: str
    id: int
    thumb_url: str
    url: str
    is_thumbnail: bool
    addon_id: int
    description: str

    INST_ID = 4

    def download(self, path: str=None) -> bytes:
        """
        Downloads the attachment.

        You can use the 'path' parameter
        to save the downloaded information to a file.

        If you provide a path to a directory and not a file,
        then we will use the name of the remote file as the name.

        :param path: Path to save the data to, optional
        :type path: str
        :return: Downloaded bytes
        :rtype: bytes
        """

        # Get our paths:

        path = self._create_name(path)

        # Call the 'low_download' function with our URL:

        return self.low_download(self.url, path=path)

    def download_thumbnail(self, path: str=None) -> bytes:
        """
        Downloads the thumbnail of this attachment.

        You can use the 'path' parameter 
        to save the thumbnail to a file.

        Like the download method,
        we automatically generate a name if the path is None,
        or is just a directory.

        :param path: Path to save the file to, defaults to None
        :type path: str, optional
        :return: downloaded bytes
        :rtype: bytes
        """

        # Get our path:

        path = self._create_name(path)

        # Call the 'low_download' function with our URL:

        return self.low_download(self.url, path=path)

    def _create_name(self, name: str=None) -> str:
        """
        Creates a name for the download file.

        If the name is none, then we return the
        title of this addon.

        We return this name as a path.

        :param name: Name to use
        :type name: str
        :return: Path to save the file under
        :rtype: str
        """

        if name is not None:

            # Check if we are working with a directory:

            return self.url.split('/')[-1] if isdir(name) else name

        # Otherwise, return the None:

        return None


@dataclass
class CurseFile(BaseDownloader):
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
        * dependencies - Tuple of CurseDependency objects
        * game_id - ID of the game this file is apart of
        * is_available - Boolean determining if this file is available for download
        * release_type - Release type of this file (beta, alpha, release), use class constants for identifying this!
        * file_status - Status of the file (approved, under review, deprecated, ect.), use the constants below for this!
        * hashes - Tuple of CurseHashes representing file hashes
        * download_count - Number of times this addon has been downloaded

    We also contain the following constants:

        * RELEASE - Used if the release type is 'release' (For for production use)
        * BETA - Used if the release type is 'beta'
        * ALPHA - Used if the release type is 'alpha'
        * PROCESSING - Used for file status if the file is currently being processed
        * CHANGES_REQUIRED - Used for file status if the file needs changes before approval
        * UNDER_REVIEW - Used for file status if the file is currently under review
        * APPROVED - Used for file status if the file is approved
        * REJECTED - Used for file status if the file is rejected
        * MALWARE_DETECTED - Used for file status if malware is detected in the uploaded file
        * DELETED - Used for file status if the file has been deleted
        * ARCHIVED - Used for the file status if the file has been archived
        * TESTING - Used for the file status if the file is in the testing phase
        * RELEASED - Used for the file status if the file is released, if this is the status, then the file is ready to be used!
        * READY_FOR_REVIEW - Used for the file status if the file is ready for review
        * DEPRECATED - Used for the file status if the file has been marked as deprecated
        * BAKING - Used for the file status TODO: What does this mean?
        * AWAITING_PUBLISHING - Used for file status if the file is awaiting publishing
        * FAILED_PUBLISHING - Used for file status if the file has failed publishing 
    """

    id: int
    addon_id: int
    display_name: str
    file_name: str
    date: str
    download_url: str
    length: int
    version: Tuple[str, ...]
    dependencies: Tuple[CurseDependency, ...]

    # Optional arguments:

    game_id: int = -1
    is_available: bool = True
    release_type: int = -1
    file_status: int = -1
    hashes: Tuple[CurseHash, ...] = field(default_factory=lambda: [])
    download_count: int = -1

    RELEASE = 1
    BETA = 2
    ALPHA = 3

    PROCESSING = 1
    CHANGES_REQUIRED = 2
    UNDER_REVIEW = 3
    APPROVED = 4
    REJECTED = 5
    MALWARE_DETECTED = 6
    DELETED = 7
    ARCHIVED = 8
    TESTING = 9
    RELEASED = 10
    READY_FOR_REVIEW = 11
    DEPRECATED = 12
    BAKING = 13
    AWAITING_PUBLISHING = 14
    FAILED_PUBLISHING = 15

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

        return self.hands.file_description(self.addon_id, self.id)

    def get_dependencies(self, depen_type: int) -> Tuple[CurseDependency, ...]:
        """
        Returns a tuple of CurseDependency objects
        that this addon file requires.

        Users can specify a dependency type,
        which will only return dependencies that match the given type.
        You can use the dependency

        :param depen_type: Dependency type to return
        :type depen_type: int
        :return: Tuple of CurseDependency objects
        :rtype: Tuple[CurseDependency, ...]
        """

        # Iterate over the dependencies:

        final = []

        for depen in self.dependencies:

            if depen.type == depen_type:
                
                final.append(depen)

        # Return the final tuple:

        return tuple(final)

    def get_addon(self) -> CurseAddon:
        """
        Gets the CurseAddon this file is apart of.

        :return: CurseAddon this file is apart of
        :rtype: CurseAddon
        """

        return self.hands.addon(self.addon_id)

    def download(self, path: str=None) -> bytes:
        """
        Downloads the file.

        If the provided path points to a directory,
        then the default file name will be used.

        :param path: Path to download the file to, optional
        :type path: str
        :return: Downloaded file bytes
        :rtype: bytes
        """

        # See if we should do some path handling:

        temp_path = None

        if path is not None:

            # Check if we are working with a directory:

            temp_path = join(path, self.file_name) if isdir(path) else path

        # Do the download operation:

        return self.low_download(self.download_url, path=temp_path)

    def good_file(self) -> bool:
        """
        This method determines if this file is valid and ready to be used.

        We do this by checking the release type, file status, and if the file is available for download.
        If this file is valid, then we return True.
        
        Just because a file is not good does not mean that it can't be used!
        On top of this, just because a file is good does not mean it will work properly!
        We only check if the file is downloadable and marked production ready.
        Production ready files could be poorly made,
        and non-production experimental files could also be valid.

        :return: Boolean determining if this file is 'good'
        :rtype: bool
        """
        
        return self.is_available and self.release_type == CurseFile.RELEASE and self.file_status == CurseFile.RELEASED


@dataclass
class CurseDependency(BaseCurseInstance):
    """
    CurseDependency - Represents a dependency of an addon.

    A dependency is an addon file that is wanted or required by another addon.
    This class represents these dependencies.

    We contain useful metadata on each dependency,
    such as the addon ID and file ID this addon is apart of.
    We also offer methods to retrieve the addon and file.

    In some cases, we will not have all the required dependency information
    such as the dependency ID and file ID.
    This can happen if you use the ForgeSVC handlers and get ALL addon files
    instead of requesting a specific one.
    If this dependency instance is limited, then 'id' and 'file_id' will be None.

    We contain the following parameters:
    
        * id - ID of the dependency
        * addon_id - ID of the addon this dependency is apart of
        * file_id - ID of the file this dependency is apart of
        * type - Type of the dependency
        * required - Whether or not this dependency is required

    We also contain the following constants:

        * INCLUDE - TODO: Document this
        * INCOMPATIBLE - This dependency is incompatible
        * TOOL - This dependency is an optional tool
        * REQUIRED - This dependency is required
        * OPTIONAL - This dependency is optional
        * EMBEDDED_LIBRARY - This dependency is an embedded library
    """

    id: int
    addon_id: int
    file_id: str
    type: str

    INCLUDE = 6
    INCOMPATIBLE = 5
    TOOL = 4
    REQUIRED = 3
    OPTIONAL = 2
    EMBEDDED_LIBRARY = 1

    INST_ID = 8

    @property
    def required(self) -> bool:
        """
        Determines if this dependency is required.

        :return: True is required, False if not
        :rtype: bool
        """

        return self.type == self.REQUIRED

    def addon(self) -> CurseAddon:
        """
        Gets the CurseAddon this dependency is apart of.

        :return: CurseAddon this dependency is apart of
        :rtype: CurseAddon
        """

        return self.hands.addon(self.addon_id)

    def file(self) -> CurseFile:
        """
        Gets the CurseFile this dependency is apart of.

        :return: CurseFile this dependency is apart of
        :rtype: CurseFile
        """

        return self.hands.file(self,addon_id, self.file_id)


@dataclass
class CurseAddon(BaseCurseInstance):
    """
    CurseAddon - Represents a addon for a specific game.

    An 'addon' is something(mod, modpack, skin) that is added onto a game
    to change or add certain features and aspects.

    The definition of a generic addon is purposely left ambiguous,
    as it can be anything from a resource pack in minecraft to a mod in Kerbal Space Program.
    If you want something a bit more helpful and specific to a game,
    then the game wrappers might be helpful!

    This class contains useful metadata on a addon.
    We do NOT contain a detailed description information.

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
        * experimental - Boolean determining if the addon is experimental
        * authors - Tuple of authors for this addon
        * attachments - Tuple of attachments attributed with this addon
        * category_id - ID of the primary category this addon is apart of
        * root_category - ID of the root category this addon is apart of
        * all_categories - Tuple of all catagories this addon is affiliated with
        * is_featured - Boolean determining if this addon is featured
        * popularity_score - Float representing this addon's popularity score
            (Most likely used for popularity ranking)
        * popularity_rank - Int representing the game's popularity rank
        * allow_distribute - If addon is allowed for distribution
        * main_file_id - ID of the main file for this addon
        * status - Status of this addon (new, approved, under review, ect.), use the class constants for this!
        * wiki_url - URL to the wiki of this mod, blank string if not specified
        * issues_url - URL to the issues page of this mod, blank string if not specified
        * source_url - URL to the source code of this mod, blank string if not specified
        
    We also contain the following constants for identifying the status:
    
        * NEW - Used if the addon is new, no further actions have been made
        * CHANGES_REQUIRED - Used if the addon needs changes before approval
        * UNDER_SOFT_REVIEW - Used if the addon is under soft review (elaborate?)
        * APPROVED - Used if this addon is approved by the backend, good to be used
        * REJECTED - Used if this addon is reject by the backend, not to be used
        * CHANGES_MADE - used if changes have been made since the last review
        * INACTIVE - Used if this addon is inactive
        * ABANDONED - Used if this addon is abandoned
        * DELETED - Used if this addon has been deleted
        * UNDER_REVIEW - Used if this addon is under review
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
    authors: Tuple[CurseAuthor, ...]
    attachments: Tuple[CurseAttachment, ...]
    category_id: int
    root_category: int
    all_categories: Tuple[CurseAddon, ...]
    is_featured: bool
    popularity_score: int
    popularity_rank: int
    allow_distribute: bool
    main_file_id: int
    status: int
    wiki_url: str
    issues_url: str
    source_url: str

    # Class constants for identifying status:

    NEW = 1
    CHANGES_REQUIRED = 2
    UNDER_SOFT_REVIEW = 3
    APPROVED = 4
    REJECTED = 5
    CHANGES_MADE = 6
    INACTIVE = 7
    ABANDONED = 8
    DELETED = 9
    UNDER_REVIEW = 10

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

    def game(self) -> CurseGame:
        """
        Gets and returns the CurseGame instance
        this addon is apart of.

        :return: CurseGame instance
        :rtype: CurseGame
        """

        return self.hands.game(self.game_id)

    def category(self) -> CurseCategory:
        """
        Gets and returns the category we are a member of

        :return: CurseCategory of the category we are in
        :rtype: CurseCategory
        """

        # Get and return the category:

        return self.hands.category(self.category_id)


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
        * url - URL to the category page
        * date - Date this category was created
        * slug - Slug of the category 
    """

    id: int
    game_id: int
    name: str
    root_id: int
    parent_id: int
    icon: CurseAttachment
    url: str
    date: str
    slug: str

    INST_ID = 1

    def sub_categories(self) -> Tuple[CurseAddon, ...]:
        """
        Gets all sub-catagories for this category.

        :return: Tuple of sub-categories for this category
        :rtype: Tuple[CurseCategory, ...]
        """

        return self.hands.sub_category(self.game_id, self.id)

    def parent_category(self) -> CurseCategory:
        """
        Gets and returns the parent category for this instance.

        If there is no parent category, 
        then 'None' will be returned instead

        :return: CurseCategory instance, or None if there is no parent
        :rtype: CurseCategory, None
        """

        # Check if we even have a parent:

        if self.parent_category is None:

            # No parent, return None:

            return None

        # Get the parent category:

        return self.hands.category(self.parent_id)

    def root_category(self) -> CurseCategory:
        """
        Gets and returns the root category for this instance.

        If there is no parent category,
        then 'None' will be returned instead.

        :return: CurseCategory instance, or None if there is no parent
        :rtype: CurseCategory, None
        """

        # Check if we even have a root category:

        if self.parent_category is None:

            # No parent, return None:

            return None

        return self.hands.category(self.root_id)


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
        * icon_url - URL to the icon of the game
        * tile_url - URL to the tile picture of the game
        * cover_url - URL to the banner/cover of the game
        * status - Status of this game (draft, test, approved, ect.), use constants for defining this!
        * api_status - Weather this game is public or private, use constants for defining this!
    """

    name: str
    slug: str
    id: int
    support_addons: float

    # Optional values:

    icon_url: str = ''
    tile_url: str = ''
    cover_url: str = ''

    # Values only used by the official CurseForge API:

    status: int = -1
    api_status: int = -1

    # Constants for determining status:

    DRAFT = 1
    TEST = 2
    PENDING_REVIEW = 3
    REJECTED = 4
    APPROVED = 5
    LIVE = 6

    PRIVATE = 1
    PUBLIC = 2

    INST_ID = 2

    def categories(self) -> Tuple[CurseCategory, ...]:
        """
        Gets a tuple of all root categories for this game.

        :return: Tuple of all root CurseCategories
        :rtype: Tuple[CurseCategory, ...]
        """

        return self.hands.catagories(self.id)

    def search(self, search: Optional[SearchParam]=None) -> Tuple[CurseAddon, ...]:
        """
        Searches for addons under this game.

        :param search: Search object to use, defaults to None
        :type search: BaseSearch, optional
        :return: Tuple of CurseAddon objects
        :rtype: Tuple[CurseAddon, ...]
        """

        # Return the results from searching:

        return self.hands.search(self.id, search)

    def iter_search(self, search_param: Optional[SearchParam]=None) -> CurseAddon:
        """
        Invokes the 'iter_search' method of the HC with the given search parameters.

        You should check out HC's documentation on 'iter_search',
        but in a nutshell it basically allows you to iterate
        though all found addons, automatically incrementing the index when necessary.

        :param search_param: [description], defaults to None
        :type search_param: Optional[SearchParam], optional
        :return: Each curse addon found
        :rtype: CurseAddon
        """

        # Return the results from 'iter_search':

        return self.hands.iter_search(self.id, search_param)


@dataclass
class CurseHash(BaseCurseInstance):
    """
    CurseHash - Represents a hash of some kind.

    Some backends distribute hashes for some reason or another.
    In most cases, these hashes are of files to ensure 
    that the downloaded data is valid.

    This class keeps track of the hash value,
    as well as the possible algorithms used to determine the hash.
    You can use the constants attached to this class to determine the hashing algorithm.

    We contain the following parameters:

        * hash - Raw hash value
        * algorithm - Hashing algorithm used, used constants to identify this!

    We also contain the following constants:

        * SHA1 - Secure Hash Algorithm 1
        * MD5 - Message Digest 5 algorithm
    """

    hash: str
    algorithm: int

    SHA1 = 1
    MD5 = 2
