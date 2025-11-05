from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block
from opi.input.blocks.util import NumList

__all__ = ("BlockCis",)


class BlockCis(Block):
    """Class to model %cis block in ORCA"""

    _name: str = "cis"
    nroots: int | None = None  # number of desired roots
    iroot: int | None = None   # root to be optimized
    irootmult: Literal["singlet", "triplet"] | None = None  # multiplicity of root to be optimized
    maxdim: int | None = None  # davidson expansion space
    maxiter: int | None = None # maximum CI iterations
    nguessmat: int | None = None # dimension of guess matrix
    maxcore: int | None = None # maximum memory to be used
    etol: float | None = None  # energy convergence tolerance
    rtol: float | None = None  # residual convergence tolerance
    tda: bool | None = None    # switch off for full TDDFT
    lrcpcm: bool | None = None # use LRCPCM
    cpcmeq: bool | None = None # which epsilon is used to compute changes
    donto: bool | None = None  # generate Natural Transition Orbitals
    saveunrnatorb: bool | None = None # Saves natural orbitals(not NTO) from unrelaxed densities for IROOT chosen
    spinflip: bool | None = None
    soc: bool | None = None  # include spin orbital coupling
    socgrad: bool | None = None # set true to compute SOC gradient for given IROOT
    triplets: bool | None = None # calculate singlet-triplet excitations
    dotrans: bool | None = None # transient spectra - starting from IROOT or compute all possible transitions
    dcorr: int | None = None    # (D) correction
    doscs: bool | None = None   # set SCS-CIS(D) to true
    intaccxc: float | None = None
    gridxc: int | None = None
    gridx: int | None = None
    ntostates: NumList | None = None # states to consider for NTO analysis
    scspar: NumList | None = None    # scaling parameters
    ewin: NumList | None = None      # orbital energy window

    @field_validator("ntostates", "ewin", "scspar", mode="before")
    @classmethod
    def numlist_from_list(cls, inp: NumList | list[int] | list[float]) -> NumList:
        """
        Parameters
        ----------
        inp : NumList | list[int] | list[float]
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp
