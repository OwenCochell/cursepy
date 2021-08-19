.. _collec_basic:

==================
CurseClient Basics
==================

Introduction
============

This section contains documentation on how to use the 'CurseClient' class!
This is a general guide that will show you how to do basic operations,
and the types of calls you can make to get information from CurseForge.

CurseClient
===========

Now, what is a 'CurseClient', and why is it relevant?

The CurseClient (Hereafter referred to as CC),
is the class that facilitates communication with CurseForge(CF).
It does many things under the hood to make the communication with CF
a very simple procedure.

Some classes will inherit CurseClient to add extra functionality.
These components are called wrappers, and they are described in detail
elsewhere in this documentation.
Just know that most features defined here will be present in all
CC instances.

CC is a critical high level component of cursepy, and will be used extensively!

Creating a CurseClient
======================

Creating a CC is simple procedure, and can be done like this:

.. code-block:: python

    # Import the CC:

    from cursepy import CurseClient

    # Create the CC:

    client = HandlerCollection()

This will create a CC with the default handlers loaded.
If you do not want the default handlers to be loaded,
then you can pass 'False' to the 'load_default' parameter, like so:

.. code-block:: python

    # Create a CC, but without default handlers:

    client = CurseClient(load_default=False)

If no default handlers are loaded, 
then every event will have a 'NullHandler'
associated with it.

We will not get into handler management in this tutorial, 
but you can have a look at the :ref:`Advanced Tutorial <collec_advn>`
for more info!

.. note::

    In all following examples,
    we assume that a CC is properly imported and instantiated
    under the name 'client'.

Important Things to Keep in Mind
================================

CC uses a collection of handlers to add functionality.
These handlers are associated with certain events.
When an event is 'fired', then the handler associated with the event 
is called.
We derive all functionality from said handlers,
meaning that CC is only as useful as the handlers that
are currently loaded!
It is important to recognize that handlers
are the components that do all the dirty work
(Getting info, decoding it, and formatting it).
The only thing the CC does is organize
and call these handlers with the relevant information.

With that being said, 
for these next examples we will assume that
all events are associated with a handler
that accepts what we expect, and does what we expect
(Gets CurseForge info from somewhere and returns a CurseInstance that represents that info).
Handlers are under no obligation to adhere to these rules or follow them,
but it is strongly recommended that they do so!
Keep in mind that the built in handlers follow these recommendations,
so you should either be wary, or have a keen understanding on any third party handlers you load!

To sum it all up: CC manages handlers, but handlers provide the functionality!

We will not be going into the dirty details
about handler development and functionality.
We will be keeping the content at a surface level understanding only!
If you want a more in-depth explanation of handler development, 
you should check out the :ref:`handler tutorial <hand_advn>`.

.. _collec-constants:

CurseClient Constants
=====================

As stated earlier,
CC objects organize handlers by attaching them to events.
These events can be identified using integers.
CC contains constants that can be used to identify these events:

* [0]: LIST_GAMES - Gets a list of all valid games
* [1]: GAME - Get information on a specific game
* [2]: LIST_CATEGORY - Gets a list of all valid categories
* [3]: CATEGORY - Get information on a specific category
* [4]: SUB_CATEGORY - Get all sub-categories for the given category
* [5]: ADDON - Get information on a specific addon
* [6]: ADDON_SEARCH - Searches the game for addons
* [7]: ADDON_DESC - Get description for a specific addon
* [8]: ADDON_LIST_FILE - Gets a tuple of all files associated with an addon
* [9]: ADDON_FILE - Get information on a specific file for an addon
* [10]: FILE_DESCRIPTION - Description of a file

Here is an example of printing the integer associated
with getting game info:

.. code-block:: python 

    print(client.GAME)

These constants are automatically used when the entry level methods are called,
so if you stick to those you shouldn't have to worry about them.
However, if you want to use the lower-level 'handle()' method,
or register callbacks, 
then having an understanding of these constants will be very useful!

CurseClient Methods
===================

CC provides some entry points for getting information,
so developers have a standardized way of interacting with handlers.

All methods will take a number of events to pass to the handler,
and will return a CurseInstance representing the retrieved info.
We will go over all the types of information you can get.

.. note::
    You can read the :ref:`CurseInstance Tutorial <curse_inst>` for an in-depth look at these objects.
    For now, just know that CurseInstances
    are classes that represent CurseForge information.

    For example, the CurseGame class
    contains all identifying information
    for a given game on CurseForge

Handle Method
-------------

The lowest level method used to interact with handlers is the 'handle()' method.
This method is one level above manually calling the handler yourself.
The 'handle()' method also processes the returned objects,
like attaching ourselves to any returned CurseInstance objects,
which is necessary for them to operate correctly.

With that being said, you should only call this method if you want low-level
access to the loaded handlers.
You should instead use the higher-level entry functions,
as they automatically provide the necessary arguments to the 'handle()'
function for you (among other things).

