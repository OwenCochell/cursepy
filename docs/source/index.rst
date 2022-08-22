Welcome to the cursepy Documentation!
=====================================

This is the documentation for cursepy - 
an easy to use python library for querying and interacting with CurseForge projects!
Here is an example of cursepy in action:

.. code-block:: python

   # Import the CurseClient:

   from cursepy import CurseClient

   # Create the CurseClient:

   curse = CurseClient(API_KEY)

   ADDON_ID = 1234

   # Get the addon info:

   addon = curse.addon(ADDON_ID)

   # Print the name of the addon:

   print(addon.name)

This documentation houses the API reference, tutorials, and best practice recommendations.

To get started, you should head over to the install page,
where we go over how to install cursepy onto your machine.
From there, you should check out the :ref:`Basic Tutorial <basic-tutorial>`.
This will give you all the info you need to use cursepy correctly. 

If you wish to gain a deeper understanding of cursepy and it's components,
you should check out the :ref:`Advanced Tutorial <advanced-tutorial>`.
Do keep in mind that this tutorial can get very complex,
and knowing it's content is not necessary!

For a quick look at all cursepy classes and functions,
you should have a look at the :ref:`API reference <api-refrence>`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   Basic Usage Tutorial <basic/index>
   Advanced Usage Tutorial <advn/index>
   api
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
