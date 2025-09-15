#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockMdci
from opi.input.simple_keywords import AuxBasisSet, BasisSet, Dlpno, Wft
from opi.input.structures import Structure
from opi.output.core import Output


# > perform a DLPNO-CCSD(T) calculation
def run_exmp031() -> Output:
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    current_folder = Path(__file__).parent
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")
    calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T, Dlpno.TIGHTPNO, BasisSet.DEF2_SVP, AuxBasisSet.DEF2_SVP_C
    )

    # modify dlpno settings
    calc.input.add_blocks(BlockMdci(tcutdo=2.5 * (10**-3), tcutpno=10 ** (-10)))

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
    run_exmp031()
