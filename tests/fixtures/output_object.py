from pathlib import Path

import pytest

from opi.output.core import Output

JSON_DIR = Path(__file__).parent.parent / "json_files"


@pytest.fixture
def output_object_factory():
    def _create_instance(identifier):
        matching_files = list(JSON_DIR.rglob(f"*{identifier}*.json"))
        if len(matching_files) == 0:
            raise FileNotFoundError(f"No matching JSON files found in {JSON_DIR}")
        prop_file = matching_files[0]
        gbw_file = matching_files[1]

        output_object = Output("test", version_check=False)
        output_object.property_json_file = prop_file
        output_object.gbw_json_files = [gbw_file]
        output_object.parse()
        return output_object

    return _create_instance


@pytest.fixture
def empty_output_object():
    return Output("empty", version_check=False)
