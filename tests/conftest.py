"""
Location of fixtures for pytest must be listed here.

To define the location of module containing fixtures, the absolute path to that model
starting from the main package folder must be given.
"""

import inspect
from pathlib import Path

import pytest

# > Location of modules containing fixtures.
# >> Searching for Python modules which do no start with an underscore and converting file path to module path.
pytest_plugins = [
    f"tests.fixtures.{filename.stem}"
    for filename in Path(__file__).parent.joinpath("fixtures").glob("*.py")
    if not filename.name.startswith("_")
]
print(pytest_plugins)


# > If a test with tmp_path fails we want to print the Path for debugging
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # > test fails
    if rep.failed:
        tmp = item.funcargs.get("tmp_path")
        # > tmp_path is a function argument
        if tmp:
            item.add_report_section(rep.when, "scratch", f"{tmp}")
            print(f"[scratch-dir] {tmp}")


@pytest.fixture
def example_path_for():
    """
    Return the directory where the given function is defined.
    Usage:
        example_path = example_path_for(run_exmp001)
    """

    def _get_path(fn):
        return Path(inspect.getfile(fn)).parent

    return _get_path


@pytest.fixture
def example_input_file(example_path_for):
    def _get(fn, filename="inp.xyz"):
        path = example_path_for(fn) / filename
        assert path.exists(), f"Missing input file: {path}"
        return path

    return _get
