# Examples for the ORCA Python Interface (OPI)

This folder contains example scripts and input files demonstrating how to use OPI with ORCA.

These examples serve **two purposes**:

- **Learning resource:** They show new users how to set up and run typical calculations with OPI.
- **Integration tests:** The same examples are executed by our test suite (see [`tests/examples`](../tests/examples)) to ensure that OPI's basic functionality and ORCA interface continue to work.

## Notes for Contributors

- If you modify an example, make sure the corresponding test still passes.
- To run an example manually, you can execute the corresponding script:

```bash
python example001.py
