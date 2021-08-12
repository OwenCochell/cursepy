=====================
Advanced Introduction
=====================

Introduction
============

Welcome to the Advanced Introduction!

In this tutorial, 
we will go over some advanced capy concepts,
and go into detail about the design and philosophy
of capy.

With that being said,
we will start with a brief section about the 
design of capy.

capy Design 
===========

CurseForge does not have a reliable way to interact
with their backend in an advanced, meaningful way.
This means that any entry point into CF can be removed,
or have certain functionality removed, at any given point.
This is what we like to call an 'unreliable API'.

Usually, API's are well documented, and are guaranteed
(For the most part)
to remain mostly in the same configuration.
In other words, they are well understood by the developer,
and can be accessed in the same way forever.
This is what we like to call a reliable API.

For reliable API's, writing code to interact with
them is usually very simple.
Unreliable API's on the other hand,
can be difficult to work with,
as nothing is guaranteed.

To work around this unreliable API,
capy uses a modular design that allows 
for components(handlers) to be registered to different events.
Handlers are designed to be ambiguous,
as they should be able to access anything,
anywhere, using any protocol.
This means that handlers can fetch info from anything ranging from 
a web server, to a backend serving JSON, to a local file on your computer.
The handler has the freedom to do anything to get the relevant info.

This modular design allows for features to be swapped 
in and out at will.
Instead of inheriting a class and building functionality around it,
a user can simply attach a handler to the HandlerCollection(HC),
and let the HC take it form there.
This allows for quick and easy swapping if a feature stops working
or does not work as well as you want it.
This loading process can also be automated!

Another benefit of the modular design
is that backbends can be mixed and matched.
For example, if a backend does not support
getting game info, then a handler from a backend
that does can be easily loaded.
This allows us to 'fill in the blanks'
and provide full functionality while using multiple backbends.

The final benefit to modular design
is that handlers can be very small and easy to write.
If a backend suddenly changes or goes dark,
then new handlers can quickly be written.

capy offers standardized methods for interacting with these handlers,
ensuring that no matter what the handler does,
it will always be called in the same way.
capy also provides standardized classes for returning CF
info, again which guarantees that no matter what the handler
is doing, it will always return the same class.
This means that programs using capy will not
have to re-write any capy code if the backend handlers 
change, as long as said handlers follow the recommended guidelines 
capy likes handlers to follow.
Just note, that handlers are under no obligation
to follow said guidelines, so it is important 
to understand what handlers you are loading!

Essentially, capy provides a platform for interacting
with CF, providing a modular framework for developers,
and ensuring that information going in and out of handlers
are standardized, so the user does not have to change code that uses
high level capy methods and components.

capy Philosophy
===============

The backbone of capy is this:

Make tasks easy for the user,
but advanced for the developer.

A 'user' in this case is someone(or something)
tha uses high level capy methods.
A 'developer' is similar to a user,
except they get into capy configuration,
such as creating custom handlers.

This philosophy means that for people 
who want to use capy for interacting with CF and nothing more
(which is 99% of people),
capy will be simple and easy to use.
Handlers will be auto-loaded, and high-level methods
will do and act as they are supposed to.

For those who have a specific goal for capy,
such digging into capy and getting into it's internals
will be very easy.
This comes with a great responsibility though,
as handlers are, again, ambiguous and under no obligation
to follow the best practices.
This means advanced users must have more than a surface level understanding of capy.

Terminology
===========

If you read through the simple tutorial,
then you should have a solid understanding of most of capy's 
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
Just keep in mind that they are the objects that get info from certain places.

CHF
---

The capy Handler Framework(CHF) is a design style 
for handlers that aims to minimize the amount of code necessary 
for writing handlers.
Using CHF is completely optional, and is not necessary
for writing handlers.

We will not go into the details about CHF,
as we will cover it later.

Conclusion
==========

Now that the meaning behind the design of capy
and the capy Philosophy,
we can now continue onward to advanced concepts.
