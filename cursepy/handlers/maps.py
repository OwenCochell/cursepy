"""
Stores Handler maps to be used by cursepy.

We store these in a separate folder to resolve circular import dependencies!
Here is a list of the following maps:

    * DEFAULT_MAP - Default handler map
    * CURSEFORGE - Handlers for the official curseforge API
    * CURSETOOLS - Handlers for using the official curse.tools backend
    * FORGESVC - Handlers for using the ForgeSVC backend (DEPRECATED!)
"""

from cursepy.handlers.forgesvc import svc_map
from cursepy.handlers.curseforge import cf_map
from cursepy.handlers.cursetools import ct_map


# Default cursepy handler map:

DEFAULT_MAP = (cf_map)

CURSEFORGE = (cf_map)
CURSETOOLS = (ct_map)
FORGESVC = (svc_map)
