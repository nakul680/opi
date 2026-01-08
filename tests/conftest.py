"""
Location of fixtures for pytest must be listed here.

To define the location of module containing fixtures, the absolute path to that model
starting from the main package folder must be given.
"""

from collections.abc import Generator
from pathlib import Path
from typing import Any, Optional, cast

import pytest
import shutil
from _pytest._code.code import ExceptionRepr
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from dataclasses import dataclass

# > Location of modules containing fixtures.
# >> Searching for Python modules which do no start with an underscore and converting file path to module path.
pytest_plugins = [
    f"tests.fixtures.{filename.stem}"
    for filename in Path(__file__).parent.joinpath("fixtures").glob("*.py")
    if not filename.name.startswith("_")
]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: Item,
    call: CallInfo[Any],
) -> Generator[None, Any, None]:
    """
    Hookwrapper for printing the scratch directory when a test with `tmp_path` in its signature fails

    Examples
    --------
    When `test_example001` fails, pytest will print something like this:
        /user/opi/examples/exmp001_scf/job.py:48: SystemExit: 1
        see ORCA files in: /tmp/pytest-of-user/pytest-24/test_exmp001_scf0
    If no error message can be retrieved, just the folder is printed:
        Test of an example failed, see ORCA files in: /tmp/pytest-of-user/pytest-24/test_exmp001_scf0

    """
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

            # > Write `long` representation of the test report
            if isinstance(rep.longrepr, ExceptionRepr):
                crash = rep.longrepr.reprcrash
                # > Try to give path, line number and error type, alternatively just the scratch_dir
                if crash is not None:
                    path = crash.path
                    lineno = crash.lineno
                    message = crash.message
                    rep.longrepr = f"{path}:{lineno}: {message}\nsee ORCA files in: {tmp}"
                else:
                    rep.longrepr = f"Test of an example failed, see ORCA files in: {tmp}"

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-json-files",
        action="store_true",
        default=False,
        help="After json file generator tests pass, copy all produced *.json from tmp_path into tests/json_files/.",
    )

@dataclass(frozen=True)
class JsonFilesExporter:
    json_files_dir: Path
    prefix: str
    enabled: bool

    def export_jsons_from(
        self,
        src_dir: Path,
        *,
        recursive: bool = False,
        overwrite: bool = True,
        gbw_subdir: str = "gbw",
        property_subdir: str = "property",
    ) -> tuple[list[Path], list[Path]]:
        """
        Copy JSON files from src_dir into tests/json_files/<plain_subdir|property_subdir>.

        - plain:     *.json excluding *.property.json
        - property:  *.property.json

        Destination filenames are prefixed:
            <prefix>__<original_filename>

        Returns: (plain_dests, property_dests)
        """
        pattern = "**/*.json" if recursive else "*.json"
        sources = sorted(p for p in src_dir.glob(pattern) if p.is_file())

        plain_out = self.json_files_dir / gbw_subdir
        prop_out = self.json_files_dir / property_subdir
        plain_out.mkdir(parents=True, exist_ok=True)
        prop_out.mkdir(parents=True, exist_ok=True)

        plain_dests: list[Path] = []
        prop_dests: list[Path] = []

        for src in sources:
            name = src.name

            is_property = name.endswith(".property.json")
            if is_property:
                dst = prop_out / f"{self.prefix}_{name}"
                prop_dests.append(dst)
            else:
                # it's a .json from the glob, but not a .property.json
                dst = plain_out / f"{self.prefix}_{name}"
                plain_dests.append(dst)

            if not self.enabled:
                continue

            if dst.exists() and not overwrite:
                raise FileExistsError(f"JSON file exists (overwrite disabled): {dst}")

            shutil.copy2(src, dst)

        if self.enabled and not (plain_dests or prop_dests):
            raise FileNotFoundError(f"No JSON files found in {src_dir} (pattern={pattern!r})")

        return plain_dests, prop_dests


@pytest.fixture(scope="session")
def json_files_dir(request: pytest.FixtureRequest) -> Path:
    return Path(request.config.rootpath) / "tests" / "json_files"


@pytest.fixture
def json_files_exporter(request: pytest.FixtureRequest, json_files_dir: Path) -> JsonFilesExporter:
    if "json_files" not in request.node.keywords:
        pytest.fail("json_files_exporter is intended for tests marked with @pytest.mark.json_files")

    return JsonFilesExporter(
        json_files_dir=json_files_dir,
        prefix=request.node.name,  # json_file basename
        enabled=request.config.getoption("--update-json-files"),
    )
