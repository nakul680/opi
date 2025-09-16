#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockElprop
from opi.input.simple_keywords import AuxBasisSet, BasisSet, Dft, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp009() -> Output:
    current_folder = Path(__file__).parent
    wd = current_folder / "RUN"
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")
    calc.input.add_simple_keywords(Dft.PBE0, BasisSet.DEF2_SVP, AuxBasisSet.DEF2_J, Task.FREQ)

    calc.input.ncores = 4
    calc.input.add_blocks(BlockElprop(polar="analytic"))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()
    return output


if __name__ == "__main__":
    run_exmp009()
