.. _collec_advn:

==========================
HandlerCollection Tutorial
==========================

Introduction 
============

Welcome to the advanced tutorial for the HandlerCollection(HC) object!

In this document, we will be going over
some advanced concepts behind the HC
that will help developers understand and work with HC classes.
Everything from loading handlers, to the internal structure
of info will be covered here.

The topics covered in this document are not necessary 
for using cursepy!
This info is only for advanced users who wish 
to gain a deeper understanding of cursepy and it's internals 
for there own uses.

If you want a surface-level tutorial on HC objects,
take a look at the :ref:`basic usage tutorial <basic-tutorial>`.

With that being said, lets get started!

.. note::

    For all upcoming examples,
    we assume that a HC is properly imported and 
    instantiated under the name 'hands'.

What is a HandlerCollection?
============================

The 'HandlerCollection' class manages handlers
and callbacks.
If you read the basic tutorial,
you will have a basic understanding of the "CurseClient' class,
and you might recall that the functionality is very similar.
As a matter of fact, the CurseClient actually inherits the HandlerCollection class!
Even so, there are some differences between the two.

The HandlerCollection is a low level component for managing handlers.
All the CurseClient does is load the default cursepy handlers,
as well as provide the entry point methods.
For the sake of simplicity,
it is recommended that you use CurseClient
as the building block for wrapper development,
unless you have a special reason not to. 

Handler Management
==================

HC contains a few methods for loading and unloading handlers.
In this section, we will go over those methods in detail.

.. note::

    If you want a look at the built in handlers,
    you should check out the :ref:`Builtin Handler List<hand-built>`.

Getting Handlers
----------------

You can get handlers by using the 'get_handler()' method:

.. code-block:: python 

    hand = hands.get_handler(ID)

Where 'ID' is the event ID.
This will return the handler instance bound to the given event ID.

Loading Handlers
----------------

You can load handlers by using the 'add_handler()' method:

.. code-block:: python

    hands.add_handler(HAND)

Where 'HAND' is the handler to add.
Handler must be instantiated to be loaded!
By default, the HC pulls the event ID out of the handler itself.
This allows handlers to define what they do,
so the developer does not have to.
You can ready about how handlers identify themselves by checking out the 
:ref:`advanced handler tutorial <hand_advn>`.

The 'add_handler()' method provides a way to manually specify the event ID the handler
should be associated with, regardless of what the handler states.
You can do this using the 'ID' parameter:

.. code-block:: python 

    hands.add_handler(HAND, id=ID)

Where 'ID' is the event ID to register the handler to.
This should be an integer, and should be defined using the HC event constants!
If the 'id' parameter is defined, then the 
ID the handler defines is ignored.

Here is an example of adding a handler by the name of
'DummyHandler' to the LIST_GAMES event:

.. code-block:: python 

    hands.add_handler(DummyHandler(), id=hands.LIST_GAMES)

The 'add_handler()' method does a few things when a handler is added.
For one, it ensures that the handler inherits 'BaseHandler'.
If this is not the case, then a 'ValueError' exception is raised.
After this check is complete,
then it removes the handler at the current event ID
(We will go over removing handlers later in this document).

.. note::

    HC ensures that a handler is ALWAYS loaded for all 
    valid event ID's.
    When a HC is first created, it loads a 'NullHandler'
    object at each position.

    This ensures that requests are always handled by something!

After this, the handler is officially added to the HC handler structure.
The HC then attaches itself to the handler,
and finally invokes the handler's 'start()' method.

As you can see, the 'add_handler()' method does many important things.
Other methods for adding handlers always use this function 
under the hood.

Unloading Handlers 
------------------

You can unload handlers by using the 'unload_handler()' method:

.. code-block:: python 

    hands.remove_handler(ID)

Where 'ID' is the event ID of the handler to remove.

The first thing this method does is invoke the 
'stop()' method of the handler associated with the given ID.
After this, we remove the handler from the handler structure
and replaces it with a 'NullHandler'.

