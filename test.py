"""
Dummy testing file for capy.

We are here for testing the two operations,
as well as doing a simple test to see which one is faster.
"""

import time

from capy.backend import ForgeSVCBackend
from capy.wrapper import SVCWrap


# Test the conventional, class based method:

print("Testing class based backend ...")

back = ForgeSVCBackend()

# Time an expensive operation:

start = time.perf_counter()

back_games = back.games()

conv_time = time.perf_counter() - start

print("Time elapsed: {}".format(conv_time))
print("Game data: {}".format(back_games))

# Test the new, handler based method:

print("Testing handler based backend ...")

hand = SVCWrap()

# Time an expensive operation:

start = time.perf_counter()

hand_games = hand.games()

hand_time = time.perf_counter() - start

print("Time elapsed: {}".format(hand_time))
print("Game data: {}".format(hand_games))

# Check if data matches:

if hand_games == back_games:

    print("Data matches!")

if hand_time < conv_time:

    print("Hand time faster by : {} secs!".format(conv_time - hand_time))

else:

    print("Conv time faster by : {} secs!".format(hand_time-conv_time))

