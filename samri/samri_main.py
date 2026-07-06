# import samri
import nipype.interfaces.ants.registration as _nr_reg
_orig_format = _nr_reg.Registration._format_registration

def _patched_format_registration(self):
    cmd = _orig_format(self)
    cmd = cmd.replace(", NULL ]", " ]")
    import re
    cmd = re.sub(r"--masks \[ NULL \]\s*", "", cmd)
    cmd = re.sub(r"--masks \[ (\S+) \]", r"--masks \1", cmd)
    return cmd

_nr_reg.Registration._format_registration = _patched_format_registration

from samri.samri.pipelines.reposit import bru2bids
from samri.samri.pipelines.preprocess import structural,biascorrect_only
import os
import shutil
from subprocess import call
import samri.data_fetcher as data_fetcher
import sys
import glob
import json
import numpy as np
from PySide6 import QtWidgets
import pandas as pd
import SimpleITK as sitk
from file_handling.loader import FileLoader
from PySide6.QtWidgets import QMessageBox

_base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else _base_dir
_config_path = os.path.join(_exe_dir, 'paths_config.json')
if not os.path.exists(_config_path):
    _config_path = os.path.join(_base_dir, 'paths_config.example.json')
with open(_config_path) as _f:
    _paths = json.load(_f)

def _resolve_ants_bin(raw):
    if os.path.isabs(raw):
        return raw
    if getattr(sys, 'frozen', False):
        # check next to executable (dist/ants/bin), then one level up (project root ants/bin)
        exe_dir = os.path.dirname(sys.executable)
        candidates = [os.path.join(exe_dir, raw), os.path.join(os.path.dirname(exe_dir), raw)]
    else:
        candidates = [os.path.join(_base_dir, raw)]
    return next((c for c in candidates if os.path.isdir(c)), candidates[0])

