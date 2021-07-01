"""
Dummy testing file for capy.

We are here for testing the two operations,
as well as doing a simple test to see which one is faster.
"""

import time
import pprint
import timeit

from capy.backend import ForgeSVCBackend
from capy.wrapper import SVCWrap


def conv():
    
    # Test the conventional, class based method:

    #print("Testing class based backend ...")

    back = ForgeSVCBackend()

    back_games = back.games()

    #print("Game data:")
    #pprint.pprint(back_games)


def hand():

    # Test the new, handler based method:

    #print("Testing handler based backend ...")

    hand = SVCWrap()

    hand_games = hand.games()

    print("Game data:")
    pprint.pprint(hand_games)


# Run the functions:

print("Testing hand based backend ...")

hand_time = timeit.timeit(hand, number=3)
print("Average hand time: {}".format(hand_time))


print("Testing class-based backend ...")

conv_time = timeit.timeit(conv, number=3)
print("Average conv time: {}".format(conv_time))


if hand_time < conv_time:

    print("Hand time faster by : {} secs!".format(conv_time - hand_time))

else:

    print("Conv time faster by : {} secs!".format(hand_time - conv_time))

