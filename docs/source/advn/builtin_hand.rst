.. _hand-built:

================
Builtin Handlers
================

Introduction
============

This document outlines the handlers that are built into cursepy.
We will go over the supported events,
protocols, and backends in use by these handlers.

SVCHandlers
===========

SVCHandlers get info from forgesvc.net.

Basic Info
----------

* Name: ForgeSVC 
* Protocol Object: URLProtocol
* Raw Data: dictionary, or HTML string if event 7 or 10
* Metadata: :ref:`URLProtocol Metadata<url-meta>`

Supported Events:
-----------------

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

Non-supported events:
---------------------

None!

Long Description
----------------

SVCHandlers utilise HTTP to get CF data.
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

SVCHandlers are loaded first by default!
