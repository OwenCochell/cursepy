"""
Handlers for using the 3rd party curse.tools API:
https://www.curse.tools
https://api.curse.tools
"""

from cursepy.handlers import metacf


class BaseCTHandler(metacf.BaseMetaCFHandler):
    """
    BaseCTHandler - Base class all curse.tools handler should inherit!

    The curse.tools backend requests that the 'user-agent' be set to the name of our application.
    Be default, we make this 'cursepy', but it is recommended to make this the name of your app that utilizes cursepy.
    This can be defined by using the 'name' parameter in the init method,
    or by using the 'set_name()' method.
    """

    DEFAULT_NAME = 'cursepy'

    def __init__(self, name: str='cursepy'):

        super().__init__("CurseTools", "https://api.curse.tools/", 'v1/cf/', '')

        # Set our user agent:

        self.name = name

    def start(self):
        """
        Start method for all CT handlers.

        We also attempt to pull a name from the HandlerCollection,
        if it exists.
        """

        # If the name is our default:

        if self.name == BaseCTHandler.DEFAULT_NAME:

            # Attempt to pull from HandlerCollection:

            try:

                self.name = self.hand_collection.ct_name

            except Exception:

                # Did not work, do nothing...

                pass

        # Set our name:

        self.set_name(self.name)

        return super().start()

    def set_name(self, name: str):
        """
        Sets our user-agent name.

        Use this for identifying your app to the curse.tools backend!

        :param name: Name to set as user agent string, should be your app name
        :type name: str
        """

        self.proto.headers.update({"Accept": "application/json",
                                   "user-agent": name})


class CTListGame(BaseCTHandler, metacf.MetaCFListGame):
    """
    Gets a list of all games available to our API key.
    """

    pass


class CTGame(BaseCTHandler, metacf.MetaCFGame):
    """
    Gets info on a specific game.
    """

    pass


class CTListCategory(BaseCTHandler, metacf.MetaCFListCategory):
    """
    Gets a list of all catagories for a given game.
    """

    pass


class CTSubCategory(BaseCTHandler, metacf.MetaCFSubCategory):
    """
    Gets sub catagories for a given category.
    """

    pass


class CTCategory(BaseCTHandler, metacf.MetaCFCategory):
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


class CTAddon(BaseCTHandler, metacf.MetaCFAddon):
    """
    Gets a specific addon.
    """

    pass


class CTAddonDescription(BaseCTHandler, metacf.MetaCFAddonDescription):
    """
    Gets the description for a specific addon.
    """

    pass


class CTAddonSearch(BaseCTHandler, metacf.MetaCFAddonSearch):
    """
    Searches for a specific addon.
    """

    pass


class CTAddonFiles(BaseCTHandler, metacf.MetaCFAddonFiles):
    """
    Gets all files for a specific addon.
    """

    pass


class CTAddonFile(BaseCTHandler, metacf.MetaCFAddonFile):
    """
    Gets a specific file from an addon.
    """

    pass


class CTFileDescription(BaseCTHandler, metacf.MetaCFFileDescription):
    """
    Gets the description for a given file.
    """

    pass


ct_map = (
    CTListGame(),
    CTGame(),
    CTListCategory(),
    CTCategory(),
    CTSubCategory(),
    CTAddon(),
    CTAddonSearch(),
    CTAddonDescription(),
    CTAddonFiles(),
    CTAddonFile(),
    CTFileDescription(),
)