Just because you might not use this method does not mean that you shouldn't understand it!
have a look at this example of the 'handle()' function in action:

.. code-block:: python

    inst = client.handle(ID)

This will invoke the handler at the given ID,
and process and return the object the handler 
gives us (Usually a CurseInstance).
Remember the event constants we listed earlier?
You can use those for the 'ID' parameter.
We also pass along all other arguments besides the ID 
to the handler. Here is an example of this in action:

.. code-block:: python 

    inst = client.handle(client.ADDON, 1234)

In this example, we call the handler that is associated with the addon event 
and pass the integer '1234'.

Again, most likely, you will not have to use the 'handle()' method.
The high-level methods not only automatically configure the 'handle()' method for you,
but also provide a standardized way of interacting with handlers. 

Getting Game Info
-----------------

To get info on a specific game, 
you can use the 'game' method:

.. code-block:: python

    game = client.game(GAME_ID)

Where GAME_ID is the game ID.
This method will return a CurseGame object
representing the game.

To get a tuple of all valid games on CurseForge,
you can use the 'games' method:

.. code-block:: python

    games = client.games()

'game' takes no parameters,
and it returns a tuple of CurseGame objects
representing each game.

Getting Category Info
---------------------

To get info on a specific category,
you can use the 'category' method:

.. code-block:: python

    cat = client.category(CAT_ID)

Where CAT_ID is the category ID.
We will return a CurseCategory object
that represents the category.

As stated earlier,
categories can have sub-categories.
To get a tuple of these sub-categories,
you can use the 'sub_category' method:

.. code-block:: python

    sub_cats = client.sub_category(CAT_ID)

If no sub-categories are found,
then the returned tuple will be empty.

Getting Addon Info
------------------

We offer a few methods for getting addon info.

First, you can get info on a specific addon
using the 'addon' method:

.. code-block:: python

    addon = client.addon(ADDON_ID)

Where ADDON_ID is the ID of the addon to get.
We will return a CurseAddon object 
that represents the addon.

However, this information is incomplete!
Another call must be made to retrieve the
addon description. You can use the 'addon_description'
method for this:

.. code-block:: python

    desc = client.addon_description(ADDON_ID)

This will return a CurseDescription
object representing the addon description.

.. _search:

You can also search for addons using the 'search' method:

.. code-block:: python

    result = client.search(GAME_ID, CAT_ID, search=search_param)

Where GAME_ID is the ID of the game to search under,
and CAT_ID is the category ID to search under.
We return a tuple of CurseAddon objects representing the search results.

Users can optionally provide a search object
to fine tune to search operation. 
You can get a search object using the 'get_search'
method:

.. code-block:: python

    search = client.get_search()

The 'SearchParam' objects contains the following values
for fine-tuning the search operation:

* filter - Value to search for 
* index - Page index to search under
* pageSize - Number of items to display per page
* gameVersion - Game version to search under
* sort - Sorting method to use

Explaining Search Parameters
____________________________

Most of these values are self-explanatory.

'filter' is the actual search term to search for.

'gameVersion' is the game version to search under.
This varies from game to game, and should be a string.

'sort' is an integer that represents the sorting type.
You can use the search constants present in SearchParam to define this:

* [0]: FEATURED - Sort by featured 
* [1]: POPULARITY - Sort by popularity 
* [2]: LAST_UPDATE - Sort by last updated
* [3]: NAME - Sort by name 
* [4]: AUTHOR - Sort by author 
* [5]: TOTAL_DOWNLOADS - Sort by total downloads

Check out this example of sorting by popularity:

.. code-block:: python

    # Get the search object:

    search = client.get_search()

    # Set the sorting type:

    search.sort = search.POPULARITY 

'index' and 'pageSize' are used since search
results are usually limited to 'pages'
to save some bandwidth.

'index' is the page to retrieve,
and 'pageSize' is the size of each page.

Here is an example of getting the second page of search results:

.. code-block:: python

    # Get the SearchParam:

    search = client.get_search()

    # Set the page index to 1:

    search.index = 1

    # Get the results:

    result = client.search(GAME_ID, CAT_ID, search)

If you want to iterate over ALL content over all valid pages,
CC has a method for that.
You can use the 'iter_search' method to iterate over all 
search results until we reach the end.
We use the 'search' method to get each page of values,
meaning that we use the handler associated with searching.
We automatically bump the index value at the end of each page.

Here is an example of this where we search for addons under the name 'test'
and print each name:

.. code-block:: python

    # Get the SearchParam:

    search = client.get_search()

    # Set the filter to 'test':

    search.filter = 'test'

    # Iterate over ALL addons:

    for addon in client.iter_search(GAME_ID, ADDON_ID, search):

        print(addon.name)

'iter_search' only bumps the index after each call,
so you can start at a page by setting the 'index'
value on the SearchParam before passing it along.
The 'iter_search' does not alter any other parameters,
so your search preferences will be saved.

