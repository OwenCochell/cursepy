.. _hand-built:

================
Builtin Handlers
================

Introduction
============

This document outlines the handlers that are built into cursepy.
We will go over the supported events,
protocols, and backends in use by these handlers.

.. _curse_handlers:

Official CurseForge Handlers
============================

CFHandlers handlers get info from the official CurseForge API.

.. note::

    These handlers require an `API key <https://forms.monday.com/forms/dce5ccb7afda9a1c21dab1a1aa1d84eb?r=use1>`_ to work correctly.

CF Basic Info
-------------

* Name: CurseForge
* Protocol Object: URLProtocol
* Raw Data: dictionary, or HTML string if event 7 or 10
* Metadata: :ref:`URLProtocol Metadata<url-meta>`

CF Supported Events
-------------------

* [0]: LIST_GAMES
* [1]: GAME
* [2]: LIST_CATEGORY
* [4]: SUB_CATEGORY
* [5]: ADDON
* [6]: ADDON_SEARCH
* [7]: ADDON_DESC
* [8]: ADDON_LIST_FILE
* [9]: ADDON_FILE
* [10]: FILE_DESCRIPTION


CF Unsupported Events
----------------------

* [3]: CATEGORY

CF Long Description
-------------------

CurseForge handlers utilize HTTP to get CF data.
The retrieved data is in JSON format,
with the exception of events 7 and 8,
which is HTML text.
This text is converted into a string.
The raw data is attached to CurseInstances as dictionaries,
with the example of 7 and 8, in which the data is a HTML string.

CFHandlers use :ref:`URLProtocol<url-proto>`
as our protocol object, and inherits :ref:`URLHandler<url-hand>`
to add this functionality.
We use the URLProtocol object to generate valid metadata on the connection,
which we attach to the CurseInstance.

Due to a limitation in the CurseForge API,
we can't lookup individual catagories by ID.
We also require a game ID to lookup sub-catagories.

You can load the handler map by using the svc_map:

.. code-block:: python

    from cursepy.handlers.curseforge import cf_map

    client.load_handlers(cf_map)

These handlers require an API key to work correctly.
One way to get an API key to the handlers is to attach the key to each handler:

.. code-block:: python

    hand.key = API_KEY

Simply attach it to the 'key' parameter of the handler.
CFhandlers will also attempt to extract the key from the :ref:`HandlerCollection<collec_advn>` it is attached to.
Simply attach a key to the 'curse_api_key' parameter of the collection it is attached to:

.. code-block:: python

    hands.curse_api_key - API_KEY

Finally, you can use the :ref:`CurseClient<curse_client>`, which requires a key to instantiate,
and will put it in the required locations.

SVCHandlers
===========

SVCHandlers get info from forgesvc.net.

.. warning::

    These handlers are now deprecated and should not be used!

Curse Forge has shut down the ForgeSVC API,
and all requests made to this service will fail.

SCV Basic Info
--------------

* Name: ForgeSVC 
* Protocol Object: URLProtocol
* Raw Data: dictionary, or HTML string if event 7 or 10
* Metadata: :ref:`URLProtocol Metadata<url-meta>`

SVC Supported Events
--------------------

* [0]: LIST_GAMES
* [1]: GAME
* [2]: LIST_CATEGORY
* [3]: CATEGORY
* [4]: SUB_CATEGORY
* [5]: ADDON
* [6]: ADDON_SEARCH
* [7]: ADDON_DESC
* [8]: ADDON_LIST_FILE
* [9]: ADDON_FILE
* [10]: FILE_DESCRIPTION

SVC Unsupported events
----------------------

None!

SVC Long Description
--------------------

SVCHandlers utilize HTTP to get CF data.
The retrieved data is in JSON format,
with the exception of events 7 and 8,
which is HTML text.
This text is converted into a string.
The raw data is attached to CurseInstances as dictionaries,
with the example of 7 and 8, in which the data is a HTML string.

SVCHandlers use :ref:`URLProtocol<url-proto>`
as our protocol object, and inherits :ref:`URLHandler<url-hand>`
to add this functionality.
We use the URLProtocol object to generate valid metadata on the connection,
which we attach to the CurseInstance.

You can load the handler map by using the svc_map:

.. code-block:: python

    from cursepy.handlers.forgesvc import svc_map

    client.load_handlers(svc_map)
