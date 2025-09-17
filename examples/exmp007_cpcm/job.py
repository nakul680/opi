#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Dft, Scf, SolvationModel, Solvent
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp007() -> Output:
    """Perform a BP86/def2-SVP single-point calculation with implicit CPCM solvation for water"""
    current_folder = Path(__file__).parent
    wd = current_folder / "RUN"
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART, Dft.BP86, BasisSet.DEF2_SVP, SolvationModel.CPCM(Solvent.WATER)
    )

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    ngeoms = len(output.results_properties.geometries)
    print("N GEOMETRIES")
    print(ngeoms)
    print("DFT ENERGY")
    print(output.results_properties.geometries[0].dft_energy.finalen)
    print("Solvent")
    print(output.results_properties.geometries[0].solvation_details.solvent)
    print("Epsilon")
    print(output.results_properties.geometries[0].solvation_details.epsilon)
    print("Surface points")
    print(output.results_properties.geometries[0].solvation_details.npoints)
    print("CPCM ENERGY")
    print(output.results_properties.geometries[0].solvation_details.cpcmdielenergy)

    return output


if __name__ == "__main__":
    run_exmp007()
