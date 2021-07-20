=================
Collection Basics
=================

Introduction
============

This section contains documentation on how to use the 'HandlerCollection' class!
This is a general guide that will show you how to do basic operations,
and the types of calls you can make to get CurseForge information.

HandlerCollection
=================

Now, what is a 'HandlerCollection', and why is it relevant?

The HandlerCollection(Hereafter referred to as HC),
is the class that manages handlers, and offers entry points into them.
This allows you to call handlers in a standardized way,
regardless of the handler type.
HC is a critical component of capy, and will be used extensively!

Some classes will inherit HandlerCollection to add extra functionality.
These components are called wrappers, and they are described in detail
elsewhere in this documentation.
Just know that most features defined here will be present in all
HC instances!

Creating HandlerCollection
===========================

Creating a HandlerCollection is simple procedure, and can be done like so:

.. code-block:: python

    # Import the HC:

    from capy import HandlerCollection

    # Create the HC:

    hands = HandlerCollection()

This will create a HC with the default handlers loaded.
If you do not want the default handlers to be loaded,
then you can pass 'False' to the 'load_default' parameter, like so:

.. code-block:: python

    # Create a HC, but without default handlers:

    hands = HandlerCollection(load_default=False)

If no default handlers are loaded, 
then every event will have a 'NullHandler'
associated with it.
(You can read all about handler types elsewhere in the documentation).

We will touch on handler management later in this section,
but first we will touch on how to get game information.

.. note::

    In all following examples,
    we assume that a HC is properly imported and instantiated
    under the name 'hands'.

Important Things to Keep in Mind
================================

As per the name, HC is a collection of handlers.
We derive all functionality from said handlers,
meaning that HC is only as useful as the handlers that
are currently loaded!
It is important to recognize that handlers
are the components that do all the dirty work
(Getting info, decoding it, formatting it).
The only thing the HC does is organize
and call these handlers with the relevant information.

With that being said, 
for these next examples we assume that 
all events are associated with a handler
the accepts what we expect, and does what we expect
(Gets CurseForge info from somewhere and returns a CurseInstance that represents that info).
Handlers are under no obligation to adhere to these rules or follow them,
but it is strongly recommended that they do so!
Keep in mind that the built in handlers follow these recommendations,
so you should either be wary, or have a keen understanding on any third party handlers you load!

To sum it all up: HC's manage handlers, but handlers are the functionality!

HandlerCollection Event IDs
===========================

To identify actions, and what handlers actually do,
HC uses integers to identify 'events'.
An 'event' is an operation that gets info from CurseForge.
Handlers are identified by these ID's, as the HC needs a way to determine what each handler does.
HC has constants the identify events,
so you don't have to play around with ints.

If you use the entry point functions,
then you should not have to work with event ID's!
Still though, it is good to have a basic idea
of event IDs, what they are mapped to, and what each event is supposed to do.

Here is a breakdown of all events, their ID's, and the constant names:

    * [0]: LIST_GAMES - Gets a list of all valid CurseForge games
    * [1]: GAME - Gets information on a specific game
    * [2]: LIST_CATEGORY - Gets a list of all valid CurseForge categories
    * [3]: CATEGORY - Information on a specific category
    * [4]: SUB-CATAGORIES - Gets a list of all sub-categories for the given category
    * [5]: ADDON - Information on a specific CurseForge addon
    * [6]: ADDON_SEARCH - Searches for addons
    * [7]: ADDON_DESC - Description of an addon
    * [8]: ADDON_LIST_FILE - List of all files for a given addon
    * [9]: ADDON_FILE - Specific file for an addon
    * [10]: FILE_DESCRIPTION - Description of a file 

Here is an example of getting the value for the 'GAME' event:

.. code-block:: python

    # Get the value of the GAME event:

    print(hands.GAME)

This code should print '1'.

HandlerCollection Methods
=========================

HC provides some entry points for getting information,
so developers have a standardized way of interacting with handlers.

All methods will take a number of events to pass to the handler,
and will return a CurseInstance representing the retrieved info

.. note::
    You can read all about CurseInstances [HERE].
    For now, just know that CurseInstances
    are classes that represent CurseForge information.

    For example, the CurseGame class
    contains all identifying information
    for a given game on CurseForge

handle
------

The 'handle()' method is the low-level way to interact with handlers.

.. warning::
    Using this method is not recommended!
    Users should really use the higher-level methods
    for getting curse information.

It accepts the following parameters:

    * id - ID of the handler to call

Any other arguments or key word arguments passed
will be passed to the handler.

This method is useful for wrappers of children of HC
that need a low-level method for calling handlers.
Using this method is not recommended for end users!
You should probably use the higher level methods 
that explicitly define necessary arguments.

Have a look at this example:

.. code-block:: python

    # Define an addon ID:

    addon_id = 123456

    # Call the handler and pass the addon ID:

    inst = hands.handle(hands.ADDON, addon_id)

In this example, we will call the 'handle' method
with the value of 'addon_id' passed as an argument.
(If you want some more info on how handlers are called,
check out the advanced usage tutorial [LINK HERE]).

This method will also return what the handler returns,
which is usually a CurseInstance.

This method does some things under the hood to the values returned.
If a CurseInstance is returned, then we automatically 
attach ourselves to it.

games
-----

Gets a list of all valid games from CurseForge.

.. warning::

    This call is very resource intensive!
    You should refrain from using this method 
    if you can help it!

This function takes no arguments,
and should return a tuple of CurseGame instances:

.. code-block:: python

    # Get list of games:

    games = hands.games()

    # Iterate over the games:

    for game in games:

        # Print the name of the game:

        print(game.name)

game
----

Gets specific info on game.

We take the game ID as the argument,
and return a CurseGame instance:

.. code-block:: python

    # Define the game ID:

    GAME_ID = 12345

    # Get the game info:

    game = hands.game(GAME_ID)

    # Print the name of the game:

    print(game.name)

catagories
----------

Gets ALL valid catagories on CurseForge.

.. warning::

    This method can be very resource intensive!
    You should refrain from using this method if you can help it!

We take no arguments, 
and return a tuple of CurseCategory
instances:

.. code-block:: python

    # Get the categories:

    cats = hands.catagories()

    # Iterate over the categories:

    for cat in cats:

        # Print the name:

        print(cat.name)

category
--------

Gets info on a specific category.

We take a category ID as our parameter,
and we return a CurseCategory:

.. code-block:: python

    # Define the category ID:
    
    CAT_ID = 123456

    # Get the category:

    cat = hands.category(CAT_ID)

    # Print the name of the category:

    print(cat.name)

sub_category
------------

Gets the sub-categories of a given category.

We take the parent category ID as our parameter,
and we return a tuple of CurseCategory objects
representing the sub-categories.

.. code-block:: python

    # Define the category ID:

    CAT_ID = 123456

    # Get the sub-categories:

    sub_cats = hands.sub_category(CAT_ID)

    # Iterate over them:

    for cat in sub_cats:

        # Print the name:

        print(cat.name)

addon
-----

Gets info on a specific addon.

We take the addon ID of the addon
as our parameter, and we return a CurseAddon
object representing the addon:

.. code-block:: python

    # Define the addon ID:

    ADDON_ID = 123456

    # Get the addon:

    addon = hands.addon(ADDON_ID)

    # Print the addon name:

    print(addon.name)

search
------

Searches a category for addons.

We take the ID of the category to search under as the 
mandatory parameter. You can optionally provide
a search parameter object to fine-tune the search options.

