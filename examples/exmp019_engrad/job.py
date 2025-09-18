#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockMethod
from opi.input.simple_keywords import BasisSet
from opi.input.simple_keywords import (
    DispersionCorrection,
)
from opi.input.simple_keywords import Method
from opi.input.simple_keywords import Scf
from opi.input.simple_keywords import SolvationModel
from opi.input.simple_keywords import Solvent
from opi.input.simple_keywords import Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp019(structure: Structure | None = None, working_dir: Path | None = Path("RUN")) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = structure
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.SP,
        SolvationModel.CPCM(Solvent.WATER),
        DispersionCorrection.D3,
    )
    calc.input.add_simple_keywords(Task.ENGRAD)

    calc.input.add_blocks(BlockMethod(d3s6=0.64, d3a1=0.3065, d3s8=0.9147, d3a2=5.0570))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    print("FINAL SINGLE POINT ENERGY")
    print(output.results_properties.geometries[0].single_point_data.finalenergy)
    print("SCF ENERGY")
    print(output.results_properties.geometries[0].energy[0].totalenergy[0][0])

    return output


if __name__ == "__main__":
    run_exmp019()
