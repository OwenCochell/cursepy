"""
This file contains base components for handler development.

A 'handler' is something that 'handels' data from a specific source of a specific type.
Essentially, when data comes from a specific source,
the handler is the thing that gets and formatts that data into something that is easy to work with.
A handler may also fetch data from elsewhere to fill in the blanks.

In this file, we outline some of the functionality of a handler,
and layout certain components that it will need to play nicely with everything else.

Because handlers can do a large variety of things,
the specific implementation is left ambiguous.

By default, the handler only works with the 'handel' method,
which will accept raw data from the service we are talking to.
There will be other components that the handler can overide if necessary.
"""

from http.client import HTTPResponse
from typing import Any, Optional, Tuple, Generic, Union

from capy.classes import base
from capy.proto import BaseProtocol, URLProtocol
from capy.errors import ProtocolMismatch
from capy.classes.search import BaseSearch, URLSearch


class BaseHandler(object):
    """
    BaseHandler - Child class all handlers must inherit!

    We define the framework of a handler,
    how it will be invoked, what information is given to it,
    and how it should integrate with other modules.

    Essentially, a module can define a few things:

        * proto_call - Call to the protocol of this handler, should return valid raw data
        * pre_process - Decodes data from the protocol before being send to the handler
        * format - Method called for formatting raw data from the protocol
        * post_process - Finalist the formatted data(Adds metadata, raw data, ect.)
        * run - Ran after all other functions, with the instance as the argument, great for user-defined code
        * handle - Invokes the handling process for this handler
        * make_proto - Should return a valid protocol object for this handler
        * check_search - Should check the incoming search object to ensure it is valid

    This allows handlers to control many aspects of their implementation.
    With smart inheritance, it also removes a lot of repeated calls and instructions.
    These functions are called in the order defined above.
    Everything from getting information to formatting can be customized. 

    Handlers are identified by instance types.
    Instance types are simply an intiger that represents an instance.

    The handle method is the entry point for handlers.
    It will accept the arguments and information from the handler collection,
    and will work with them as necessary.
    The default handle method will call all componets in order,
    so it is a good idea to use 'super()' once you have configured your methods.
    You can configure the handle method to accept any arguments you like, 
    the HandlerCollection will pass all arguments that it receives to the handler that is being called. 

    The handler ID will be stored under the ID parameter.
    Unidentified handlers will have an ID of -1.
    Handlers must be identified if they are to be used for handler processes!

    Handlers can optionally provide a method to check search objects,
    to ensure that they are valid objects for this handler.
    This ensures that the handler will always receive the correct search object.
    If an invalid search object is provided,
    then the HandlerCollection will raise an excpetion.
    """

    ID: int = -1

    def __init__(self, name: str='') -> None:
        
        self.backend = None  # Backend instance that has us loaded
        self.hand_collection: HandlerCollection  # Handlers instance we are apart of
        self.name = name  # Name of this handler, used to identify like-minded handlers
        self.search_type: Any = None  # Search type to use for search checking

        self.proto = None  # Underlying protocol object in use

    def start(self):
        """
        Function called when this handler is attached to a HandlerCollection.

        The user can put any relevant code here
        that would be appropriate to run at loadtime.
        """

        pass

    def stop(self):
        """
        Function called when this handler is removed from a HandlerCollection.

        Again, the user can put any relevant code here
        that would be appropriate to run at stoptime.
        """

        pass

    def format(self, data: Any):
        """
        Converts the given raw data into something,
        usually a CurseInstance.

        In here, we format and organise the given data
        into something that is usefull to the user.

        This formatter can do other things if necessary,
        and they don't necessarily have to be within the scope of formatting!
        However, it is recommended to use the 'handel' method for other use cases.

        :param data: Data to be formatted
        :type data: Any
        """

        # Return the data given to us

        return data

    def proto_call(self) -> Any:
        """
        Calls the underlying protocol instance of this handler.

        This function only calls the protocol instance!
        We do not decode or interpret this information,
        we only get it and return.

        :return: Raw data from the protocol
        :rtype: Any
        """

        pass

    def pre_process(self, data: Any) -> Any:
        """
        We pre-process the raw information for the protocol,
        and convert it into something the handler can understand.

        :param data: Data to decode
        :type data: Any
        """

        pass

    def post_process(self, data: Any) -> Any:
        """
        Finalizes the packet after it is created.

        This can do many things, attach raw data,
        metadata, anything the developer thinks is necessary.

        :param data: Data packet to be finalized
        :type data: Any
        :return: Finalized packet
        :rtype: Any
        """

        pass

    def run(self, data: base.BaseCurseInstance):
        """
        Contains code to be ran after the packet is received and formatted.

        This is useful if you want something to be ran each time certain data is handled.
        This is an optional implementation,
        as the handler collection will always return a CurseInstance representing the received data.

        :param data: Final CurseInstace representing the data we formatted
        :type data: BaseCurseInstance
        """

        pass

    def handel(self, *args, **kwargs) -> Any:
        """
        Default handle method.

        We call all the componets in order.

        If you want to fine-tune this process,
        then you can overload this method,
        and not call the parent method.
        TODO: Fix this description!
        """

        # First, call the proto_get method:

        data_bytes = self.proto_call(*args, **kwargs)

        # Next, call the pre-process method:

        raw_data = self.pre_process(data_bytes)

        # Format the data:

        data = self.format(raw_data)

        # Check if we are working with tuples:

        if type(data) == tuple:

            # Iterate over the data:

            final = []

            for item in data:

                # Process this item:

                post = self.post_process(item)

                # Attach the HandlerCollection:

                post.hans = self.hand_collection

                # Attach to the tuple:

                final.append(post)

            data_final = tuple(final)

        else:

            # Post-process the data:

            data_final = self.post_process(data)

            # Attach ourselves:

            data_final.hands = self.hand_collection

        # Return the final data:

        return data_final

    def make_proto(self):
        """
        Function called when we need a valid protocol object.

        This usually occurs when a 'get_proto' check determines that no protocol exists for this handler.
        If this is the case, then this function should return a valid protocol object for this handler
        and other handlers of this same name.
        """

        return None

    def get_proto(self) -> BaseProtocol:
        """
        Gets the given protocol object from the HandlerCollection.

        If a protocol of our name is present,
        then we will get it for our continued use.
        If not, then we will create one and register it to our name.

        If a protocol of our name is present,
        and it does not match the type of the protocol we are attempting to assign,
        then a 'ProtocolMismatch' exception will be raised.

        :param proto: Protocol object type to fetch
        :type proto: BaseProtocol
        :return: Protocol instance that we will use
        :rtype: BaseProtocol
        :raises ProtocolMismatch: Raised when a protocol mismatch occurs
        """

        # Check if our name is present:

        temp_proto = self.make_proto()

        if self.name in self.hand_collection.proto_map:

            # Let's make sure our protocol is of our type:

            target = self.hand_collection.proto_map[self.name]

            if isinstance(target, type(temp_proto)):

                # Correct instance, lets return:

                return target

            # Invalid handler, let's do someting!

            raise ProtocolMismatch("Protocol is of type: '{}', must be of type: '{}'!".format(type(temp_proto), type(target)))

        # Not present, let's make our own:

        self.hand_collection.proto_map[self.name] = temp_proto

        return self.hand_collection.proto_map[self.name]

    def check_search(self, search: BaseSearch) -> bool:
        """
        Checks the given search object,
        and determines if it is valid.

        This function can and should be overloaded
        if we are a search handler.
        This ensures that we will only receive the correct search objects.

        This function should return True if the search object is valid.
        Conversely, we should return False if the search object is invalid.
        The process for determining weather a search object is valid
        is purposefully left ambiguous.  

        If this function is not overloaded, 
        then we check to see if the search object inherits BaseSearch.

        :param search: Search object to check
        :type hand: BaseSearch
        :return: Boolean determining if the search object is valid
        :rtype: bool
        """

        # Check to see if search inherits BaseSearch:

        return isinstance(search, BaseSearch)