class InitSAMRI:
    def __init__(self,samri_input):
        _ANTS_BIN = _resolve_ants_bin(_paths['ants_bin'])
        if os.path.isdir(_ANTS_BIN) and _ANTS_BIN not in os.environ.get("PATH", "").split(":"):
            os.environ["PATH"] = _ANTS_BIN + ":" + os.environ.get("PATH", "")
        os.environ["ANTSPATH"] = _ANTS_BIN

        self.start_bruker2_bids(samri_input)

    def start_bruker2_bids(self,samri_input):
        server = samri_input['server']
        password = samri_input['password']
        self.animal_id = samri_input['animal_id']

        # Enables bru2bids
        bids_flag = samri_input['bids_flag'] #True

        # Raw data to bids conversion
        raw_base = samri_input['raw_base'] + self.animal_id
        if not samri_input['fetch']:
            self.bids_base = samri_input['raw_base'] + self.animal_id
            return self.bids_base
        if not os.path.exists(raw_base):
            os.makedirs(raw_base)

        self.bids_base = samri_input['raw_base'] + self.animal_id
        call(['rm','-rf',raw_base+'/.DS_Store'])
        #call(['chmod', '-R', 'u+rwX', raw_base]) # every new file is writeable

        #A = get_data_selection(raw_base)
        data_fetcher.main(server=server, password=password, local_path=raw_base, animal_id=self.animal_id,local_fodler=samri_input['raw_base'])

        if bids_flag:
            # for file in bids_base:
            exclude_sessions = [""]
        if samri_input['exclude_existing'] and os.path.exists(self.bids_base):
            if os.path.exists(self.bids_base+"/bids/sub-"+self.animal_id):
                #if os.path.exists(self.bids_base+"/bids/sub-"+self.animal_id):
                for file in os.listdir(self.bids_base+"/bids/sub-"+self.animal_id):
                    filename = os.fsdecode(file)
                    if filename.startswith("ses-"):
                        exclude_sessions.append(filename.split("ses-")[-1])

        bru2bids(raw_base,
                #functional_match={"acquisition": ["geEPI"]},
                # structural_match={"acquisition": ["T2starMapMGE"]},
                structural_match={"acquisition": ["TurboRARE", "UTE","TOF", "T1Flash", "T2TurboRARE", "T2TurboRAREhighRes", "T2MapMSME", "RAREInvRec", "TurboRARE3D", "T2starMapMGE"]},
                out_base=self.bids_base,
                exclude={"session": exclude_sessions},
                keep_work=True,
                )

        # Run Diagnostics
        ##diagnose(self.bids_base+"/bids/sub-"+self.animal_id) - not working: wrong mach_regex?

        return self.bids_base


    def biascorrection(self,samri_input):
        # Enables registering
        #base_path= samri_input['base_path'] #"/Users/mri_registration/SAMRI/samri_output/"
        #working_session = samri_input['working_session']
        #register = samri_input['register'] #False

        # Registers post-op images to pre-op images
        #presurgery = samri_input['presurgery'] #False
        # Enables elastic registering
        #elastic = samri_input['elastic'] #True
        register_key = samri_input['register_key'] #["TurboRARE"]
        #num_threads = samri_input['num_threads'] #8
        tasks = samri_input['tasks'] #["coronal"]

        # Sessions to be excluded
        sessions = [""]
        for file in os.listdir(self.bids_base+"/bids/sub-"+self.animal_id):
            filename = os.fsdecode(file)
            if filename.startswith("ses-"):
                if filename.split("ses-")[-1] != samri_input['working_session'][0]:
                    sessions.append(filename.split("ses-")[-1])

        atlas = os.path.join(samri_input['atlas_folder'], _paths['atlas_template'])
        atlas_mask = []
        if samri_input['atlas_mask']:
            atlas_mask = os.path.join(samri_input['atlas_folder'], _paths['atlas_mask'])

        filepath = biascorrect_only(bids_base=self.bids_base+'/bids',
            template=atlas,
            debug=True,
            exclude={"session": sessions},
            functional_match={},
            keep_work=True,
            n_jobs=False,
            n_jobs_percentage=0.8,
            out_base=self.bids_base+'/results',
            registration_mask=atlas_mask,
            sessions=[],
            structural_match={"acq": register_key, "task": tasks, "type": ["anat"]},
            subjects=[],
            workflow_name='generic',
            #enforce_dummy_scans=DUMMY_SCANS,
        )

        return filepath


    def start_registration(self,samri_input):
        ##


        # Enables registering
        register = samri_input['register'] #False

        # Registers post-op images to pre-op images
        presurgery = samri_input['presurgery'] #False
        # Enables elastic registering
        elastic = samri_input['elastic'] #True
        register_key = samri_input['register_key'] #["TurboRARE"]
        num_threads = samri_input['num_threads'] #8
        tasks = samri_input['tasks'] #["coronal"]

        # Sessions to be excluded
        sessions = [""]
        for file in os.listdir(self.bids_base+"/bids/sub-"+self.animal_id):
            filename = os.fsdecode(file)
            if filename.startswith("ses-"):
                if filename.split("ses-")[-1] != samri_input['working_session'][0]:
                    sessions.append(filename.split("ses-")[-1])

        # Moving image mask
        moving_img_mask_path = []
        if samri_input['moving_mask']:
            moving_img_mask_path = samri_input['moving_img_mask_name']

        atlas = os.path.join(samri_input['atlas_folder'], _paths['atlas_template'])
        atlas_mask = []
        if samri_input['atlas_mask']:
            atlas_mask = os.path.join(samri_input['atlas_folder'], _paths['atlas_mask'])

        if register:
            filepath = structural(
                bids_base=self.bids_base+'/bids',
                template=atlas,
                out_base=self.bids_base+'/results',
                presurgery=presurgery,
                structural_match={"acq": register_key, "task": tasks, "type": ["anat"]},
                debug=True,
                keep_work=True,
                elastic=elastic,
                moving_img_mask=moving_img_mask_path,
                registration_mask=atlas_mask,
                num_threads=num_threads,
                reference_template=atlas,
                # presurgery_template=presurgery_atlas,
                exclude={"session": sessions}
                )


            #copy h5 file to registration folder
            fixedImg = sitk.ReadImage(os.path.join(samri_input['atlas_folder'], _paths['atlas_volume']))
            movingImg = sitk.ReadImage(filepath)
            csv_path = f"{self.bids_base}/results/generic_work/data_selection.csv"
            df = pd.read_csv(csv_path, index_col=0)
            original_path = f"{'_'.join(filepath.split('_')[:-1])}.nii.gz"
            print(df['path'],flush=True)
            print('op',filepath,original_path,flush=True)
            idx = df.loc[df['path'] == filepath].index[0] #original_path?
            transformPath = f"{self.bids_base}/results/generic_work/_ind_type_{idx}/s_register/output_Composite.h5"
            transform_moving2fixed = sitk.ReadTransform(transformPath)
            size = fixedImg.GetSize()
            fixed_px = []
            moving_px = []
            for x in range(size[0]):
                for y in range(size[1]):
                    for z in range(size[2]):
                        fixed_px.append([x,y,z])
                        fixedpnt = fixedImg.TransformIndexToPhysicalPoint([x,y,z]) #mm
                        movingpnt = transform_moving2fixed.TransformPoint(fixedpnt) #mri
                        idx_mri = movingImg.TransformPhysicalPointToIndex(movingpnt) #px
                        moving_px.append(idx_mri)

            #save files
            folder = f"{self.bids_base}/bids/sub-{self.animal_id}/ses-{samri_input['working_session'][0]}/registration"
            os.makedirs(folder, exist_ok=True)
            np.save(f"{folder}/fixed_img-indeces.npy", np.array(fixed_px))
            np.save(f"{folder}/moving_img_resampled25um-indeces.npy", np.array(moving_px))
            shutil.copy(transformPath, f"{folder}/output_Composite.h5")


        return filepath


    def visualize_results(self,MW,logging):

        MW.ui.stackedWidget_3d.setVisible(False)

        path_main = os.path.join(_paths['atlas_folder'], _paths['atlas_volume'])
        MW.restart_gui(path_main, full_restart=False,label_file=True,data_view='coronal')
        MW.ui.dockWidget_ephys.setVisible(False)
        MW.ui.textEdit_SAMRI_reg.setVisible(True)

        #add image
        csv_path = f"{self.bids_base}/results/generic_work/data_selection.csv"
        df = pd.read_csv(csv_path, index_col=0)
        idx = df.loc[df['path'] == self.output_filepath].index[0]
        img_path = f"{self.bids_base}/results/generic_work/_ind_type_{idx}/s_warp/{os.path.basename(self.output_filepath)}"

        if MW.ui.comboBox_movingimg.findText(os.path.basename(img_path)) == -1:
            MW.FileLoader = FileLoader(MW)
            MW.FileLoader.is_4d = False #3d file
        else:
            MW.FileLoader.layer_index += 1
        MW.FileLoader.initialize_file(img_path,MW.FileLoader.layer_index,'coronal',0)
        MW.ui.comboBox_movingimg.addItem(os.path.basename(img_path))
        MW.LoadMRI.movingimg_filename.append(img_path)
        MW.LoadMRI.combo_Regimgname = MW.ui.comboBox_movingimg

        logging.info("SAMRI finished")



