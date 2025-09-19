import pytest

from examples.exmp045_existing_calc.job import run_exmp045


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp045_existing_calc() -> None:
    """Ensure OPI can obtain energy from existing calculation."""
    output = run_exmp045()

    # Assert final energy
    assert output.get_final_energy()
