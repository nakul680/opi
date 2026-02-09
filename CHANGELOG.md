# Changelog

## [2.0] - 2026-02-10

### Added 
- Added Pydantic output models for S,H,F,J and K integrals.
- Added templates for bug reports, feature requests and pull requests.
- Added function to access optimized structure easier from Output class.
- Added `Output._safe_get()` function to search output tree 
- Addition of functions in `Output` to check if geometry optimization and scf have converged.
- Add parameters to `Output.parse()` function to control whether respective json file is parsed or not.
- Enable use of ExtOPT wrappers.
- Addition of `Output` getter functions for easier access to energies.
- Added `Element.from_atomic_number()` to get corresponding `Element` from atomic number.
- Added getters in `Output` for molecular orbitals
- Initial support for orca_plot, which allows plotting of molecular orbitals, densities and spin-densities.
- Added getters for `Output` attributes.
- Introduce `MOData` class to hold index and spin channel data.
- Added support for multiple gbw files.
- Add `atomic_number` to `Element` class
- Added `Output.print_graph()` that shows which fields in the output are populated.
- Added class methods to initialize Structure class:
  - `from_ase` : from Atoms object of ASE
  - `from_list`: from a list
  - `from_xyz_string`: to directly read xyz string
  - `from_trj_xyz`: reads multi xyz files and returns list of Structure objects
- Added `get_version()` and `check_version()` to get ORCA version from main binary and return or check it against minimum
required version for OPI respectively
- Add simple property function `Strucure.nelectrons` to count number of electrons.
- Added `UserWarning` for if multiplicity in `Structure` and number of electrons are invalid.
- Added `Structure.set_ls_multiplicity()` which selects lowest possible multiplicity.
- Functions to check if multiplicity of given structure is possible have been added to `Structure`.
- Added `Calculator.write_and_run()` to write the ORCA .inp file and execute the calculation in one go.
- Add example tests using pytest. These are marked by the marker "examples".
- Introduction of tests that require ORCA binaries, these are marked by marker "ORCA".
- Users can now add an arbitrary variable to blocks which will be printed in the block along with the other variables.
  - These arbitrary variables are stores in a dict that the users can add to, remove from or clear completely.
- `PropertyResults` and `GbwResults` objects can now be initialized from json files.
- Introduction of OPI unit tests . These tests are marked with marker "unit".
  - Input-side unit tests are marked with marker "input".
  - Output-side unit tests are marked with marker "output".
- Added `Properties` class for reading (relative) energies from comment line of multi XYZ files.
- Added `IrMode` class for keeping IR data.
- Addition of strict argument to `BaseStructureFile`.
- `IntGroupEnd` class created to model certain attributes in blocks.

### Fixed 
- Fixed the links on the tutorial start page.
- Fixed bug where `%moinp` block was printed without quotation marks around the path
- Fixed `nuc` attribute in nmr to include index 0.
- Type annotation for fragments to `StrictNonNegativeInt`.
- Type annotation for `MayerPopulationAnalysis.nbondordersprint` changed to `StrictNonNegativeInt`.
- Renamed `xyzfraglib` to `xzyfraglib` in `BlockFrag`.
- Solved error using CPCM with epsilon= inf
- Fixed bug in `OrcaVersion` not recognizing '-f.x' tags in ORCA version string.
- Fixed `opi.__version__` which would previously always show '0.0.0'
- Fixed lookup of ORCA binaries on Windows.
- Windows compatibility issues have been fixed.
- Bug that reading of structures failed for empty lines at the end has been fixed.
- Fixed inconsistent indexing in `Structure.add_atom()`.
- Fixed inconsistency in return type of `_buffer` method in `Structure`. Now it raises `EOFError` instead of returning None.
- Addition of DFT keywords to method block.
- Fixed error in formatting of `QMMM` block attributes.
- Common ide configuration directories now added to .gitignore, preventing git from tracking them.

## Changed
- Configuration of a path to OPENMPI is now optional.
- `Element` enum is now case-insensitive.
- `Input.get_structure()` now adds fragment IDs to the structure with argument with_fragments
- HOMO and LUMO getters now keep information about the index and mo channel.
- `Output.gbw_json_file` is now a list of json files.
- `Calculator` class now does ORCA binary version check by default, but it can be turned off.
- Move create logic in `Output` from `init()` to `parse()`.
- If ruff alters source code then nox exits with non-zero-status
- `Calculator.write_input()` now returns boolean that says whether an existing input has been overwritten.
  - Overwriting existing input can be controlled using `force` argument.
- `Calculator.run()` now returns boolean that indicates whether the ORCA calculation terminated normally.
- Allow variable suffixes when creating gbw json files.
- Calculator.write_input() now delegates formatting to `Input.format_before_coords()` and `Input.format_after_coords()`.
- `Output.parse()` now delegates parsing of gbw and property json files to `Output.parse_gbw()` and `Output.parse_property()` respectively.
- `property_json_file` and `gbw_json_files` are now properties, allowing custom JSON file names to be set via setters. 
Users should use new properties to read custom json files.
- Improved typing of the `_orca_environment` decorator using PEP 612 (`ParamSpec` and `Concatenate`), 
preserving function signatures for IDEs and type checkers.