class SAMRI_InputDialog:
    def __init__(self, MW,parent=None):
        self.MW = MW
        self.raw_base = self.MW.ui.lineEdit_rawBase
        self.raw_base.setText(_paths['raw_base'])
        self.raw_base.textChanged.connect(self.check_rawbase)
        self.MW.ui.pushButton_browse.clicked.connect(self.browse_path)

        bruker_info_path = os.path.join(_base_dir, 'samri', 'bruker_info.json')
        bruker_info = {}
        if os.path.exists(bruker_info_path):
            with open(bruker_info_path) as f:
                bruker_info = json.load(f)
        self.server       = self.MW.ui.lineEdit_server
        self.server.setText(bruker_info.get("server", ""))
        self.password     = self.MW.ui.lineEdit_password
        self.password.setText(bruker_info.get("password", ""))
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.bids_flag = self.MW.ui.checkBox_bidsflag
        self.bids_flag.setChecked(True)

        self.animal_id = self.MW.ui.lineEdit_animalid
        self.animal_id.textChanged.connect(self.check_rawbase)

        self.MW.ui.pushButton_fetch.clicked.connect(lambda: self.get_values(fetch=True))
        self.MW.ui.pushButton_continue.clicked.connect(lambda: self.get_values(fetch=False))
        self.MW.ui.pushButton_re_fetch.clicked.connect(lambda: self.get_values(fetch=True,exclude_existing=False))


    def browse_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder", self.raw_base.text())
        if path:
            self.raw_base.setText(path)

    def check_rawbase(self):
        if os.path.exists(self.raw_base.text() + self.animal_id.text()):
            self.MW.ui.pushButton_continue.setEnabled(True)
            self.MW.ui.pushButton_re_fetch.setEnabled(True)
        else:
            self.MW.ui.pushButton_continue.setEnabled(False)
            self.MW.ui.pushButton_re_fetch.setEnabled(False)

    def get_values(self,fetch=True,exclude_existing=True):
        """Call after exec() to retrieve all values."""
        samri_input = {
            "server":               self.server.text(),
            "password":             self.password.text(),
            "animal_id":            self.animal_id.text(),
            "bids_flag":            self.bids_flag.isChecked(),
            "raw_base":             self.raw_base.text(),
            "fetch":                fetch,
            "exclude_existing":     exclude_existing,
        }
        self.MW.fetch_data(samri_input)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = SAMRI_InputDialog()


