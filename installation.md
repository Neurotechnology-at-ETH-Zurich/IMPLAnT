---
title: Installation
nav_order: 2
---

# Installation
{: .no_toc }

1. TOC
{:toc}

## Requirements

- **OS**: Linux (tested on Ubuntu 24) or macOS (dependencies pinned for both). Pre-built releases are available for both Linux and **Apple Silicon** Macs (M1/M2/M3+) — see [Download](download); not Intel Macs, which need a from-source build instead (see [Building the standalone application](#building-the-standalone-application)). The macOS build is unsigned/not notarized, so the first launch needs a right-click → Open (or `xattr -cr` if macOS reports it as damaged after a transfer).
- **Python**: 3.10 (from source only)
- **ANTs**: required to build from source or to build the standalone executable yourself — **not** required just to run a pre-built release, its binaries are bundled in
- **ffprobe** (part of FFmpeg): required to run from source, for video frame-rate detection in the electrophysiology visualisation tab — **not** required for a pre-built release, it's bundled in the same way as ANTs
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

## Dependencies: ffprobe

IMPLAnT also uses **ffprobe** (part of FFmpeg) to read a video's frame rate/frame count in the electrophysiology visualisation tab's video player. This is separate from video *playback* itself, which goes through Qt's own bundled multimedia backend and needs nothing extra.

- **Running from source**: install FFmpeg via your OS package manager, e.g. `sudo apt install ffmpeg` (Ubuntu/Debian) or `brew install ffmpeg` (macOS) — this puts `ffprobe` on your `PATH`, which is all IMPLAnT needs.
- **Building the standalone executable yourself**: place a copy of the `ffprobe` binary at `IMPLAnT/ffmpeg/bin/ffprobe` (same convention as `ants/bin/` above; `MRID_GUI.spec` reads it from here at build time).
- **Downloading a pre-built release**: nothing to do, `ffprobe` is already bundled in.

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

Pre-built Apple Silicon and Linux executables are already published on the [Download](download) page — only build your own if you need an Intel Mac build, or a build from a specific commit.

1. Install ANTs and ffprobe as described above — build-time requirements only; `MRID_GUI.spec` bundles the specific ANTs tools and ffprobe the app calls straight into the build automatically.
2. Build the executable:

   ```bash
   pyinstaller MRID_GUI.spec
   ```

3. On Linux, the app is created at `dist/IMPLAnT`, ready to distribute as-is. On macOS, building also produces `dist/IMPLAnT.app`; it's unsigned (no Apple Developer ID certificate involved), so the first launch needs a right-click → Open (or `xattr -cr` if macOS still reports it as damaged/quarantined after being copied to another machine) — distributing it further would need signing and notarization.

---

Next: [configure the atlas, paths, and MRID library](configuration), or head straight to the [tutorials](tutorials).
