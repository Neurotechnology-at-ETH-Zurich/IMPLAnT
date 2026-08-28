---
title: Installation
nav_order: 2
---

# Installation
{: .no_toc }

1. TOC
{:toc}

## Requirements

- **OS**: Linux (tested on Ubuntu 24) or macOS (dependencies pinned for both; from source only for now — no macOS standalone build yet)
- **Python**: 3.10 (from source only)
- **ANTs**: required to build from source or to build the standalone executable yourself — **not** required just to run a pre-built release, its binaries are bundled in
- **Internet connection**: needed the *first* time you open ephys data, start SAMRI registration, or start trajectory planning — IMPLAnT downloads and caches the ~1.3GB reference atlas automatically at that point (see [Configuration](configuration#atlas-files)). Not needed to just browse a 3D/4D MRI volume, and not needed again once the atlas is cached locally.

## Choose an option

- **[Download the release]({{ site.aux_links["IMPLAnT on GitHub"][0] }}/releases)** — no Python installation or separate ANTs install needed. Recommended for most users.
- **Run from source** — requires Python 3.10, all dependencies, and a local ANTs install.

## Dependencies: ANTs

IMPLAnT requires **ANTs** (Advanced Normalization Tools) for MRI registration. ANTs is not a Python package. Running from source, or building the standalone executable yourself, needs a local ANTs install; pre-built releases already bundle the specific ANTs tools they call, so if you're just downloading a release you can skip this section.

1. Download ANTs from the [ANTs releases page](https://github.com/ANTsX/ANTs/releases).
2. Place the ANTs binaries so the folder structure looks like this — the same layout whether you're running from source or building the standalone executable (`MRID_GUI.spec` reads its ANTs binaries from here at build time):

   ```
   IMPLAnT/
     ants/
       bin/
         antsRegistration
         antsApplyTransforms
         ...
   ```

## Running from source

1. Clone the repository, including its submodules (`electrode2geometry`, `rippl-AI`):

   ```bash
   git clone --recurse-submodules https://github.com/Neurotechnology-at-ETH-Zurich/IMPLAnT.git
   cd IMPLAnT
   ```

   If you already have a clone without them, fetch the submodules into it with:

   ```bash
   git submodule update --init --recursive
   ```

2. Create a Python 3.10 virtual environment and install dependencies into it:

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Install ANTs as described above.

4. Run the app:

   ```bash
   python main_window.py
   ```

## Building the standalone application

1. Install ANTs as described above — a build-time requirement only; `MRID_GUI.spec` bundles the specific ANTs tools the app calls straight into the build automatically.
2. Build the executable:

   ```bash
   pyinstaller MRID_GUI.spec
   ```

3. The app is created at `dist/IMPLAnT`, ready to distribute as-is.

---

Next: [configure the atlas, paths, and MRID library](configuration), or head straight to the [tutorials](tutorials).