class SAMRI_InputDock:
    def __init__(self, MW,parent=None):
        self.MW = MW
        self.ui = MW.ui

        self.connect_buttons()


    def connect_buttons(self):
        self.ui.lineEdit_animalID.setText(f"Animal ID: {self.MW.Samri.animal_id}")
        self.ui.lineEdit_bru2_path.setText(_paths['raw_base'])
        self.ui.lineEdit_base_path.setText(_paths['raw_base'])
        self.ui.lineEdit_atlas_path.setText(_paths['atlas_folder'])

        self.ui.pushButton_browseBru2.clicked.connect(lambda: self.browse_path(self.ui.lineEdit_bru2_path))
        self.ui.pushButton_browseBase.clicked.connect(lambda: self.browse_path(self.ui.lineEdit_base_path))
        self.ui.pushButton_browseAtlas.clicked.connect(lambda: self.browse_path(self.ui.lineEdit_atlas_path))
        self.ui.pushButton_browseMov.clicked.connect(lambda: self.browse_path(self.ui.lineEdit_movMask,file=True))

        # fill comboboxes
        if not os.path.exists(self.MW.Samri.bids_base+"/bids/sub-"+self.MW.Samri.animal_id):
            #pop up asking for the view if 4D data used
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Animal ID not found")
            msg_box.setText("NO such Animal ID found!")
            msg_box.addButton("OK", QMessageBox.ActionRole)
            msg_box.exec()
            return
        for file in os.listdir(self.MW.Samri.bids_base+"/bids/sub-"+self.MW.Samri.animal_id):
            filename = os.fsdecode(file)
            if filename.startswith("ses-"):
                self.ui.comboBox_working_session.addItem(filename.split("ses-")[-1])

        self.ui.comboBox_register_key.addItems(["TurboRARE", "UTE", "TOF", "T1Flash", "T2TurboRARE",
                                     "T2TurboRAREhighRes", "T2MapMSME", "RAREInvRec",
                                     "TurboRARE3D", "T2starMapMGE"])

        self.ui.comboBox_tasks.addItems(["coronal", "sagittal", "axial"])

        #fill spinbox
        self.ui.spinBox_num_threads.setValue(6) #int(os.cpu_count()-7)) #25
        self.ui.spinBox_num_threads.setRange(1, 8) #29

        # fill moving mask text line
        self.update_mov_mask_path()

        self.ui.pushButton_createMovMask.clicked.connect(self.create_mov_mask)
        self.ui.buttonBox.accepted.connect(self.get_values)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.ui.checkBox_mov_mask.toggled.connect(self.ui.pushButton_createMovMask.setEnabled)
        self.ui.checkBox_mov_mask.toggled.connect(self.ui.pushButton_browseMov.setEnabled)
        self.ui.checkBox_mov_mask.toggled.connect(self.ui.lineEdit_movMask.setEnabled)
        self.ui.pushButton_createMovMask.setEnabled(self.ui.checkBox_mov_mask.isChecked())

        self.ui.comboBox_working_session.currentIndexChanged.connect(self.update_mov_mask_path)
        self.ui.comboBox_register_key.currentIndexChanged.connect(self.update_mov_mask_path)

        self.ui.checkBox_biascorrection.toggled.connect(
            lambda checked: self.ui.checkBox_registration.setChecked(False) if checked else None
        )

        self.ui.checkBox_registration.toggled.connect(
            lambda checked: self.ui.checkBox_biascorrection.setChecked(False) if checked else None
        )


    def create_mov_mask(self):
        path = self.matches[0]
        self.MW.restart_gui(path, full_restart=False,label_file=False,data_view='coronal')
        self.ui.dockWidget_ephys.setVisible(False)
        self.ui.textEdit_SAMRI_reg.setVisible(True)
        self.MW.ButtonsGUI_3D.initialize_segmentation(samri=True)

    def update_mov_mask_path(self):
        folder = (self.MW.Samri.bids_base + "/bids/sub-" + self.MW.Samri.animal_id
                  + "/ses-" + self.ui.comboBox_working_session.currentText() + "/anat")
        key = self.ui.comboBox_register_key.currentText()
        self.matches = [p for p in glob.glob(os.path.join(folder, f"*-{key}_*.nii.gz")) if '-mask' not in os.path.basename(p)]
        mov_mask_path = self.matches[0][:-7] + "-mask.nii.gz"
        if os.path.exists(mov_mask_path):
            self.ui.lineEdit_movMask.setText(mov_mask_path)
        else:
            self.ui.lineEdit_movMask.setText('No mask found: Browse or Create Mask')

    def browse_path(self, text_edit,file=False):
        if file:
            folder = (self.MW.Samri.bids_base + "/bids/sub-" + self.MW.Samri.animal_id
                      + "/ses-" + self.ui.comboBox_working_session.currentText() + "/anat")
            path, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Select Mask", folder ,"NIfTI files (*.nii.gz)")
        else:
            path = QtWidgets.QFileDialog.getExistingDirectory(self.MW, "Select Folder", text_edit.toPlainText())
        if path:
            text_edit.setText(path)

    def get_values(self):
        """Call after exec() to retrieve all values."""
        samri_input = {}
        samri_input["bru2_path"] =          self.ui.lineEdit_bru2_path.toPlainText()
        samri_input["base_path"] =          self.ui.lineEdit_base_path.toPlainText()
        samri_input["working_session"] =    [self.ui.comboBox_working_session.currentText()]
        samri_input["register_key"]=        [self.ui.comboBox_register_key.currentText()]
        samri_input["tasks"]=               [self.ui.comboBox_tasks.currentText()]
        samri_input["num_threads"]=         self.ui.spinBox_num_threads.value()
        samri_input["moving_img_mask_name"]=self.ui.lineEdit_movMask.toPlainText()
        samri_input["register"]=            self.ui.checkBox_registration.isChecked()
        samri_input["presurgery"]=          self.ui.checkBox_presurgery.isChecked()
        samri_input["elastic"]=             self.ui.checkBox_elastic.isChecked()
        samri_input["atlas_folder"]=        self.ui.lineEdit_atlas_path.toPlainText()
        samri_input["moving_mask"]=         self.ui.checkBox_mov_mask.isChecked()
        samri_input["atlas_mask"]=          self.ui.checkBox_atlasmask.isChecked()
        samri_input["biascorrection"]=      self.ui.checkBox_biascorrection.isChecked()

        self.MW.start_registration(samri_input)


    def reject(self):
        return None
