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

        # Separate files by type
        prop_file = next((f for f in matching_files if f.name.endswith(".property.json")), None)
        gbw_file = next((f for f in matching_files if not f.name.endswith(".property.json")), None)

        if prop_file is None:
            raise FileNotFoundError(f"No .property.json file found for identifier {identifier}")
        if gbw_file is None:
            raise FileNotFoundError(f"No GBW JSON file found for identifier {identifier}")

        output_object = Output("test", version_check=False)
        output_object.property_json_file = prop_file
        output_object.gbw_json_files = [gbw_file]
        output_object.parse()
        return output_object

    return _create_instance


@pytest.fixture
def empty_output_object():
    return Output("empty", version_check=False)
