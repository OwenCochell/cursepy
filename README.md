# cursepy
A modular API for interacting with [CurseForge](https://curseforge.com).

[![Documentation Status](https://readthedocs.org/projects/cursepy/badge/?version=latest)](https://cursepy.readthedocs.io/en/latest/?badge=latest)

# Disclaimer

cursepy is a work in progress!

Use this library at your own risk!
We will be complete with docs soon.

# Introduction

cursepy allows you to interact with CurseForge
addons and files in a simply, easy to use way.
We offer easy to use entry points into certain CurseForge APIs and backbends.

Our goal is to be modular and heavily customizable for developers who
have very specific use cases, while also being simple and intuitive
for developers who want something that 'just works'.

We support getting information on all games,
addons, categories, files, and so much more!
We also offer easy to use methods for downloading 
said files.

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

Here, we will give brief examples of cursepy features.

## Modular Design

Each operation is managed by a component called a 'handler'.
Handlers are simply classes that get information and process it.
This information can be from any location,
and it can be retrieved in many different ways.

The only limit is your imagination!

Our modular method allows for functionality to be swapped and
mixed around, allowing for automated and easier customization
compared to sub-classing.

Have a look at the documentation on handler development [here](https://cursepy.readthedocs.io/en/latest/advn/hand.html)!

## Curse Instances

As stated earlier, curse data can come from any location,
which can be retired in many different ways.
Because of this, the developer would have to check and work
with data in many different formats and in many different makeups.

Not ideal!

cursepy offers curse instances that normalize data,
and offer a container for data to be kept in.
This ensures that no matter what,
the developer will be working with data in the same way,
regardless of how or where we got the data from.
They are dataclasses, which makes retrieving and working 
with information very easy.

Curse Instances have plenty of other nifty features for 
easing your development, so be sure to check out their [documentation](https://cursepy.readthedocs.io/en/latest/basic/curse_inst.html)!

## Wrappers

Wrappers ease the process of interacting with certain games and projects on CurseForge.
They do this by keeping track of relevant information, such as game and category ID's,
so you as the developer do not have to.

For example, the 'MinecraftWrapper' eases the process of getting 
information on Minecraft projects and addons.
We hope to implement more wrappers for more games at a later date.

Again, have a look at our [documentation](https://cursepy.readthedocs.io/en/latest/basic/wrap.html) for more info!

# Installation

You can install cursepy via pip:

    $ pip install cursepy

For more information on installing cursepy,
check out the installation section in our [documentation](https://cursepy.readthedocs.io/en/latest/install.html). 

# Documentation

As stated many times before, we have an extensive documentation. It contains tutorials, the API reference,
and best practice recommendations.

I'm sure you know this already, but the documentation can be found here:

[https://cursepy.readthedocs.io/en/latest/index.html](https://cursepy.readthedocs.io/en/latest/index.html)

Be sure to check out the [cursepy PyPi page](https://pypi.org/project/cursepy/) for more information

# Contributing

Pull requests are welcome and encouraged :) ! If you want to see a feature in cursepy,
or have a fix for a bug you came across, then a PR will be the fastest way to 
to get you change included in cursepy.

If you wish to simply report a bug, then you should open an issue,
and I will get back to you as soon as I can.

I also accept comments and feedback at my email address listed under my GitHub account.

# Changelog

You can have a look at the changelog [here]().

# Special Thanks

Sir Quinn - Documentation work

# Conclusion

cursepy offers a pythonic, intuitive way to interact with CurseForge projects!
We offer high levels of customizability,
while at the same time being easy to use. 
