# This Python file uses the following encoding: utf-8
"""Runs ephys/init_ephys.py's InitEphys.__init__ MRIDInfo.from_file call in
its own process. Invoked by that file via gui_utils/subprocess_worker.py's
run_json_subprocess -- mirrors samri/samri_worker.py's --input/--output
JSON-payload convention. Also works when main_window.py's
--mrid-info-worker sentinel re-invokes a frozen build."""
import argparse
import json
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from ephys.mrid_info import MRIDInfo


def _do_mrid_info(payload):
    """Pure logic behind the old run_off_thread(lambda: MRIDInfo.from_file(...))
    call -- runs inside this subprocess, not the GUI process. mrid_coordinates'
    values and totalatlasCoordinates_pkl's entries are numpy arrays on the
    dataclass; converted to plain lists here since neither crosses back as
    anything but JSON."""
    info = MRIDInfo.from_file(payload['filename'], payload['session_path'],
                               group_idx=payload['group_idx'])
    return {
        'mrid_tags': info.mrid_tags,
        'totalatlasCoordinates_pkl': [[a.tolist(), b.tolist()] for a, b in info.totalatlasCoordinates_pkl],
        'xml_group_idx': info.xml_group_idx,
        'mrid': info.mrid,
        'mrid_coordinates': {k: v.tolist() for k, v in info.mrid_coordinates.items()},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run MRIDInfo.from_file out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_mrid_info(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
