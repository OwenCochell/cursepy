"""
Caching tools and components for capy protocols.    
"""

from time import time
from typing import Any


class CapCache(object):
    """
    The CAPY caching engine.

    We offer easy methods for caching and content retrieval.
    This allows for better prefromance on our end,
    as instead of calling a remote server,
    we can instead provide the saved content.

    This also reduces strain on the target server,
    as we will overall make less requests.

    We offer a framework for saving requested information,
    and allow this information to be stored in memory,
    or written to a file.

    We save the raw data from the request,
    meaning that we do not do any decoding!
    When valid cached information is found,
    then we return the raw data.
    The protocol using us should also return the raw data.

    We are designed to work well with HTTP caching
    conventions, although it should work fine with other protocols.

    We are designed to be modular in lots of ways,
    particularly in methods of saving and loading previously cached values.
    
    We store the cached responses in the following format:

    {
        '[PROTO]': {
            '[ADDR]': {
                'content': '[CONTENT]',
                'expires': '[EXPIRE]',
                'extra': {[MISC]}
            }
        }
    }

    Where:

    * PROTO - The protocol type
    * ADDR - Address(URL, command, resource, ect.) called
    * CONTENT - The actual cached content
    * EXPIRE - Time when the content expires, source can be customized
    * MISC - Dictionary of extra information that a protocol can attach

    We offer methods for creating and accessing these values.
    """

    def __init__(self) -> None:
        
        self.cache = {}  # Cache dictionary
        self.time_method = time  # Time method to use for time calculations

    def add_content(self, proto: Any, addr: str, cont: Any, exp: int, misc: dict):
        """
        Adds the given content to the cache.

        We automatically format the content into
        our supported format.

        This function will probably be wrapped
        by another function or class
        that will fill in a lot of this information on the protocol level.

        We accept any item of any type for protocol identification,
        although we reccomend using the protocol type.
        The object must also be hashable,
        as we use dictionaries to store the values. 

        :param proto: Protocol instance used to determine what protocol to save the data under
        :type proto: Any
        :param addr: Remote address used to get the information
        :type addr: str
        :param cont: Content to be cached
        :type cont: Any
        :param exp: Expire value for this content
        :type exp: int
        :param misc: Misc. data to be attached to the cached data,
            usually used by protocol objects to keep track of state
        :type misc: dict
        """

        # Check if the protocol is present:

        if proto not in self.cache.keys:

            # Create a new proto cache:

            self._init_proto(proto)

        # Save the formatted content:

        self.cache[proto][addr] = {
            'content': cont,
            'expires': exp,
            'misc': misc
        }

    def get_content(self, proto: Any, addr: str) -> Any:
        """
        Gets the cached data at the current position.

        If the cached data is invalid,
        then we will return 'None'.

        The protocol can decide weather to clear the value,
        keep it intact, or update it!

        :param proto: Protocol identifier
        :type proto: Any
        :param addr: Addess used to get content
        :type addr: str
        :return: Cached content for the address, or None if content is stale
        :rtype: Any
        """

        # Check if the content is stale:

        if self.is_stale:

            # Stale content, return None:

            return None

        # Otherwise, return the content as usual:

        return self.cache[proto][addr]['content']

    def is_stale(self, proto: Any, addr: str) -> bool:
        """
        Determines if the content at the given address is stale.

        We use our time funcion to determine this.

        :param proto: Protocol identifier
        :type proto: Any
        :param addr: Address used to get content
        :type addr: str
        :return: Boolean determining if the content is stale
        :rtype: bool
        """

        # Check if the content is stale:

        if self.cache[proto][addr]['expires'] < self.time_method():

            # Value is stale!

            return False

        # Value is fresh:

        return True

    def get_time(self) -> int:
        """
        Gets the current time value of our time function.

        This value can differ quite a bit depending on the time function,
        but we expect that it should normally return an int.

        :return: Current value of our time function
        :rtype: int
        """

        # Call and return the value:

        return self.time_method()

    def reset(self):
        """
        Resets the internal state of the cache.

        This will remove all cached content,
        as well as registered protocols.

        Use this method at your own risk!
        """

        # Clear the internal state:

        self.cache = {}

    def clean(self, proto: Any=None) -> int:
        """
        Searches the cache for expired entries and removes them.
        Be aware, that this will also remove associated misc. data!

        By default, we search under ALL protocols.
        However, if a protocol identifier is provided via 'proto',
        then we will only search under that identifier.

        We return the number of stale items removed.

        :param proto: Protocol identifer to clean
        :type proto: Any
        :return: Number of items removed
        :rtype: int
        """

        data = self.cache

        # Check if we are only searching under a certain identifier:

        if proto is not None:

            # Search only under a certain category:

            data = [proto]

        # Iterate over the protocols:

        invalid = {}

        for iden in data:

            # Iterate over each value in the protocol:

            for item in self.cache[iden]:

                # Check to see if the item is expired:

                if self.time_method() > self.cache[iden][item]['expires']:

                    # Invalid item, let's log it:

                    invalid[iden] = item

        # Iterate over logged items:

        for item in invalid:

            # Remove the value from the cache:

            del self.cache[item][invalid[item]]

        # Return the number of items removed:

        return len(invalid)

    def _init_proto(self, proto: Any):
        """
        Creates the dictionaries for a new protocol instacne.

        :param proto: Key to use for protocol identification
        :type proto: Any
        """

        # Create the new dictionary:

        self.cache[proto] = {}
