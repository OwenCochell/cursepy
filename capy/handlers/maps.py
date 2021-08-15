"""
Stores Handler maps to be used by capy.

We store these in a separate folder to resolve circular import dependencies!
Here is a list of the follwing maps:

    * DEFAULT_MAP - Default handler map
"""

from capy.handlers.forgesvc import svc_map


# Default capy handler map:

DEFAULT_MAP = (svc_map)
