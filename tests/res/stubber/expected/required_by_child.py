__all__ = [
    'CfgTopSecondShouldBeOptionalStub',
    'CfgTopSecondMustExistStub',
    'CfgTopSecondStub',
    'CfgTopStub',
    'CfgStub',
    'AllConfConfigStub',
]

from typing import *
from allconf.structs import Empty
from allconf.structs.cfgstub import _BaseCfgStub
from allconf.structs import BaseConfig


class CfgTopSecondShouldBeOptionalStub(_BaseCfgStub, dict):
    bar: Union[str, Empty]


class CfgTopSecondMustExistStub(_BaseCfgStub, dict):
    foo: str


class CfgTopSecondStub(_BaseCfgStub, dict):
    should_be_optional: Union[CfgTopSecondShouldBeOptionalStub, Empty]
    must_exist: CfgTopSecondMustExistStub


class CfgTopStub(_BaseCfgStub, dict):
    second: CfgTopSecondStub


class CfgStub(_BaseCfgStub, dict):
    top: CfgTopStub


class AllConfConfigStub(BaseConfig, CfgStub):
    pass
