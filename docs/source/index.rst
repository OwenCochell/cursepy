Welcome to the capy documentation!
==================================

This is the documentation for Curseforge Api Python(capy) - 
an easy to use python library for querying and interacting with CurseForge projects!
Here is an example of capy in action:

.. code-block:: python

   # Import the CurseClient:

   from capy import CurseClient

   # Create the CurseClient:

   curse = CurseClient()

   ADDON_ID = 1234

   # Get the addon info:

   addon = curse.addon(ADDON_ID)

   # Print the name of the addon:

   print(addon.name)

This documentation houses the API reference, tutorials, and best practice recommendations. 

To get started, you should head over to the install page,
where we go over how to install capy onto your machine.
From there, you should check out the :ref:`Basic Tutorial <basic-tutorial>`.
This will give you all the info you need to use capy correctly. 

If you wish to gain a deeper understanding of capy and it's components,
you should check out the :ref:`Advanced Tutorial <advanced-tutorial>`.
Do keep in mind that this tutorial can get very complex,
and knowing it's content is not necessary!

For a quick look at all capy classes and functions,
you should have a look at the API reference.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   Basic Usage Tutorial <basic/index>
   Advanced Usage Tutorial <advn/index>
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
