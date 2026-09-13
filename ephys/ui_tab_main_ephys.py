# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tab_main_ephys.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox, QApplication,
    QComboBox, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSlider, QSpinBox,
    QStackedWidget, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_tab_ephys(object):
    def setupUi(self, tab_ephys):
        if not tab_ephys.objectName():
            tab_ephys.setObjectName(u"tab_ephys")
        tab_ephys.resize(898, 584)
        self.gridLayout = QGridLayout(tab_ephys)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textEdit_ephys = QLabel(tab_ephys)
        self.textEdit_ephys.setObjectName(u"textEdit_ephys")
        self.textEdit_ephys.setMinimumSize(QSize(300, 100))
        self.textEdit_ephys.setMaximumSize(QSize(300, 16777215))
        self.textEdit_ephys.setWordWrap(True)

        self.gridLayout.addWidget(self.textEdit_ephys, 0, 0, 1, 1)

        self.tabWidget_ephys = QTabWidget(tab_ephys)
        self.tabWidget_ephys.setObjectName(u"tabWidget_ephys")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_46 = QGridLayout(self.tab_4)
        self.gridLayout_46.setObjectName(u"gridLayout_46")
        self.groupBox_37 = QGroupBox(self.tab_4)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.groupBox_37.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_74 = QGridLayout(self.groupBox_37)
        self.gridLayout_74.setObjectName(u"gridLayout_74")
        self.spinBox_y_ephys = QSpinBox(self.groupBox_37)
        self.spinBox_y_ephys.setObjectName(u"spinBox_y_ephys")
        self.spinBox_y_ephys.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_ephys.setReadOnly(True)
        self.spinBox_y_ephys.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_y_ephys.setMinimum(1)
        self.spinBox_y_ephys.setMaximum(1000)

        self.gridLayout_74.addWidget(self.spinBox_y_ephys, 0, 2, 1, 1)

        self.spinBox_x_ephys = QSpinBox(self.groupBox_37)
        self.spinBox_x_ephys.setObjectName(u"spinBox_x_ephys")
        self.spinBox_x_ephys.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_ephys.setReadOnly(True)
        self.spinBox_x_ephys.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_x_ephys.setMinimum(1)
        self.spinBox_x_ephys.setMaximum(1000)

        self.gridLayout_74.addWidget(self.spinBox_x_ephys, 0, 1, 1, 1)

        self.spinBox_z_ephys = QSpinBox(self.groupBox_37)
        self.spinBox_z_ephys.setObjectName(u"spinBox_z_ephys")
        self.spinBox_z_ephys.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_ephys.setReadOnly(True)
        self.spinBox_z_ephys.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_z_ephys.setMinimum(1)
        self.spinBox_z_ephys.setMaximum(1000)

        self.gridLayout_74.addWidget(self.spinBox_z_ephys, 0, 3, 1, 1)


        self.gridLayout_46.addWidget(self.groupBox_37, 1, 0, 1, 1)

        self.frame_32 = QFrame(self.tab_4)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setEnabled(True)
        self.frame_32.setMinimumSize(QSize(0, 200))
        self.frame_32.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_32.setFrameShape(QFrame.NoFrame)
        self.gridLayout_68 = QGridLayout(self.frame_32)
        self.gridLayout_68.setSpacing(0)
        self.gridLayout_68.setObjectName(u"gridLayout_68")
        self.gridLayout_68.setContentsMargins(4, 4, 4, 4)
        self.groupBox_6 = QGroupBox(self.frame_32)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_169 = QGridLayout(self.groupBox_6)
        self.gridLayout_169.setObjectName(u"gridLayout_169")
        self.groupBox_8 = QGroupBox(self.groupBox_6)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_171 = QGridLayout(self.groupBox_8)
        self.gridLayout_171.setObjectName(u"gridLayout_171")
        self.horizontalSlider_OtherRegions = QSlider(self.groupBox_8)
        self.horizontalSlider_OtherRegions.setObjectName(u"horizontalSlider_OtherRegions")
        self.horizontalSlider_OtherRegions.setMinimum(0)
        self.horizontalSlider_OtherRegions.setMaximum(100)
        self.horizontalSlider_OtherRegions.setSingleStep(0)
        self.horizontalSlider_OtherRegions.setOrientation(Qt.Horizontal)

        self.gridLayout_171.addWidget(self.horizontalSlider_OtherRegions, 0, 0, 1, 1)


        self.gridLayout_169.addWidget(self.groupBox_8, 1, 1, 1, 1)

        self.groupBox_9 = QGroupBox(self.groupBox_6)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_172 = QGridLayout(self.groupBox_9)
        self.gridLayout_172.setObjectName(u"gridLayout_172")
        self.horizontalSlider_Background = QSlider(self.groupBox_9)
        self.horizontalSlider_Background.setObjectName(u"horizontalSlider_Background")
        self.horizontalSlider_Background.setMaximum(100)
        self.horizontalSlider_Background.setOrientation(Qt.Horizontal)

        self.gridLayout_172.addWidget(self.horizontalSlider_Background, 0, 0, 1, 1)


        self.gridLayout_169.addWidget(self.groupBox_9, 1, 2, 1, 1)

        self.groupBox_11 = QGroupBox(self.groupBox_6)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.gridLayout_170 = QGridLayout(self.groupBox_11)
        self.gridLayout_170.setObjectName(u"gridLayout_170")
        self.horizontalSlider_ElectrodeRegion = QSlider(self.groupBox_11)
        self.horizontalSlider_ElectrodeRegion.setObjectName(u"horizontalSlider_ElectrodeRegion")
        self.horizontalSlider_ElectrodeRegion.setMaximum(100)
        self.horizontalSlider_ElectrodeRegion.setOrientation(Qt.Horizontal)

        self.gridLayout_170.addWidget(self.horizontalSlider_ElectrodeRegion, 0, 0, 1, 1)


        self.gridLayout_169.addWidget(self.groupBox_11, 1, 0, 1, 1)

        self.gridLayout_169.setColumnStretch(0, 1)
        self.gridLayout_169.setColumnStretch(1, 1)
        self.gridLayout_169.setColumnStretch(2, 1)

        self.gridLayout_68.addWidget(self.groupBox_6, 1, 0, 1, 7)

        self.pushButton_slicez = QPushButton(self.frame_32)
        self.pushButton_slicez.setObjectName(u"pushButton_slicez")
        self.pushButton_slicez.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon = QIcon()
        icon.addFile(u"Icons/ephys/slicing_axial_top.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicez.setIcon(icon)
        self.pushButton_slicez.setIconSize(QSize(60, 60))
        self.pushButton_slicez.setCheckable(True)

        self.gridLayout_68.addWidget(self.pushButton_slicez, 3, 5, 2, 1)

        self.pushButton_slicey = QPushButton(self.frame_32)
        self.pushButton_slicey.setObjectName(u"pushButton_slicey")
        self.pushButton_slicey.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon1 = QIcon()
        icon1.addFile(u"Icons/ephys/slicing_coronal_front.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicey.setIcon(icon1)
        self.pushButton_slicey.setIconSize(QSize(60, 60))
        self.pushButton_slicey.setCheckable(True)

        self.gridLayout_68.addWidget(self.pushButton_slicey, 3, 4, 2, 1)

        self.pushButton_slicex = QPushButton(self.frame_32)
        self.pushButton_slicex.setObjectName(u"pushButton_slicex")
        self.pushButton_slicex.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon2 = QIcon()
        icon2.addFile(u"Icons/ephys/slicing_sagittal_right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicex.setIcon(icon2)
        self.pushButton_slicex.setIconSize(QSize(60, 60))
        self.pushButton_slicex.setCheckable(True)

        self.gridLayout_68.addWidget(self.pushButton_slicex, 3, 3, 2, 1)

        self.pushButton_Noslicing = QPushButton(self.frame_32)
        self.pushButton_Noslicing.setObjectName(u"pushButton_Noslicing")
        self.pushButton_Noslicing.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon3 = QIcon()
        icon3.addFile(u"Icons/ephys/no_slicing.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_Noslicing.setIcon(icon3)
        self.pushButton_Noslicing.setIconSize(QSize(60, 60))

        self.gridLayout_68.addWidget(self.pushButton_Noslicing, 3, 2, 2, 1)

        self.change_perspective_ephys = QPushButton(self.frame_32)
        self.change_perspective_ephys.setObjectName(u"change_perspective_ephys")
        self.change_perspective_ephys.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon4 = QIcon()
        icon4.addFile(u"Icons/ephys/projection_parallel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.change_perspective_ephys.setIcon(icon4)
        self.change_perspective_ephys.setIconSize(QSize(60, 60))

        self.gridLayout_68.addWidget(self.change_perspective_ephys, 3, 1, 2, 1)

        self.vtkWidget_ephys = QVTKRenderWindowInteractor(self.frame_32)
        self.vtkWidget_ephys.setObjectName(u"vtkWidget_ephys")
        self.vtkWidget_ephys.setEnabled(True)
        self.vtkWidget_ephys.setMinimumSize(QSize(0, 0))
        self.vtkWidget_ephys.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_68.addWidget(self.vtkWidget_ephys, 0, 0, 1, 7)

        self.resetCamera_ephys = QPushButton(self.frame_32)
        self.resetCamera_ephys.setObjectName(u"resetCamera_ephys")
        self.resetCamera_ephys.setEnabled(True)
        self.resetCamera_ephys.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon5 = QIcon(QIcon.fromTheme(u"go-home"))
        self.resetCamera_ephys.setIcon(icon5)
        self.resetCamera_ephys.setIconSize(QSize(60, 60))
        self.resetCamera_ephys.setAutoDefault(False)
        self.resetCamera_ephys.setFlat(False)

        self.gridLayout_68.addWidget(self.resetCamera_ephys, 3, 0, 2, 1)

        self.gridLayout_68.setColumnStretch(0, 1)
        self.gridLayout_68.setColumnStretch(1, 1)
        self.gridLayout_68.setColumnStretch(2, 1)
        self.gridLayout_68.setColumnStretch(3, 1)
        self.gridLayout_68.setColumnStretch(4, 1)
        self.gridLayout_68.setColumnStretch(5, 1)

        self.gridLayout_46.addWidget(self.frame_32, 0, 0, 1, 1)

        self.tabWidget_ephys.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_166 = QGridLayout(self.tab_5)
        self.gridLayout_166.setObjectName(u"gridLayout_166")
        self.stackedWidget_video = QStackedWidget(self.tab_5)
        self.stackedWidget_video.setObjectName(u"stackedWidget_video")
        self.page_12 = QWidget()
        self.page_12.setObjectName(u"page_12")
        self.gridLayout_167 = QGridLayout(self.page_12)
        self.gridLayout_167.setObjectName(u"gridLayout_167")
        self.lineEdit_3 = QLineEdit(self.page_12)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setReadOnly(True)

        self.gridLayout_167.addWidget(self.lineEdit_3, 1, 1, 1, 1)

        self.pushButton_videoPlay = QPushButton(self.page_12)
        self.pushButton_videoPlay.setObjectName(u"pushButton_videoPlay")
        icon6 = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.pushButton_videoPlay.setIcon(icon6)
        self.pushButton_videoPlay.setIconSize(QSize(40, 40))

        self.gridLayout_167.addWidget(self.pushButton_videoPlay, 1, 0, 1, 1)

        self.spinBox_frame = QSpinBox(self.page_12)
        self.spinBox_frame.setObjectName(u"spinBox_frame")

        self.gridLayout_167.addWidget(self.spinBox_frame, 1, 2, 1, 1)

        self.widget_video = QVideoWidget(self.page_12)
        self.widget_video.setObjectName(u"widget_video")

        self.gridLayout_167.addWidget(self.widget_video, 0, 0, 1, 3)

        self.stackedWidget_video.addWidget(self.page_12)
        self.page_15 = QWidget()
        self.page_15.setObjectName(u"page_15")
        self.gridLayout_77 = QGridLayout(self.page_15)
        self.gridLayout_77.setObjectName(u"gridLayout_77")
        self.pushButton_AddVideo = QPushButton(self.page_15)
        self.pushButton_AddVideo.setObjectName(u"pushButton_AddVideo")
        self.pushButton_AddVideo.setMinimumSize(QSize(0, 72))

        self.gridLayout_77.addWidget(self.pushButton_AddVideo, 0, 0, 1, 1)

        self.stackedWidget_video.addWidget(self.page_15)

        self.gridLayout_166.addWidget(self.stackedWidget_video, 0, 0, 1, 4)

        self.tabWidget_ephys.addTab(self.tab_5, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_185 = QGridLayout(self.tab_7)
        self.gridLayout_185.setSpacing(0)
        self.gridLayout_185.setObjectName(u"gridLayout_185")
        self.gridLayout_185.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_13 = QLineEdit(self.tab_7)
        self.lineEdit_13.setObjectName(u"lineEdit_13")

        self.gridLayout_185.addWidget(self.lineEdit_13, 0, 0, 1, 1)

        self.tabWidget_LFP = QTabWidget(self.tab_7)
        self.tabWidget_LFP.setObjectName(u"tabWidget_LFP")
        self.tab_13 = QWidget()
        self.tab_13.setObjectName(u"tab_13")
        self.gridLayout_201 = QGridLayout(self.tab_13)
        self.gridLayout_201.setObjectName(u"gridLayout_201")
        self.lineEdit_61 = QLineEdit(self.tab_13)
        self.lineEdit_61.setObjectName(u"lineEdit_61")
        self.lineEdit_61.setReadOnly(True)

        self.gridLayout_201.addWidget(self.lineEdit_61, 0, 0, 1, 1)

        self.lineEdit_62 = QLineEdit(self.tab_13)
        self.lineEdit_62.setObjectName(u"lineEdit_62")
        self.lineEdit_62.setReadOnly(True)

        self.gridLayout_201.addWidget(self.lineEdit_62, 0, 1, 1, 1)

        self.doubleSpinBox_ClusterLimits = QDoubleSpinBox(self.tab_13)
        self.doubleSpinBox_ClusterLimits.setObjectName(u"doubleSpinBox_ClusterLimits")
        self.doubleSpinBox_ClusterLimits.setMaximumSize(QSize(16777215, 16777215))
        self.doubleSpinBox_ClusterLimits.setMinimum(0.010000000000000)
        self.doubleSpinBox_ClusterLimits.setMaximum(2.000000000000000)
        self.doubleSpinBox_ClusterLimits.setSingleStep(0.050000000000000)
        self.doubleSpinBox_ClusterLimits.setValue(0.300000000000000)

        self.gridLayout_201.addWidget(self.doubleSpinBox_ClusterLimits, 0, 2, 1, 1)

        self.widget_hierClustering = QWidget(self.tab_13)
        self.widget_hierClustering.setObjectName(u"widget_hierClustering")

        self.gridLayout_201.addWidget(self.widget_hierClustering, 1, 0, 1, 3)

        self.tabWidget_LFP.addTab(self.tab_13, "")
        self.tab_14 = QWidget()
        self.tab_14.setObjectName(u"tab_14")
        self.gridLayout_202 = QGridLayout(self.tab_14)
        self.gridLayout_202.setObjectName(u"gridLayout_202")
        self.widget_Spectrogram_ripple = QWidget(self.tab_14)
        self.widget_Spectrogram_ripple.setObjectName(u"widget_Spectrogram_ripple")

        self.gridLayout_202.addWidget(self.widget_Spectrogram_ripple, 1, 0, 1, 4)

        self.lineEdit_64 = QLineEdit(self.tab_14)
        self.lineEdit_64.setObjectName(u"lineEdit_64")
        self.lineEdit_64.setReadOnly(True)

        self.gridLayout_202.addWidget(self.lineEdit_64, 0, 0, 1, 1)

        self.pushButton_axisLog = QPushButton(self.tab_14)
        self.pushButton_axisLog.setObjectName(u"pushButton_axisLog")

        self.gridLayout_202.addWidget(self.pushButton_axisLog, 0, 3, 1, 1)

        self.pushButton_colorMap = QPushButton(self.tab_14)
        self.pushButton_colorMap.setObjectName(u"pushButton_colorMap")

        self.gridLayout_202.addWidget(self.pushButton_colorMap, 0, 2, 1, 1)

        self.tabWidget_LFP.addTab(self.tab_14, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.gridLayout_24 = QGridLayout(self.tab_8)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.lineEdit_65 = QLineEdit(self.tab_8)
        self.lineEdit_65.setObjectName(u"lineEdit_65")
        self.lineEdit_65.setReadOnly(True)

        self.gridLayout_24.addWidget(self.lineEdit_65, 0, 0, 1, 1)

        self.pushButton_exportCSD = QPushButton(self.tab_8)
        self.pushButton_exportCSD.setObjectName(u"pushButton_exportCSD")

        self.gridLayout_24.addWidget(self.pushButton_exportCSD, 0, 1, 1, 1)

        self.widget_CSD = QWidget(self.tab_8)
        self.widget_CSD.setObjectName(u"widget_CSD")

        self.gridLayout_24.addWidget(self.widget_CSD, 1, 0, 1, 2)

        self.tabWidget_LFP.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayout_207 = QGridLayout(self.tab_9)
        self.gridLayout_207.setObjectName(u"gridLayout_207")
        self.pushButton_allChannels_axis = QPushButton(self.tab_9)
        self.pushButton_allChannels_axis.setObjectName(u"pushButton_allChannels_axis")

        self.gridLayout_207.addWidget(self.pushButton_allChannels_axis, 0, 1, 1, 1)

        self.pushButton_Timeframe_spectrogram = QPushButton(self.tab_9)
        self.pushButton_Timeframe_spectrogram.setObjectName(u"pushButton_Timeframe_spectrogram")

        self.gridLayout_207.addWidget(self.pushButton_Timeframe_spectrogram, 1, 0, 1, 2)

        self.lineEdit_66 = QLineEdit(self.tab_9)
        self.lineEdit_66.setObjectName(u"lineEdit_66")
        self.lineEdit_66.setReadOnly(True)

        self.gridLayout_207.addWidget(self.lineEdit_66, 0, 0, 1, 1)

        self.widget_Spectrogram_allChannels = QWidget(self.tab_9)
        self.widget_Spectrogram_allChannels.setObjectName(u"widget_Spectrogram_allChannels")

        self.gridLayout_207.addWidget(self.widget_Spectrogram_allChannels, 2, 0, 1, 2)

        self.tabWidget_LFP.addTab(self.tab_9, "")

        self.gridLayout_185.addWidget(self.tabWidget_LFP, 0, 1, 3, 1)

        self.widget_spike_ruster = QWidget(self.tab_7)
        self.widget_spike_ruster.setObjectName(u"widget_spike_ruster")
        self.gridLayout_203 = QGridLayout(self.widget_spike_ruster)
        self.gridLayout_203.setObjectName(u"gridLayout_203")

        self.gridLayout_185.addWidget(self.widget_spike_ruster, 1, 0, 2, 1)

        self.tabWidget_ephys.addTab(self.tab_7, "")

        self.gridLayout.addWidget(self.tabWidget_ephys, 0, 1, 2, 1)

        self.frame_2 = QFrame(tab_ephys)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(300, 16777215))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_168 = QGridLayout(self.frame_2)
        self.gridLayout_168.setObjectName(u"gridLayout_168")
        self.pushButton_deselectAll = QPushButton(self.frame_2)
        self.pushButton_deselectAll.setObjectName(u"pushButton_deselectAll")

        self.gridLayout_168.addWidget(self.pushButton_deselectAll, 2, 2, 1, 1)

        self.tableWidget_ephys = QTableWidget(self.frame_2)
        self.tableWidget_ephys.setObjectName(u"tableWidget_ephys")
        self.tableWidget_ephys.setMaximumSize(QSize(300, 16777215))
        font = QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.tableWidget_ephys.setFont(font)
        self.tableWidget_ephys.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_ephys.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_ephys.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.tableWidget_ephys.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_ephys.horizontalHeader().setCascadingSectionResizes(False)

        self.gridLayout_168.addWidget(self.tableWidget_ephys, 1, 1, 1, 2)

        self.pushButton_selectAll = QPushButton(self.frame_2)
        self.pushButton_selectAll.setObjectName(u"pushButton_selectAll")

        self.gridLayout_168.addWidget(self.pushButton_selectAll, 2, 1, 1, 1)

        self.pushButton_showChannels = QPushButton(self.frame_2)
        self.pushButton_showChannels.setObjectName(u"pushButton_showChannels")
        self.pushButton_showChannels.setCheckable(True)
        self.pushButton_showChannels.setChecked(True)

        self.gridLayout_168.addWidget(self.pushButton_showChannels, 3, 1, 1, 2)

        self.pushButton_anatRegion = QPushButton(self.frame_2)
        self.pushButton_anatRegion.setObjectName(u"pushButton_anatRegion")
        self.pushButton_anatRegion.setMinimumSize(QSize(0, 72))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        self.pushButton_anatRegion.setFont(font1)
        self.pushButton_anatRegion.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_168.addWidget(self.pushButton_anatRegion, 4, 1, 1, 2)

        self.groupBox_5 = QGroupBox(self.frame_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(16777215, 300))
        self.gridLayout_165 = QGridLayout(self.groupBox_5)
        self.gridLayout_165.setObjectName(u"gridLayout_165")
        self.comboBox_mridTag = QComboBox(self.groupBox_5)
        self.comboBox_mridTag.setObjectName(u"comboBox_mridTag")
        self.comboBox_mridTag.setEnabled(True)
        self.comboBox_mridTag.setMinimumSize(QSize(0, 0))
        self.comboBox_mridTag.setStyleSheet(u"color: rgb(224, 27, 36);")
        self.comboBox_mridTag.setEditable(False)
        self.comboBox_mridTag.setInsertPolicy(QComboBox.InsertAtBottom)
        self.comboBox_mridTag.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.gridLayout_165.addWidget(self.comboBox_mridTag, 1, 0, 1, 1)

        self.lineEdit_60 = QLineEdit(self.groupBox_5)
        self.lineEdit_60.setObjectName(u"lineEdit_60")
        self.lineEdit_60.setReadOnly(True)

        self.gridLayout_165.addWidget(self.lineEdit_60, 0, 0, 1, 1)


        self.gridLayout_168.addWidget(self.groupBox_5, 0, 1, 1, 2)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(tab_ephys)

        self.tabWidget_ephys.setCurrentIndex(2)
        self.resetCamera_ephys.setDefault(False)
        self.stackedWidget_video.setCurrentIndex(0)
        self.tabWidget_LFP.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(tab_ephys)
    # setupUi

    def retranslateUi(self, tab_ephys):
        tab_ephys.setWindowTitle(QCoreApplication.translate("tab_ephys", u"Form", None))
        self.textEdit_ephys.setText(QCoreApplication.translate("tab_ephys", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.groupBox_37.setToolTip(QCoreApplication.translate("tab_ephys", u"Voxel coordinates of the selected channel's electrode \u2014 updates automatically when you click a channel in the table.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_37.setTitle(QCoreApplication.translate("tab_ephys", u"Coordinates of selected Channel", None))
#if QT_CONFIG(tooltip)
        self.spinBox_y_ephys.setToolTip(QCoreApplication.translate("tab_ephys", u"Y voxel coordinate of the selected channel's electrode position.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_x_ephys.setToolTip(QCoreApplication.translate("tab_ephys", u"X voxel coordinate of the selected channel's electrode position.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_z_ephys.setToolTip(QCoreApplication.translate("tab_ephys", u"Z voxel coordinate of the selected channel's electrode position.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_6.setToolTip(QCoreApplication.translate("tab_ephys", u"Opacity sliders for the region meshes shown in the 3D view.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_6.setTitle(QCoreApplication.translate("tab_ephys", u"Change Opacity of Meshes", None))
#if QT_CONFIG(tooltip)
        self.groupBox_8.setToolTip(QCoreApplication.translate("tab_ephys", u"Opacity of the atlas regions the selected shank(s) traverse.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_8.setTitle(QCoreApplication.translate("tab_ephys", u"Regions of Shank", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider_OtherRegions.setToolTip(QCoreApplication.translate("tab_ephys", u"Opacity of the atlas regions the selected shank(s) traverse, from transparent to fully opaque.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_9.setToolTip(QCoreApplication.translate("tab_ephys", u"Opacity of the background brain mesh.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_9.setTitle(QCoreApplication.translate("tab_ephys", u"Background", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider_Background.setToolTip(QCoreApplication.translate("tab_ephys", u"Opacity of the background brain mesh, from transparent to fully opaque.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_11.setToolTip(QCoreApplication.translate("tab_ephys", u"Opacity of the atlas region highlighted for the currently selected channel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_11.setTitle(QCoreApplication.translate("tab_ephys", u"Region of Selected Electrode", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider_ElectrodeRegion.setToolTip(QCoreApplication.translate("tab_ephys", u"Opacity of the atlas region highlighted for the currently selected channel, from transparent to fully opaque.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_slicez.setToolTip(QCoreApplication.translate("tab_ephys", u"Axial Slicing", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicez.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicey.setToolTip(QCoreApplication.translate("tab_ephys", u"Coronal Slicing", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicey.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicex.setToolTip(QCoreApplication.translate("tab_ephys", u"Sagittal Slicing", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicex.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_Noslicing.setToolTip(QCoreApplication.translate("tab_ephys", u"Exit Slicing Mode", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Noslicing.setText("")
#if QT_CONFIG(tooltip)
        self.change_perspective_ephys.setToolTip(QCoreApplication.translate("tab_ephys", u"Change Perspective", None))
#endif // QT_CONFIG(tooltip)
        self.change_perspective_ephys.setText("")
#if QT_CONFIG(tooltip)
        self.resetCamera_ephys.setToolTip(QCoreApplication.translate("tab_ephys", u"Reset Camera View", None))
#endif // QT_CONFIG(tooltip)
        self.resetCamera_ephys.setText("")
        self.tabWidget_ephys.setTabText(self.tabWidget_ephys.indexOf(self.tab_4), QCoreApplication.translate("tab_ephys", u"Anatomy", None))
        self.lineEdit_3.setText(QCoreApplication.translate("tab_ephys", u"Jump to Frame", None))
#if QT_CONFIG(tooltip)
        self.pushButton_videoPlay.setToolTip(QCoreApplication.translate("tab_ephys", u"Play or pause the loaded behavior video.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_videoPlay.setText("")
#if QT_CONFIG(tooltip)
        self.spinBox_frame.setToolTip(QCoreApplication.translate("tab_ephys", u"Jump to this video frame.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_AddVideo.setToolTip(QCoreApplication.translate("tab_ephys", u"Load a behavior video file to sync alongside the ephys recording.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_AddVideo.setText(QCoreApplication.translate("tab_ephys", u"OPEN VIDEO", None))
        self.tabWidget_ephys.setTabText(self.tabWidget_ephys.indexOf(self.tab_5), QCoreApplication.translate("tab_ephys", u"Video", None))
        self.lineEdit_13.setText(QCoreApplication.translate("tab_ephys", u"Spike Ruster Plot Unit/Neurons over Time [min:sec:msec] - Skipped Channels are not shown", None))
        self.lineEdit_61.setText(QCoreApplication.translate("tab_ephys", u"Pairwise Neuronal Spike-Count Correlation", None))
        self.lineEdit_62.setText(QCoreApplication.translate("tab_ephys", u"Colour-axis Limits", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_ClusterLimits.setToolTip(QCoreApplication.translate("tab_ephys", u"Symmetric color-scale limit (\u00b1value) for the hierarchical correlation heatmap.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_LFP.setTabText(self.tabWidget_LFP.indexOf(self.tab_13), QCoreApplication.translate("tab_ephys", u"Hierarchical Correlation", None))
        self.lineEdit_64.setText(QCoreApplication.translate("tab_ephys", u"Spectrogram of selected Channel in same time window as ephys data displayed", None))
#if QT_CONFIG(tooltip)
        self.pushButton_axisLog.setToolTip(QCoreApplication.translate("tab_ephys", u"Toggle the spectrogram's frequency axis between linear and logarithmic scale.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_axisLog.setText(QCoreApplication.translate("tab_ephys", u"Change Axis", None))
#if QT_CONFIG(tooltip)
        self.pushButton_colorMap.setToolTip(QCoreApplication.translate("tab_ephys", u"Cycle through the available spectrogram colormaps.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_colorMap.setText(QCoreApplication.translate("tab_ephys", u"ColorMap", None))
        self.tabWidget_LFP.setTabText(self.tabWidget_LFP.indexOf(self.tab_14), QCoreApplication.translate("tab_ephys", u"Spectrogram", None))
        self.lineEdit_65.setText(QCoreApplication.translate("tab_ephys", u"Current source density estimation ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_exportCSD.setToolTip(QCoreApplication.translate("tab_ephys", u"Export the current CSD (current source density) data as a binary file with a JSON sidecar.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_exportCSD.setText(QCoreApplication.translate("tab_ephys", u"Export as Binary", None))
        self.tabWidget_LFP.setTabText(self.tabWidget_LFP.indexOf(self.tab_8), QCoreApplication.translate("tab_ephys", u"CSD", None))
#if QT_CONFIG(tooltip)
        self.pushButton_allChannels_axis.setToolTip(QCoreApplication.translate("tab_ephys", u"Toggle the all-channels spectrogram's frequency axis between linear and logarithmic scale.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_allChannels_axis.setText(QCoreApplication.translate("tab_ephys", u"Change Axis", None))
#if QT_CONFIG(tooltip)
        self.pushButton_Timeframe_spectrogram.setToolTip(QCoreApplication.translate("tab_ephys", u"Switch the all-channels spectrogram between the full recording and a window centered on a detected ripple.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Timeframe_spectrogram.setText(QCoreApplication.translate("tab_ephys", u"Entire Frame / Around Ripple", None))
        self.lineEdit_66.setText(QCoreApplication.translate("tab_ephys", u"Spectrogram at selected time over all channels", None))
        self.tabWidget_LFP.setTabText(self.tabWidget_LFP.indexOf(self.tab_9), QCoreApplication.translate("tab_ephys", u"Spectrogram all Channels", None))
        self.tabWidget_ephys.setTabText(self.tabWidget_ephys.indexOf(self.tab_7), QCoreApplication.translate("tab_ephys", u"Analysis", None))
#if QT_CONFIG(tooltip)
        self.pushButton_deselectAll.setToolTip(QCoreApplication.translate("tab_ephys", u"Uncheck every channel, hiding them all from the 3D view.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_deselectAll.setText(QCoreApplication.translate("tab_ephys", u"Deselect All", None))
#if QT_CONFIG(tooltip)
        self.pushButton_selectAll.setToolTip(QCoreApplication.translate("tab_ephys", u"Check every channel, showing them all in the 3D view.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_selectAll.setText(QCoreApplication.translate("tab_ephys", u"Select All", None))
#if QT_CONFIG(tooltip)
        self.pushButton_showChannels.setToolTip(QCoreApplication.translate("tab_ephys", u"Show only the checked channels in the 3D view; unchecked channels stay hidden.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_showChannels.setText(QCoreApplication.translate("tab_ephys", u"Show only selected Channels", None))
#if QT_CONFIG(tooltip)
        self.pushButton_anatRegion.setToolTip(QCoreApplication.translate("tab_ephys", u"Manually reassign the anatomical region label of the currently selected channel (opens a picker of nearby atlas regions).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_anatRegion.setText(QCoreApplication.translate("tab_ephys", u"CHANGE ANAT REGION", None))
        self.groupBox_5.setTitle("")
#if QT_CONFIG(tooltip)
        self.comboBox_mridTag.setToolTip(QCoreApplication.translate("tab_ephys", u"Select which channel group / MRID tag to display in the 3D view.", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_mridTag.setCurrentText("")
        self.lineEdit_60.setText(QCoreApplication.translate("tab_ephys", u"Selected Shank", None))
    # retranslateUi

