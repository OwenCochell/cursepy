.. _hand_advn:

================
Handler Tutorial
================

Introduction
============

Welcome to the handler tutorial!

This tutorial should give you an
advanced look at handler development!

Creating a Handler
==================

Every handler is essentially a class that does something.
Simple as that.

All handlers MUST inherit 'BaseHandler'!
If you attempt to load an object 
that does not inherit 'BaseHandler',
then an exception will be raised!

This is the one and only restriction
to handlers.
The reason why this is the case is because
capy must guarantee that a 'handel()' method 
is present on the object to load
(You will find out why this is later).
It is also important for the HandlerCollection(HC),
as it will assign some values in the object,
and capy does not want weird errors to occur.

Here is an example of making a simple handler 
that does nothing:

.. code-block:: python

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Create a simple handler:

    class DummyHand(BaseHandler):

        pass

The 'DummyHand' class is a valid handler,
as it inherits the 'BaseHandler' class.

The 'BaseHandler' class implements some methods,
which will cover in the next section.
In the meantime, let's go over the attributes
that 'BaseHandler' adds to the object that inherits it:

* hand_collection - Instance of the HC that loaded the handler 
* name - Name of the handler
* proto - Instance of the protocol object this handler uses(More on this later)

The handler name is important for identifying
like minded handlers.
It is good practice to make all handlers 
of the same backend share the same name.
You can set a name by passing a value to the init method
of BaseHandler like so:

