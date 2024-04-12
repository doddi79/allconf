__all__ = [
    'JsonFileConfigLoader',
]

from .base import *
import json

import logging
log = logging.getLogger(__name__)


class JsonFileConfigLoader(BaseLoader):
    @staticmethod
    def load(file_name: str) -> dict:
        """
        LEGACY STUFF!
        """
        ldr = JsonFileConfigLoader()
        ldr.load_file(file_name)
        return ldr.data

    # def load_url(self, url: str):
    #     pass

    def load_raw(self, raw_data: str, no_resolve: bool = False,
                 no_extend: bool = False, no_includes: bool = False, no_env_load: bool = False,
                 no_fidelius: bool = False):
        self._data = self._load_dict(json.loads(raw_data))
        self._set_chains()
        if not no_extend:
            self._extend()
        if not no_includes:
            self._includes()
        if not no_resolve:
            self._resolve()
        if not no_fidelius:
            self._fetch_fidelius()

    @property
    def rendered(self) -> str:
        return json.dumps(self._data, indent=4)
