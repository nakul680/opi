# Changelog

## [2.0] - 2026-02-10

### Added 
- Added Pydantic output models for S,H,F,J and K integrals in #7.
- Added templates for bug reports, feature requests and pull requests in #4.
- Added function to access optimized structure easier from Output class in #10.
- Added `Output._safe_get()` function to search output tree in #10.
- Addition of functions in `Output` to check if geometry optimization and scf have converged in #12.
- Add parameters to `Output.parse()` function to control whether respective json file is parsed or not in #33.
- Enable use of ExtOPT wrappers in #30.
- Addition of `Output` getter functions for easier access to energies in #32.
- Added `Element.from_atomic_number()` to get corresponding `Element` from atomic number in #52.
- Added getters in `Output` for molecular orbitals in #56.
- Initial support for orca_plot, which allows plotting of molecular orbitals, densities and spin-densities in #60.
- Added getters for `Output` attributes in #83.
- Introduce `MOData` class to hold index and spin channel data in #83.
- Added support for multiple gbw files in #83.
- Add `atomic_number` to `Element` class in #93.
- Added `Output.print_graph()` that shows which fields in the output are populated in #84.
- Added class methods to initialize Structure class in #96:
  - `from_ase` : from Atoms object of ASE
  - `from_list`: from a list
  - `from_xyz_string`: to directly read xyz string
  - `from_trj_xyz`: reads multi xyz files and returns list of Structure objects.(#138)
- Added `get_version()` and `check_version()` to get ORCA version from main binary and return or check it against minimum
required version for OPI respectively in #112
- Add simple property function `Strucure.nelectrons` to count number of electrons in #117.
- Added `UserWarning` for if multiplicity in `Structure` and number of electrons are invalid in #127.
- Added `Structure.set_ls_multiplicity()` which selects lowest possible multiplicity in #127.
- Functions to check if multiplicity of given structure is possible have been added to `Structure` in #127.
- Added `Calculator.write_and_run()` to write the ORCA .inp file and execute the calculation in one go in #124.
- Add example tests using pytest in #137. These are marked by the marker "examples".
- Introduction of tests that require ORCA binaries in #137, these are marked by marker "ORCA".
- Users can now add an arbitrary variable to blocks which will be printed in the block along with the other variables with #61.
  - These arbitrary variables are stores in a dict that the users can add to, remove from or clear completely.
- `PropertyResults` and `GbwResults` objects can now be initialized from json files with #159.
- Introduction of OPI unit tests . These tests are marked with marker "unit".
  - Input-side unit tests are marked with marker "input"(#145).
  - Output-side unit tests are marked with marker "output".
- Added `Properties` class for reading (relative) energies from comment line of multi XYZ files in #151.
- Addition of DFT keywords to method block in #173.
- Added `IrMode` class for keeping IR data in #168.
- Addition of strict argument to `BaseStructureFile` in #189.
- `IntGroupEnd` class created to model certain attributes in blocks in #190.

### Fixed 
- Fixed the links on the tutorial start page in #2
- Fixed bug where `%moinp` block was printed without quotation marks around the path in #50.
- Fixed `nuc` attribute in nmr to include index 0 in #89.
- Type annotation for fragments to `StrictNonNegativeInt` in #90.
- Type annotation for `MayerPopulationAnalysis.nbondordersprint` changed to `StrictNonNegativeInt` in #99.
- Renamed `xyzfraglib` to `xzyfraglib` in `BlockFrag` in #98.
- Solved error using CPCM with epsilon= inf in #101.
- Fixed bug in `OrcaVersion` not recognizing '-f.x' tags in ORCA version string in #112.
- Fixed `opi.__version__` which would previously always show '0.0.0' in #122
- Fixed lookup of ORCA binaries on Windows in #123.
- Windows compatibility issues have been fixed in #134.
- Bug that reading of structures failed for empty lines at the end has been fixed with #138.
- Fixed inconsistent indexing in `Structure.add_atom()` with #152.
- Fixed inconsistency in return type of `_buffer` method in `Structure` in #151. Now it raises `EOFError` instead of returning None.
- Fixed error in formatting of `QMMM` block attributes in #190.
- Common ide configuration directories now added to .gitignore, preventing git from tracking them in #192.

## Changed
- Configuration of a path to OPENMPI is now optional in #17.
- `Element` enum is now case-insensitive with #52.
- `Input.get_structure()` now adds fragment IDs to the structure with argument `with_fragments` with #34.
- HOMO and LUMO getters now keep information about the index and mo channel in #83.
- `Output.gbw_json_file` is now a list of json files in #83.
- `Calculator` class now does ORCA binary version check by default with #112, but it can be turned off.
- Move create logic in `Output` from `init()` to `parse()` in #116.
- If ruff alters source code then nox exits with non-zero-status with #126.
- `Calculator.write_input()` now returns boolean that says whether an existing input has been overwritten in #124.
  - Overwriting existing input can be controlled using `force` argument.
- `Calculator.run()` now returns boolean that indicates whether the ORCA calculation terminated normally in #124.
- Allow variable suffixes when creating gbw json files with #147.
- Calculator.write_input() now delegates formatting to `Input.format_before_coords()` and `Input.format_after_coords()` with #155.
- `Output.parse()` now delegates parsing of gbw and property json files to `Output.parse_gbw()` and `Output.parse_property()` respectively with #172.
- `property_json_file` and `gbw_json_files` are now properties, allowing custom JSON file names to be set via setters with #172. 
Users should use new properties to read custom json files.
- Improved typing of the `_orca_environment` decorator using PEP 612 (`ParamSpec` and `Concatenate`) with #182, 
preserving function signatures for IDEs and type checkers.