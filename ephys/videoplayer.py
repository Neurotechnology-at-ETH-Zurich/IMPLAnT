# This Python file uses the following encoding: utf-8
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl
import subprocess
import json
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QMessageBox, QFileDialog
import scipy.io
from pymatreader import read_mat


class VideoPlayer:
    def __init__(self,MW):
        self.MW = MW

        self.MW.ui.spinBox_frame.editingFinished.connect(self.seek_frame)
        self.MW.ui.pushButton_videoPlay.clicked.connect(self.play_pause)

    def add_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Open Video File",
            "",
            "Video files (*.avi)"
        )

        #User cancelled
        if not file_path:
            return

        #pop up asking for the view if 4D data used
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Open Main File")
        msg_box.setText(f"Do you want to open the file \n {file_path}?")
        msg_box.addButton("Yes", QMessageBox.ActionRole)
        btn_no = msg_box.addButton("No, other Video", QMessageBox.ActionRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.ActionRole)
        msg_box.exec()
        if msg_box.clickedButton()==btn_cancel:
            return
        if msg_box.clickedButton()==btn_no:
            self.add_video()
            return

        ## initiate video class
        self.MW.ui.stackedWidget_video.setCurrentIndex(0)

        self.get_frame_rate(file_path)

        self.player = QMediaPlayer()
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.player.play()
        self.currently_play = True
        self.player.setVideoOutput(self.MW.ui.widget_video)

        self.synchronize_frames(file_path)

    def get_frame_rate(self,file_path):
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", file_path],
            capture_output=True, text=True
        )
        info = json.loads(result.stdout)
        stream = info["streams"][0]
        num, den = stream["r_frame_rate"].split("/")
        self.frame_rate = int(num) / int(den)
        self.MW.ui.spinBox_frame.setMaximum(int(stream["nb_frames"])) #total frames

    def play_pause(self):
        if self.currently_play:
            self.player.pause()
            self.currently_play = False
            icon = self.MW.style().standardIcon(QStyle.SP_MediaPause)
            self.MW.ui.pushButton_videoPlay.setIcon(icon)
        else:
            self.player.play()
            self.currently_play = True

            icon = self.MW.style().standardIcon(QStyle.SP_MediaPlay)
            self.MW.ui.pushButton_videoPlay.setIcon(icon)


    def seek_frame(self):
        frame = self.MW.ui.spinBox_frame.value()
        ms = int((frame / self.frame_rate) * 1000)
        self.player.setPosition(ms)

    def synchronize_frames(self,file_path):
        mat_path = file_path[:-4] + '.mat'
        mat = scipy.io.loadmat(mat_path,squeeze_me=True,struct_as_record=False)
        mat = read_mat(mat_path)
        print(mat,flush=True)
        samples_on_off = mat['position']['sample']

        #from samples to sth (each row is one frame)
        #'amplifier_sample_rate': 20000, 'video_sample_rate': 30

