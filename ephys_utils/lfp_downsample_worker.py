# This Python file uses the following encoding: utf-8
"""Runs ephys_utils/lfp_creation_dialog.py's create_lfp compute step
(ephys_utils/downsample_filter_LFP.downsample_filter_LFP) in its own
process. Invoked by that file's create_lfp via
gui_utils/subprocess_worker.py's run_json_subprocess -- mirrors samri/
samri_worker.py's --input/--output JSON-payload convention. Also works when
main_window.py's --lfp-downsample-worker sentinel re-invokes a frozen
build."""
import argparse
import json
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from ephys_utils.downsample_filter_LFP import downsample_filter_LFP


def _do_downsample(payload):
    """Pure logic behind create_lfp's old work() closure -- runs inside
    this subprocess, not the GUI process."""
    ds_data_file = downsample_filter_LFP(
        payload['raw_dir'], payload['dat_name'],
        num_channels=payload['num_channels'],
        sample_rate=payload['sample_rate'],
        cutoff=payload['cutoff'],
        stopband=payload['stopband'],
        filter_order=payload['filter_order'],
    )
    return {'ds_data_file': ds_data_file}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run the LFP downsample/filter step out-of-process')
    parser.add_argument('--input', required=True, help='Path to input .json payload')
    parser.add_argument('--output', required=True, help='Path to write result .json')
    args = parser.parse_args(argv)

    with open(args.input) as f:
        payload = json.load(f)

    result = _do_downsample(payload)

    with open(args.output, 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
