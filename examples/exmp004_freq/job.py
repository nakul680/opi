#!/usr/bin/env python3

import shutil
from pathlib import Path
import sys

from opi.core import Calculator
from opi.input.simple_keywords import (
    BasisSet,
    Dft,
    Scf,
    Task,
)
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp004() -> Output:
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    current_folder = Path(__file__).parent
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, BasisSet.DEF2_TZVP, Dft.TPSS, Task.FREQ)
    calc.input.ncores = 4

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
    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())
    print("Temperature [K]")
    print(output.results_properties.geometries[0].thermochemistry_energies[0].temperature)
    print("Final Gibbs free energy")
    print(output.get_free_energy())
    print("Zero-point energy")
    print(output.get_zpe())
    print("Final enthalpy H")
    print(output.get_enthalpy())
    print("Final entropy S")
    print(output.get_entropy())
    print("G-E(el)")
    print(output.get_free_energy_delta())
    return output


if __name__ == "__main__":
    run_exmp004()

