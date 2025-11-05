from pydantic import field_validator

from opi.input.blocks import Block
from opi.input.blocks.util import InputFilePath
from opi.input.simple_keywords import SimpleKeyword, Solvent

__all__ = ("BlockCosmors",)


class BlockCosmors(Block):
    """Class to model %cosmors block in ORCA"""

    _name: str = "cosmors"
    orbs_vac: bool | None = None # reyse gas-phase orbitals for calculation involving solute in a conductor
    aeff: float | None = None    # effective contact area between surface segments
    lnalpha: float | None = None # logarithm of misfit prefactor
    lnchb: float | None = None   # hydrogen bond strength parameter
    chbt: float | None = None    # parameter for temperature dpendance of the HB
    sigmahb: float | None = None # HB threshold parameter
    rav: float | None = None     # radius to average ideal screening charges in Angstrom
    fcorr: float | None = None   # Parameter adjusted from dielectric screening energies
    ravcorr: float | None = None # Additional radius to calculate misfit energy in Angstrom
    astd: float | None = None    # Standard surface area ( normalization factor )
    zcoord: float | None = None  # Cooridnation number
    dgsolv_eta: float | None = None # Offset for solv. energy calculation
    dgsolv_omegaring: float | None = None # Correction for solv. energy of molecules with rings
    temp: float | None = None    # reference temperature in Kelvin
    dftfunc: SimpleKeyword | None = None # DFT functional
    dftbas: SimpleKeyword | None = None  # Basis set
    solvent: Solvent | None = None  # Solvent from internal database
    solventfilename: InputFilePath | None = None # NAme of .cosmorsxyz solvent file

    @field_validator("solventfilename", mode="before")
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
