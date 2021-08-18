"""
Stores Handler maps to be used by cursepy.

We store these in a separate folder to resolve circular import dependencies!
Here is a list of the follwing maps:

    * DEFAULT_MAP - Default handler map
"""

from cursepy.handlers.forgesvc import svc_map


# Default cursepy handler map:

DEFAULT_MAP = (svc_map)
