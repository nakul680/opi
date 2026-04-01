import typing

from opi.input.simple_keywords import Dft, SimpleKeyword
from opi.tasks.task_base import MethodSettings


class DFTSettings(MethodSettings):
    method: typing.Annotated[SimpleKeyword, Dft]
    _name: str = "dft"
