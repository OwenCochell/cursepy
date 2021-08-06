=================
Protocol Tutorial 
=================

Introduction 
============

Welcome to the Protocol tutorial!

This document will go over the finer details on 
protocol objects, and how to use them effectively.

Like the other advanced tutorials in this series,
the content covered in this document are not necessary 
for basic capy usage!
You should only have to care bout this stuff if you are 
looking to get into handler development,
or wish to gain a deeper understanding of capy's internals.

With that being said, let's get started!

What is a Protocol Object?
==========================

A protocol object is a component that gets data from somewhere.
Where it gets this data from and how it gets this data 
can vary widely.
For example, the URLProtocol gets info from a remote source via the HTTP protocol.

Protocol objects are designed to work in tandem with handlers.
Not only are protocol objects able to be used for multiple handler types,
but they can also be shared between like minded handlers.
The HandlerCollection does this by keeping a 'protocol map'
which maps protocol objects to handler names.
If a loaded handler has the same name as another,
then it will be provided the same protocol instance
as the rest of the like-minded handlers.
This is to ensure that the state of the protocol object is synchronized
between similar handlers, and that there aren't any redundant 
objects floating around in memory.

Now that we have a basic understanding of protocol
objects, we can now go into designing a protocol object.

Creating a Protocol Object 
==========================

Creating protocol objects are actually quite simple.
Any and all protocol objects MUST inherit the 'BaseProtocol' class!

The only thing you must provide is a hostname, port, and timeout value,
which are usually provided by the user.
Any of these values can be interpreted or ignored as the 
protocol object see fit.

Lets create a simple DummyProtocol object to demonstrate:

.. code-block:: python

    # Import the BaseProtocol

    from capy.protocol import BaseProtocol

    # Create the class:

    class DummyProtocol(BaseProtocol):

        def __init__(self, hostname, port):

            # Pass the arguments along, and set our timeout to 50:

            super().__init__(hostname, port, timeout=50)

We now have a valid DummyProtocol object that can be used in handler development.
This protocol object is not very interesting, so lets add some functionality:

.. code-block:: python

    # Import the BaseProtocol

    from capy.protocol import BaseProtocol

    # Create the class:

    class DummyProtocol(BaseProtocol):

        def __init__(self, hostname, port):

            # Pass the arguments along, and set our timeout to 50:

            super().__init__(hostname, port, timeout=50)

        def get_data(self):

            # Just return a dictionary:

            return {'data': 1234}

We have now added some functionality to this protocol object!
Now, handlers that use this protocol object can call the 'get_data()'
method to get some data to work with
(even if that data is a simple dictionary that does not change).

As you can see, the implementation for handlers is very ambiguous.
Protocol objects should define their own methods for getting handler data.
implementation can and will vary widely depending on the protocol object in use.

For this final example, we will implement some advanced features into the protocol object:

.. code-block:: python

    # Import the BaseProtocol

    from capy.protocol import BaseProtocol

    # Create the class:

    class DummyProtocol(BaseProtocol):

        def __init__(self, hostname, port):

            # Pass the arguments along, and set our timeout to 50:

            super().__init__(hostname, port, timeout=50)

        def get_data(self):

            # Just return a dictionary:

            self.total_received += 1

            return {'data': 1234}


We now keep track of how many times this method has been called!
Protocol objects have a 'total_received' and 'total_sent'
attributes which can be used to keep track of statistics.
These usually record the number of bytes sent and received,
but in this case it keeps track of the number of times the data was fetched.

Built in Handlers 
=================

Lets go over the built in handlers that are shipped with capy.
They can make handler development much easier,
so using them is recommended!