import re

from opi.input.blocks.base import Block
from opi.input.blocks.util import NoCaseDict

__all__ = [
    "ORCABlock",
]


_NAME_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z_0-9]*$")


class ORCABlock(Block):
    """
    Class used to create arbitrary blocks that have not yet been implemented in OPI. The key-value pairs for an arbitrary
    block option are stored as arbitrary options, hence both must be strings.

    Examples
    --------

    >> arbit_block = ORCABlock(name='arbitrary_block', values = {'arbitrary_key': 'arbitrary_value'})


    """

    def __init__(self, name: str, values: dict[str, str] | None = None, aftercoord: bool = False):
        """

        Parameters
        ----------
        name: Name of arbitrary block

        values: Values to be added to the block. They will be added as arbitrary options, so both key and value must be strings.

        aftercoord: Sets whether block will appear before or after coordinates in the ORCA .inp file.
        """
        super().__init__(aftercoord=aftercoord)

        name = self.normalize(name)
        self._name = name
        if values:
            self._arbitrary = NoCaseDict(values)

    def normalize(self, name: str) -> str:
        """
        Normalize the arbitrary block name. Strips leading '%' and whitespaces.
        Parameters
        ----------
        name: User-given name of arbitrary block.

        Returns
        -------
        str
            Normalized string.

        Raises
        ------
        ValueError
            If user-given name is invalid, or an ORCa block with that name is already implemented.
        """
        name = name.strip("% ").lower()

        if not _NAME_PATTERN.fullmatch(name):
            raise ValueError("Invalid name for ORCA block")

        block_class = Block.get_block_class(name)

        if block_class:
            raise ValueError(
                f"ORCA block with this name already exists. Use {block_class.__name__} instead."
            )

        return name
