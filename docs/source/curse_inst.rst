=======================
Curse Instance Tutorial
=======================

Introduction
============

Welcome to the CurseInstance(CI) tutorial!

This tutorial aims to give you an understanding of
CIs, and how to use them efficiently!

What is a CurseInstance?
========================

A 'CurseInstance' is a class that represents 
CurseForge(CF) information.

For example, 
the CurseAddon class contains info such as
the addon name, slug, id, release date, ect.

You can access the name of the addon like so:

.. code-block:: python

    # Print the name of the addon
    # (Assume 'addon' is a valid CurseAddon instance)

    print(addon.name)

CIs also offer convince methods for interacting with said data.
These convenience methods automatically make the necessary 
HandlerCollection calls with the correct arguments to get the relevant data.

.. note::

    You should have already read the HandlerCollection tutorial.
    If you haven't, you should really check it out,
    as HandlerCollections are very important classes!

    Have a look at the tutorial [HERE]

Why CurseInstances?
-------------------

CurseInstances are in place to normalize CF data.
They ensure that no matter what the capy configuration is,
your program will always interact with the same classes.
If this were not the case, 
then the end user using capy would have to 
determine what format the raw data being is in,
and how to decode it.
Because capy is modular, this data can be literally anything!
So having a standardized way to get this data is very important.

CIs also provide all addon info in a convent way.
Most users do not want to manually parse request data!

Finally, CI's convenience methods make using capy much easier.
As stated earlier, these methods take the steps to automatically 
get extra info.
This makes the end user's life much easier,
and allows for a more pythonic, class-based way
of interacting with CF.

Types of CurseInstances
=======================

We will now go through each CI,
and lay out there parameters and methods.

More info can be found in the API reference for CIs.

.. note::

    For all coming examples,
    assume that 'inst' is a valid CurseInstance
    of the type being described.


Extra Functionality
-------------------

Some CIs have extra functionality 
that allows them to do extra things,
such as write content to an external file,
or download data from a remote source to a custom file.

Writer
______

A CI with writer functionality will allow you to write content 
to an external file.
You can invoke this process by using the 'write' method:

.. code-block:: python

    inst.write(PATH, append=False)

Where 'PATH' is a path like object giving the pathname
of the file to be written to.
You can also specify if the content is to be 
appended to the external file by using the 'append' parameter.

The CI determines what will be written to the external file.
If a CI has this feature,
then we will go over what exactly they write in this tutorial.

Downloader
__________

A CI with downloader functionality will allow 
you to download external content and write it to a file.
You can invoke this process by using the 'download' method:

.. code-block:: python

    inst.download(PATH)

Where 'PATH', like in the writer,
is a path like object giving the pathname of the file to be written to.

Again, the CI determines what will be downloaded and written to the external file.
If a CI has this feature, then we will go over exactly what they download and write.

CurseAttachment 
---------------

Represents an attachment on CF.

    * title - Title of the attachment
    * id - ID of the attachment
    * thumb_url - URL to the thumbnail of the attachment
        (If the attachment is an image, then the thumbnail is a smaller version of the image)
    * url - URL of the attachment 
    * is_thumbnail - Boolean determining if this attachment is a thumbnail of an addon 
    * addon_id - ID this addon is apart of 
    * description - Description of this attachment 

CurseAttachments have the download feature,
which means that you can download this attachment using the 'download' method:

.. code-block:: python 

    data = inst.download()

This will download the raw bytes and return them.
If you want to write this content to a file,
then you can pass a path to the 'path' parameter, like so:

.. code-block:: python 

    written = inst.download('path/to/file.jpg')

Where 'written' will be the number of bytes written.
If you provide a directory instead of a file to write,
then we will automatically use the default name
as the file to write to.
You can also download the thumbnail using the 'download_thumbnail' method,
which operates in the same way.

CurseDescription 
----------------

Represents a description on CF.
This description can be any HTMl text!

    * description - Raw HTML description text
    * formatter - Formatter attached to this description.

The stored description is usually in HTML.
This may make interpreting and displaying the description difficult.
To alleviate this problem, CurseDescription allows for the registration 
of formatters that can change or alter the text.
A formatter is a class that alters the description into something new.
You can register valid formatters using the 'attach_formatter' method:

.. code-block:: python 

    inst.attach_formatter(FORM)

Where 'FORM' is the formatter to attach.
If the formatter is invalid, then we raise a TypeError exception.
A formatter is valid if it inherits the 'BaseFormat' class.

HandlerCollection objects can automatically attach formatters to
CurseDescription objects if specified.
You can pass a valid formatter to the 'default_formatter()'
method on the HC, and the formatter will be attached
to every CurseDescription object returned.

Here is a list of all built in formatters:

    * NullFormatter - Does nothing!
    * StripHTML - Strips all HTML elements, leaving(In theory) valid text.
    * BSFormatter - Loads the HTML data into beautiful soup for further parsing.
        This formatter returns a bs4 instance, and beautiful soup MUST be installed,
        or an exception will be raised!