Loading Multiple Handlers
-------------------------

HC provides a method for loading multiple handlers at a time,
and in a certain priority.
To do this, you can use the 'load_handlers()' function:

.. code-block:: python 

    hands.load_handlers(MAPPER)

Where 'MAPPER' is a valid handler map.
This method uses the 'add_handler()' function under the hood.

Let's go over handler maps quickly before we continue.

What is a Handler Map?
______________________

A handler map is an iterable(usually a list or tuple)
that contains instructions on how to load handlers.
This iterable can be multi-dimensional,
which allows users to specify the order of handlers to be loaded.

It is better to show an example than trying explain it.
Consider this example:

.. code-block:: python 

    (
        Hand1(),
        Hand2(),
        Hand3()
    )

If this handler map was passed to the 'load_handlers()' method,
then the handlers will be bound to these events:

* [1]: Hand1 
* [2]: Hand2
* [3]: Hand3

In other words, 'Hand1' will be bound to the 'LIST_GAMES' event,
'Hand2' will be bound to the 'GAME' event,
and 'Hand3' will be bound to the 'LIST_CATEGORY' event.
cursepy uses the index of the handler to determine the event ID it should be bound to.
For example, the index of 'Hand1' is zero, which means it will be bound to the event ID of zero
(The 'LIST_GAMES' event).
If the provided object is a dictatory,
then the key will be used to map the handlers.
For example, if this dictionary is provided:

.. code-block:: python 

    {
        0: Hand0()
        2: Hand2()
        3: Hand4()
    }

Then the handlers will be bound to these events:

* [0]: Hand0
* [1]: Hand2
* [2]: Hand3 

The keys of dictionaries can technically be anything, 
although it is recommended that they are integers
and are valid event ID values.

You can also specify the priority of the handler map,
which will determine the oder of which handlers are loaded.
Here is an example of a priority handler map:

.. code-block:: python

    (
        (
            Hand1(),
            Hand1(),
            Hand1()
        ),
        {   
            0: Hand2(),
            2: Hand2(),
            3: Hand2()
        }
    )

This tuple contains two maps,
a tuple and a dictionary.
The order of these objects determine the order of the map,
meaning that the lower the index, the higher it's priority.
Using the above example, the handlers will be bound to these events:

* [0]: Hand1 
* [1]: Hand1 
* [2]: Hand1 
* [3]: Hand2

As you can see, the handlers in the first map are given priority
over those in the second. 
Notice that Hand2, even though being associated with event IDs 0 and 2,
are not used, as Hand1 has a higher priority.
The only handler that made it though 
from the second map is the one bound event ID 3,
as it is not specified in the first map.
You can also use dictionaries to specify the map priority.

Again, handler maps MUST be iterables!
This includes lists, tuples, dictionaries, 
generators, ect.
Any thing that the python 'for' loop can iterate over!

Now that you have a valid handler map, you can pass it along to the 'load_handlers()'
method to load multiple handlers at once!

Misc. Methods
=============

HC has a few miscellaneous methods that we will cover here.

reset 
-----

The 'reset()' method resets the state of the HC back to its initial state.
This clears all handlers, callbacks, protocol objects, and resets the 
default formatter.

Be aware, that the handlers are not stopped,
and are simply removed.
This means that if they are not referenced elsewhere,
then garbage collection will remove them and all affiliated info.

Use this method at your own risk!

load_default 
------------

The 'load_default()' method automatically loads the default handlers.
This can vary depending on the HC used,
and some wrappers can overload this method.

get_search 
----------

Returns a valid search object to be used for searching.
Again, this function can be overloaded by a wrapper ,
and can be configured to return something else.

HandlerCollection Structures
============================

In this section,
we will go over the internal data structures
HC uses to organize and store components.
Knowing this info is not necessary at all for using cursepy!
However, if you want to get into cursepy development,
or simply wish to have a deeper understanding,
then this section could be useful for you.

Handler Structures
------------------

