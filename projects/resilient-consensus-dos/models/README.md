# Original Simulink Model Files

The source package supplied for this project contains the following original Simulink files:

| Filename | Size | SHA-256 | Stored stop time |
|---|---:|---|---:|
| `withoutDOS.slx` | 29,325 bytes | `13557be4eb67170ab639cfc4b9c3bac4fa41a72ff4f903e6c8bb890fd680f12b` | 30 s |
| `withDOS.slx` | 34,031 bytes | `381e8ab8dbc72b6eb38342ae8e6b8395a380610272d820c970e8a9169fea2a1e` | 5 s |
| `RESILIENT.slx` | 35,148 bytes | `145e7a927674edb33f2949ac6e30d0d05c9e4ae9c9a5f095c5d8aba0f49a43db` | 10 s |

**Repository status:** the original binary model files are not yet present in this directory. Add the three source files here without renaming or modifying them. The SHA-256 values above provide an integrity check after upload.

The files in the supplied package were checked as ZIP archives, their embedded `simulink/stateflow.xml` files were parsed successfully, and five MATLAB Function block scripts were identified in each model. This verifies package readability and script extraction only; it does not prove that the models execute successfully in MATLAB/Simulink.

## Execution note

`withDOS.slx` and `RESILIENT.slx` contain a **From Workspace** block configured to read a base-workspace variable named `tuvar`. The original attack-signal data or script was not present in the supplied package. Restore the original signal before running these variants; do not substitute an arbitrary signal when claiming reproduction of the paper.

See [Reproducibility Notes](../docs/REPRODUCIBILITY.md) for the preflight check and validation requirements.
