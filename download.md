---
title: Download
nav_order: 5
---

# Download

Pre-built standalone executables — no Python installation and no separate ANTs install required. Download the executable for your OS below and configure `paths_config.json` as described in [Configuration](configuration).

<div class="release-table" markdown="1">

| Version | Released | Linux | macOS (Apple Silicon) | Windows |
|:--|:--|:--:|:--:|:--:|
| **v0.2.0** | 2026 | [🐧 Download](https://github.com/Neurotechnology-at-ETH-Zurich/IMPLAnT/releases/download/v0.2.0/IMPLAnT-linux.zip){: .btn .btn-blue } | [🍎 Download](https://github.com/Neurotechnology-at-ETH-Zurich/IMPLAnT/releases/download/v0.2.0/IMPLAnT-macos.zip){: .btn .btn-blue } | *coming soon* |

</div>

{: .note }
The macOS build is for **Apple Silicon (M1/M2/M3+) only** — not Intel Macs, which need to [run from source](installation#running-from-source) or [build their own](installation#building-the-standalone-application) instead. It's also unsigned/not notarized, so the first launch needs a right-click → Open (or `xattr -cr` if macOS reports it as damaged after the download). Windows isn't available yet — no column to fill in until that build exists.

## Source code

```bash
git clone --recurse-submodules https://github.com/Neurotechnology-at-ETH-Zurich/IMPLAnT.git
```

All releases (including changelogs and older versions) are also browsable on the [GitHub Releases page](https://github.com/Neurotechnology-at-ETH-Zurich/IMPLAnT/releases).

## License

IMPLAnT is released under the [MIT License](https://github.com/Neurotechnology-at-ETH-Zurich/IMPLAnT/blob/main/LICENSE).