Handlers are kept in a dictionary under the 'handlers' parameter,
which can be accessed like so:

.. code-block:: python 

    hand_dict = hands.handlers

The handler dictionary's format is quite simple.
The key is the event ID, and the value is the handler.

Here is an example of a normal handler dictionary:

.. code-block::

    {
        1: hand1 
        2: hand2 
        3: hand3 
    }

Where 'hand1' is bound to the event ID 1, hand 2 is bound to event ID 2, and so on.

Usually, the key is an integer, and it is a valid event ID.
The key does not have to follow this convention.
The 'handle()' method searches the handler dictionary
using the given event ID,
so one could retrieve/set a handler under a custom ID.

Here is an example of loading/getting a handler 
under a custom event ID:

.. code-block:: python

    # Load a handler:

    hands.add_handler(hand, 'custom')

    # Get the handler:

    hand = hands.get_handler('custom')

    # Invoke the handler:

    hands.handle('custom')

This code will work correctly!
The handler will be saved under the event ID of 'custom',
and can be retrieved/invoked using that ID.
Along with this, then handler dictionary will look something like this:

.. code-block::

    {
        ...,
        'custom': hand,
        ...
    }

Along with the other loaded handlers,
the handler 'hand' is loaded under the event ID of 'custom'.

With all this being said, one could manually edit this dictionary
to change the state of the loaded handlers.
However, this is not recommended!
HC goes through many steps to ensure handlers 
are loaded and unloaded correctly.
Attempting to alter this dictionary could lead to trouble,
so be sure that you know what you are doing!

Protocol Structure
------------------

We store protocol objects in the same format as the handler dictionary.
The name of the handler is the key, and the protocol object is the value.
This is used to organize protocol objects,
and would allow all like-minded handlers to use the same object.
This allows the state to be synchronized across handlers,
and prevents any unnecessary objects from floating around.

Lets say we have a handler with the name of 'dummy_handle'.
If this handler is loaded,
then the protocol dictionary will look something like this:

.. code-block::

    {
        'dummy_handle': proto 
    }

Where 'proto' is the protocol object associated withe the handler.

Again, it is NOT recommended to alter the dictionary yourself!
This could seriously mess up the state of the HC.

Callback Structure
------------------

The callback structure is a bit more complex than the others.
At the top level, the structure is a dictionary.
Like the previous structures, 
the key is the event ID, and the value is the callback data.
This is where the callback structure differs:
the value is a list.
Because multiple callbacks can be bound to an event,
we keep the value as a list so we can store as much callback info as we want.

Each value in this list represents a single callback.
The value is a tuple,
where the first index is the callback instance,
the second index is a tuple of arguments,
and the third argument is a dictionary of keyword args.

Lets have a look at an example. Suppose a callback is loaded like so:

.. code-block:: python 

    hands.bind_callback(call, 2, arg1, arg2, arg3=3)

The handler 'call' is bound to the event ID of '2'
with the given arguments.
After this function is completed,
the callback structure will look like this:

.. code-block::

    {
        2: (
            (call, (arg1, arg2), {arg3=3})
        )
    }

As you can see, the structure changes into the format we specified earlier.
Let's say we bind another callback to the HC by the name of 'call2'.
The structure will look like this:

.. code-block::

    {
        2: (
            (call, (arg1, arg2), {arg3=3}),
            (call2, (), {})
        )
    }

For our final example, we will add 'call3' to the event ID of 3:

.. code-block::

    {
        2: (
            (call, (arg1, arg2), {arg3=3}),
            (call2, (), {})
        ),
        3: (
            (call3, (), {})
        )
    }

As stated many times before, altering this structure is not recommended!
You should use the higher-level methods for altering this structure,
as it will ensure stability.

Conclusion 
==========

You should now have a deep understand of HC objects 
and all their advanced features!

This concludes the advanced tutorial 
for advanced cursepy usage.

If you still want more info on cursepy and it's components, 
you should check out the API reference.
