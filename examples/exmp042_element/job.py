#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.output.core import Output
from opi.utils.element import Element
from opi.input.structures import Structure

def run_exmp042() -> Output:
    current_folder = Path(__file__).parent
    wd = current_folder / "RUN"
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")

    # > Print cardinal numbers of input file
    for atom in calc.structure.atoms:
        print(atom.element.atomic_number)

    # > Print some other cardinal numbers
    he_element = Element("he")
    print(he_element.atomic_number)

    return calc.get_output()


if __name__ == "__main__":
    run_exmp042()





