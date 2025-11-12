from pathlib import Path

from opi.output.models.base.get_item import GetItem
from opi.output.models.json.property.properties.calc_info import CalcInfo
from opi.output.models.json.property.properties.calc_status import (
    CalculationStatus,
)
from opi.output.models.json.property.properties.calc_time import (
    CalculationTiming,
)
from opi.output.models.json.property.properties.geometries import Geometries
from opi.output.models.json.property.properties.pal import PalFlags
import json


class PropertyResults(GetItem):
    """
    Has all the information calculated in the ORCA job

    Attributes
    ----------
    calculation_info: CalcInfo
        contains general information about the calculation
    calculation_status: CalculationStatus
        contains information about the Status of the calculation
    calculation_timings : CalculationTiming
        contains timings of the calculation
    pal_flags: PalFlags default = None
        Contains information about the parallel Jobs used in the calculation
    """

    calculation_info: CalcInfo | None = None
    calculation_status: CalculationStatus | None = None
    calculation_timings: CalculationTiming | None = None
    pal_flags: PalFlags | None = None
    geometries: list[Geometries] | None = None

    @classmethod
    def from_json(cls, file_path:Path | str) -> "PropertyResults":
        with open(file_path, "r") as file:
            data = json.load(file)

        calc_info = data.get("Calculation_Info",{})
        calc_info = {k.lower(): v for k,v in calc_info.items()}
        calc_status = data.get("Calculation_Status",{})
        calc_status = {k.lower(): v for k,v in calc_status.items()}
        calc_timings = data.get("Calculation_Timings",{})
        calc_timings = {k.lower(): v for k, v in calc_timings.items()}
        pal_flags = data.get("PAL_Flags",{})
        pal_flags = {k.lower(): v for k, v in pal_flags.items()}
        geometries = data.get("Geometries",[])

        return cls(
            calculation_info=CalcInfo(**calc_info),
            calculation_status=CalculationStatus(**calc_status),
            calculation_timings=CalculationTiming(**calc_timings),
            pal_flags=PalFlags(**pal_flags),
            geometries=geometries,
        )
