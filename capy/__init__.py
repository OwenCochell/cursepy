"""
capy init file.    
"""

# Import the necessary components:

from capy.handlers.base import HandlerCollection
from capy.handlers.forgesvc import svc_map

# Define some metadata here:

__version__ = '1.0.0'
__author__ = 'Owen Cochell'

# Define the default handler map:

HandlerCollection.DEFAULT_MAP = (svc_map)