.. code-block:: python

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Create a simple handler:
    
    class DummyHand(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

This will set the handler's name to 'DummyHand'.

Handlers can also run code when they are started and stopped.
This can be defined by using the 'start()' and 'stop()' methods:

.. code-block:: python

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Create a simple handler:
    
    class DummyHand(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def start(self):

            # Start this handler, somehow:

            print("Handler is started!")

        def stop(self):

            # Stop this handler, somehow:

            print("Handler is stopped!")

When this handler is loaded, then 'Handler is started!'
is printed to the terminal.
When the handler is unloaded, then 'Handler is stopped'
is printed to the terminal.

It is also important for the handler to identify
what event they are registered to.
This is helpful for end users and the HC class,
as it can use this info to determine what a handler does.
By default, this value is -1,
which is guaranteed by capy to NEVER be a valid event ID. 
To specify what event this handler is tied to,
you can use the ID parameter, as documented here:

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Create a simple handler:

    class DummyHand(BaseHandler):
        
        ID = 1

        def __init__(self):
    
            # Set our name:
    
            super().__init__(name='DummyHand')

In this example, the DummyHandler 
is associated with the 'GAME' event.
This means that the handler should have something to do 
with getting game data.
You can (and should!) use the :ref:`HC constants <collec_constants>` to define this.

All upcoming examples will NOT utilise the ID parameter!
Just keep in mind that specifying the handler ID is highly 
recommended in production environments.

Adding Functionality
====================

To add functionality to a handler,
you can simply overload the 'handle()' method
(Not to be confused with the HC 'handle()' method).

Simple as that.

When the handler is loaded into a HC,
and the event it is registered to is invoked,
then the HC calls the 'handle()' method 
of the handler associated with the event.

Here is an example of printing 'Hello!'
to the terminal every time the handler is called:

.. code-block:: python

        # Import the BaseHandler:

        from capy.handlers.base import BaseHandler

        # Create a simple handler:
        
        class DummyHand(BaseHandler):
        
            def __init__(self):
    
                # Set our name:
    
                super().__init__(name='DummyHand')
    
            def handle():

                # Print 'Hello':

                print("Hello!")

The HC also passes all arguments to the 'handle()' method.
capy has a standard which determines the types of arguments
each handler should receive, but lets ignore that for now.
Let's say your DummyHandler will take two arguments, 
one int and one string.

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Create a simple handler:

    class DummyHand(BaseHandler):

        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def handle(arg1: int, arg2: str):

            # Print the arguments:

            print("Arg1: {} Arg2: {}".format(arg1, arg2))

The DummyHandler will now print both arguments to the terminal.

It is standard that the 'handel()' method returns a CurseInstance 
(Or tuple of CurseInstance) objects that correspond to the action 
preformed by the handler.
For example, the handler associated with getting game info
should return a CurseGame object.
Again, we can't stress this enough,
but handlers do not have to follow this rule!
The standard is highly recommended if the developer can help it,
but if there is a specific use case that goes against this standard,
then developers should feel free to deviate at there own risk.
The HC will return the object that is returned by the 'handle()' method.
HC will also process any relevant objects(objects that inherit 'BaseCurseInstance')
by attaching itself to the object,
and attaching the default formatter to any CurseDescription objects.

Using the 'handle()' method is fine for simple operations.
However, if you want a recommended implementation
that should reduce the amount of code you will have to write,
with smart inheritance, then you should use the capy handler framework.

capy Handler Framework 
======================

The capy Handler Framework(CHF) is an implementation
for handlers that aims to minimize the amount of code written in the long run.
Using inheritance, each method can be utilized,
thus leaving only the necessary methods to be written.
Don't worry if you don't understand this concept yet,
it will make sense to you later.

The CHF lifecycle is as follows:

Get Data -> Decode Data -> Format Data -> Post-Process Data -> Return Data 

There are methods for each event in this chain.
This chain should also help illustrate the importance of smart inheritance.
If you have multiple handlers that interact with the same remote entity 
using the same protocol, then you could make a parent class that handles 
getting the data, decoding it, and post-processing it.
It is unnecessary for each handler to specify these actions as they will be the same.
The only things the handlers need to do is convert this decoded data 
into a CurseInstance(Or anything else for that matter).
You will see in-depth examples of this later.

The only thing to keep in mind is that you SHOULD NOT 
overload the 'handle()' method, as it is the one invoking these methods.
If you put other stuff into the 'handel()' method,
then any content in the CHF methods will not be ran
(Unless you run them yourself)!

proto_call
----------

The 'proto_call()' method is called when 
info is needed from the protocol object associated 
with the handler.
This usually entails getting info from a remote source,
although this is not always the case,
as protocol objects can do anything.

Bottom line, this method should return raw bytes of info.
No decoding should be done to this info!

This is the first method called,
as getting the data is the first event in the CHF chain.
All arguments provided to the handler will be passed to this method.

Here is an example of this in action:

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Create a simple handler:
    
    class DummyHand(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def proto_call(self, arg1: int) -> bytes:

            # Call our protocol object:

            return self.proto.call()

Notice that the 'proto_call()' method returns bytes.
After the bytes are returned,
then they will be passed along for decoding.

pre_process
-----------

The 'pre_process()' method is called when raw data from the 'proto_call()'
method needs to be decoded.
The operations done here can be anything!

The 'pre_process()' method should accept a single parameter,
which is the raw bytes.
It should return something the next method in the chain should understand,
usually an object or dictionary.

Using our example from earlier,
here is an example of decoding the raw bytes using JSON:

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Import JSON:

    import json

    # Create a simple handler:
    
    class DummyHand(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def proto_call(self, arg1: int) -> bytes:

            # Call our protocol object:

            return self.proto.call()

        def pre_process(self, data: bytes) -> dict:

            # Decode the data:

            return json.loads(data)

Now, we can see that the data is decoded via JSON,
and the resulting dictionary is returned.

format
------

The next method in the chain is the 'format()' method.

The 'format()' method should convert the decoded data into something,
usually a CurseInstance.
It should accept a single argument,
which is the decoded data.
It should also return something meaningful from the given data,
usually a CurseInstance.

Lets say that our DummyHandler decodes info about CurseAuthors.
Here is the previous example with that addition:

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Import CurseAuthor:

    from capy.classes.base import CurseAuthor

    # Import JSON:

    import json

    # Create a simple handler:
    
    class DummyHand(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def proto_call(self, arg1: int) -> bytes:

            # Call our protocol object:

            return self.proto.call()

        def pre_process(self, data: bytes) -> dict:

            # Decode the data:

            return json.loads(data)

        def format(self, data: dict) -> CurseAuthor:

            # Format and return:

            return CurseAuthor(data['id'], data['name'], data['url'])

As you can see, the format method takes the data in dictionary format,
and formats it into a CurseAuthor object and returns it.
We are finally playing with something the user can work with.
But wait! We are not done yet!
This formatted object will no be passed to the next ring of the chain.

post_process
------------

The 'post_process()' method should finalize the returned
formatted object.
This can be anything the handler deems important.

This method should take one argument, the formatted object,
and return the finalized formatted object.

For our DummyHandler,
lets say that we wish to attach the current time to 
the formatted object:

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Import CurseAuthor:

    from capy.classes.base import CurseAuthor

    # Import JSON:

    import json

    # Import time:

    import time

    # Create a simple handler:
    
    class DummyHand(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def proto_call(self, arg1: int) -> bytes:

            # Call our protocol object:

            return self.proto.call()

        def pre_process(self, data: bytes) -> dict:

            # Decode the data:

            return json.loads(data)

        def format(self, data: dict) -> CurseAuthor:

            # Format and return:

            return CurseAuthor(data['id'], data['name'], data['url'])

        def post_process(self, obj: CurseAuthor) -> CurseAuthor:

            # Finalize the object:
                
            obj.time = time.time()

Now, the object has the time attached to it.
You may be thinking, why not attach the time during the format
operation?
You defiantly can! There is nothing stopping you.
But adding that instruction to every handler you plan to write
is redundant, and leads to unnecessary code.
If you make a master class for you handlers,
you can define this operation once,
so all object will have the time attached to them 
without having to explicitly specify it.
We will go deep into this concept later, but keep this in mind!

It is recommended to attach raw data and metadata from the protocol object 
to the CurseInstance using this method!
Most users will expect this data to be present,
so it is a good idea to provide it!

Here is an example of attaching this data to a CurseInstance:

.. code-block:: python

    inst.raw = RAW_DATA
    inst.meta = META_DATA

Where 'RAW_DATA' is the raw data to add,
and 'META_DATA' is the metadata to add.

make_proto
----------

Method called when a protocol object is needed.

This method should normally return a instantiated
protocol object.
The HC ensures that the same protocol object is used for like-minded 
handlers.
This is to ensure that the sate is synchronized across
all handlers of the same type.
It also ensures that there aren't too many unnecessary objects floating around in memory.

Here is an example of this method:

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Import CurseAuthor:

    from capy.classes.base import CurseAuthor

    # Import JSON:

    import json

    # Create a simple handler:
    
    class DummyHand(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def proto_call(self, arg1: int) -> bytes:

            # Call our protocol object:

            return self.proto.call()

        def pre_process(self, data: bytes) -> dict:

            # Decode the data:

            return json.loads(data)

        def format(self, data: dict) -> CurseAuthor:

            # Format and return:

            return CurseAuthor(data['id'], data['name'], data['url'])

        def post_process(self, obj: CurseAuthor) -> CurseAuthor:

            # Finalize the object:
                
            obj.time = time.time()

        def make_proto(self):

            # Return a valid protocol object:

            return DummyProto()

In this example, we return a 'DummyProto' object 
that all DummyHandler objects will use.
Again, the handler does not have to worry about keeping track
of protocol instances.
All they need to do is provide a valid protocol object,
and know that their protocol object is present at the 'proto' attribute.

Tieing it all together
----------------------

You now have a handler using the CHF!
Now, let's go over how using this framework can save some time.

The first thing you should do is create a master 
class, like so:

.. code-block:: python 

    # Import the BaseHandler:

    from capy.handlers.base import BaseHandler

    # Import CurseAuthor:

    from capy.classes.base import CurseAuthor

    # Import JSON:

    import json

    # Create a master handler:
    
    class DummyMaster(BaseHandler):
    
        def __init__(self):

            # Set our name:

            super().__init__(name='DummyHand')

        def proto_call(self, arg1: int) -> bytes:

            # Call our protocol object:

            return self.proto.call()

        def pre_process(self, data: bytes) -> dict:

            # Decode the data:

            return json.loads(data)

        def post_process(self, obj: CurseAuthor) -> CurseAuthor:

            # Finalize the object:
                
            obj.time = time.time()

        def make_proto(self):

            # Return a valid protocol object:

            return DummyProto()

    class DummyHandler(DummyMaster):
    
        def format(self, data: dict) -> CurseAuthor:

            # Format and return:

            return CurseAuthor(data['id'], data['name'], data['url'])

As you can see, the other methods are defined in the master class,
meaning that they don't have to be defined again.
Now, the only method in the DummyHandler that is defined is the 
format method, thus removing the need to define the other operations.

You may think that creating a master class for a single handler is unnecessary,
and you would be right.
However, once you define multiple handlers,
this framework will make you write less code in the long run,
as all the repeating redundant operations are now no longer specified.
The only contents in the handler is the 'format' method,
which should be different every time.
This also falls in line with the Don't Repeat Yourself(DRY) principle,
as again, the only parts that are specified are those that are unique.

Built in Handlers 
=================

capy has a few built in handlers
for development purposes.

Lets go over these in detail.

.. note::

    If you want a list of all functional 
    handlers and the features they support,
    then have a look '[HERE]'

NullHandler
-----------

This handler does, you guessed it, nothing!

We return 'None' upon each call,
and do no operations!

This handler is actually loaded to every event by default,
to ensure that there is always a handler to work with,
even if it does nothing.

This handler is great if you want to disable a certain feature.

RaiseHandler
------------

This handler raises an exception upon each handle request.
It raises a 'HandlerRaise' exception upon each call.

This handler is great of you want to forcefully disable an option!

URLHandler
----------

This handler acts as a parent class for handlers communicating via HTTP.

URLHandler automatically assigns URLProtocol as the protocol 
object for the handler.
It also keeps track of the HTTP request of the last made request,
and offers the ability to generate valid metadata for CurseInstances,
which is a dictionary with the following values:

* headers - A tuple of (header, value) tuples
* version - HTTP protocol version 
* url - URL of the resource retrieved
* status - Status code returned by the server 
* reason - Reason phrase returned by the server.

It takes over the 'proto_call()' method as well,
and uses the 'build_url()' method to get a valid URL.
Handlers now only have to specify the 'build_url()' method,
and the URLHandler takes care of the rest.
URLHandler also passes all arguments given to the 'build_url()'
method.

You should also define the host and portname, 
which will be passed along to the protocol object.
You can also provide an 'extra' string that is appended to the
end of the hostname, but before the custom info,
when the URLProtocol 'url_build()' is called.

You can also specify the 'path',
which will be appended after the extra URL info.
This is great if your data is in a standard place,
and does not differ.
By default, the 'build_url()' method calls the URLProtocol's 
'url_build()' method with the path as the parameter.

At the end of the day, the generated URL will look like this:

.. code-block::

    [HOSTNAME]/[EXTRA]/[PATH]

If you don't want this to be the case,
than you can overload the 'build_url()' method,
and generate a valid URL your own way.

These can all be defined using the URLHandlers init method:

.. code-block:: python

    # Import URLHandler:

    from capy.handlers.base import URLHandler

    # Create the handler:

    hand = URLHandler('Name of the Handler', host='www.example.com', port=80, extra='/extra/info', path='/data')

This handler parent is great for easily adding HTTP support to your handlers!

Conclusion
==========

You should now have a solid understanding of handlers
and how they operate!
If you are still unsure about the topics discussed,
then be sure to check out the API reference!

The next section will go over protocol development.