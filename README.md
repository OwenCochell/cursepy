# cursepy
A modular API for interacting with [CurseForge](https://curseforge.com).

[![Documentation Status](https://readthedocs.org/projects/cursepy/badge/?version=latest)](https://cursepy.readthedocs.io/en/latest/?badge=latest)

The documentation for cursepy is still a work in progress!
The core content will remain the same,
but expect minor corrections and rephrasing.

# Introduction

cursepy allows you to interact with CurseForge,
which allows you to add, addons and files in a simple, easy to use format.
We offer easy entry points into certain CurseForge APIs and backends.

Our goal is to be modular and heavily customizable for developers who
have very specific wants and needs, while also being simple and intuitive
for developers who want something that 'just works'.

We support getting information on all games,
addons, categories, files, and so much more!
We also offer easy to use methods for downloading 
files.

# Example

```python
from cursepy import CurseClient  # Import the CurseClient

GAME_ID = 432  # ID of the game you want to fetch, in this case Minecraft

# Create the CurseClient:

curse = CurseClient()

# Get the game info:

game = curse.game(GAME_ID)

# Print the name of the game:

print(game.name)
```

# Features

Here, we will give brief descriptions of cursepy features:

## Ease of Use

using cursepy is very simple!
Simply import the CurseClient class:

```python
from cursepy import CurseClient

# Create the client:

client = CurseClient()

# Get a tuple of all games:

games = client.games()
```

The CurseClient offers simple to use navigational methods for obtaining necessary information from CurseForge.
CurseClient also allows for callbacks to be bound to events, 
meaning when an event is fired,
your custom callback will also be cued.
Here is an example of this in action:

```python
# Define a custom callback:

def callback(data)
    # Print the data we have:

    print(data)

# Bind the callback to the ADDON event:

client.bind_callback(callback, client.ADDON)
```

When the ADDON event is triggered, then this callback will be called,
and the data we received by the handler will be passed along to the callback.

If you want a closer look at working with CurseClient,
you should check out the [CurseClient Documentation](https://cursepy.readthedocs.io/en/latest/basic/collection.html).

## Modular Design

Each operation is managed by a component called a 'handler'.
Handlers are simply classes that get information and process it.
This information can be from any location
and it can be retrieved in many different ways.
Here is an example of a simple handler thats pulls HTTP data from somewhere and returns it:

```python
from urllib.request import urlopen

# Import the BaseHandler:

from cursepy.handlers.base import BaseHandler


class HTTPGet(BaseHandler):

    def handle(self):

        # Get and return HTTP data:

        return urlopen('somedomain.com/some/path')
```

The only limit is your imagination!

Our modular method allows for functionality to be swapped and
mixed around, allowing for automated and easier customization
compared to sub-classing.

cursepy has extensive documentation on handler development,
which contains best practice recommendations. Docs on the cusepy Handler Framework(CHF)/tutorials on how to use the development handlers are already built into cursepy.
Have a look at the [Handler Development Tutorial](https://cursepy.readthedocs.io/en/latest/advn/hand.html)!

## Curse Instances

As stated earlier, curse data can come from any location,
which can be retired in many different ways.
Because of this, the developer would have to check and work
with data in many different formats and in many different makeups.

Not ideal!

cursepy offers curse instances that normalize data,
and offer a container for data to be kept in.
This ensures that no matter what
the developer will be working with data in the same way,
regardless of how or where we got the data from.
They're dataclasses, which makes retrieving and working 
with information very easy.

Curse Instances have plenty of other nifty features for 
easing your development, so be sure to check out the [CurseInstance Tutorial](https://cursepy.readthedocs.io/en/latest/basic/curse_inst.html)!

## Wrappers

Wrappers ease the process of interacting with certain games and projects on CurseForge.
They do this by keeping track of relevant information, such as game and category ID's,
so you, as the developer, do not have to.

For example, the 'MinecraftWrapper' eases the process of getting 
information on Minecraft projects and addons.
We hope to implement more wrappers for more games at a later date.

Have a look at the [Wrapper Tutorial](https://cursepy.readthedocs.io/en/latest/basic/wrap.html) for more info!

# Installation

You can install cursepy via pip:

    $ pip install cursepy

For more information on installing cursepy,
check out the installation section in our [documentation](https://cursepy.readthedocs.io/en/latest/install.html). 

# Documentation

As stated many times before, we have an extensive documentation. It contains tutorials, the API reference,
and best practice recommendations.

If you don't know this already, the documentation can be found here:

[https://cursepy.readthedocs.io/en/latest/index.html](https://cursepy.readthedocs.io/en/latest/index.html)

Be sure to check out the [cursepy PyPi page](https://pypi.org/project/cursepy/) for more information

The documentation is built using [sphinx](https://www.sphinx-doc.org/en/master/index.html).
Building the docs yourself is very simple.
You can start by installing sphinx:

```
pip install sphinx
```

Now, navigate to the 'docs' directory in your favorite terminal.
Next, you can issue the 'make' command to build the docs:

```
make html
```

This will build the docs into HTML,
and will be placed into build directory.

# Contributing

Pull requests are welcome and encouraged! If you want to see a feature in cursepy
or have a fix for a bug you came across, then a PR will be the fastest way for you 
to get the change (included in cursepy).

If you wish to simply report a bug, then you should open an issue,
and I will get back to you as soon as I can.

I also accept comments and feedback at my email address listed under my GitHub account.

# Changelog

You can have a look at the changelog [here](https://cursepy.readthedocs.io/en/latest/changelog.html).

# Special Thanks

Sir Quinn - Documentation work

Sally Miller - Proof reading

# Conclusion

cursepy offers a pythonic, intuitive way to interact with CurseForge projects!
We offer high levels of customizability
while at the same time being easy to use. 
