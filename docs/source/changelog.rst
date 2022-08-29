=========
Changelog
=========

2.1.0
=====

This update fixes some bugs and adds support for a new backend

Features Added
--------------

* Added handlers for interacting with the curse.tools backend
* Added meta CurseForge handlers, which make developing for CurseForge like backends easier

Bug Fixes
---------

* Fixed an issue with the MinecraftWrapper passing a category ID to the search() and iter_search() methods.
* MinecraftWrapper now uses 'rootCategoryId' instead of 'categoryId' on the SearchParam when searching

2.0.0
=====

This update adds some major functionality!

Features Added
--------------

* Added two new errors, 'HandlerNotImplemented' and 'HandlerNotSupported'
* New class, BaseClient which defines the basic functionality for all wrappers (replaces old CurseClient)
* For listing catagories, we now need a game ID, as we only get all catagories for a specific game
* When listing files, a SearchParam can be provided to filter results
* New values in SearchParam that allows for more advanced searching and sorting
* Many curse instances have more parameters available
* New curse instance, CurseHash, represents fille hashes
* Added handlers for interacting with the official CurseForge API (Needs an API key!)
* Added new wrapper, CurseClient (different from old CurseClient) that makes working with the official API easier

Bug Fixes
---------

* Various formatting and spelling corrections

Other Fixes
-----------

* Many additions and changes in the official documentation

1.3.1
=====

Bug Fixes
---------

* We now properly quote the path section of any URLs given to the URLProtocol

1.3.0
======

This update fixes some major bugs,
and corrects an issue with searching.

Features Added
--------------

* Added the 'set_page()' and 'bump_page()' methods to the SearchParam class, which makes traversing pages easy
* Added the 'Bukkit Plugins' category to the MinecraftWrapper
* The MinecraftWrapper is now imported in the init file, so users can import the class like so:

.. code-block:: python

    from cursepy import MinecraftWrapper

(This will be the case for any new wrappers added)

Bug Fixes
---------

* Fixed an issue in the code and docs where the index is treated as the page of results to retrieve, which is incorrect
* We now download addon files correctly
* We now load reduced dependency info when ForgeSVC handlers are used to retrieve all files for a particular addon
* Fixed the 'iter_search()' method to correctly stop iteration
* Fixed some random typos in the documentation

1.2.0
=====

Features Added
--------------

* We now keep track of dependency info in the new CurseDependency class
* Users can retrieve the file ID as well as the addon ID of the dependency
* Users can retrieve optional and/or required dependencies

1.1.3
=====

Bug Fixes
---------

* Fix search filtering issue

1.1.2
=====

Bug Fixes
---------

* Fix dictionary calling issue

1.1.1
=====

Bug Fixes
---------

* Fixed an issue with sub-modules not being included in distribution files

1.1.0
=====

This update simply adds some basic protocol objects.

Features Added 
--------------

* Added 'TCPProtocol'
* Added 'UDProtocol'

1.0.0
=====

Initial Commit