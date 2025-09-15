#!/usr/bin/env python3

import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockGoat
from opi.input.simple_keywords import Sqm, Goat
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp025() -> Output:
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    current_folder = Path(__file__).parent
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")
    calc.input.add_simple_keywords(Sqm.GFN2_XTB, Goat.GOAT)
    calc.input.add_blocks(BlockGoat(maxiter=128, explore=True))
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    # > there is not really much output to be gained from a goat run
    # > other than the finalensemble.xyz or a final single point energy

    return calc.get_output()


if __name__ == "__main__":
    run_exmp025()
