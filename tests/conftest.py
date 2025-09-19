"""
Location of fixtures for pytest must be listed here.

To define the location of module containing fixtures, the absolute path to that model
starting from the main package folder must be given.
"""

import inspect
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any, Optional, cast

import pytest
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

# > Location of modules containing fixtures.
# >> Searching for Python modules which do no start with an underscore and converting file path to module path.
pytest_plugins = [
    f"tests.fixtures.{filename.stem}"
    for filename in Path(__file__).parent.joinpath("fixtures").glob("*.py")
    if not filename.name.startswith("_")
]


# > hookwrapper for printing the scratch directory when a test with `tmp_path` in its signature fails
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: Item,
    call: CallInfo[Any],
) -> Generator[None, Any, None]:
    # In a hookwrapper, the value of `outcome = yield` is *sent* into the generator.
    # We declare the generator's SendType as `Any`.
    outcome = yield

    # > cast outcome result to the concrete pytest report.
    rep = cast(TestReport, outcome.get_result())

    # > If the test failed
    if rep.failed:
        # `funcargs` isn't in Item's public stubs; use getattr + cast to satisfy mypy.
        funcargs = cast(dict[str, Any], getattr(item, "funcargs", {}))

        # > if `tmp_path` is in the functions signature
        tmp = cast(Optional[Path], funcargs.get("tmp_path"))
        if tmp is not None:
            # > make mypy happy by making sure `when` is not None
            when = rep.when or "call"
            item.add_report_section(when, "scratch", str(tmp))
            print(f"[scratch-dir] {tmp}")


@pytest.fixture
def example_path_for() -> Callable[[Callable[..., object]], Path]:
    """Return the directory where the given function is defined."""

    def _get_path(fn: Callable[..., object]) -> Path:
        return Path(inspect.getfile(fn)).parent

    return _get_path


@pytest.fixture
def example_input_file(
    example_path_for: Callable[[Callable[..., object]], Path],
) -> Callable[[Callable[..., object], str], Path]:
    """Return inp.xyz from the directory where the given function is defined."""

    def _get(fn: Callable[..., object], filename: str = "inp.xyz") -> Path:
        path = example_path_for(fn) / filename
        assert path.exists(), f"Missing input file: {path}"
        return path

    return _get
