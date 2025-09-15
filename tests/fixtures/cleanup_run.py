import shutil
from pathlib import Path

import pytest


@pytest.fixture
def cleanup_run(request):
    yield
    run_path = Path(__file__).parent.parent / "RUN"
    if run_path.exists():
        if getattr(request.node, "rep_call", None) and request.node.rep_call.passed:
            shutil.rmtree(run_path)
            # shutil.rmtree(str(run_path))
        else:
            print(f"\nTest failed , RUN directory of failed test {run_path}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach test outcome reports (setup/call/teardown) to the item object."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
