=====================
Advanced Introduction
=====================

Introduction
============

Welcome to the Advanced Introduction!

In this tutorial, 
we will go over some advanced cursepy concepts
and go into detail about the design and philosophy
of cursepy.

We will start with a brief explanation about the 
design of cursepy.

cursepy Design 
==============

CurseForge (CF) doesn't have a reliable way to interact
with their backend in an advanced, meaningful way.
This means that any entry point into CF can be removed
or have certain functions removed at any given point.
This is what we like to call an 'unreliable API'.

Usually APIs are well documented and are guaranteed
(For the most part)
to remain mostly in the same configuration.
In other words, they are well understood by the developer
and can be accessed in the same way forever.
This is what we like to call a 'reliable API'.

For reliable APIs, writing code to interact with
them is usually very simplistic.
Unreliable APIs on the other hand,
can be very difficult to work with
because nothing is guaranteed.

To work around this unreliable API,
cursepy uses a modular design that allows 
for components (handlers) to be registered to different events.
Handlers are designed to be ambiguous,
as they should be able to access anything,
anywhere, or anytime by using any protocol put in place by the user.
This means that handlers can fetch information from anything! Ranging from 
a web server, to a backend serving JSON, or to a local file on your computer.
The handler has the freedom to get the relevant information you need at any time.

This modular design allows for features to be swapped 
in and out at will.
Instead of inheriting a class and building functionality around it,
the user can simply attach a handler to the HandlerCollection (HC),
and let the HC take it from there.
This allows for quick and easy swapping if a feature stops working
or doesn't work as smoothly as you want it to.
This loading process can also be automated!

Another benefit of the modular design
is that backbends can be mixed and matched.
For example, if a backend does not support
getting game information, then a handler from a backend
that does can be easily loaded in to fix the issue.
This allows us to 'fill in the blanks'
and provide full functionality while using multiple backbends.

The final benefit to modular design
is that handlers can be very small and easy to write.
If a backend suddenly changes or goes dark,
new handlers can quickly be written in to fix it.

cursepy offers standardized methods for interacting with these handlers,
ensuring that no matter what the handler does,
it will always be called in the same way.
cursepy also provides standardized classes for returning CF
information, in turn guarantees that no matter what the handler
is doing it will always return the same class.
This means that programs using cursepy will not
have to re-write any cursepy code if the backend handlers 
change. As long the handlers follow the cursepy recommended guidelines 
then it is expected to flow as instructed.
**Just note, that handlers are under no obligation
to follow said guidelines you put in place. It is vital  
to understand what handlers you are loading.**

Essentially, cursepy provides a platform for interacting
with CF in a simple to manage way. Via providing a modular framework for developers
and ensuring that information going in and out of handlers
is standardized so the user doesn't have to change the code that uses
high level cursepy methods and components.

cursepy Philosophy
==================

The backbone of cursepy is this:

**Make tasks easy for the user,
but advanced for the developer.**

A 'user' in this case is someone (or something)
tha uses high level cursepy methods.
A 'developer' is similar to a user,
except they get into cursepy configuration,
such as creating custom handlers.

This philosophy means that for people 
who want to use cursepy for interacting with CF and nothing more
(which is 99% of people).
Cursepy will be simple and easy to use.
Handlers will be auto-loaded and high-level methods
will do and act as they are supposed to.

For those who have a specific goal for cursepy,
such as digging into cursepy and getting into it's internals
will be very easy!
This comes with a great responsibility though,
as handlers are ambiguous and under no obligation to follow the code put in place by the user.
This means advanced users must have a deeper understanding of cursepy.

Terminology
===========

If you read through the simple tutorial
then you should have a solid understanding of most cursepy's 
components.

We do have a few more things to define here.
Don't worry if you don't completely understand them yet,
we will define them in detail later.

Protocol Objects 
----------------

Protocol Objects are components that get data from somewhere.
This can be anything from a remote entity to a file residing on your computer.

They are purposefully left ambiguous,
as they can really do anything.
all you have to keep in mind is that they are the objects that get information from certain places.

CHF
---

The cursepy Handler Framework (CHF) is a design style 
for handlers that aim to minimize the amount of code necessary 
for writing handlers.
**Using CHF is completely optional and is not necessary
for writing handlers.**

We will not go into the details about CHF, 
because we will go more in depth about its functions at a later date. 

HandlerCollection
-----------------

The HandlerCollection is a low-level class that 
manages handlers and callbacks.
It provides easy to use methods for loading 
and unloading these components.

If you remember from the basic usage tutorial,
we covered a class called 'CurseClient'.
'CurseClient' inherits the 'HandlerCollection' class!
The only thing 'CurseClient' does is auto-load the default cursepy handlers
and provides entry points into said handlers.

Conclusion
==========

Now that the meaning behind the design of cursepy
and the cursepy Philosophy is now explained,
we can continue onward into advanced concepts about them.
