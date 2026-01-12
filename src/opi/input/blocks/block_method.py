from typing import Literal

from pydantic import field_validator, BaseModel

from opi.input.blocks import Block
from opi.input.blocks.util import InputFilePath

__all__ = ("BlockMethod",)

class ExternalParam(BaseModel):
    """
    Class to model `extparamx'. `extparamx` and `extparamxc` attributes in `BlockMethod`.

    Attributes
    -----------
    paramname : str
        Name of parameter.

    new_value : float
        New value of parameter.

    """
    paramname: str
    new_value: float

    @classmethod
    def from_string(cls, string: str) -> "ExternalParam":
        paramname, value = string.rsplit(" ", maxsplit=1)
        try:
            return ExternalParam(paramname=paramname.strip(), new_value=float(value.strip()))
        except TypeError:
            raise TypeError(f"Invalid string'{string}'")


    def __str__(self) -> str:
        return f"\"{self.paramname}\" {self.new_value}"



class BlockMethod(Block):
    """Class to model %method block in ORCA"""

    _name: str = "Method"

    method: Literal["dft"] | None = None
    exchange: (
        Literal[
            "x_nox",
            "x_slater",
            "x_becke",
            "x_wb88",
            "x_g96",
            "x_pw91",
            "x_mpw",
            "x_pbe",
            "x_rpbe",
            "x_optx",
            "x_x",
            "x_tpss",
            "x_b97d",
            "x_b97becke",
            "x_scan",
            "x_rscan",
            "x_r2scan",
        ]
        | None
    ) = None
    correlation: (
        Literal[
            "c_noc",
            "c_vwn5",
            "c_vwn3",
            "c_pwlda",
            "c_p86",
            "c_pw91",
            "c_pbe",
            "c_lyp",
            "c_tpss",
            "c_b97d",
            "c_b97becke",
            "c_scan",
            "c_rscan",
            "c_r2scan",
        ]
        | None
    ) = None
    ldaopt: Literal["c_noc", "c_pwlda", "c_vwn5", "c_vwn3"] | None = None
    xalpha: float | None = None
    xbeta: float | None = None
    xkappa: float | None = None
    xmuepbe: float | None = None
    cbetapbe: float | None = None
    rangesepexx: bool | None = None
    rangesepmu: float | None = None
    rangesepscal: float | None = None
    scalhfx: float | None = None
    scaldfx: float | None = None
    scalggac: float | None = None
    scalldac: float | None = None
    extparamx: ExternalParam | None = None
    extparamc: ExternalParam | None = None
    extparamxc: ExternalParam | None = None

    # > Options DFT-D
    d3s6: float | None = None
    d3a1: float | None = None
    d3s8: float | None = None
    d3a2: float | None = None

    # > Options for Extopt
    ProgExt: InputFilePath | None = None  # Path to wrapper script
    Ext_Params: str | None = None  # Arbitrary optional command line arguments

    @field_validator("ProgExt", mode="before")
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

    @field_validator("extparamx", "extparamc", "extparamxc", mode= "before")
    @classmethod
    def init_ext_param_from_string(cls, string: str) -> ExternalParam:
        """

        Parameters
        ----------
        string: str

        Returns
        -------
        ExternalParam
        """
        return ExternalParam.from_string(string=string)


