# Original Simulink Model Files

The source archive supplied for this project contains these original files:

| Filename | SHA-256 | Stored stop time |
|---|---|---:|
| withoutDOS.slx | 13557be4eb67170ab639cfc4b9c3bac4fa41a72ff4f903e6c8bb890fd680f12b | 30 s |
| withDOS.slx | 381e8ab8dbc72b6eb38342ae8e6b8395a380610272d820c970e8a9169fea2a1e | 5 s |
| RESILIENT.slx | 145e7a927674edb33f2949ac6e30d0d05c9e4ae9c9a5f095c5d8aba0f49a43db | 10 s |

**Repository upload status:** the three original SLX binaries have been extracted from the prepared ZIP archive and independently checked against the SHA-256 values above. They are not yet committed to this GitHub folder because the connected GitHub file-writing action accepts UTF-8 text files only, not binary SLX uploads. Upload the three originals into this `models/` directory to make the case study fully downloadable. A GitHub Actions integrity workflow is configured to verify their hashes when the binaries are added. The documentation intentionally does not link to missing model binaries.

Do not rename or edit the originals before uploading. The hashes above can be used to verify file integrity after upload.

## Execution note

withDOS.slx and RESILIENT.slx require a workspace variable named tuvar, which was not included in the source archive. See [Reproducibility Notes](../docs/REPRODUCIBILITY.md).
