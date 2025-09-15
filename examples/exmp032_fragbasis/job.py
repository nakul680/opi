#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockBasis, FragBasis, FragAuxJ, FragEcp
from opi.input.simple_keywords import Dft, Scf, OutputControl, BasisSet, AuxBasisSet, Ecp
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp032() -> Output:
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    current_folder = Path(__file__).parent
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")
    calc.input.add_simple_keywords(
        OutputControl.PRINTBASIS,Dft.BP86, Scf.NOITER, BasisSet.DEF2_SVP, AuxBasisSet.DEF2_J
    )

    calc.input.add_blocks(
        BlockBasis(fragbasis= FragBasis(frag={1:BasisSet.DEF2_TZVP,2:BasisSet.DEF2_QZVP}),
                   fragauxj = FragAuxJ(frag={2:AuxBasisSet.AUTOAUX,3:AuxBasisSet.DEF2_JK}),
                   fragecp = FragEcp(frag={3:Ecp.SK_MCDHF_RSC}),

        )
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

    return output


if __name__ == "__main__":
    run_exmp032()
