# This Python file uses the following encoding: utf-8
"""
Standalone worker-subprocess dispatch, split out of main_window.py's top
(where these checks used to live inline) purely to get ~170 lines of
repetitive boilerplate out of that file -- no behavior change.

maybe_run_worker_and_exit() must be called as the very first thing
main_window.py does, before any GUI import (PySide6/VTK/SimpleITK etc.) --
each frozen (PyInstaller) build re-invokes its own exe with one of these
`--xxx-worker` flags to run a single heavy step in a clean subprocess
instead of on a BusyWorker QThread inside the already-loaded GUI process:
importing e.g. tensorflow into the SAME process as the already-loaded GUI
stack segfaults (confirmed) -- checking and exiting here, before any of
that GUI stack is ever imported, keeps this process completely clean of
Qt/VTK. See each `main_window.py` call site referenced below for why that
particular step wants to run out-of-process.

This module must not import anything GUI-related at module level either,
for the same reason -- each branch below does its own scoped import.
"""
import os
import sys


def maybe_run_worker_and_exit():
    # ephys/init_ephys.py's _run_ripple_detection.
    if len(sys.argv) > 1 and sys.argv[1] == '--ripple-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, os.path.join(_worker_base_dir, 'rippl-AI'))
        import run_rippl
        run_rippl.main(sys.argv[2:])
        sys.exit(0)

    # SAMRI's bruker2bids/registration/biascorrection pipelines (see
    # samri/samri_main.py's _run_worker_subprocess): runs them in a separate
    # process instead of BusyWorker's QThread, so a stuck/OOMing registration
    # can be killed without taking the whole GUI down, and so the GUI
    # process's memory footprint stays decoupled from antsRegistration's
    # (which has driven single runs to ~38GB RSS).
    if len(sys.argv) > 1 and sys.argv[1] == '--samri-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from samri import samri_worker
        samri_worker.main(sys.argv[2:])
        sys.exit(0)

    # The trajectory-planning resample step (see main_window.py's
    # _run_trajectory_worker_subprocess): keeps a heavy first-time 25/50um
    # resample off the GUI process's memory footprint and killable
    # independently, same reasoning as --samri-worker above.
    if len(sys.argv) > 1 and sys.argv[1] == '--trajectory-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from trajectory_planning import trajectory_worker
        trajectory_worker.main(sys.argv[2:])
        sys.exit(0)

    # trajectory_planning/registration.py's register_to_main_img (see
    # gui_utils/subprocess_worker.py's run_json_subprocess and
    # trajectory_planning/registration_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--trajectory-registration-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from trajectory_planning import registration_worker
        registration_worker.main(sys.argv[2:])
        sys.exit(0)

    # gui_utils/buttons_gui_structural.py's resample100um/resample25um (see
    # file_handling/resample_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--resample-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from file_handling import resample_worker
        resample_worker.main(sys.argv[2:])
        sys.exit(0)

    # gui_utils/buttons_gui_structural.py's _start_registration (see
    # core/structural_registration_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--structural-registration-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from core import structural_registration_worker
        structural_registration_worker.main(sys.argv[2:])
        sys.exit(0)

    # ephys/init_ephys.py's run_hierarchical_clustering (see
    # ephys_utils/clustering_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--clustering-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from ephys_utils import clustering_worker
        clustering_worker.main(sys.argv[2:])
        sys.exit(0)

    # ephys_utils/all_channels_spectrogram.py's ripple-triggered average (see
    # ephys_utils/ripple_spec_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--ripple-spec-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from ephys_utils import ripple_spec_worker
        ripple_spec_worker.main(sys.argv[2:])
        sys.exit(0)

    # ephys_utils/lfp_creation_dialog.py's create_lfp (see
    # ephys_utils/lfp_downsample_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--lfp-downsample-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from ephys_utils import lfp_downsample_worker
        lfp_downsample_worker.main(sys.argv[2:])
        sys.exit(0)

    # gui_utils/buttons_gui_time_series.py's activate_get_gaussian_analysis
    # (see core/gaussian_centers_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--gaussian-centers-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from core import gaussian_centers_worker
        gaussian_centers_worker.main(sys.argv[2:])
        sys.exit(0)

    # ephys/init_ephys.py's InitEphys.__init__ MRIDInfo.from_file call (see
    # ephys/mrid_info_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--mrid-info-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from ephys import mrid_info_worker
        mrid_info_worker.main(sys.argv[2:])
        sys.exit(0)

    # ephys/init_ephys.py's _run_theta_detection (see
    # ephys_utils/theta_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--theta-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from ephys_utils import theta_worker
        theta_worker.main(sys.argv[2:])
        sys.exit(0)

    # ephys/init_ephys.py's _load_spike_sorting_file (see
    # ephys_utils/spike_sorting_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--spike-sorting-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from ephys_utils import spike_sorting_worker
        spike_sorting_worker.main(sys.argv[2:])
        sys.exit(0)

    # ephys/visualisation3D.py's create_atlas_region_file (see
    # ephys/atlas_region_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--atlas-region-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from ephys import atlas_region_worker
        atlas_region_worker.main(sys.argv[2:])
        sys.exit(0)

    # trajectory_planning/rendering_mri.py's DWI load (see
    # trajectory_planning/dwi_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--dwi-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from trajectory_planning import dwi_worker
        dwi_worker.main(sys.argv[2:])
        sys.exit(0)

    # trajectory_planning_3d/window.py's _rebuild_background_mesh (see
    # trajectory_planning_3d/background_mesh_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--background-mesh-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from trajectory_planning_3d import background_mesh_worker
        background_mesh_worker.main(sys.argv[2:])
        sys.exit(0)

    # intraoperative/mri_preview.py's _render (see
    # intraoperative/mri_shell_worker.py).
    if len(sys.argv) > 1 and sys.argv[1] == '--mri-shell-worker':
        _worker_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _worker_base_dir)
        from intraoperative import mri_shell_worker
        mri_shell_worker.main(sys.argv[2:])
        sys.exit(0)
