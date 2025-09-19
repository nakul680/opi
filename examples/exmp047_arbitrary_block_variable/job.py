#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockScf
from opi.input.simple_keywords import Sqm
from opi.input.simple_keywords import Scf
from opi.input.simple_keywords import Task
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Sqm.NATIVE_GFN2_XTB,
        Task.SP,
    )

    scf_block = BlockScf()
    scf_block.add_option(879 , "True")
    calc.input.add_blocks(scf_block)

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # check for convergence of the SCF
    if output.results_properties.geometries[0].single_point_data.converged:
        print("SCF CONVERGED")
    else:
        print("SCF DID NOT CONVERGE")
        sys.exit(1)

    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())
