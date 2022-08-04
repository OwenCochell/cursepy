"""
Modrinth - Handlers for getting requests for Modrinth
A back up source of API requests just in case Curse Forge fails or receives errors
"""

from __future__ import annotations

import json
from typing import Any, Tuple

from cursepy.classes.search import SearchParam, url_convert
from cursepy.handlers.base import URLHandler
from cursepy.classes import base

class BaseModrinthHandler(URLHandler):
    
    def __init__(self):
        super().__init__('Modrinth', "https://api.modrinth.com", "/v2", '')
    
    def pre_process(self, data: Any) -> Any:
        return json.loads(data)

    def post_process(self, data: Any) -> Any:
        print("Hello!")


class ModrinthProject(URLHandler):

    def build_url(self):

        return self.proto.url_build('project/{}'.format('Modrinth'))

    def format(self, data: dict):

        return base.CurseAddon(data)
    
class SearchMods(BaseModrinthHandler):
    """ """
    
class ModrinthMaven(BaseModrinthHandler):
    """ All projects uploaded to Modrinth are automatically placed on a Maven repository (henceforth "the Maven"). 
    This can be used for a variation of reasons, in tandem with a JVM build automation tool such as Gradle. 
    This tool will not be of any use to an everyday user, but can be very useful for mod or plugin developers.
    
    Potential auto updater?"""