from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block
from opi.input.blocks.util import NumList

__all__ = ("BlockElprop",)


class BlockElprop(Block):
    """Class to model %elprop block in ORCA"""

    _name: str = "elprop"
    printlevel: int | None = None     #
    dipole: bool | None = None        # calculate dipole
    quadrupole: bool | None = None    # calculate quadrupole
    polarvelocity: bool | None = None # polarizability w.r.t velocity perturbations
    polardipquad: bool | None = None  # dipole-quadrupole polarixability
    polarquadquad: bool | None = None # quadrupole-quadrupole polarizability
    kinetic: bool | None = None
    efield: float | None = None
    polar: Literal["analytic", "semianalytic", "numeric"] | None = None
    freq_real: float | None = None    # purely real frequency
    freq_imag: float | None = None    # purely imaginary frequency
    dipoleatom: bool | None = None
    quadrupoleatom: bool | None = None
    polaratom: int | None = None
    solver: Literal["cg", "diis", "pople"] | None = None
    maxiter: int | None = None        # max. number of iterations in CPSCF
    maxdiis: int | None = None
    tol: float | None = None          # Convergence of the CP-SCF equations
    levelshift: float | None = None
    origin: (
        Literal[
            "centerofmass",
            "centerofnuccharge",
            "centerofnuclearcharge",
            "centerofelcharge",
            "centerofspindens",
            "centerofspindensity",
        ]
        | NumList
        | None
    ) = None

    @field_validator("origin", mode="before")
    @classmethod
    def numlist_from_list(cls, inp: NumList | str | list[int] | list[float]) -> NumList | str:
        """
        Parameters
        ----------
        inp : NumList | str | list[int] | list[float]
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp
