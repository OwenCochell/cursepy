.. _hand-built:

================
Builtin Handlers
================

Introduction
============

This document outlines the handlers that are built into cursepy.
We will go over the supported events,
protocols, and backends in use by these handlers.

.. _meta_curse:

Meta CurseForge Handlers
========================

Meta CurseForge handlers allow for handlers to interact with APIs similar to the official CurseForge API.

.. note:: 

    These handlers are designed for development use only, and should not be used!

MCF Basic Info
--------------

* Name: Meta-CurseForge
* Protocol Object: URLProtocol
* Raw Data: dictionary, or HTML string if event 7 or 10
* Metadata: :ref:`URLProtocol Metadata<url-meta>`

MCF Supported Events
--------------------

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


MCF Unsupported Events
----------------------

* [3]: CATEGORY

MCF Long Description
--------------------

These handlers are designed to be used by handlers that communicate with APIs 
that are similar to the official CurseForge API.
They only implement the 'format()', 'pre_process()', and 'post_process()' methods.
Because of this, these handlers do nothing, and should not be used outside of development purposes.

An API is regarded as 'similar' if it follows these qualifications:

 * The service utilizes HTTP(s)
 * Data is returned in JSON format
 * Response data matches the schema of the official CurseForge API (with some exceptions)

CurseForge handlers utilize HTTP to get CF data.
The retrieved data is in JSON format,
with the exception of events 7 and 8,
which is HTML text.
This text is converted into a string.
The raw data is attached to CurseInstances as dictionaries,
with the example of 7 and 8, in which the data is a HTML string.

MCFHandlers use :ref:`URLProtocol<url-proto>`
as our protocol object, and inherits :ref:`URLHandler<url-hand>`
to add this functionality.
We use the URLProtocol object to generate valid metadata on the connection,
which we attach to the CurseInstance.

Due to a limitation in the CurseForge API,
we can't lookup individual catagories by ID.
We also require a game ID to lookup sub-catagories.

These handlers also implement some compatibility features to make working 
with multiple backends easier.
For example, we make all incoming keys lowercase to remove issues with key formatting.
We also have some error checking on keys that are sometimes not included in the response data,
such as 'thumbsUpCount'.

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

These handlers communicate with the official CurseForge API.
We inherit from :ref:`Meta CurseForge Handlers<meta_curse>` to add functionality.

As stated in the :ref:`Meta CurseForge Handlers<meta_curse>` section,
we do not support individual category lookup.

You can load the handler map by using the svc_map:

.. code-block:: python

    from cursepy.handlers.curseforge import cf_map

    client.load_handlers(cf_map)

These handlers require an API key to work correctly.
One way to get an API key to the handlers is to attach the key to each handler:

.. code-block:: python

    hand.set_key(KEY)

You can use the 'set_key()' method to do this.
CFhandlers will also attempt to extract the key from the :ref:`HandlerCollection<collec_advn>` it is attached to.
Simply attach a key to the 'curse_api_key' parameter of the collection it is attached to:

.. code-block:: python

    hands.curse_api_key = API_KEY

Finally, you can use the :ref:`CurseClient<curse_client>`, which requires a key to instantiate,
and will put it in the required locations.

.. _ct_handlers:

Curse Tools Handlers
====================

CTHandlers handlers get data from the `CurseTools API <https://www.curse.tools/>`_.

CT Basic Info
-------------

* Name: CurseTools
* Protocol Object: URLProtocol
* Raw Data: dictionary, or HTML string if event 7 or 10
* Metadata: :ref:`URLProtocol Metadata<url-meta>`

CT Supported Events
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


CT Unsupported Events
----------------------

* [3]: CATEGORY

CT Long Description
-------------------

The CurseTools handlers retrieve data from the `CurseTools API <https://www.curse.tools/>`_.
We inherit from :ref:`Meta CurseForge Handlers<meta_curse>` to add functionality.
These handlers do not require an API key to work correctly.

This service acts as a drop in replacement for the official CurseForge API.
It also utilizes caching which will result in less hits on the official CurseForge API.
The syntax and data returned is (for the most part) identical to the official CurseForge API.
These handlers do NOT require an API key to communicate with the service.

The `CurseTools API <https://api.curse.tools/>`_ requests that all users have a custom user-agent string
defined in the header, likely so the API can determine who is using the service.
By default, this value is set to 'cursepy', but it is recommended to set this value to the name of your app.

.. code-block:: python

    hand.set_name(NAME)

You can use the above method to set the name on a per-handler basis.
You can also utilize the :ref:`CTClient<ct_client>` to set the name for all handlers loaded.
Simply pass the name to the client upon instantiation:

.. code-block:: python

    client = CTClient(NAME)

With all that being said,
this service is somewhat unreliable.
Some calls to this backend will fail due to one reason or another,
we will document some common issues here:

 * When listing catagories, the service may return 'null' as the data
 * The 'classId' parameter is sometimes not present in addon data
 * Keys that are usually camel case are sometimes all lowercase (for example, 'iconUrl' is instead 'iconurl') for catagories
 * 'thumbsUpCount' and 'gamePopularityRank' are NEVER present in addon data, and are saved as 'None' in the :ref:`CurseAddon instance<curse_addon>`

The :ref:`Meta CurseForge handlers<meta_curse>` have some safeguards in place to minimize these issues,
but major problems such as 'null' being returned instead of valid data can't be avoided.
In the event that you encounter these issues, it is recommended to try the operation again, as it will usually work after a few tries.

Same as the :ref:`Meta CurseForge handlers<meta_curse>`,
this backend is unable to lookup individual catagories by ID.

You can load the handler map by using the svc_map:

.. code-block:: python

    from cursepy.handlers.curseforge import cf_map

    client.load_handlers(ct_map)

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
