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
CurseClient is actually a wrapper!
It loads the default handlers and offers entry 
points into said handlers.

ALL built in handlers inherit CurseClient,
meaning that the entry point methods will always be available,
regardless of the wrapper.
Do keep in mind, that not all third party handlers
will inherit CurseClient, meaning that some methods may be unavailable.
Be sure that you know your handlers before you use them!

MinecraftWrapper
================

The MinecraftWrapper makes working with minecraft addons much easier.
We have the following constants:

* GAME_ID - ID of the Minecraft game(432)
* RESOURCE_PACKS - ID of the resource packs category(12)
* MODPACKS - ID of the modpack category(4471)
* MODS - ID of the mods category(6)
* WORLDS - ID of the worlds category(17)

You can use these constants in the entry point methods.
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

Conclusion
==========

That concludes the wrapper tutorial!

You should now have an understanding of all built in wrappers.