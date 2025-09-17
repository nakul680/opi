#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import Approximation, AuxBasisSet, BasisSet, Dlpno, Scf, Wft
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp014() -> Output:
    """Perform an LED decomposition with DLPNO-CCSD(T)/cc-pVDZ"""
    current_folder = Path(__file__).parent
    wd = current_folder / "RUN"
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz")

    calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T,
        BasisSet.CC_PVDZ,
        AuxBasisSet.CC_PVDZ_C,
        AuxBasisSet.CC_PVTZ_JK,
        Dlpno.TIGHTPNO,
        Scf.TIGHTSCF,
        Approximation.RIJK,
        Dlpno.LED,
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

    # > Obtain the structure and write a new input file with the same fragment IDs
    new_structure = output.get_structure()
    new_calc = Calculator(basename="new_job", working_dir=wd)
    new_calc.structure = new_structure
    new_calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T,
        BasisSet.CC_PVDZ,
        AuxBasisSet.CC_PVDZ_C,
        AuxBasisSet.CC_PVTZ_JK,
        Dlpno.TIGHTPNO,
        Scf.TIGHTSCF,
        Approximation.RIJK,
        Dlpno.LED,
    )

    new_calc.write_input()
    return output


if __name__ == "__main__":
    run_exmp014()

