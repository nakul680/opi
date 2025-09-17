#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet
from opi.input.simple_keywords import Dft
from opi.input.simple_keywords import Scf
from opi.input.simple_keywords import Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp035() -> Output:
    current_folder = Path(__file__).parent
    wd = current_folder / "RUN"
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz(current_folder/"inp.xyz",charge=1,multiplicity=2)
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Dft.TPSS,
        BasisSet.DEF2_SVP,
        Task.SP,
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

    # check for convergence of the SCF
    if output.scf_converged():
        print("SCF CONVERGED")
    else:
        print("SCF DID NOT CONVERGE")
        sys.exit(1)

    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())

    # Use orca_plot to plot mo 5,the density and the spin_density
    mo_5 = output.plot_mo(5)
    density = output.plot_density()
    spin_density = output.plot_spin_density()

    # Print paths to the cube files
    print(mo_5)
    print(density)
    print(spin_density)

    # > save mo in working dir line by line
    with open(current_folder / f"{mo_5.path.name}.from_iterator", "w") as file:
        for line in mo_5:
            file.write(line)

    return output


if __name__ == "__main__":
    run_exmp035()

