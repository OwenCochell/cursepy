=================
Collection Basics
=================

Introduction
============

This section contains documentation on how to use the 'HandlerCollection' class!
This is a general guide that will show you how to do basic operations,
and the types of calls you can make to get information from CurseForge.

HandlerCollection
=================

Now, what is a 'HandlerCollection', and why is it relevant?

The HandlerCollection(Hereafter referred to as HC),
is the class that manages handlers, and offers entry points into them.
This allows you to call handlers in a standardized way,
regardless of the handler type.
It is best practice to use the HC entry points
instead of calling handlers directly.

Some classes will inherit HandlerCollection to add extra functionality.
These components are called wrappers, and they are described in detail
elsewhere in this documentation.
Just know that most features defined here will be present in all
HC instances.

HC is a critical component of capy, and will be used extensively!


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
for these next examples we will assume that
all events are associated with a handler
that accepts what we expect, and does what we expect
(Gets CurseForge info from somewhere and returns a CurseInstance that represents that info).
Handlers are under no obligation to adhere to these rules or follow them,
but it is strongly recommended that they do so!
Keep in mind that the built in handlers follow these recommendations,
so you should either be wary, or have a keen understanding on any third party handlers you load!

To sum it all up: HC's manage handlers, but handlers provide the functionality!

We will not be going into the dirty details
about handler development and functionality.
We will be keeping the content at a surface level understanding only!
If you want a more in-depth explanation of handler development, 
you can go [HERE].

HandlerCollection Methods
=========================

HC provides some entry points for getting information,
so developers have a standardized way of interacting with handlers.

All methods will take a number of events to pass to the handler,
and will return a CurseInstance representing the retrieved info.
We will go over all the types of information you can get.

.. note::
    You can read all about CurseInstances [HERE].
    For now, just know that CurseInstances
    are classes that represent CurseForge information.

    For example, the CurseGame class
    contains all identifying information
    for a given game on CurseForge

Getting Game Info
-----------------

To get info on a specific game, 
you can use the 'game' method:

.. code-block:: python

    game = hands.game(GAME_ID)

Where GAME_ID is the game ID.
This method will return a CurseGame object
representing the game.

To get a tuple of all valid games on CurseForge,
you can use the 'games' method:

.. code-block:: python

    games = hands.games()

'game' takes no parameters,
and it returns a tuple of CurseGame objects
representing each game.

Getting Category Info
---------------------

To get info on a specific category,
you can use the 'category' method:

.. code-block:: python

    cat = hands.category(CAT_ID)

Where CAT_ID is the category ID.
We will return a CurseCategory object
that represents the category.

As stated earlier,
categories can have sub-categories.
To get a tuple of these sub-categories,
you can use the 'sub_category' method:

.. code-block:: python

    sub_cats = hands.sub_category(CAT_ID)

If no sub-categories are found,
then the returned tuple will be empty.

Getting Addon Info
------------------

We offer a few methods for getting addon info.

First, you can get info on a specific addon
using the 'addon' method:

.. code-block:: python

    addon = hands.addon(ADDON_ID)

Where ADDON_ID is the ID of the addon to get.
We will return a CurseAddon object 
that represents the addon.

However, this information is incomplete!
Another call must be made to retrieve the
addon description. You can use the 'addon_description'
method for this:

.. code-block:: python

    desc = hands.addon_description(ADDON_ID)

This will return a CurseDescription
object representing the addon description.

You can also search for addons using the 'search' method:

.. code-block:: python

    result = hands.search(GAME_ID, CAT_ID, search=search_param)

Where GAME_ID is the ID of the game to search under,
and CAT_ID is the category ID to search under.
We return a tuple of CurseAddon objects representing the search results.

Users can optionally provide search object
to fine tune to search operation. 
You can get a search object using the 'get_search'
method:

.. code-block:: python

    search = hands.get_search()

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

    search = hand.get_search()

    # Set the sorting type:

    search.sort = search.POPULARITY 

'index' and 'pageSize' are used due to search
results are usually limited to 'pages'
to save some bandwidth.

'index' is the page to retrieve,
and 'pageSize' is the size of each page.

Here is an example of getting the second page of search results:

.. code-block:: python

    # Get the SearchParam:

    search = hands.get_search()

    # Set the page index to 1:

    search.index = 1

    # Get the results:

    result = hands.search(GAME_ID, CAT_ID, search)

If you want to iterate over ALL content over all valid pages,
HC has a method for that.
You can use the 'iter_search' method to iterate over all 
search results until we reach the end.
We use the 'search' method to get each page of values,
meaning that we use the handler associated with searching.
We automatically bump the index value at the end of each page.

Here is an example of this where we search for addons under the name 'test'
and print each name:

.. code-block:: python

    # Get the SearchParam:

    search = hands.get_search()

    # Set the filter to 'test':

    search.filter = test

    # Iterate over ALL addons:

    for addon in hands.iter_search(GAME_ID, ADDON_ID, search):

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

    files = hands.addon_files(ADDON_ID)

Where ADDON_ID is the ID of the addon to get files for.
This function will return a tuple of CurseFile instances
representing each file.

To get info on a specific file,
you can use the 'addon_file' method:

.. code-block:: python

    file = hands.addon_files(ADDON_ID, FILE_ID)

Where FILE_ID is the ID of the file to get info for.
This function will return a CurseFile
instance representing the file. 

Like the addon methods documented earlier,
this info is incomplete!
You can get the file description like so:

.. code-block:: python

    desc = hands.file_description(ADDON_ID, FILE_ID)

This will return a CurseDescription object,
much like the 'addon_description' method.


Conclusion
==========

That concludes the tutorial on basic
HC features!

Be sure to check the other tutorials for 
info on other components, especially the
CurseInstance tutorial!

If you want some insight into advanced HC features,
such as handler loading, be sure to check out the Advanced Tutorial.
