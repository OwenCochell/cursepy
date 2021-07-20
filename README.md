# capy
A modular API for interacting with [CurseForge](https://curseforge.com).

# Introduction

Curseforge Api PYthon(or capy for short) allows you to interact with CurseForge
addons and files in a simply, easy to use way.

Our goal is to be modular and heavily customizable for developers who
have very specific use cases, while also being simple and intuitive
for developers who want something that 'just works'.

We support getting information on all games,
addons, categories, files, and so much more!
We also offer easy to use methods for downloading 
said files.

# Example

```python
from capy import HandlerCollection  # Import the HandlerCollection

GAME_ID = 432  # ID of the game you want to fetch, in this case Minecraft

# Create the HandlerCollection:

curse = HandlerCollection()

# Get the game info:

game = curse.game(GAME_ID)

# Print the name of the game:

print(game.name)
```

# Features

Here, we will give brief examples of capy features.
For more information, you should check out our [documentation]()!

## Modular Design

Each operation is managed by a component called a 'handler'.
Handlers are simply classes that get information and process it.
This information can be from any location,
and it can be retrieved using any protocol.

The only limit is your imagination!

Our modular method allows for functionality to be swapped and
mixed around, allowing for automated and easier customization
compared to sub-classing.

Have a look at the documentation on handler development [here]()!

## Curse Instances

As stated earlier, curse data can come from any location
using any protocol.
Because of this, the developer might have to check and work
with data in many different formats and in many different makeups.

Not ideal!

capy offers curse instances that normalize data,
and offer a container for data to be kept in.
This ensures that no matter what,
the developer will be working with data in the same way,
regardless of how or where we got the data from.

Curse Instances have plenty of other nifty features for 
easing your development, so be sure to check out their [documentation]()!

## Wrappers

Wrappers ease the process of interacting with certain games and projects on CurseForge.
They do this by keeping track of relevant information, such as game and category ID's,
so you as the developer do not have to.

For example, the 'MinecraftWrapper' eases the process of getting 
information on Minecraft projects and addons.

Again, have a look at our [documentation]() for more info!

# Installation

You can install capy via pip:

    $ pip install mctools

For more information on installing capy,
check out the installation section in our [documentation](). 

# Documentation

As stated many times before, we have an extensive documentation. It contains tutorials, the API reference,
and best practice recommendations.

I'm sure you know this already, but the documentation can be found here:

    [doc link]

Be sure to check out the [capy PyPi page]() for more information

# Contributing

Pull requests are welcome and encouraged :) ! If you want to see a feature in capy,
or have a fix for a bug you came across, then a PR will be the fastest way to 
to get you change included in capy.

I also accept comments and feedback at my email address listed under my GitHub account.

# Changelog

## 1.0.0

Initial Commit

# Special Thanks

Sir Quinn - Documentation work

# Conclusion

capy offers a pythonic, intuitive way to interact with CurseForge projects!
We offer high levels of
