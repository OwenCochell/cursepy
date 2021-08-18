"""
Testing each and every feature cursepy has to offer!

Should really be unit tests...
"""

import time
import pprint
import timeit

from cursepy import CurseClient
from cursepy.formatters import StripHTML
from cursepy.classes.search import SearchParam


GAME_ID = 432
CATEGORY = 6
ADDON = 60089
FILE = 2671937


# Simple callbacks for testing

def call(data):
    print("In callback!")

def call2(data, thing, thing1='blah'):
    print("In callback 2!")
    print(thing)
    print(thing1)

# Create CurseClient with default handlers loaded:

client = CurseClient()

def test_call():

    # Get the games:

    print("Getting games:")

    games = client.games()

    # Get a game:

    print("Getting game:")

    game = client.game(GAME_ID)

    # Get catagories

    print("Getting categories:")

    cats = client.catagories()

    # get category:

    print("Get category")

    cat = client.category(CATEGORY)

    # Get sub-category:

    print("Sub-category:")

    sub = client.sub_category(CATEGORY)

    # Get the adddon:

    print("Getting addon:")

    addon = client.addon(ADDON)

    # Get the description:

    print("Get addon description:")

    addon_desc = client.addon_description(ADDON)

    # Get addon files:

    print("Addon files:")

    addon_files = client.addon_files(ADDON)

    # Get a file:

    print("Addon file:")

    addon_file = client.addon_file(ADDON, FILE)

    # File description:

    print("File description:")

    file_desc = client.file_description(ADDON, FILE)

    # Search

    print("Search")

    searched = client.search(GAME_ID, CATEGORY)

def iter_search():

    for addon in client.iter_search(GAME_ID, CATEGORY, SearchParam(filter='JEI', pageSize=5)):

        # Print the name:

        print(addon.name)
        inp = input("Wait")

def formatter():

    format = StripHTML()

    # Set the default formatter:

    client.default_formatter(format)

    # Make a call

    print(client.file_description(ADDON, FILE).format())

def callback():

    # Register the callback:

    client.bind_callback(call, 3)

    client.bind_callback(call2, 3, 'test', thing1='thing1')

    client.category(CATEGORY)

    # Remove the callback:

    client.clear_callback(3, call)

    client.category(CATEGORY)

    client.clear_callback(3)

    client.category(CATEGORY)