Here is an example of setting a StripHTML as the default
formatter for a HC:

.. code-block:: python 

    hc.default_formatter(StripHTML())

Where 'hc' is a valid HandlerCollection object.

To get the formatted content, you can use the format method:

.. code-block:: python 

    cont = desc.format()

Where 'desc' is a valid CurseDescription object.
'format' will send the description thorough the formatter,
and return the content the formatter provides.

You can also create your own custom formatters as well.
Just inherit the 'BaseFormatter' class, and overload the 'format' method.
The 'format' method should return the formatted content.

Here is an example of a custom formatter that appends 'Super Slick!' to the end of the description:

.. code-block:: python

    # Import BaseFormat:

    from capy.formatters import BaseFormat
        
    class SuperFormatter(BaseFormat):

        def format(self, data: str) -> str:
            """
            Returns the description, but with 
            'Super Slick!' appended to the end.
            """

            return data + 'Super Slick!'

    # Attach to a CurseDescription object:

    desc.attach_formatter(SuperFormatter())

CurseDescription objects can write content to an external file,
as it has writing functionality. 

CurseAuthor
-----------

Represents an author on CF.

    * id - ID of the author 
    * name - Name of the author 
    * url - URL to the authors page 

CurseAuthor classes is not necessary for CF development,
and only acts as extra info if you want it.

CurseGame
---------

Represents a game on CF.

    * name - Name of the game
    * slug - Slug of the game 
    * id - ID of the game 
    * support_addons - Boolean determining if the game supports addons
    * cat_ids - List of root category ID's associated with the game

The CurseGame instance does not have valid classes representing the root level catagories,
only there ID's.
If you want to retrieve the objects that represent the catagories,
you can use the 'categories' method to retrieve category info like so:

.. code-block:: python

    cats = inst.catagories()

This will return a tuple of CurseCatagories objects representing each root category.

CurseCategory
-------------

Represents a CurseCategory,
and provides methods for getting sub and parent catagories.

    * id - ID of the catagory
    * game_id - ID of the game the category is associated with 
    * name - Name of the category
    * root_id - ID of this objects root category(None if there is no root ID)
    * parent_id - ID of this objects parent category(None if there is no root ID)
    * icon - Icon of the category(CurseAttachment)
    * date - Date this category was created

If you read the into tutorial
(You did read the into tutorial right?),
then you will know that catagories can have
parent and sub-catagories.
CurseCategory objects have methods for traveling
though the hierarchy,
and each returns CurseCategory objects representing
these catagories.

'sub_categories' returns a tuple of 
CurseCategory objects representing each sub-category,
returns an empty tuple if there is no sub-categories.

'parent_category' returns a CurseCategory object 
representing the parent category, returns
None if there is no root category.

'root_category' returns a CurseCategory object 
representing the root category, returns
None if there is no root category.

CurseAddon also makes searching a breeze.
We automatically provide the correct game and category ID's.
Users can provide a 'SearchParameter' object for 
fine-tuning the search operation.

You can use the 'search' method to get a list of valid addons.
You can also use the 'iter_search' method to iterate 
over each addon. 

.. note::
    If you need a primer on searching,
    check out the Basic Tutorial[HERE]

CurseAddon 
----------

Represents an addon on CurseForge.

    * name - Name of the addon 
    * slug - Slug of the addon 
    * summary - Summary of the addon(Not a full description, 
    * url - URL of the addon page 
    * lang - Language of the addon
    * date_created - Date this addon was created 
    * date_modified - Date this addon was last modified 
    * date_release - Date the addons latest release 
    * ID - ID of this addon 
    * download_count - Number of times this addon has been downloaded
    * game_id - ID of the game this addon is in 
    * available - Boolean determining if the addon is available 
    * experimental - Boolean determining if the addon is experimental 
    * authors - Tuple of CurseAuthor instances for this addon
    * attachments - Tuple of CurseAttachments associated with the object 
    * category_id - ID of the category this addon is in 
    * is_featured - Boolean determining if this addon is featured 
    * popularity_score - Float representing this popularity score(Most likely used for ranking)
    * popularity_rank - int representing the addon game's popularity 
    * game_name - Name of the game 

CurseAddon objects do not keep the description info!
A special call must be made to retrieve this.
CurseAddon offers a property that that can retrieve the description 
as a CurseDescription object:

.. code-block:: python

    desc = inst.description 

You can get the files associated with this addon by using the 'file' method:

.. code-block:: python 

    file = inst.file(ID)

Where ID is the ID of the file to retrieve.
This method returns a CurseFile object representing the files
(We will go over CurseFile objects later in this tutorial!).
If you want a list of all files associated with the addon, 
you can use the 'files()' method,
which returns a tuple of CurseFile objects.

You can retrieve the CurseGame object representing the game
this addon is apart of using the 'game' method. You can also get a CurseCategory 
object representing the category this addon is apart of
by using the 'category' method:

.. code-block:: python 

    # Get the game:

    game = inst.game()

    # Get the category:

    cat = inst.category()

