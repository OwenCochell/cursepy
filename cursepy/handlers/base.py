"""
This file contains base components for handler development.

A 'handler' is something that 'handles' data from a specific source of a specific type.
Essentially, when data comes from a specific source,
the handler is the thing that gets and formatts that data into something that is easy to work with.
A handler may also fetch data from elsewhere to fill in the blanks.

In this file, we outline some of the functionality of a handler,
and layout certain components that it will need to play nicely with everything else.

Because handlers can do a large variety of things,
the specific implementation is left ambiguous.

By default, the HandlerCollection only works with the 'handle' method,
which will accept raw data from the service we are talking to.
There will be other components that the handler can overide if necessary.
"""

from typing import Any, Callable, Optional

from cursepy.classes import base
from cursepy.proto import BaseProtocol, URLProtocol
from cursepy.errors import ProtocolMismatch, HandlerRaise
from cursepy.classes.search import SearchParam
from cursepy.formatters import BaseFormat, NullFormatter


class BaseHandler(object):
    """
    BaseHandler - Child class all handlers must inherit!

    We offer some basic methods that a handler should inherit,
    as well as define the cappy Handler Framework(CHF).

    Essentially, the function makeup of the CHF is this:

        * make_proto - Should return a valid protocol object for this handler
        * proto_call - Call to the protocol of this handler, should return valid raw data
        * pre_process - Decodes data from the protocol before being send to the handler
        * format - Method called for formatting raw data from the protocol
        * post_process - Finalizes the formatted data(Adds metadata, raw data, ect.)
        * handle - Invokes the handling process for this handler

    This allows handlers to control many aspects of their implementation.
    With smart inheritance, it also removes a lot of repeated calls and instructions.
    These functions are called in the order defined above.
    Everything from getting information to formatting can be customized. 

    Handlers are identified by instance types.
    Instance types are simply an intiger that represents what this handler does.

    The handle method is the entry point for handlers.
    It will accept the arguments and information from the handler collection,
    and will work with them as necessary.
    The default handle method will call all componets in order,
    so it is a good idea to use 'super()' once you have configured your methods.
    You can configure the handle method to accept any arguments you like, 
    the HandlerCollection will pass all arguments that it receives to the 'handle' method,
    so you should use this as the primary way to accept arguments. 

    The handler ID will be stored under the ID parameter.
    Unidentified handlers will have an ID of -1.
    Handlers must be identified if they are to be used for handler processes!

    These handlers are designed to be customizable!
    The CHF is designed to be a good default implementation,
    that minimizes the amount of code developers have to write for handler development.

    Don't like the CHF? No problem!
    Most of the functions defined here are not necessary for handlers to work!
    The only functions that NEED to be defined are 'handle' and 'make_proto'.
    This means you can define your own methods and frameworks by creating a custom 'handle' method,
    that can call/do anything you would like it too.
    """

    ID: int = -1

    def __init__(self, name: str='') -> None:
        
        self.hand_collection: HandlerCollection  # Handlers instance we are apart of
        self.name = name  # Name of this handler, used to identify like-minded handlers

        self.proto: BaseProtocol  # Underlying protocol object in use

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
        However, it is recommended to use the 'handle' method for other use cases.

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

    def handle(self, *args, **kwargs) -> Any:
        """
        Default handle method.

        This is the default handle method,
        meaning that we call all components in order.

        We pass all arguments to 'proto_call',
        as this is the component that will need these arguments to fetch information.

        We also check to see if we are working with a tuple of instances.
        If this is the case, then we iterate over them and post-process each instance.
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

    def make_proto(self) -> Any:
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

        # Get and return the metadata:

        return self.proto.make_meta()

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

        # Get and return the data:

        return self.proto.get_data(self.url)

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

    def handle(self, *args) -> Any:
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

        return super().handle()


class NullHandler(BaseHandler):
    """
    NullHandler - Does nothing

    As in the name, all information given to us will be ignored,
    and we will simply return 'None'.

    Great if you want to disable a certain feature.

    The only thing that needs to be specified is what ID
    we are being registered to.
    This is optional, as you can manually provide your own ID in the HandlerCollection.

    We are used as a default handler that is attached to ID's
    that have no handlers associated with them.
    """

    def __init__(self, name: str='Nullhandle', id: int=0) -> None:

        super().__init__(name=name)

        ID: int = id

    def handle(self, *args, **kwargs) -> None:
        """
        As we are a NullHandler, we simply return None.

        :return: None
        :rtype: None
        """

        return None


class RaiseHandler(BaseHandler):
    """
    Raises an exception when the 'handle' method is called.

    This is very similar to the NullHandler,
    but we go a step further by raising an exception.

    This can be used as a more explicit, forceful way
    of disabling a feature, compared to just doing nothing.

    You can optionally change the name of the handler,
    as well as provide a custom ID. 
    """

    def __init__(self, name: str='RaiseHandler', id: int=0) -> None:

        super().__init__(name=name)

        ID: int = id

    def handle(self, *args, **kwargs):
        """
        Raise a 'HandlerRaise' excpetion.

        :raises: HandlerRaise: Always
        """

        raise HandlerRaise()


class HandlerCollection(object):
    """
    HandlerCollection - Manages and works with handlers! 

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

    Users can optionally attach callbacks to certain events.
    These callbacks should be a callable, which will be called after 
    the handle event is complete.
    Callbacks should accept at least one argument,
    which is the data the handler is returned.
    Any other arguments can be optionally provided.

    You can utilise wrappers to change what functions expect and return.
    Be aware, that default dataclasses will call the functions defined here
    with the given arguments!

    Sub-classing us is recommended and encouraged!
    This allows developers to easily automate actions,
    and make interacting with certain games much easier.

    By default, we call the 'load_default()' method upon instantiation.
    Wrappers should probably overload that method!
    If this is not something you want, you can pass False to the 'load_default'
    parameter.
    """

    LIST_GAMES = 0  # Gets a list of all valid games
    GAME = 1  # Get information on a specific game
    LIST_CATEGORY = 2  # Gets a list of all valid categories
    CATEGORY = 3  # Get information on a specific category
    SUB_CATEGORY = 4  # Get all sub-categories for the given category
    ADDON = 5  # Get information on a specific addon
    ADDON_SEARCH = 6  # Searches the game for addons
    ADDON_DESC = 7 # Get description for a specific addon
    ADDON_LIST_FILE = 8  # Gets a tuple of all files associated with an addon
    ADDON_FILE = 9  # Get information on a specific file for an addon
    FILE_DESCRIPTION = 10  # Description of a file
    
    DEFAULT_MAP: tuple = () # Default handler map

    def __init__(self, load_default=True):
        
        self.handlers = {}  # Dictionary of handler objects
        self.proto_map = {}  # Maps handler names to protocol objects
        self.callbacks = {}  # List of callbacks to run
        self.formatter = NullFormatter()  # Default formatter to attach to CurseDesciprion

        # Create a good starting state:

        self.reset()

        # Add the default handlers, if applicable:

        if load_default:

            self.load_default()

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

        for num in range(11):

            # Create the NullHandler for this ID:

            self.add_handler(NullHandler(), id=num)

        # Remove the protocol objects:

        self.proto_map.clear()

        # Remove the callbacks:

        self.callbacks = {}

        # Remove the default formatter:

        self.formatter = NullFormatter()

    def add_handler(self, hand: BaseHandler, id: Optional[int]=None):
        """
        Adds the given handler to the HandlerCollection.

        By default, we pull the instance ID out of thew handler.
        However, the developer can manually provide an instance ID to register the handler to.
        If this is the case, then the ID on the handler will be ignored.

        We use 'remove_handler()' to remove the handler at this location.

        The handler to be added MUST inherit BaseHandler!
        If it does not, then a ValueError will be raised.

        :param hand: Handler to register
        :type hand: BaseHandler
        :param id: ID to register the handler to, None to use ID on given handler
        :type id: int
        :raises: TypeError: If the handler does not inherit BaseHandler
        """

        # Check if the handler is valid:

        if not isinstance(hand, BaseHandler):

            # Handler is not valid!

            raise TypeError("Handler does not inherit BaseHandler!")

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

    def load_handlers(self, mapper: Any):
        """
        Loads handlers from the given iterable.

        This function allows multiple handlers to be loaded at once,
        and in a certain priority.

        We use the iterables to determine the priority and ID of the handler.
        During the load, if the handler at the given ID is NOT a NullHandler,
        then it will be skipped.
        This allows for handler priorities to be set.

        The 'root' iterable should contain sub-iterables
        that map handlers to ID's.
        The lower the index, or key, of the handler map,
        the higher priority they will have.
        This allows lower priority handlers to 'fill in the blanks'
        of there higher priority counterparts.

        The iterables can be lists or tuples,
        (Tuples are recommended for memory and speed reasons,
        and are the iterable method used for built in handlers).
        You can also use a dictionary to denote ordering.
        The keys for the dictionary should be an intiger.
        Higher integers mean they are lower priority.
        
        If the dictionary is used as a handler map,
        then the key should be the ID that the handler is going to
        associate with.

        Here is an example of an iterable for loading handlers:

        .. code-block::

            (
                (
                    Hand1(),
                    Hand1(),
                    Hand1()
                ),
                {
                    0: Hand2(),
                    2: Hand2(),
                    4: Hand2()
                }
            )

        In this example, the handler map will look like this:

        * 0 - Hand1
        * 1 - Hand1
        * 2 - Hand1
        * 4 - Hand2

        Notice, that even though Hand2 was assigned to ID's 0 and 2,
        it was not used, as Hand1 had a higher priority.
        However, ID 4 had no handlers assigned to it,
        so Hand2 was allowed to associate with it.

        Here is another example, and instead of utilizing
        dictionaries for skipped indexes, we simply use a NullHandler as a placeholder:

        .. code-block::

            (
                (
                    Hand1(),
                    Hand1(),
                    NullHandler(),
                    Hand1()
                ),
                (
                    Hand2(),
                    NullHandler(),
                    Hand2(),
                )
            )

        In this example, we do not assign a handler for the 2nd index
        in the first priority handler map, and instead assign a NullHandler in it's place.
        Because NullHandlers are ALWAYS a lower priority,
        the lower priorities will overrite them, even though they have been specified.
        This allows users to skip ID's without having to use dictionaries.

        We use 'add_handler()' under the hood,
        and we use recursion to iterate over the handlers.

        :param loader: Iterable to load
        :type loader: Any
        """

        iterable = None

        # Dictionary check:

        if type(mapper) == dict:

            # Working with a dictionary, change the iter method:

            iterable = sorted(mapper.items(), key= lambda item: item(0))

        else:

            # Check if what we are working with is a valid iterable:

            try:

                # Check if we can iterate:

                iter(mapper)

                # Set our iterable:

                iterable = enumerate(mapper)

            except TypeError:

                # Not a valid iterable!

                raise ValueError("Not a valid iterable!")

        # Now, iterate over the content:

        for num, value in iterable:

            # Check if we are registering a handler:

            if isinstance(value, BaseHandler) and type(self.get_handler(num)) == NullHandler:

                # Got a valid handler!

                self.add_handler(value, num)

                continue

            # Something else, lets use some recurision!

            self.load_handlers(value)

    def load_default(self):
        """
        Loads the default handlers for this HandlerCollection.

        We are called at instantiation if load_default is True.
        It can also be called at any point during the lifecycle of the collection.

        This function should load a set of handlers that is relevant to the 
        operation of the HandlerCollection.

        By default,
        we raise a 'NotImplementedError'.
        It is up to wrappers to implement this function!

        It is probably best if this function used the 'load_handlers()'
        method to do all the dirty work.
        """

        raise NotImplementedError("Must be implemented in child class!")

    def get_handler(self, id: int) -> BaseHandler:
        """
        Returns the handler at the given ID.

        :param id: ID of the handler to get
        :type id: int
        :return: The handler in question
        :rtype: BaseHandler
        """

        return self.handlers[id]

    def bind_callback(self, call: Callable, id: int, *args, **kwargs) -> Callable:
        """
        Binds a callback function to the handler
        at the given ID.

        We can either be called the conventional way,
        or we can be used as a decorator.

        Your run function should take at least one parameter,
        which will be the CurseInstance associated with the handler.
        Other arguments can optionally be provided.

        We keep a reference of the callback
        and arguments in this class as a dictionary.
        You can alter this structure yourself,
        but it is recommended to use the higher level methods for this.

        Any extra arguments that are passed will be saved and passed 
        to the callback at a later time.

        Multiple callbacks can be registered to an event!
        The order that they are added will be the order that they will be called.

        The callback will be called after the data is retrieved, decoded, and formatted!

        :param call: Callback function to add to the handler
        :type call: function
        :param id: ID of the handler to bind the callback to
        :type id: int
        """

        # Setup the basic structure:

        if id not in self.callbacks.keys():

            # Set the value to a list:

            self.callbacks[id] = []

        # Add the callback and argument info to the structure:

        self.callbacks[id].append((call, args, kwargs))

        return call

    def clear_callback(self, id: int, call: Callable=None) -> int:
        """
        Clears the callback from the given event.

        If a callback is not specified,
        then ALL callbacks will be cleared.
        If a callback is specified, 
        then the callbacks that match the provided object will be deleted.

        :param id: ID to clear
        :type id: int
        :param call: Callback to remove, optional
        :type call: Callbale, None
        :return: Number of callbacks removed.
        :rtype: int
        """

        removed = 0

        # Check if the ID is present:

        if id not in self.callbacks.keys():

            # Key is NOT present, return

            return removed

        # Iterate over callbacks at the ID:

        for index, val in enumerate(self.callbacks[id]):

            # Check if the callback matches:

            if val[0] == call or call is None:

                # Remove the callback:

                self.callbacks[id].pop(index)
                
                removed += 1

        # Return the number of items removed:

        return removed

    def get_search(self) -> SearchParam:
        """
        Returns a SearchParam used for searching.

        :return: SearchParam object used for searching
        :rtype: SearchParam
        """

        # Return a SearchParam object:

        return SearchParam()

    def default_formatter(self, form: BaseFormat):
        """
        Registers a default formatter to this object.

        We automatically attach the default formatter to
        any CurseDesciprion objects we return.

        If the CurseDescrpition does not inherit
        BaseFormat, then we will raise a TypeError excpetion.

        :param form: Formatter to register
        :type form: BaseFormat
        :raises: TypeError: If formatter does not inherit BaseFormat!
        """

        # Check if the given object inherits 'BaseFormatter':

        if not isinstance(form, BaseFormat):

            raise TypeError("Formatter must inherit 'BaseFormat'!")

        # Save the formatter instance:

        self.formatter = form

    def handle(self, id: int, *args, **kwargs) -> Any:
        """
        Invokes the handle process at the handler with the given ID.

        As outlined earlier,
        this gets and formats data from an external location.

        We pass all arguments and keyword arguments
        to the handler at the given ID.

        We also attach ourselves to valid CurseInstances automatically!
        If the returned data does not inherit BaseCurseInstance,
        then we will not attempt to attach ourselves to it,
        and simply return it.

        :param id: ID of the handler to call
        :type id: int
        :return: The final class provided by the handler
        :rtype: BaseCurseInstance
        """

        # First, we get the handler in question:

        hand = self.handlers[id]

        # Invoke the 'handle()' method:

        inst = hand.handle(*args, **kwargs)

        # Check if we are working with a tuple:

        if type(inst) == tuple:

            # Iterate over the tuple:

            for pack in inst:

                # Check if we are working with a valid instance:

                self._format_object(pack)

        else:

            # Check if we are working with a valid instance:

            self._format_object(inst)

        # Check if there is a valid event:

        if id in self.callbacks.keys():

            # Run all callbacks associated with the event:

            for call in self.callbacks[id]:

                # Run the callback:

                call[0](inst, *call[1], **call[2])

        # Return the instance:

        return inst

    def _format_object(self, pack):
        """
        Adds ourselves to any valid CurseInstances.

        :param pack: CurseInstance to format
        :type pack: BaseFormat
        """

        if isinstance(pack, base.BaseCurseInstance):

            # Attach ourselves to the instance:

            pack.hands = self

            # Check if we are working with CurseDescription:

            if isinstance(pack, base.CurseDescription):

                # Attach our formatter:

                pack.attach_formatter(self.formatter)
