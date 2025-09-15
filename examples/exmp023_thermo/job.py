#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import (
    BlockFreq,
)
from opi.input.simple_keywords import (
    BasisSet,
    Dft,
    Scf,
    Task,
)
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp023() -> Output:
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    current_folder = Path(__file__).parent
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, BasisSet.DEF2_TZVP, Dft.TPSS, Task.FREQ)
    calc.input.add_blocks(
        BlockFreq(temp=500, numfreq=True, quasirrho=False, pressure=1.5, partial_hess=[0, 1])
    )
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
    print(output.results_properties.geometries[0].dft_energy.finalen)
    print("Temperature [K]")
    print(output.results_properties.geometries[0].thermochemistry_energies[0].temperature)
    print("Final Gibbs free energy")
    print(output.results_properties.geometries[0].thermochemistry_energies[0].freeenergyg)

    return output


if __name__ == "__main__":
    run_exmp023()
