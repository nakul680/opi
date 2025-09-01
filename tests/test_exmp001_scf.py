import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

example_folder = Path("../examples/exmp001_scf").resolve()


@pytest.mark.skipif(not example_folder.exists(), reason="example not found")
def test_exmp001_scf(tmp_path: Path) -> None:
    test_file = tmp_path / "job.py"
    test_xyz = tmp_path / "inp.xyz"
    shutil.copy(example_folder / "job.py", test_file)  # copy example script to file in temp folder
    shutil.copy(example_folder / "inp.xyz", test_xyz)  # copy the given structure file as well

    cwd = os.getcwd()  # save current working directory
    os.chdir(tmp_path)  # change working directory to that of temporary file

    result = subprocess.run(
        [sys.executable, str(test_file)], env=os.environ.copy(), capture_output=True, text=True
    )
    output = result.stdout.splitlines()  # read output

    os.chdir(cwd)  # change working directory back to previous value

    assert "ORCA calculation failed" not in output
    assert "SCF did not converge" not in output

    assert "SCF CONVERGED" == output[0]
    assert output[2] == output[3] == output[4]
