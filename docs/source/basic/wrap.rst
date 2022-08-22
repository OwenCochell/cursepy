=============
Wrap Tutorial
=============

Introduction
============

This section contains documentation on built in wrappers.
We will cover what a handler is, 
and how to use them to your advantage.

What is a Wrapper?
==================

A 'wrapper' is a class that makes communicating with a certain game much easier.
They may contain category IDs and methods that allow for easy communication.
wrappers might also load certain handlers that work well
with the game.

Just to put this in perspective,
BaseClient is actually a wrapper!
It loads the default handlers and offers entry 
points into said handlers.

ALL built in wrappers inherit BaseClient,
meaning that the entry point methods will always be available,
regardless of the wrapper.
Do keep in mind, that not all third party handlers
will inherit BaseClient, meaning that some methods may be unavailable.
Be sure that you know your handlers before you use them!

.. _curse_client:

CurseClient
===========

The CurseClient is a wrapper that is altered to work with the official CurseForge backend.

To do this, we load the official :ref:`CurseForge handlers<curse_handlers>`.
Because these handlers require an API key to work correctly,
you will need to provide an API key when this wrapper is instantiated:

.. code-block:: python

    from cursepy.wrapper import CurseClient

    client = CurseClient(API_KEY)

Where API_KEY is the API key you `obtained from CurseForge <https://docs.curseforge.com/#what-is-curseforge-core>`_.

CurseClient also requires a game ID when getting sub-catagories:

.. code-block:: python

    client.sub_category(GAME_ID, CAT_ID)

Where GAME_ID is the game ID the category lies under,
and CAT_ID is the category you wish to get sub-catagories for.

Finally, because the :ref:`CurseForge handlers<curse_handlers>` do not support individual category lookup,
you will be unable to use the 'category()' method.
This is a limitation with the official CurseForge API.

MinecraftWrapper
================

The MinecraftWrapper makes working with minecraft addons much easier.
We have the following constants:

* GAME_ID - ID of the Minecraft game(432)
* RESOURCE_PACKS - ID of the resource packs category(12)
* MODPACKS - ID of the modpack category(4471)
* MODS - ID of the mods category(6)
* WORLDS - ID of the worlds category(17)
* BUKKIT - ID of the bukkit category(5)

You can use these constants in the entry point methods.
This wrapper has the following methods:

get_minecraft
-------------

Returns a :ref:`CurseGame<curse_game>` object for the game 'Minecraft'.
This method takes no arguments.

mine_sub_category
-----------------

Returns all sub-catagories (tuple of :ref:`CurseCategory<curse_category>` objects) for the given category ID.
We automatically fill in the game ID for you,
so this makes working with Minecraft sub-catagories identical to the BaseClient.
We take one parameter, the category ID.

MinecraftWrapper also provides some methods to make searching easier.
Each method takes one parameter, a SearchParam object.

search_resource_packs
---------------------

Searches the resource packs category for addons.

search_modpacks
---------------

Searches the modpacks category for addons.

search_mods
-----------

Searches the mods category for addons.

search_worlds
-------------

Searches the worlds category for addons.

search_plugins
--------------

Searches the Bukkit plugins category for addons.

Conclusion
==========

That concludes the wrapper tutorial!

You should now have an understanding of all built in wrappers.