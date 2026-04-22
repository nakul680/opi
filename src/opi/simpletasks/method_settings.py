import typing
import warnings

from pydantic import field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from opi.input import Input
from opi.input.simple_keywords import Dft, SimpleKeyword, Grid, DispersionCorrection, Sqm, Wft, Method, ForceField, \
    BasisSet, SolvationModel, Solvent
from opi.input.simple_keywords.scf import ScfThreshold, ScfSolver, Scf, ScfConvergence
from opi.simpletasks.settings import Settings



class MethodSettings(Settings):
    method: typing.Annotated[SimpleKeyword, Method] | None = None
    basis_set: typing.Annotated[SimpleKeyword, BasisSet] | None = None
    solvation_model: typing.Annotated[SimpleKeyword, SolvationModel] | None = None
    solvent: typing.Annotated[str, Solvent] | None = None


class DFTSettings(MethodSettings):
    _name: str = "dft"
    method: typing.Annotated[SimpleKeyword, Dft] | None = None
    grid: typing.Annotated[SimpleKeyword, Grid] | None = None
    scf_maxiter: typing.Annotated[int, "BlockScf", "maxiter"] | None = None
    scf_threshold: typing.Annotated[SimpleKeyword, ScfThreshold] | None = None
    scf_solver: typing.Annotated[SimpleKeyword, ScfSolver] | None = None
    scf_stab: bool = False
    scf_conv: typing.Annotated[SimpleKeyword, ScfConvergence] | None = None


    @field_validator("*", mode="before")
    @classmethod
    def validate_fields(cls, value: typing.Any, info: ValidationInfo) -> typing.Any:
        if info.field_name == "method":
            try:
                new_keyword = Dft.find_keyword(value)
            except ValueError:
                new_keyword = cls._find_dft_disp_keyword(value)
            return new_keyword
        else:
            return super().validate_fields(value, info)



    @model_validator(mode="after")
    def cross_validate(self) -> "DFTSettings":
        """
        Cross-validation for `DftSettings`.
        If the method keyword contains '3c', the `basis_set` attribute will be set to `None`.

        The `DftSettings` object is then returned.
        Parameters
        ----------
        data: DFTSettings
            `DFTSettings` object given as input.

        Returns
        -------
        DFTSettings
            Cross-validated `DFTSettings` object.

        """
        if (self.method and "3c" in self.method.keyword) and self.basis_set:
            warnings.warn("Basis Set will be ignored due to selection of Method", UserWarning)
            self.basis_set = None

        return self

    def map_to_input(self, input_object: Input) -> Input:
        input_object = super().map_to_input(input_object)

        if self.scf_stab:
            input_object.add_simple_keywords(Scf.SCFSTAB)

        return input_object

    @classmethod
    def _find_dft_disp_keyword(cls, value: str | SimpleKeyword) -> SimpleKeyword:
        """
        Function to search for a `Dft` keyword along with `DispersionCorrection`.
        In the case that an - is present in keyword, the keyword is split along the - and it is verified whether the
        given keyword is a valid combination of `Dft` and `DispersionCorrection` keyword.

        If it is , a `SimpleKeyword` object is created and returned. If not , a `ValueError` is raised.
        Parameters
        ----------
        value: str | SimpleKeyword
            The value to search for.

        Returns
        -------
        SimpleKeyword
            The created `SimpleKeyword` object.

        Raises
        ------
        ValueError
            If given value is invalid

        """
        if isinstance(value, SimpleKeyword):
            value = value.keyword

        if '-' in value:
            try:
                keywords = value.split('-')
                Dft.find_keyword(keywords[0])
                DispersionCorrection.find_keyword(keywords[1])

                return SimpleKeyword(value)
            except ValueError:
                raise ValueError(f"Invalid Dft keyword or dispersion correction given: {value}")
        else:
            raise ValueError(f"Invalid Dft keyword '{value}'")


class SQMSettings(MethodSettings):
    _name: str = "sqm"
    method: typing.Annotated[SimpleKeyword, Sqm]


class WftSettings(MethodSettings):
    _name: str = "wft"
    method: typing.Annotated[SimpleKeyword, Wft]

class HFSettings(MethodSettings):
    _name: str = "hf"
    method: typing.Annotated[SimpleKeyword, Method]

class ForceFieldSettings(MethodSettings):
    _name: str = "forcefield"
    method: typing.Annotated[SimpleKeyword, ForceField]



