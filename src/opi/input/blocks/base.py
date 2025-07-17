from abc import ABC
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from opi.input.blocks.util import InputFilePath
from opi.input.simple_keywords import SimpleKeyword

__all__ = "Block"


class Block(BaseModel, ABC):
    """
    Base Class for Block.
    Each ORCA input block is defined in the module block_<block_name>.py
    Every class defined for a block is derived from this base Block class ,
    which defines attributes, methods and properties shared by all blocks.

    Attributes
    ----------
        aftercoord (bool): Indicates whether the block is positioned after a coordinate transformation.

    Private Attributes
    ------------------
        _name (str): Internal name identifier for the block.
        _arbitrary (dict[str, str]): A dictionary storing arbitrary variable names as keys and the variable values as value. Both are stored as strings.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    _name: str
    aftercoord: bool = False
    _arbitrary: dict[str, str] = {}

    def add_arbitrary_attributes(self, var: dict[str, str]) -> None:
        """
        Add arbitrary attributes to this block.

        Parameters
        ----------
        var: dict[str, str]
            Dictionary storing arbitrary variable names as keys and the variable values as value
        """
        self._arbitrary.update(var)

    def remove_arbitrary_attribute(self, name: str) -> None:
        """
        Remove arbitrary attribute from this block.

        Parameters
        ----------
        name: str
        Name of arbitrary attribute to remove
        """
        self._arbitrary.pop(name)

    def clear_arbitrary(self) -> None:
        """
        Clear arbitrary attributes from this block.

        """
        self._arbitrary.clear()

    def format_orca(self) -> str:
        """
        Method to convert a Block instance into string for the ORCA input file.
        Returns the string representation of the respective class it is called by.
        """
        s = f"%{self.name}\n"
        for key, value in self._arbitrary.items():
            s += f"    {key} {value.lower()}\n"
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "aftercoord":
                    continue
                elif isinstance(value, SimpleKeyword):
                    s += f'    {key} "{str(value).lower()}"\n'
                else:
                    s += f"    {key} {str(value).lower()}\n"
        s += "end"

        return s

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
        """
        raise AttributeError("*Block.name* is a read-only property!")

    @field_validator("*", mode="before")
    @classmethod
    def init_inputpath(cls, inp: Any) -> Any:
        if isinstance(inp, Path):
            return InputFilePath(file=inp)
        else:
            return inp
