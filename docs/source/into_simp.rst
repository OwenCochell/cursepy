==================
Usage Introduction
==================

Introduction
============

Welcome to the usage tutorial for capy!

In this document, we outline some terminology
and concepts that will offer some insight into not only capy,
but CurseForge itself!

We will keep the concepts at the surface level only, 
as this tutorial is meant to give you an understanding
of basic understanding of capy and it's components.
If you want a advanced look at capy,
such as handler development,
then you should have a look at the advanced tutorial[LIKE HERE]

What is CurseForge?
===================

`CurseForge<https://www.curseforge.com/>`_
(Hereafter referred to as CF),
is a service that provides modifications(or addons)
to games, which alters the game in a certain way.
This can be anything ranging from re-textures,
to adding new features, or modifying existing ones.
The types of addons you can install varies from game to game.

For example, have a look at the `JEI<https://www.curseforge.com/minecraft/mc-mods/jei>`_ addon for the game Minecraft.
JEI alters the UI, displaying extra info about items and recipes.
We will not go into the dirty details about game mods,
but JEI is an excellent example of an addon that changes aspects of a game.

If you checked out the above example
(You should do so if you haven't!),
then you will see that CF hosts the JEI mod,
offering info and the ability to download the mod files.
CF also offers a client that will fetch and automatically install
mods to there relevant locations. This client will also keep mods updated,
and resolve any dependencies, so the end user does not have to manage mods themselves.
You can find this client `here<https://download.curseforge.com/>`_.

Suffice it to say, CF plays a huge role in addon distribution,
and the addon catalog and supported games grow bigger each day!

The Role of capy
================

capy aims to provide a modular, easy to use interface
for communicating with CF.

We offer the ability to download addon info,
get addon files, and other misc. operations 
like getting supported games and categories.

We do this by offering intuitive calls to capy components, 
allowing you to get the info you need without being too complicated.

Before we get into the swing of things, 
we have just a few more concepts to go over.

CF Hierarchy
============

CF has a hierarchy of components that organize addons:

.. code-block::

    Games -> Categories -> Sub-Categories -> Addons -> Files

Essentially, games hold categories,
categories hold addons, and addons hold files.
Each category can hold a variable amount of objects.
An addon can be in multiple categories or sub-categories.

This architecture allows for addons to be organized
into categories, and for files to be kept solely
in the addon they belong to.

capy allows you to work with components 
in each layer of the hierarchy.
You will understand how to do this in a later tutorial,
but for now keep this hierarchy in mind! 

capy Terms
==========

capy has a few concepts that might be better understood with some explanation.

HandlerCollection
-----------------


