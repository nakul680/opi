from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block
from opi.input.blocks.util import InputFilePath

__all__ = ("BlockDocker",)


class BlockDocker(Block):
    """Class to model %docker block in ORCA"""

    _name: str = "docker"
    docklevel: Literal["screening", "normal", "quick", "complete"] | None = None  # general strategy for docking
    evpes: Literal["gfnff", "gfn0xtb", "gfn1xtb", "gfn2xtb"] | None = None
    maxiter: int | None = None  # maximum number of iterations
    miniter: int | None = None  # minimum number of iterations
    printlevel: Literal["low", "normal", "high"] | None = None  # output level
    popdensity: float | None = None  # population density per Angstrom squared
    nopt: int | None = None  # fixed number of structures to be optimized
    cumulative: bool | None = None # add the contents of "GUEST" file on top of each other?
    popsize: int | None = None  # fixed number for the population size
    fixhost: bool | None = None # freeze coodinates for the HOST during all steps?
    guestcharge: int | None = None # can be used to define a charge for the guest
    guestmult: int | None = None   # can be used to define multiplicity for a guest
    nrepeatguest: int | None = None # number of times to repeat content of the GUEST file
    evoptlevel: Literal["sloppyopt", "looseopt", "normalopt"] | None = None # optimization criteria
    randomseed: bool | None = None  # whether to allow for the process to be truly random
    checkguesttopo: bool | None = None  # check topology of guest during docking process?
    guest: InputFilePath | None = None  # .xyz file from where guest will be read

    @field_validator("guest", mode="before")
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
