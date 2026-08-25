# This Python file uses the following encoding: utf-8
"""Maintainer-only, one-off script: package the 5 raw atlas files (the
same ones paths_config.example.json's atlas_volume/atlas_labels/atlas_dwi/
atlas_template/atlas_mask point at) into a single tarball, for publishing
as a GitHub Release asset that mrid_utils/atlas_fetch.py downloads on
demand. NOT imported by the app itself -- run manually whenever the atlas
bundle needs to be (re)published.

Usage:
    python3 mrid_utils/build_atlas_bundle.py

Then, to (re-)publish (bump the tag, e.g. atlas-v2, if atlas-v1 already exists):
    gh release create atlas-v2 atlas_bundle/whs_sd_rat_raw_atlas.tar.gz \\
        --repo Neurotechnology-at-ETH-Zurich/IMPLAnT --title "WHS SD rat atlas (raw files)" \\
        --notes "Raw atlas files auto-fetched by mrid_utils/atlas_fetch.py"

...then paste the printed URL + sha256 into atlas_fetch.py's
ATLAS_BUNDLE_URL / ATLAS_BUNDLE_SHA256. (Currently pointing at the
atlas-v1 release already published there.)
"""
import hashlib
import os
import sys
import tarfile

# Running this as `python3 mrid_utils/build_atlas_bundle.py` puts mrid_utils/
# itself on sys.path, not the repo root -- so paths_config (which lives at
# the repo root) wouldn't be found without this, regardless of cwd.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paths_config import _paths

OUTPUT_DIR = "atlas_bundle"
OUTPUT_NAME = "whs_sd_rat_raw_atlas.tar.gz"

_ATLAS_FILE_KEYS = ('atlas_volume', 'atlas_labels', 'atlas_dwi', 'atlas_template', 'atlas_mask')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_NAME)

    missing = [
        _paths[key] for key in _ATLAS_FILE_KEYS
        if not os.path.exists(os.path.join(_paths['atlas_folder'], _paths[key]))
    ]
    if missing:
        raise SystemExit(
            f"Missing atlas file(s) under {_paths['atlas_folder']}: {missing}\n"
            "Update paths_config.json's atlas_folder to wherever your raw atlas "
            "files currently live before running this.")

    print(f"Packaging from: {_paths['atlas_folder']}")
    with tarfile.open(output_path, "w:gz") as tar:
        for key in _ATLAS_FILE_KEYS:
            filename = _paths[key]
            path = os.path.join(_paths['atlas_folder'], filename)
            print(f"  adding {filename} ({os.path.getsize(path) / 1e6:.1f} MB)")
            tar.add(path, arcname=filename)

    digest = hashlib.sha256()
    with open(output_path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(chunk)

    print(f"\nDone: {output_path} ({os.path.getsize(output_path) / 1e6:.1f} MB)")
    print(f"sha256: {digest.hexdigest()}")
    print("\nNext: publish this as a GitHub Release asset (see this file's docstring "
          "for the exact `gh release create` command), then paste the asset URL and "
          "the sha256 above into mrid_utils/atlas_fetch.py's ATLAS_BUNDLE_URL / "
          "ATLAS_BUNDLE_SHA256.")


if __name__ == "__main__":
    main()
