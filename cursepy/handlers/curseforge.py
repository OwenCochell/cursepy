"""
Handlers for using the official CurseForge API:
https://docs.curseforge.com/
"""

from cursepy.handlers import metacf


class BaseCFHandler(metacf.BaseMetaCFHandler):
    """
    BaseCFHandler - Base class all curseforge handlers should inherit!

    We require an API key to access the API.
    This can be set by using the 'set_ley()' method.
    This handler will also attempt to extract the API key from
    the handler collection we are attached to.
    """

    def __init__(self):

        super().__init__("CurseForge", "https://api.curseforge.com/", 'v1/', '')

        self.key = None  # API Key to use
        self.raw = ""  # RAW data of the last event

    def start(self):
        """
        We extract the API key from the HandlerCollection we are apart of.
        """

        self.set_key(self.hand_collection.curse_api_key)

        super().start()

    def set_key(self, key: str):
        """
        Sets the API key for this handler.

        :param key: API key to use
        :type key: str
        """

        # Set the key:

        self.key = key

        # Create the headers:

        self.proto.headers.update({"Accept": "application/json",
                                   "x-api-key": self.key})


class CFListGame(BaseCFHandler, metacf.MetaCFListGame):
    """
    Gets a list of all games available to our API key.
    """

    pass


class CFGame(BaseCFHandler, metacf.MetaCFGame):
    """
    Gets info on a specific game.
    """

    pass


class CFListCategory(BaseCFHandler, metacf.MetaCFListCategory):
    """
    Gets a list of all catagories for a given game.
    """

    pass


class CFSubCategory(BaseCFHandler, metacf.MetaCFSubCategory):
    """
    Gets sub catagories for a given category.
    """

    pass


class CFCategory(BaseCFHandler, metacf.MetaCFCategory):
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

    pass


class CFAddon(BaseCFHandler, metacf.MetaCFAddon):
    """
    Gets a specific addon.
    """

    pass


class CFAddonDescription(BaseCFHandler, metacf.MetaCFAddonDescription):
    """
    Gets the description for a specific addon.
    """

    pass


class CFAddonSearch(BaseCFHandler, metacf.MetaCFAddonSearch):
    """
    Searches for a specific addon.
    """

    pass


class CFAddonFiles(BaseCFHandler, metacf.MetaCFAddonFiles):
    """
    Gets all files for a specific addon.
    """

    pass


class CFAddonFile(BaseCFHandler, metacf.MetaCFAddonFile):
    """
    Gets a specific file from an addon.
    """

    pass


class CFFileDescription(BaseCFHandler, metacf.MetaCFFileDescription):
    """
    Gets the description for a given file.
    """

    pass


cf_map = (
    CFListGame(),
    CFGame(),
    CFListCategory(),
    CFCategory(),
    CFSubCategory(),
    CFAddon(),
    CFAddonSearch(),
    CFAddonDescription(),
    CFAddonFiles(),
    CFAddonFile(),
    CFFileDescription(),
)
