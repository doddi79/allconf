__all__ = [
    "SingletonConfig",
]

from .baseconfig import *
from batutils.structs import *


class SingletonConfig(BaseConfig, metaclass=Singleton):
    pass
