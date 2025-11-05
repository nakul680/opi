from pydantic import field_validator

from opi.input.blocks import Block
from opi.input.blocks.util import InputFilePath

__all__ = ("BlockEda",)


class BlockEda(Block):
    """Class to model %eda block in ORCA"""

    _name: str = "eda"
    frag1_c: int | None = None  # charge of molecular fragment 1
    frag2_c: int | None = None  # charge of molecular fragment 2
    frag1_m: int | None = None  # multiplicity of molecular fragment 1
    frag2_m: int | None = None  # multiplicity of molecular fragment 2
    frag1_sf: bool | None = None # flip the spin of uncoupled electrons in fragment 1
    frag2_sf: bool | None = None # flip the spin of uncoupled electrons in fragment 2
    printinfo: bool | None = None
    frag2_fs: bool | None = None
    frag1: InputFilePath | None = None
    frag2: InputFilePath | None = None
    frag1_methodfile: InputFilePath | None = None # file that contains method input for fragment 1
    frag2_methodfile: InputFilePath | None = None # file that contains method input for fragment 2

    @field_validator("frag1", "frag2", "frag1_methodfile", "frag2_methodfile", mode="before")
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path
