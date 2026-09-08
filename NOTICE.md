# Third-party licenses

IMPLAnT itself is licensed under the MIT License (see [LICENSE](LICENSE)).

It vendors one third-party project under a different, copyleft license:

## SAMRI (`samri/`)

- **Source**: https://github.com/IBT-FMI/SAMRI
- **Author**: Horea Christian
- **License**: GNU General Public License v3.0 (see [`samri/LICENSE`](samri/LICENSE))

`samri/` is used for MRI registration (SAMRI/ANTs pipeline) and is bundled directly
into the standalone `dist/IMPLAnT` executable (see `MRID_GUI.spec`). Because SAMRI
is GPLv3-licensed, the combined standalone build is subject to GPLv3's terms,
notwithstanding the MIT license that covers the rest of this repository's own code.
