"""
capy wrapper classes.

These classes add functionality to the HandlerCollection,
automatically registering the relevant handlers,
and adding new functionality.
"""

from capy.handlers.base import HandlerCollection, NullHandler
from capy.handlers import forgesvc


class SVCWrap(HandlerCollection):
    """
    Wraps the HandlerCollection for SVC use.
    """

    def __init__(self):

        super().__init__()

        # Load our addon map:

        self.load_map({
                        1: forgesvc.SVCListGame,
                        2: forgesvc.SVCGame,
                        3: NullHandler,
                        4: forgesvc.SVCCategory,
                        5: forgesvc.SVCSubCategory,
                        6: forgesvc.SVCAddon,
                        7: NullHandler,
                        8: forgesvc.SVCAddonDescription,
                        9: forgesvc.SVCAddonFiles,
                        10: forgesvc.SVCFile,
                        11: forgesvc.SVCFileDescription
                    })

    def load_map(self, addon_map: dict):
        """
        Loads the given addon map.

        :param addon_map: Map to load
        :type addon_map: dict
        """

        for item in addon_map:

            # Check if we are working with an int:

            if type(item) == int:

                # Add the item:

                self.add_handler(addon_map[item]())
