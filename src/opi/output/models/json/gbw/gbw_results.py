import json
from pathlib import Path

from pydantic import Field

from opi.output.models.base.get_item import GetItem
from opi.output.models.json.gbw.properties.cite import Cite
from opi.output.models.json.gbw.properties.header import OrcaHeader
from opi.output.models.json.gbw.properties.molecule import Molecule
from opi.utils.dict_to_lower import dict_to_lower


class GbwResults(GetItem):
    """
    This class contains all the information from the baseman.json file

    Attributes
    ----------
    orca header: OrcaHeader
        Contains information from the ORCA-Header
    citations: List[Cite]
        Contains the paper that are necessary to cite
    molecule: Molecule
        Contains information about the molecule
    """

    orca_header: OrcaHeader | None = Field(alias="orca header")
    citations: list[Cite] | None = None
    molecule: Molecule | None = None

    class Configuration:
        allow_population_by_field_name = True

    @classmethod
    def from_json(cls, json_file: Path | str) -> "GbwResults":
        """
        Creates a `GbwResults` instance from a JSON file.
        Parameters
        ----------
        json_file: Path | str
            Path to the JSON file

        Returns
        -------
        GbwResults
            An instance of the `GbwResults` class
        """
        with open(json_file, "r") as file:
            data = json.load(file)

        data = dict_to_lower(data)
        if not isinstance(data, dict):
            raise AssertionError("Data is not a dictionary")

        return cls(**data)