class URLHandler(BaseHandler):
    """
    URLHandler - Parent class for handlers using URLProtocol.

    We offer some ease of use features,
    such as automatically registering our protocol as URLProtocol,
    and simplifying the process for getting information from remote resources.
    We use the given information to automatically build URLs to get data from.

    We also offer ways to get the HTTPResponse of the last made request,
    and offer an easy way to generate metadata for curse instances.
    """

    def __init__(self, name: str, host: str, extra: str='/', path: str=''):

        super().__init__(name=name)

        self.host = host  # Hostname of the remote entity
        self.extra = extra  # Extra paths at the end of the hostname
        self.path = path  # Path to the correct data, appended after extra
        self.resp: HTTPResponse  # Last HTTPResponse from the protocol

        self.url = ''  # URL to use for the next request, can and SHOULD be overridden!

        self.proto: URLProtocol

    def make_proto(self) -> URLProtocol:
        """
        Creates and returns a valid URLProtocol instance.

        We automatically add the extra path information
        to the protocol instance.

        :return: Valid URLProtocol for this handler
        :rtype: URLProtocol
        """

        # Create the URL protocol

        url = URLProtocol(self.host)

        # Add the extra path:

        url.extra = self.extra

        # Return the final URLProtocol:

        return url

    def make_meta(self) -> dict:
        """
        Makes valid metadata about the request and connection
        and returns it.

        This is a good way to integrate connection stats into your CurseInstances!

        The meta information is structured like this:

            * headers - A list of (header, value) tuples
            * version - HTTP Protocol version used by server
            * url - URL of the resource retrieved
            * status - Status code returned by server
            * reason - Reason phase returned by server
    
        These values are returned in dictionary format.
        """

        # Create and return the metadata:

        return {'headers': self.resp.getheaders(), 'version': self.resp.version, 
                'url': self.resp.geturl(), 'status':self.resp.status, 'reason': self.resp.reason}

    def proto_call(self, *args) -> bytes:
        """
        Creates a valid URL using 'build_url()',
        and then passes this value to the protocol instance.
        We pass all arguments to the 'build_url()' method.

        We return the raw data from the HTTP request for further processing.
        We also save the HTTPResponse for future reference,
        specifically to generate metadata fro curse instances.

        :return: Raw data from the protocol object
        :rtype: bytes
        """

        # Generate the URL:

        url = self.build_url(*args)

        # Get and save the HTTPResponse

        self.resp = self.proto.low_get(url)

        # Return bytes of the response:

        return self.resp.read()

    def build_url(self, *args) -> str:
        """
        Method called by the 'proto_call()' method when a URL needs to be built.

        This is useful for generating custom URL's that may change with diffrent requests.
        By default, we simply return the result of URLProtocol's build_url() method,
        with the path parameter as the argument.

        :return: Build URL to make our request to
        :rtype: str
        """

        # Build our URL with the path:

        return self.proto.url_build(self.path)

    def check_search(self, search: URLSearch) -> bool:
        """
        Checks to make sure the search object
        inherits URLSearch.

        :param search: Search object to check
        :type search: URLSearch
        :return: Boolean determining if the search object is valid
        :rtype: bool
        """

        # Check to see if we inherit URLSearch:

        return isinstance(search, URLSearch)

    def handel(self, *args) -> Any:
        """
        We do the same as the BaseHandler's handle method,
        except we call the 'build_url' method to generate a valid URL.

        We pass all arguments to the 'build_url()' method.

        :return: CursesInstance generated from this handler
        :rtype: BaseCurseInstance
        """

        # Generate the URL:

        self.url = self.build_url(*args)

        # Pass it along to the parent handler:

        return super().handel()