Getting File Info
-----------------

Like the previous sections,
we have a few ways of getting file info.

First things first, you can get a list of all files
associated with an addon:

.. code-block:: python

    files = client.addon_files(ADDON_ID)

Where ADDON_ID is the ID of the addon to get files for.
This function will return a tuple of CurseFile instances
representing each file.

To get info on a specific file,
you can use the 'addon_file' method:

.. code-block:: python

    file = client.addon_files(ADDON_ID, FILE_ID)

Where FILE_ID is the ID of the file to get info for.
This function will return a CurseFile
instance representing the file. 

Like the addon methods documented earlier,
this info is incomplete!
You can get the file description like so:

.. code-block:: python

    desc = client.file_description(ADDON_ID, FILE_ID)

This will return a CurseDescription object,
much like the 'addon_description' method.

Callbacks
=========

Usually, users will call the entry point methods,
and react to the objects that get returned.
This is great for most user cases.
However, if you want to go for a more 'reactive' model,
you can bind callbacks to events which will be called 
upon after each handle request.

A 'callback' is a callable that does something with the data returned by the handler.
It should have at least one argument, which will be the object returned by the handler.
Any other arguments are optional.

Here is an example callback that prints the given data to the terminal:

.. code-block:: python 

    def dummy_callback(data):

        # Just print the data:

        print(data)

In this case, the callback is a simple function.
Now, let's bind this function to the CC under the 'FILE' event:

.. code-block:: python 

    client.bind_callback(client.FILE, dummy_callback)

Remember the event constants defined earlier?
You can use those again here to define the event the callback should be bound to!
After we receive the data from the handler associated with the FILE event,
the CC will automatically call this function, and pass the returned value to the callback.

Consider this next example:

.. code-block:: python 

    inst = client.addon_file(ADDON_ID, FILE_ID)

This method, as stated earlier, will return a CurseFile instance.
The 'ADDON_ID' is the ID of the addon, and the 'FILE_ID' is the ID of the file.
This method will return a CurseFile object as usual, 
but before it does it will call the 'dummy_callback' method,
and pass along the CurseFile object.
You can see how this can be useful!

The user can bind as many callbacks to an event as they see fit.
They will be called in the order they have been added.
For example, if the user was to attach a method named 'cool_method' to the FILE event,
then 'dummy_method' will be called first, and 'cool_method' will be called second.

You can also specify arguments that will be passed to the callback once it is ran.
Keep in mind that the first argument should ALWAYS be the data returned by the handler!
Let's see an example of this in action:

.. code-block:: python

    def multi_arg(data, arg1, arg2, arg3=None):

        # We take many arguments!

        print("Data: {}, arg1: {}, arg2: {}, arg3: {}".format(data, arg1, arg2, arg3))

    # Attach the callback:

    client.bind_callback(client.FILE, multi_arg, 1, 2, arg3=3)

As you can see, any extra arguments specified in the 'bind_callback()' method will be saved and passed along to the callback.
In this case, the arguments provided are integers, but they can be anything. 
When the FILE event is invoked, then the callback will be ran and the output will be this:

.. code-block::

    Data: [HANDLER DATA], arg1: 1, arg2: 2, arg3: 3

Where HANDLER_DATA is whatever the handler returned.
Again, we save and pass all arguments and keyword arguments to the callback upon runtime!

Finally, callbacks can be added using decorators.
Here is an example of this in action:

.. code-block:: python

    @client.bind_callback(client.GAME)
    def callback(data):
        
        print("We have been ran!")

In this example, the function 'callback()' 
is automatically registered to the CC by using the 'bind_callback()'
as a decorator.
As stated earlier, any other arguments will be saved and passed 
to the callback at runtime.

Removing callbacks is very easy to do.
You can simply use the 'clear_callback()' method:

.. code-block:: python 

    client.clear_callback(ID)

Where ID is the event ID to remove callbacks from.
For example, if you provide the FILE event ID,
then all callbacks associated with the FILE event will be removed.
This method returns an integer representing the number of callbacks removed.

If you want to remove a specific callback,
then you can use the 'call' parameter:

.. code-block:: python

    client.clear_callback(ID, call=CALL)

Where 'call' is the instance of the callback to remove.
The 'clear_callback()' method will only return callbacks that 
match the 'call' parameter.
This is great if you have multiple callbacks associated 
with a certain event, 
and only want to remove a certain callback.

For example, let's remove the 'dummy_callback()'
function that is associated with the FILE event:

.. code-block:: python 

    client.clear_callback(client.FILE, call=dummy_callback)

Again, this ensures that only the 'dummy_callback()' function will be removed.

Conclusion
==========

That concludes the tutorial on basic
CC features!

If you want some insight into advanced CC features,
such as handler loading, be sure to check out the :ref:`Advanced Tutorial <collec_advn>`.