class NullHandler(BaseHandler):
    """
    NullHandler - Does nothing

    As in the name, all information given to it and requested
    will simply be nothing.

    Great if you want to disable a certain feature.

    The only thing that needs to be specified is what ID
    we are being registered to.
    This is optional, as you can manually provide your own ID in the HandlerCollection.
    """

    def __init__(self, name: str='NullHandel', id: int=0) -> None:

        super().__init__(name=name)

        ID: int = id


class HandlerCollection(object):
    """
    Handlers - Manages and works with handlers! 

    This class works with and manages handlers.
    This allows wrappers and backends to easily manage
    and work with handlers.

    We normalize calling, adding, and removing handlers.
    This allows for handler autoconfiguration,
    and other time saving features.

    We also provide a collective space for handlers
    to share protocol objects between like-minded handlers.

    Only one handler can be registered to a given event!
    These handlers can be of diffrent types and come from diffrent sources,
    but only one can be registered to a given event!

    We define some entry points for calling handlers.
    These functions will be called by the users actually using these handlers.
    We define some arguments that should be defined,
    as well as what we expect the functions to return.

    You can utilise wrappers to change what functions expect and return.
    Be aware, that default dataclasses will call the functions defined here
    with the given arguments!
    """

    LIST_GAMES = 1  # Gets a list of all valid games
    GAME = 2  # Get information on a specific game
    LIST_CATEGORY = 3  # Gets a list of all valid categories
    CATEGORY = 4  # Get information on a specific category
    SUB_CATEGORY = 5  # Get all sub-categories for the given category
    ADDON = 6  # Get information on a specific addon
    ADDON_SEARCH = 7  # Searches the game for addons
    ADDON_DESC = 8 # Get description for a specific addon
    ADDON_LIST_FILE = 9  # Gets a tuple of all files associated with an addon
    ADDON_FILE = 10  # Get information on a specific file for an addon
    FILE_DESCRIPTION = 11  # Description of a file
    
    def __init__(self):
        
        self.handlers = {}  # Dictionary of handler objects
        self.proto_map = {}  # Maps handler names to protocol objects

        # Create a good starting state:

        self.reset()

    def reset(self):
        """
        Resets the HandlerCollection back to it's original state.

        This clears all handlers and replaces them with NullHandlers.
        We also remove all affiliated protocol instances.

        Be warned, if not referenced,
        the removed handlers and all information on them may be erased!
        """

        # Remove all handlers:

        self.handlers.clear()

        # Create null handlers for each INST_ID:

        for num in range(1,9):

            # Create the NullHandler for this ID:

            self.add_handler(NullHandler(id=num))

        # Remove the protocol objects:

        self.proto_map.clear()

    def add_handler(self, hand: BaseHandler, id: Optional[int]=None):

        """
        Adds the given handler to the HandlerCollection.

        By default, we pull the instance ID out of thew handler.
        However, the developer can manually provide an instance ID to register the handler to.
        If this is the case, then the ID on the handler will be ignored.

        We use 'remove_handler()' to remove the handler at this location.

        :param hand: Handler to register
        :type hand: BaseHandler
        :param id: ID to register the handler to, None to use ID on given handler
        :type id: int
        """

        # Remove the handler at this position:

        self.remove_handler(hand.ID if id is None else id)

        # Add the handler:

        self.handlers[hand.ID if id is None else id] = hand

        # Attach ourself to the handler:

        hand.hand_collection = self

        # Check if a new protocol object is necessary:

        hand.proto = hand.get_proto()

        # Start the handler:

        hand.start()

    def remove_handler(self, id: int):
        """
        Removes the handler at the given ID.

        We replace the handler with a NullHandler
        to ensure that something is working with data no matter what.

        We will automatically stop the handler at this location.

        :param id: ID of the handler to remove
        :type id: int
        """

        # Check if a handler is even present:

        if id not in self.handlers.keys():

            # No handler present, just return:

            return

        # Stop the handler at the ID:

        self.handlers[id].stop()

        # Replace the handler with NullHandler:

        self.handlers[id] = NullHandler(id=id)

    def handel(self, id: int, *args, **kwargs) -> Any:
        """
        Invokes the handel process at the handler with the given ID.

        As outlined earlier,
        this gets and formats data from an external location.

        We pass all arguments and keyword arguments
        to the handler at the given ID.

        :param id: ID of the handler to call
        :type id: int
        :return: The final class provided by the handler
        :rtype: BaseCurseInstance
        """

        # First, we get the handler in question:

        hand = self.handlers[id]

        # Invoke the 'handle()' method:

        inst = hand.handel(*args, **kwargs)

        # Return the instance:

        return inst

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

        return self.handel(1)

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

        return self.handel(2, id)

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

        return self.handel(3, category_id)

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

        return self.handel(4, category_id)

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

        return self.handel(5, addon_id)

    def search(self, game_id: int, category_id: int, search: Any) -> Tuple[base.CurseAddon, ...]:
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
        :param search: Search options to fine tune the search
        :type search: Any
        :return: Tuple of addons that matched the search parameters
        :rtype: Tuple[base.CurseAddon, ...]
        :raises: TypeError: If the search object fails the search check
        """ 

        # Check to make sure the search object is valid:

        if not self.handlers[5].check_search(search):

            # Raise an exception, the search object is invalid!

            raise TypeError("Invalid search object!")

        # Lets pass the data along:

        return self.handel(6, game_id, category_id, search)

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

        return self.handel(7, addon_id)

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

        return self.handel(8, addon_id)

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

        return self.handel(9, addon_id, file_id)

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

        return self.handel(10, addon_id, file_id)
