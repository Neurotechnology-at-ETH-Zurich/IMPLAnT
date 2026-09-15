# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox, QApplication,
    QCheckBox, QComboBox, QDial, QDockWidget,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollBar, QSizePolicy, QSlider,
    QSpinBox, QStackedWidget, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QToolButton,
    QWidget)

from mplwidget import MplWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(2000, 2307)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1600, 0))
        MainWindow.setMaximumSize(QSize(2000, 16777215))
        MainWindow.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        MainWindow.setMouseTracking(True)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(True)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionAdd = QAction(MainWindow)
        self.actionAdd.setObjectName(u"actionAdd")
        self.actionSave_Image = QAction(MainWindow)
        self.actionSave_Image.setObjectName(u"actionSave_Image")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionPaintbrush = QAction(MainWindow)
        self.actionPaintbrush.setObjectName(u"actionPaintbrush")
        self.actionmain_code_2 = QAction(MainWindow)
        self.actionmain_code_2.setObjectName(u"actionmain_code_2")
        self.actionGaussian_Centers = QAction(MainWindow)
        self.actionGaussian_Centers.setObjectName(u"actionGaussian_Centers")
        self.actionGet_Coordinates = QAction(MainWindow)
        self.actionGet_Coordinates.setObjectName(u"actionGet_Coordinates")
        self.actionStart_with_Labels = QAction(MainWindow)
        self.actionStart_with_Labels.setObjectName(u"actionStart_with_Labels")
        self.actionAddViewImage = QAction(MainWindow)
        self.actionAddViewImage.setObjectName(u"actionAddViewImage")
        self.actionContrast_Adjustments = QAction(MainWindow)
        self.actionContrast_Adjustments.setObjectName(u"actionContrast_Adjustments")
        self.actionResample = QAction(MainWindow)
        self.actionResample.setObjectName(u"actionResample")
        self.actionRegister = QAction(MainWindow)
        self.actionRegister.setObjectName(u"actionRegister")
        self.actionContrast_Adjustments_2 = QAction(MainWindow)
        self.actionContrast_Adjustments_2.setObjectName(u"actionContrast_Adjustments_2")
        self.actionStart_MRIDlabels = QAction(MainWindow)
        self.actionStart_MRIDlabels.setObjectName(u"actionStart_MRIDlabels")
        self.actionOpen_ephys_Data = QAction(MainWindow)
        self.actionOpen_ephys_Data.setObjectName(u"actionOpen_ephys_Data")
        self.actionSegmentation = QAction(MainWindow)
        self.actionSegmentation.setObjectName(u"actionSegmentation")
        self.actionGet_Position_in_HPC = QAction(MainWindow)
        self.actionGet_Position_in_HPC.setObjectName(u"actionGet_Position_in_HPC")
        self.actionMeasurement = QAction(MainWindow)
        self.actionMeasurement.setObjectName(u"actionMeasurement")
        self.actionVisualize_3D_data = QAction(MainWindow)
        self.actionVisualize_3D_data.setObjectName(u"actionVisualize_3D_data")
        self.actionStart_SAMRI_process = QAction(MainWindow)
        self.actionStart_SAMRI_process.setObjectName(u"actionStart_SAMRI_process")
        self.actionTd = QAction(MainWindow)
        self.actionTd.setObjectName(u"actionTd")
        self.actionNew_Window = QAction(MainWindow)
        self.actionNew_Window.setObjectName(u"actionNew_Window")
        self.actionRippl_AI = QAction(MainWindow)
        self.actionRippl_AI.setObjectName(u"actionRippl_AI")
        self.actionTheta_Detection = QAction(MainWindow)
        self.actionTheta_Detection.setObjectName(u"actionTheta_Detection")
        self.actionLoad_Spike_Sorting = QAction(MainWindow)
        self.actionLoad_Spike_Sorting.setObjectName(u"actionLoad_Spike_Sorting")
        self.actionOpen_Session = QAction(MainWindow)
        self.actionOpen_Session.setObjectName(u"actionOpen_Session")
        self.actionOpen_Session_2 = QAction(MainWindow)
        self.actionOpen_Session_2.setObjectName(u"actionOpen_Session_2")
        self.actionOpen_Session_3 = QAction(MainWindow)
        self.actionOpen_Session_3.setObjectName(u"actionOpen_Session_3")
        self.actionOpen_Session_4 = QAction(MainWindow)
        self.actionOpen_Session_4.setObjectName(u"actionOpen_Session_4")
        self.actionLoad_Prev_Session = QAction(MainWindow)
        self.actionLoad_Prev_Session.setObjectName(u"actionLoad_Prev_Session")
        self.actionIntraoperative = QAction(MainWindow)
        self.actionIntraoperative.setObjectName(u"actionIntraoperative")
        self.actionTrajectory_Planning_2 = QAction(MainWindow)
        self.actionTrajectory_Planning_2.setObjectName(u"actionTrajectory_Planning_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_34 = QGridLayout(self.centralwidget)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.gridLayout_34.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.tabWidget_visualisation = QTabWidget(self.centralwidget)
        self.tabWidget_visualisation.setObjectName(u"tabWidget_visualisation")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_79 = QGridLayout(self.tab_2)
        self.gridLayout_79.setObjectName(u"gridLayout_79")
        self.tabWidget = QTabWidget(self.tab_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setBold(False)
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setContextMenuPolicy(Qt.NoContextMenu)
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")
        self.tabWidget.setTabBarAutoHide(False)
        self.PostSurgery = QWidget()
        self.PostSurgery.setObjectName(u"PostSurgery")
        self.gridLayout_70 = QGridLayout(self.PostSurgery)
        self.gridLayout_70.setObjectName(u"gridLayout_70")
        self.gridLayout_70.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.groupBox_data2 = QGroupBox(self.PostSurgery)
        self.groupBox_data2.setObjectName(u"groupBox_data2")
        self.groupBox_data2.setMinimumSize(QSize(0, 177))
        self.gridLayout_99 = QGridLayout(self.groupBox_data2)
        self.gridLayout_99.setObjectName(u"gridLayout_99")
        self.groupBox_32 = QGroupBox(self.groupBox_data2)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.gridLayout_33 = QGridLayout(self.groupBox_32)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.spinBox_x_data2 = QSpinBox(self.groupBox_32)
        self.spinBox_x_data2.setObjectName(u"spinBox_x_data2")
        self.spinBox_x_data2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_data2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_x_data2.setMinimum(1)
        self.spinBox_x_data2.setMaximum(120)

        self.gridLayout_33.addWidget(self.spinBox_x_data2, 1, 0, 1, 1)

        self.spinBox_y_data2 = QSpinBox(self.groupBox_32)
        self.spinBox_y_data2.setObjectName(u"spinBox_y_data2")
        self.spinBox_y_data2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data2.setMinimum(1)
        self.spinBox_y_data2.setMaximum(120)

        self.gridLayout_33.addWidget(self.spinBox_y_data2, 1, 1, 1, 1)

        self.spinBox_z_data2 = QSpinBox(self.groupBox_32)
        self.spinBox_z_data2.setObjectName(u"spinBox_z_data2")
        self.spinBox_z_data2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data2.setMinimum(1)
        self.spinBox_z_data2.setMaximum(60)

        self.gridLayout_33.addWidget(self.spinBox_z_data2, 1, 2, 1, 1)

        self.lineEdit_98 = QLineEdit(self.groupBox_32)
        self.lineEdit_98.setObjectName(u"lineEdit_98")
        self.lineEdit_98.setReadOnly(True)

        self.gridLayout_33.addWidget(self.lineEdit_98, 0, 0, 1, 1)

        self.lineEdit_99 = QLineEdit(self.groupBox_32)
        self.lineEdit_99.setObjectName(u"lineEdit_99")
        self.lineEdit_99.setReadOnly(True)

        self.gridLayout_33.addWidget(self.lineEdit_99, 0, 1, 1, 1)

        self.lineEdit_100 = QLineEdit(self.groupBox_32)
        self.lineEdit_100.setObjectName(u"lineEdit_100")
        self.lineEdit_100.setReadOnly(True)

        self.gridLayout_33.addWidget(self.lineEdit_100, 0, 2, 1, 1)


        self.gridLayout_99.addWidget(self.groupBox_32, 1, 0, 1, 1)

        self.groupBox_time20 = QGroupBox(self.groupBox_data2)
        self.groupBox_time20.setObjectName(u"groupBox_time20")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_time20.sizePolicy().hasHeightForWidth())
        self.groupBox_time20.setSizePolicy(sizePolicy2)
        self.groupBox_time20.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        self.groupBox_time20.setFont(font1)
        self.groupBox_time20.setStyleSheet(u"")
        self.gridLayout_97 = QGridLayout(self.groupBox_time20)
        self.gridLayout_97.setObjectName(u"gridLayout_97")
        self.frame_8 = QFrame(self.groupBox_time20)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 200))
        self.frame_8.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.gridLayout_98 = QGridLayout(self.frame_8)
        self.gridLayout_98.setSpacing(0)
        self.gridLayout_98.setObjectName(u"gridLayout_98")
        self.gridLayout_98.setContentsMargins(4, 4, 4, 4)
        self.fit_to_zoom_data20 = QPushButton(self.frame_8)
        self.fit_to_zoom_data20.setObjectName(u"fit_to_zoom_data20")
        self.fit_to_zoom_data20.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data20.setAutoDefault(False)
        self.fit_to_zoom_data20.setFlat(False)

        self.gridLayout_98.addWidget(self.fit_to_zoom_data20, 1, 0, 2, 1)

        self.vtkWidget_data20 = QVTKRenderWindowInteractor(self.frame_8)
        self.vtkWidget_data20.setObjectName(u"vtkWidget_data20")
        self.vtkWidget_data20.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_98.addWidget(self.vtkWidget_data20, 0, 0, 1, 9)

        self.Scroll_data2 = QScrollBar(self.frame_8)
        self.Scroll_data2.setObjectName(u"Scroll_data2")
        self.Scroll_data2.setPageStep(10)

        self.gridLayout_98.addWidget(self.Scroll_data2, 0, 9, 1, 1)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.go_down_data20 = QToolButton(self.frame_8)
        self.go_down_data20.setObjectName(u"go_down_data20")
        icon = QIcon()
        icon.addFile(u"Icons/mri/downArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_down_data20.setIcon(icon)

        self.horizontalLayout_31.addWidget(self.go_down_data20)

        self.go_up_data20 = QToolButton(self.frame_8)
        self.go_up_data20.setObjectName(u"go_up_data20")
        icon1 = QIcon()
        icon1.addFile(u"Icons/mri/upArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_up_data20.setIcon(icon1)

        self.horizontalLayout_31.addWidget(self.go_up_data20)

        self.go_left_data20 = QToolButton(self.frame_8)
        self.go_left_data20.setObjectName(u"go_left_data20")
        icon2 = QIcon()
        icon2.addFile(u"Icons/mri/leftArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_left_data20.setIcon(icon2)

        self.horizontalLayout_31.addWidget(self.go_left_data20)

        self.go_right_data20 = QToolButton(self.frame_8)
        self.go_right_data20.setObjectName(u"go_right_data20")
        icon3 = QIcon()
        icon3.addFile(u"Icons/mri/rightArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_right_data20.setIcon(icon3)

        self.horizontalLayout_31.addWidget(self.go_right_data20)


        self.gridLayout_98.addLayout(self.horizontalLayout_31, 2, 8, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.zoom_in_data20 = QToolButton(self.frame_8)
        self.zoom_in_data20.setObjectName(u"zoom_in_data20")
        icon4 = QIcon()
        icon4.addFile(u"Icons/mri/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoom_in_data20.setIcon(icon4)

        self.horizontalLayout_4.addWidget(self.zoom_in_data20)

        self.zoom_out_data20 = QToolButton(self.frame_8)
        self.zoom_out_data20.setObjectName(u"zoom_out_data20")
        icon5 = QIcon()
        icon5.addFile(u"Icons/mri/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoom_out_data20.setIcon(icon5)

        self.horizontalLayout_4.addWidget(self.zoom_out_data20)


        self.gridLayout_98.addLayout(self.horizontalLayout_4, 2, 7, 1, 1)


        self.gridLayout_97.addWidget(self.frame_8, 0, 0, 1, 2)


        self.gridLayout_99.addWidget(self.groupBox_time20, 0, 0, 1, 1)

        self.tabWidget_time2 = QTabWidget(self.groupBox_data2)
        self.tabWidget_time2.setObjectName(u"tabWidget_time2")
        self.tabWidget_time20 = QWidget()
        self.tabWidget_time20.setObjectName(u"tabWidget_time20")
        self.gridLayout_116 = QGridLayout(self.tabWidget_time20)
        self.gridLayout_116.setObjectName(u"gridLayout_116")
        self.groupBox_57 = QGroupBox(self.tabWidget_time20)
        self.groupBox_57.setObjectName(u"groupBox_57")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        self.groupBox_57.setFont(font2)
        self.gridLayout_125 = QGridLayout(self.groupBox_57)
        self.gridLayout_125.setObjectName(u"gridLayout_125")
        self.changetimestamp_data20 = QSlider(self.groupBox_57)
        self.changetimestamp_data20.setObjectName(u"changetimestamp_data20")
        self.changetimestamp_data20.setStyleSheet(u"")
        self.changetimestamp_data20.setMaximum(99)
        self.changetimestamp_data20.setSingleStep(1)
        self.changetimestamp_data20.setPageStep(1)
        self.changetimestamp_data20.setValue(0)
        self.changetimestamp_data20.setOrientation(Qt.Horizontal)

        self.gridLayout_125.addWidget(self.changetimestamp_data20, 0, 0, 1, 1)

        self.displaytimestamp_data20 = QSpinBox(self.groupBox_57)
        self.displaytimestamp_data20.setObjectName(u"displaytimestamp_data20")
        self.displaytimestamp_data20.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data20.setMinimum(1)
        self.displaytimestamp_data20.setMaximum(120)

        self.gridLayout_125.addWidget(self.displaytimestamp_data20, 0, 1, 1, 1)


        self.gridLayout_116.addWidget(self.groupBox_57, 1, 0, 1, 1)

        self.groupBox_58 = QGroupBox(self.tabWidget_time20)
        self.groupBox_58.setObjectName(u"groupBox_58")
        self.groupBox_58.setFont(font2)
        self.gridLayout_126 = QGridLayout(self.groupBox_58)
        self.gridLayout_126.setObjectName(u"gridLayout_126")
        self.pushButton_reset_data20 = QPushButton(self.groupBox_58)
        self.pushButton_reset_data20.setObjectName(u"pushButton_reset_data20")

        self.gridLayout_126.addWidget(self.pushButton_reset_data20, 0, 0, 1, 1)

        self.pushButton_auto_data20 = QPushButton(self.groupBox_58)
        self.pushButton_auto_data20.setObjectName(u"pushButton_auto_data20")

        self.gridLayout_126.addWidget(self.pushButton_auto_data20, 0, 1, 1, 1)


        self.gridLayout_116.addWidget(self.groupBox_58, 1, 1, 1, 1)

        self.tabWidget_time2.addTab(self.tabWidget_time20, "")
        self.tabWidget_time21 = QWidget()
        self.tabWidget_time21.setObjectName(u"tabWidget_time21")
        self.gridLayout_127 = QGridLayout(self.tabWidget_time21)
        self.gridLayout_127.setObjectName(u"gridLayout_127")
        self.groupBox_59 = QGroupBox(self.tabWidget_time21)
        self.groupBox_59.setObjectName(u"groupBox_59")
        self.groupBox_59.setFont(font2)
        self.gridLayout_128 = QGridLayout(self.groupBox_59)
        self.gridLayout_128.setObjectName(u"gridLayout_128")
        self.changetimestamp_data21 = QSlider(self.groupBox_59)
        self.changetimestamp_data21.setObjectName(u"changetimestamp_data21")
        self.changetimestamp_data21.setStyleSheet(u"")
        self.changetimestamp_data21.setMaximum(99)
        self.changetimestamp_data21.setSingleStep(1)
        self.changetimestamp_data21.setPageStep(1)
        self.changetimestamp_data21.setValue(0)
        self.changetimestamp_data21.setOrientation(Qt.Horizontal)

        self.gridLayout_128.addWidget(self.changetimestamp_data21, 0, 0, 1, 1)

        self.displaytimestamp_data21 = QSpinBox(self.groupBox_59)
        self.displaytimestamp_data21.setObjectName(u"displaytimestamp_data21")
        self.displaytimestamp_data21.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data21.setMinimum(1)
        self.displaytimestamp_data21.setMaximum(120)

        self.gridLayout_128.addWidget(self.displaytimestamp_data21, 0, 1, 1, 1)


        self.gridLayout_127.addWidget(self.groupBox_59, 0, 0, 1, 1)

        self.groupBox_60 = QGroupBox(self.tabWidget_time21)
        self.groupBox_60.setObjectName(u"groupBox_60")
        self.groupBox_60.setFont(font2)
        self.gridLayout_129 = QGridLayout(self.groupBox_60)
        self.gridLayout_129.setObjectName(u"gridLayout_129")
        self.pushButton_auto_data21 = QPushButton(self.groupBox_60)
        self.pushButton_auto_data21.setObjectName(u"pushButton_auto_data21")

        self.gridLayout_129.addWidget(self.pushButton_auto_data21, 0, 1, 1, 1)

        self.pushButton_reset_data21 = QPushButton(self.groupBox_60)
        self.pushButton_reset_data21.setObjectName(u"pushButton_reset_data21")

        self.gridLayout_129.addWidget(self.pushButton_reset_data21, 0, 0, 1, 1)


        self.gridLayout_127.addWidget(self.groupBox_60, 0, 1, 1, 1)

        self.tabWidget_time2.addTab(self.tabWidget_time21, "")
        self.tabWidget_time22 = QWidget()
        self.tabWidget_time22.setObjectName(u"tabWidget_time22")
        self.gridLayout_130 = QGridLayout(self.tabWidget_time22)
        self.gridLayout_130.setObjectName(u"gridLayout_130")
        self.groupBox_61 = QGroupBox(self.tabWidget_time22)
        self.groupBox_61.setObjectName(u"groupBox_61")
        self.groupBox_61.setFont(font2)
        self.gridLayout_131 = QGridLayout(self.groupBox_61)
        self.gridLayout_131.setObjectName(u"gridLayout_131")
        self.changetimestamp_data22 = QSlider(self.groupBox_61)
        self.changetimestamp_data22.setObjectName(u"changetimestamp_data22")
        self.changetimestamp_data22.setStyleSheet(u"")
        self.changetimestamp_data22.setMaximum(99)
        self.changetimestamp_data22.setSingleStep(1)
        self.changetimestamp_data22.setPageStep(1)
        self.changetimestamp_data22.setValue(0)
        self.changetimestamp_data22.setOrientation(Qt.Horizontal)

        self.gridLayout_131.addWidget(self.changetimestamp_data22, 0, 0, 1, 1)

        self.displaytimestamp_data22 = QSpinBox(self.groupBox_61)
        self.displaytimestamp_data22.setObjectName(u"displaytimestamp_data22")
        self.displaytimestamp_data22.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data22.setMinimum(1)
        self.displaytimestamp_data22.setMaximum(120)

        self.gridLayout_131.addWidget(self.displaytimestamp_data22, 0, 1, 1, 1)


        self.gridLayout_130.addWidget(self.groupBox_61, 0, 0, 1, 1)

        self.groupBox_62 = QGroupBox(self.tabWidget_time22)
        self.groupBox_62.setObjectName(u"groupBox_62")
        self.groupBox_62.setFont(font2)
        self.gridLayout_132 = QGridLayout(self.groupBox_62)
        self.gridLayout_132.setObjectName(u"gridLayout_132")
        self.pushButton_reset_data22 = QPushButton(self.groupBox_62)
        self.pushButton_reset_data22.setObjectName(u"pushButton_reset_data22")

        self.gridLayout_132.addWidget(self.pushButton_reset_data22, 0, 0, 1, 1)

        self.pushButton_auto_data22 = QPushButton(self.groupBox_62)
        self.pushButton_auto_data22.setObjectName(u"pushButton_auto_data22")

        self.gridLayout_132.addWidget(self.pushButton_auto_data22, 0, 1, 1, 1)


        self.gridLayout_130.addWidget(self.groupBox_62, 0, 1, 1, 1)

        self.tabWidget_time2.addTab(self.tabWidget_time22, "")

        self.gridLayout_99.addWidget(self.tabWidget_time2, 1, 1, 1, 1)

        self.heatmap_data2 = QGroupBox(self.groupBox_data2)
        self.heatmap_data2.setObjectName(u"heatmap_data2")
        self.heatmap_data2.setFont(font1)
        self.gridLayout_93 = QGridLayout(self.heatmap_data2)
        self.gridLayout_93.setObjectName(u"gridLayout_93")
        self.frame_29 = QFrame(self.heatmap_data2)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setEnabled(True)
        self.frame_29.setMinimumSize(QSize(0, 200))
        self.frame_29.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_29.setFrameShape(QFrame.NoFrame)
        self.gridLayout_94 = QGridLayout(self.frame_29)
        self.gridLayout_94.setSpacing(0)
        self.gridLayout_94.setObjectName(u"gridLayout_94")
        self.gridLayout_94.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.go_down_data23 = QToolButton(self.frame_29)
        self.go_down_data23.setObjectName(u"go_down_data23")
        self.go_down_data23.setEnabled(False)
        self.go_down_data23.setIcon(icon)

        self.horizontalLayout_27.addWidget(self.go_down_data23)

        self.go_up_data23 = QToolButton(self.frame_29)
        self.go_up_data23.setObjectName(u"go_up_data23")
        self.go_up_data23.setEnabled(False)
        self.go_up_data23.setIcon(icon1)

        self.horizontalLayout_27.addWidget(self.go_up_data23)

        self.go_left_data23 = QToolButton(self.frame_29)
        self.go_left_data23.setObjectName(u"go_left_data23")
        self.go_left_data23.setEnabled(False)
        self.go_left_data23.setIcon(icon2)

        self.horizontalLayout_27.addWidget(self.go_left_data23)

        self.go_right_data23 = QToolButton(self.frame_29)
        self.go_right_data23.setObjectName(u"go_right_data23")
        self.go_right_data23.setEnabled(False)
        self.go_right_data23.setIcon(icon3)

        self.horizontalLayout_27.addWidget(self.go_right_data23)


        self.gridLayout_94.addLayout(self.horizontalLayout_27, 2, 7, 1, 1)

        self.vtkWidget_data23 = QVTKRenderWindowInteractor(self.frame_29)
        self.vtkWidget_data23.setObjectName(u"vtkWidget_data23")
        self.vtkWidget_data23.setEnabled(True)
        self.vtkWidget_data23.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_94.addWidget(self.vtkWidget_data23, 0, 0, 1, 8)

        self.fit_to_zoom_data23 = QPushButton(self.frame_29)
        self.fit_to_zoom_data23.setObjectName(u"fit_to_zoom_data23")
        self.fit_to_zoom_data23.setEnabled(False)
        self.fit_to_zoom_data23.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data23.setAutoDefault(False)
        self.fit_to_zoom_data23.setFlat(False)

        self.gridLayout_94.addWidget(self.fit_to_zoom_data23, 1, 0, 2, 1)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.zoom_in_data23 = QToolButton(self.frame_29)
        self.zoom_in_data23.setObjectName(u"zoom_in_data23")
        self.zoom_in_data23.setEnabled(False)
        self.zoom_in_data23.setIcon(icon4)
        self.zoom_in_data23.setIconSize(QSize(14, 16))

        self.horizontalLayout_28.addWidget(self.zoom_in_data23)

        self.zoom_out_data23 = QToolButton(self.frame_29)
        self.zoom_out_data23.setObjectName(u"zoom_out_data23")
        self.zoom_out_data23.setEnabled(False)
        self.zoom_out_data23.setIcon(icon5)

        self.horizontalLayout_28.addWidget(self.zoom_out_data23)


        self.gridLayout_94.addLayout(self.horizontalLayout_28, 2, 6, 1, 1)


        self.gridLayout_93.addWidget(self.frame_29, 0, 1, 1, 1)


        self.gridLayout_99.addWidget(self.heatmap_data2, 0, 3, 1, 1)

        self.groupBox_39 = QGroupBox(self.groupBox_data2)
        self.groupBox_39.setObjectName(u"groupBox_39")
        self.groupBox_39.setMinimumSize(QSize(400, 100))
        self.groupBox_39.setMaximumSize(QSize(400, 180))
        self.gridLayout_133 = QGridLayout(self.groupBox_39)
        self.gridLayout_133.setObjectName(u"gridLayout_133")
        self.gridLayout_133.setContentsMargins(-1, -1, 9, 9)
        self.tableintensity_data2 = QTableWidget(self.groupBox_39)
        if (self.tableintensity_data2.columnCount() < 4):
            self.tableintensity_data2.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableintensity_data2.setObjectName(u"tableintensity_data2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tableintensity_data2.sizePolicy().hasHeightForWidth())
        self.tableintensity_data2.setSizePolicy(sizePolicy3)
        self.tableintensity_data2.setMaximumSize(QSize(16777215, 1677))
        self.tableintensity_data2.setContextMenuPolicy(Qt.NoContextMenu)
        self.tableintensity_data2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableintensity_data2.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableintensity_data2.horizontalHeader().setDefaultSectionSize(67)

        self.gridLayout_133.addWidget(self.tableintensity_data2, 1, 0, 1, 1)


        self.gridLayout_99.addWidget(self.groupBox_39, 1, 2, 1, 1)

        self.groupBox_time21 = QGroupBox(self.groupBox_data2)
        self.groupBox_time21.setObjectName(u"groupBox_time21")
        sizePolicy2.setHeightForWidth(self.groupBox_time21.sizePolicy().hasHeightForWidth())
        self.groupBox_time21.setSizePolicy(sizePolicy2)
        self.groupBox_time21.setFont(font1)
        self.gridLayout_91 = QGridLayout(self.groupBox_time21)
        self.gridLayout_91.setObjectName(u"gridLayout_91")
        self.frame_19 = QFrame(self.groupBox_time21)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(0, 200))
        self.frame_19.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_19.setFrameShape(QFrame.NoFrame)
        self.gridLayout_92 = QGridLayout(self.frame_19)
        self.gridLayout_92.setSpacing(0)
        self.gridLayout_92.setObjectName(u"gridLayout_92")
        self.gridLayout_92.setContentsMargins(4, 4, 4, 4)
        self.fit_to_zoom_data21 = QPushButton(self.frame_19)
        self.fit_to_zoom_data21.setObjectName(u"fit_to_zoom_data21")
        self.fit_to_zoom_data21.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data21.setAutoDefault(False)
        self.fit_to_zoom_data21.setFlat(False)

        self.gridLayout_92.addWidget(self.fit_to_zoom_data21, 1, 0, 2, 1)

        self.vtkWidget_data21 = QVTKRenderWindowInteractor(self.frame_19)
        self.vtkWidget_data21.setObjectName(u"vtkWidget_data21")
        self.vtkWidget_data21.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_92.addWidget(self.vtkWidget_data21, 0, 0, 1, 11)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.go_down_data21 = QToolButton(self.frame_19)
        self.go_down_data21.setObjectName(u"go_down_data21")
        self.go_down_data21.setIcon(icon)

        self.horizontalLayout_25.addWidget(self.go_down_data21)

        self.go_up_data21 = QToolButton(self.frame_19)
        self.go_up_data21.setObjectName(u"go_up_data21")
        self.go_up_data21.setIcon(icon1)

        self.horizontalLayout_25.addWidget(self.go_up_data21)

        self.go_left_data21 = QToolButton(self.frame_19)
        self.go_left_data21.setObjectName(u"go_left_data21")
        self.go_left_data21.setIcon(icon2)

        self.horizontalLayout_25.addWidget(self.go_left_data21)

        self.go_right_data21 = QToolButton(self.frame_19)
        self.go_right_data21.setObjectName(u"go_right_data21")
        self.go_right_data21.setIcon(icon3)

        self.horizontalLayout_25.addWidget(self.go_right_data21)


        self.gridLayout_92.addLayout(self.horizontalLayout_25, 1, 10, 1, 1)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.zoom_in_data21 = QToolButton(self.frame_19)
        self.zoom_in_data21.setObjectName(u"zoom_in_data21")
        self.zoom_in_data21.setIcon(icon4)

        self.horizontalLayout_26.addWidget(self.zoom_in_data21)

        self.zoom_out_data21 = QToolButton(self.frame_19)
        self.zoom_out_data21.setObjectName(u"zoom_out_data21")
        self.zoom_out_data21.setIcon(icon5)

        self.horizontalLayout_26.addWidget(self.zoom_out_data21)


        self.gridLayout_92.addLayout(self.horizontalLayout_26, 1, 9, 1, 1)


        self.gridLayout_91.addWidget(self.frame_19, 0, 1, 1, 2)


        self.gridLayout_99.addWidget(self.groupBox_time21, 0, 1, 1, 1)

        self.groupBox_time22 = QGroupBox(self.groupBox_data2)
        self.groupBox_time22.setObjectName(u"groupBox_time22")
        sizePolicy2.setHeightForWidth(self.groupBox_time22.sizePolicy().hasHeightForWidth())
        self.groupBox_time22.setSizePolicy(sizePolicy2)
        self.groupBox_time22.setFont(font1)
        self.gridLayout_95 = QGridLayout(self.groupBox_time22)
        self.gridLayout_95.setObjectName(u"gridLayout_95")
        self.frame_25 = QFrame(self.groupBox_time22)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(0, 200))
        self.frame_25.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_25.setFrameShape(QFrame.NoFrame)
        self.gridLayout_96 = QGridLayout(self.frame_25)
        self.gridLayout_96.setSpacing(0)
        self.gridLayout_96.setObjectName(u"gridLayout_96")
        self.gridLayout_96.setContentsMargins(4, 4, 4, 4)
        self.fit_to_zoom_data22 = QPushButton(self.frame_25)
        self.fit_to_zoom_data22.setObjectName(u"fit_to_zoom_data22")
        self.fit_to_zoom_data22.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data22.setAutoDefault(False)
        self.fit_to_zoom_data22.setFlat(False)

        self.gridLayout_96.addWidget(self.fit_to_zoom_data22, 1, 0, 2, 1)

        self.vtkWidget_data22 = QVTKRenderWindowInteractor(self.frame_25)
        self.vtkWidget_data22.setObjectName(u"vtkWidget_data22")
        self.vtkWidget_data22.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_96.addWidget(self.vtkWidget_data22, 0, 0, 1, 8)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.go_down_data22 = QToolButton(self.frame_25)
        self.go_down_data22.setObjectName(u"go_down_data22")
        self.go_down_data22.setIcon(icon)

        self.horizontalLayout_29.addWidget(self.go_down_data22)

        self.go_up_data22 = QToolButton(self.frame_25)
        self.go_up_data22.setObjectName(u"go_up_data22")
        self.go_up_data22.setIcon(icon1)

        self.horizontalLayout_29.addWidget(self.go_up_data22)

        self.go_left_data22 = QToolButton(self.frame_25)
        self.go_left_data22.setObjectName(u"go_left_data22")
        self.go_left_data22.setIcon(icon2)

        self.horizontalLayout_29.addWidget(self.go_left_data22)

        self.go_right_data22 = QToolButton(self.frame_25)
        self.go_right_data22.setObjectName(u"go_right_data22")
        self.go_right_data22.setIcon(icon3)

        self.horizontalLayout_29.addWidget(self.go_right_data22)


        self.gridLayout_96.addLayout(self.horizontalLayout_29, 2, 7, 1, 1)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.zoom_in_data22 = QToolButton(self.frame_25)
        self.zoom_in_data22.setObjectName(u"zoom_in_data22")
        self.zoom_in_data22.setIcon(icon4)
        self.zoom_in_data22.setIconSize(QSize(14, 16))

        self.horizontalLayout_30.addWidget(self.zoom_in_data22)

        self.zoom_out_data22 = QToolButton(self.frame_25)
        self.zoom_out_data22.setObjectName(u"zoom_out_data22")
        self.zoom_out_data22.setIcon(icon5)

        self.horizontalLayout_30.addWidget(self.zoom_out_data22)


        self.gridLayout_96.addLayout(self.horizontalLayout_30, 2, 6, 1, 1)


        self.gridLayout_95.addWidget(self.frame_25, 0, 0, 1, 2)


        self.gridLayout_99.addWidget(self.groupBox_time22, 0, 2, 1, 1)

        self.groupbox_legend2 = QGroupBox(self.groupBox_data2)
        self.groupbox_legend2.setObjectName(u"groupbox_legend2")
        self.groupbox_legend2.setMaximumSize(QSize(16777215, 120))
        self.gridLayout_134 = QGridLayout(self.groupbox_legend2)
        self.gridLayout_134.setObjectName(u"gridLayout_134")
        self.frame_31 = QFrame(self.groupbox_legend2)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setEnabled(True)
        self.frame_31.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_31.setFrameShape(QFrame.NoFrame)
        self.gridLayout_135 = QGridLayout(self.frame_31)
        self.gridLayout_135.setSpacing(0)
        self.gridLayout_135.setObjectName(u"gridLayout_135")
        self.gridLayout_135.setContentsMargins(4, 4, 4, 4)
        self.vtkWidget_legend2 = QVTKRenderWindowInteractor(self.frame_31)
        self.vtkWidget_legend2.setObjectName(u"vtkWidget_legend2")
        self.vtkWidget_legend2.setEnabled(True)
        self.vtkWidget_legend2.setMinimumSize(QSize(0, 30))
        self.vtkWidget_legend2.setMaximumSize(QSize(16777215, 167))
        self.vtkWidget_legend2.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_135.addWidget(self.vtkWidget_legend2, 0, 0, 1, 1)


        self.gridLayout_134.addWidget(self.frame_31, 0, 0, 1, 1)


        self.gridLayout_99.addWidget(self.groupbox_legend2, 1, 3, 1, 1)

        self.gridLayout_99.setColumnStretch(0, 1)
        self.gridLayout_99.setColumnStretch(1, 1)
        self.gridLayout_99.setColumnStretch(2, 1)

        self.gridLayout_70.addWidget(self.groupBox_data2, 3, 1, 1, 4)

        self.groupBox_data0 = QGroupBox(self.PostSurgery)
        self.groupBox_data0.setObjectName(u"groupBox_data0")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.groupBox_data0.sizePolicy().hasHeightForWidth())
        self.groupBox_data0.setSizePolicy(sizePolicy4)
        self.groupBox_data0.setMinimumSize(QSize(900, 289))
        self.groupBox_data0.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_7 = QGridLayout(self.groupBox_data0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(9, 9, -1, -1)
        self.data_4d_3d = QStackedWidget(self.groupBox_data0)
        self.data_4d_3d.setObjectName(u"data_4d_3d")
        sizePolicy4.setHeightForWidth(self.data_4d_3d.sizePolicy().hasHeightForWidth())
        self.data_4d_3d.setSizePolicy(sizePolicy4)
        self.data_4d_3d.setFrameShape(QFrame.NoFrame)
        self.page_4Ddata0 = QWidget()
        self.page_4Ddata0.setObjectName(u"page_4Ddata0")
        self.gridLayout_data0 = QGridLayout(self.page_4Ddata0)
        self.gridLayout_data0.setSpacing(6)
        self.gridLayout_data0.setObjectName(u"gridLayout_data0")
        self.gridLayout_data0.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_data0.setContentsMargins(9, 9, 9, 9)
        self.tabWidget_time0 = QTabWidget(self.page_4Ddata0)
        self.tabWidget_time0.setObjectName(u"tabWidget_time0")
        self.tabWidget_time0.setMinimumSize(QSize(0, 0))
        self.tabWidget_time0.setMaximumSize(QSize(16777215, 200))
        self.tabWidget_time00 = QWidget()
        self.tabWidget_time00.setObjectName(u"tabWidget_time00")
        self.gridLayout_72 = QGridLayout(self.tabWidget_time00)
        self.gridLayout_72.setObjectName(u"gridLayout_72")
        self.groupBox_46 = QGroupBox(self.tabWidget_time00)
        self.groupBox_46.setObjectName(u"groupBox_46")
        self.groupBox_46.setFont(font2)
        self.gridLayout_57 = QGridLayout(self.groupBox_46)
        self.gridLayout_57.setObjectName(u"gridLayout_57")
        self.changetimestamp_data00 = QSlider(self.groupBox_46)
        self.changetimestamp_data00.setObjectName(u"changetimestamp_data00")
        self.changetimestamp_data00.setStyleSheet(u"")
        self.changetimestamp_data00.setMaximum(99)
        self.changetimestamp_data00.setSingleStep(1)
        self.changetimestamp_data00.setPageStep(1)
        self.changetimestamp_data00.setValue(0)
        self.changetimestamp_data00.setOrientation(Qt.Horizontal)

        self.gridLayout_57.addWidget(self.changetimestamp_data00, 0, 0, 1, 1)

        self.displaytimestamp_data00 = QSpinBox(self.groupBox_46)
        self.displaytimestamp_data00.setObjectName(u"displaytimestamp_data00")
        self.displaytimestamp_data00.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data00.setMinimum(1)
        self.displaytimestamp_data00.setMaximum(120)

        self.gridLayout_57.addWidget(self.displaytimestamp_data00, 0, 1, 1, 1)


        self.gridLayout_72.addWidget(self.groupBox_46, 1, 0, 1, 1)

        self.groupBox_49 = QGroupBox(self.tabWidget_time00)
        self.groupBox_49.setObjectName(u"groupBox_49")
        self.groupBox_49.setFont(font2)
        self.gridLayout_56 = QGridLayout(self.groupBox_49)
        self.gridLayout_56.setObjectName(u"gridLayout_56")
        self.pushButton_reset_data00 = QPushButton(self.groupBox_49)
        self.pushButton_reset_data00.setObjectName(u"pushButton_reset_data00")

        self.gridLayout_56.addWidget(self.pushButton_reset_data00, 0, 0, 1, 1)

        self.pushButton_auto_data00 = QPushButton(self.groupBox_49)
        self.pushButton_auto_data00.setObjectName(u"pushButton_auto_data00")

        self.gridLayout_56.addWidget(self.pushButton_auto_data00, 0, 1, 1, 1)


        self.gridLayout_72.addWidget(self.groupBox_49, 1, 1, 1, 1)

        self.tabWidget_time0.addTab(self.tabWidget_time00, "")
        self.tabWidget_time01 = QWidget()
        self.tabWidget_time01.setObjectName(u"tabWidget_time01")
        self.gridLayout_62 = QGridLayout(self.tabWidget_time01)
        self.gridLayout_62.setObjectName(u"gridLayout_62")
        self.groupBox_41 = QGroupBox(self.tabWidget_time01)
        self.groupBox_41.setObjectName(u"groupBox_41")
        self.groupBox_41.setFont(font2)
        self.gridLayout_60 = QGridLayout(self.groupBox_41)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.changetimestamp_data01 = QSlider(self.groupBox_41)
        self.changetimestamp_data01.setObjectName(u"changetimestamp_data01")
        self.changetimestamp_data01.setStyleSheet(u"")
        self.changetimestamp_data01.setMaximum(99)
        self.changetimestamp_data01.setSingleStep(1)
        self.changetimestamp_data01.setPageStep(1)
        self.changetimestamp_data01.setValue(0)
        self.changetimestamp_data01.setOrientation(Qt.Horizontal)

        self.gridLayout_60.addWidget(self.changetimestamp_data01, 0, 0, 1, 1)

        self.displaytimestamp_data01 = QSpinBox(self.groupBox_41)
        self.displaytimestamp_data01.setObjectName(u"displaytimestamp_data01")
        self.displaytimestamp_data01.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data01.setMinimum(1)
        self.displaytimestamp_data01.setMaximum(120)

        self.gridLayout_60.addWidget(self.displaytimestamp_data01, 0, 1, 1, 1)


        self.gridLayout_62.addWidget(self.groupBox_41, 0, 0, 1, 1)

        self.groupBox_42 = QGroupBox(self.tabWidget_time01)
        self.groupBox_42.setObjectName(u"groupBox_42")
        self.groupBox_42.setFont(font2)
        self.gridLayout_61 = QGridLayout(self.groupBox_42)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.pushButton_auto_data01 = QPushButton(self.groupBox_42)
        self.pushButton_auto_data01.setObjectName(u"pushButton_auto_data01")

        self.gridLayout_61.addWidget(self.pushButton_auto_data01, 0, 1, 1, 1)

        self.pushButton_reset_data01 = QPushButton(self.groupBox_42)
        self.pushButton_reset_data01.setObjectName(u"pushButton_reset_data01")

        self.gridLayout_61.addWidget(self.pushButton_reset_data01, 0, 0, 1, 1)


        self.gridLayout_62.addWidget(self.groupBox_42, 0, 1, 1, 1)

        self.tabWidget_time0.addTab(self.tabWidget_time01, "")
        self.tabWidget_time02 = QWidget()
        self.tabWidget_time02.setObjectName(u"tabWidget_time02")
        self.gridLayout_73 = QGridLayout(self.tabWidget_time02)
        self.gridLayout_73.setObjectName(u"gridLayout_73")
        self.groupBox_44 = QGroupBox(self.tabWidget_time02)
        self.groupBox_44.setObjectName(u"groupBox_44")
        self.groupBox_44.setFont(font2)
        self.gridLayout_59 = QGridLayout(self.groupBox_44)
        self.gridLayout_59.setObjectName(u"gridLayout_59")
        self.changetimestamp_data02 = QSlider(self.groupBox_44)
        self.changetimestamp_data02.setObjectName(u"changetimestamp_data02")
        self.changetimestamp_data02.setStyleSheet(u"")
        self.changetimestamp_data02.setMaximum(99)
        self.changetimestamp_data02.setSingleStep(1)
        self.changetimestamp_data02.setPageStep(1)
        self.changetimestamp_data02.setValue(0)
        self.changetimestamp_data02.setOrientation(Qt.Horizontal)

        self.gridLayout_59.addWidget(self.changetimestamp_data02, 0, 0, 1, 1)

        self.displaytimestamp_data02 = QSpinBox(self.groupBox_44)
        self.displaytimestamp_data02.setObjectName(u"displaytimestamp_data02")
        self.displaytimestamp_data02.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data02.setMinimum(1)
        self.displaytimestamp_data02.setMaximum(120)

        self.gridLayout_59.addWidget(self.displaytimestamp_data02, 0, 1, 1, 1)


        self.gridLayout_73.addWidget(self.groupBox_44, 0, 0, 1, 1)

        self.groupBox_43 = QGroupBox(self.tabWidget_time02)
        self.groupBox_43.setObjectName(u"groupBox_43")
        self.groupBox_43.setFont(font2)
        self.gridLayout_58 = QGridLayout(self.groupBox_43)
        self.gridLayout_58.setObjectName(u"gridLayout_58")
        self.pushButton_reset_data02 = QPushButton(self.groupBox_43)
        self.pushButton_reset_data02.setObjectName(u"pushButton_reset_data02")

        self.gridLayout_58.addWidget(self.pushButton_reset_data02, 0, 0, 1, 1)

        self.pushButton_auto_data02 = QPushButton(self.groupBox_43)
        self.pushButton_auto_data02.setObjectName(u"pushButton_auto_data02")

        self.gridLayout_58.addWidget(self.pushButton_auto_data02, 0, 1, 1, 1)


        self.gridLayout_73.addWidget(self.groupBox_43, 0, 1, 1, 1)

        self.tabWidget_time0.addTab(self.tabWidget_time02, "")

        self.gridLayout_data0.addWidget(self.tabWidget_time0, 2, 1, 1, 1)

        self.heatmap_data0 = QGroupBox(self.page_4Ddata0)
        self.heatmap_data0.setObjectName(u"heatmap_data0")
        self.heatmap_data0.setMaximumSize(QSize(16777215, 1000))
        self.heatmap_data0.setFont(font1)
        self.gridLayout_49 = QGridLayout(self.heatmap_data0)
        self.gridLayout_49.setObjectName(u"gridLayout_49")
        self.frame_26 = QFrame(self.heatmap_data0)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setEnabled(True)
        self.frame_26.setMinimumSize(QSize(0, 200))
        self.frame_26.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_26.setFrameShape(QFrame.NoFrame)
        self.gridLayout_48 = QGridLayout(self.frame_26)
        self.gridLayout_48.setSpacing(0)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.gridLayout_48.setContentsMargins(4, 4, 4, 4)
        self.vtkWidget_data03 = QVTKRenderWindowInteractor(self.frame_26)
        self.vtkWidget_data03.setObjectName(u"vtkWidget_data03")
        self.vtkWidget_data03.setEnabled(True)
        self.vtkWidget_data03.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_48.addWidget(self.vtkWidget_data03, 0, 0, 1, 7)


        self.gridLayout_49.addWidget(self.frame_26, 0, 0, 1, 1)


        self.gridLayout_data0.addWidget(self.heatmap_data0, 0, 3, 1, 1)

        self.groupBox_time00 = QGroupBox(self.page_4Ddata0)
        self.groupBox_time00.setObjectName(u"groupBox_time00")
        sizePolicy2.setHeightForWidth(self.groupBox_time00.sizePolicy().hasHeightForWidth())
        self.groupBox_time00.setSizePolicy(sizePolicy2)
        self.groupBox_time00.setMinimumSize(QSize(20, 100))
        self.groupBox_time00.setMaximumSize(QSize(16777215, 1000))
        self.groupBox_time00.setFont(font1)
        self.groupBox_time00.setStyleSheet(u"")
        self.gridLayout_53 = QGridLayout(self.groupBox_time00)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.frame_3 = QFrame(self.groupBox_time00)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 200))
        self.frame_3.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.gridLayout_52 = QGridLayout(self.frame_3)
        self.gridLayout_52.setSpacing(0)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.gridLayout_52.setContentsMargins(4, 4, 4, 4)
        self.fit_to_zoom_data00 = QPushButton(self.frame_3)
        self.fit_to_zoom_data00.setObjectName(u"fit_to_zoom_data00")
        self.fit_to_zoom_data00.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data00.setAutoDefault(False)
        self.fit_to_zoom_data00.setFlat(False)

        self.gridLayout_52.addWidget(self.fit_to_zoom_data00, 1, 0, 2, 1)

        self.vtkWidget_data00 = QVTKRenderWindowInteractor(self.frame_3)
        self.vtkWidget_data00.setObjectName(u"vtkWidget_data00")
        self.vtkWidget_data00.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_52.addWidget(self.vtkWidget_data00, 0, 0, 1, 9)

        self.Scroll_data0 = QScrollBar(self.frame_3)
        self.Scroll_data0.setObjectName(u"Scroll_data0")
        self.Scroll_data0.setPageStep(10)

        self.gridLayout_52.addWidget(self.Scroll_data0, 0, 9, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.go_down_data00 = QToolButton(self.frame_3)
        self.go_down_data00.setObjectName(u"go_down_data00")
        self.go_down_data00.setIcon(icon)

        self.horizontalLayout_9.addWidget(self.go_down_data00)

        self.go_up_data00 = QToolButton(self.frame_3)
        self.go_up_data00.setObjectName(u"go_up_data00")
        self.go_up_data00.setIcon(icon1)

        self.horizontalLayout_9.addWidget(self.go_up_data00)

        self.go_left_data00 = QToolButton(self.frame_3)
        self.go_left_data00.setObjectName(u"go_left_data00")
        self.go_left_data00.setIcon(icon2)

        self.horizontalLayout_9.addWidget(self.go_left_data00)

        self.go_right_data00 = QToolButton(self.frame_3)
        self.go_right_data00.setObjectName(u"go_right_data00")
        self.go_right_data00.setIcon(icon3)

        self.horizontalLayout_9.addWidget(self.go_right_data00)


        self.gridLayout_52.addLayout(self.horizontalLayout_9, 2, 8, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.zoom_in_data00 = QToolButton(self.frame_3)
        self.zoom_in_data00.setObjectName(u"zoom_in_data00")
        self.zoom_in_data00.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.zoom_in_data00)

        self.zoom_out_data00 = QToolButton(self.frame_3)
        self.zoom_out_data00.setObjectName(u"zoom_out_data00")
        self.zoom_out_data00.setIcon(icon5)

        self.horizontalLayout_2.addWidget(self.zoom_out_data00)


        self.gridLayout_52.addLayout(self.horizontalLayout_2, 2, 7, 1, 1)

        self.fit_to_zoom_data00.raise_()
        self.Scroll_data0.raise_()
        self.vtkWidget_data00.raise_()

        self.gridLayout_53.addWidget(self.frame_3, 0, 0, 1, 2)


        self.gridLayout_data0.addWidget(self.groupBox_time00, 0, 0, 1, 1)

        self.groupBox_time01 = QGroupBox(self.page_4Ddata0)
        self.groupBox_time01.setObjectName(u"groupBox_time01")
        sizePolicy2.setHeightForWidth(self.groupBox_time01.sizePolicy().hasHeightForWidth())
        self.groupBox_time01.setSizePolicy(sizePolicy2)
        self.groupBox_time01.setMinimumSize(QSize(20, 0))
        self.groupBox_time01.setMaximumSize(QSize(16777215, 1000))
        self.groupBox_time01.setFont(font1)
        self.gridLayout_54 = QGridLayout(self.groupBox_time01)
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.frame_17 = QFrame(self.groupBox_time01)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMinimumSize(QSize(0, 200))
        self.frame_17.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.gridLayout_51 = QGridLayout(self.frame_17)
        self.gridLayout_51.setSpacing(0)
        self.gridLayout_51.setObjectName(u"gridLayout_51")
        self.gridLayout_51.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.zoom_in_data01 = QToolButton(self.frame_17)
        self.zoom_in_data01.setObjectName(u"zoom_in_data01")
        self.zoom_in_data01.setIcon(icon4)

        self.horizontalLayout_14.addWidget(self.zoom_in_data01)

        self.zoom_out_data01 = QToolButton(self.frame_17)
        self.zoom_out_data01.setObjectName(u"zoom_out_data01")
        self.zoom_out_data01.setIcon(icon5)

        self.horizontalLayout_14.addWidget(self.zoom_out_data01)


        self.gridLayout_51.addLayout(self.horizontalLayout_14, 2, 9, 1, 1)

        self.fit_to_zoom_data01 = QPushButton(self.frame_17)
        self.fit_to_zoom_data01.setObjectName(u"fit_to_zoom_data01")
        self.fit_to_zoom_data01.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data01.setAutoDefault(False)
        self.fit_to_zoom_data01.setFlat(False)

        self.gridLayout_51.addWidget(self.fit_to_zoom_data01, 2, 0, 2, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.go_down_data01 = QToolButton(self.frame_17)
        self.go_down_data01.setObjectName(u"go_down_data01")
        self.go_down_data01.setIcon(icon)

        self.horizontalLayout_15.addWidget(self.go_down_data01)

        self.go_up_data01 = QToolButton(self.frame_17)
        self.go_up_data01.setObjectName(u"go_up_data01")
        self.go_up_data01.setIcon(icon1)

        self.horizontalLayout_15.addWidget(self.go_up_data01)

        self.go_left_data01 = QToolButton(self.frame_17)
        self.go_left_data01.setObjectName(u"go_left_data01")
        self.go_left_data01.setIcon(icon2)

        self.horizontalLayout_15.addWidget(self.go_left_data01)

        self.go_right_data01 = QToolButton(self.frame_17)
        self.go_right_data01.setObjectName(u"go_right_data01")
        self.go_right_data01.setIcon(icon3)

        self.horizontalLayout_15.addWidget(self.go_right_data01)


        self.gridLayout_51.addLayout(self.horizontalLayout_15, 2, 10, 1, 1)

        self.vtkWidget_data01 = QVTKRenderWindowInteractor(self.frame_17)
        self.vtkWidget_data01.setObjectName(u"vtkWidget_data01")
        self.vtkWidget_data01.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_51.addWidget(self.vtkWidget_data01, 0, 0, 1, 11)


        self.gridLayout_54.addWidget(self.frame_17, 0, 0, 1, 2)


        self.gridLayout_data0.addWidget(self.groupBox_time01, 0, 1, 1, 1)

        self.groupBox_34 = QGroupBox(self.page_4Ddata0)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_71 = QGridLayout(self.groupBox_34)
        self.gridLayout_71.setObjectName(u"gridLayout_71")
        self.spinBox_x_data0 = QSpinBox(self.groupBox_34)
        self.spinBox_x_data0.setObjectName(u"spinBox_x_data0")
        self.spinBox_x_data0.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_data0.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_x_data0.setMinimum(1)
        self.spinBox_x_data0.setMaximum(120)

        self.gridLayout_71.addWidget(self.spinBox_x_data0, 1, 1, 1, 1)

        self.spinBox_z_data0 = QSpinBox(self.groupBox_34)
        self.spinBox_z_data0.setObjectName(u"spinBox_z_data0")
        self.spinBox_z_data0.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data0.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data0.setMinimum(1)
        self.spinBox_z_data0.setMaximum(60)

        self.gridLayout_71.addWidget(self.spinBox_z_data0, 1, 3, 1, 1)

        self.spinBox_y_data0 = QSpinBox(self.groupBox_34)
        self.spinBox_y_data0.setObjectName(u"spinBox_y_data0")
        self.spinBox_y_data0.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data0.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data0.setMinimum(1)
        self.spinBox_y_data0.setMaximum(120)

        self.gridLayout_71.addWidget(self.spinBox_y_data0, 1, 2, 1, 1)

        self.lineEdit_87 = QLineEdit(self.groupBox_34)
        self.lineEdit_87.setObjectName(u"lineEdit_87")
        self.lineEdit_87.setReadOnly(True)

        self.gridLayout_71.addWidget(self.lineEdit_87, 0, 1, 1, 1)

        self.lineEdit_104 = QLineEdit(self.groupBox_34)
        self.lineEdit_104.setObjectName(u"lineEdit_104")
        self.lineEdit_104.setReadOnly(True)

        self.gridLayout_71.addWidget(self.lineEdit_104, 0, 2, 1, 1)

        self.lineEdit_105 = QLineEdit(self.groupBox_34)
        self.lineEdit_105.setObjectName(u"lineEdit_105")
        self.lineEdit_105.setReadOnly(True)

        self.gridLayout_71.addWidget(self.lineEdit_105, 0, 3, 1, 1)


        self.gridLayout_data0.addWidget(self.groupBox_34, 2, 0, 1, 1)

        self.groupBox_time02 = QGroupBox(self.page_4Ddata0)
        self.groupBox_time02.setObjectName(u"groupBox_time02")
        sizePolicy2.setHeightForWidth(self.groupBox_time02.sizePolicy().hasHeightForWidth())
        self.groupBox_time02.setSizePolicy(sizePolicy2)
        self.groupBox_time02.setMinimumSize(QSize(20, 0))
        self.groupBox_time02.setMaximumSize(QSize(16777215, 1000))
        self.groupBox_time02.setFont(font1)
        self.gridLayout_55 = QGridLayout(self.groupBox_time02)
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.frame_23 = QFrame(self.groupBox_time02)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMinimumSize(QSize(0, 200))
        self.frame_23.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_23.setFrameShape(QFrame.NoFrame)
        self.gridLayout_50 = QGridLayout(self.frame_23)
        self.gridLayout_50.setSpacing(0)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.gridLayout_50.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.go_down_data02 = QToolButton(self.frame_23)
        self.go_down_data02.setObjectName(u"go_down_data02")
        self.go_down_data02.setIcon(icon)

        self.horizontalLayout_13.addWidget(self.go_down_data02)

        self.go_up_data02 = QToolButton(self.frame_23)
        self.go_up_data02.setObjectName(u"go_up_data02")
        self.go_up_data02.setIcon(icon1)

        self.horizontalLayout_13.addWidget(self.go_up_data02)

        self.go_left_data02 = QToolButton(self.frame_23)
        self.go_left_data02.setObjectName(u"go_left_data02")
        self.go_left_data02.setIcon(icon2)

        self.horizontalLayout_13.addWidget(self.go_left_data02)

        self.go_right_data02 = QToolButton(self.frame_23)
        self.go_right_data02.setObjectName(u"go_right_data02")
        self.go_right_data02.setIcon(icon3)

        self.horizontalLayout_13.addWidget(self.go_right_data02)


        self.gridLayout_50.addLayout(self.horizontalLayout_13, 2, 7, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.zoom_in_data02 = QToolButton(self.frame_23)
        self.zoom_in_data02.setObjectName(u"zoom_in_data02")
        self.zoom_in_data02.setIcon(icon4)
        self.zoom_in_data02.setIconSize(QSize(14, 16))

        self.horizontalLayout_10.addWidget(self.zoom_in_data02)

        self.zoom_out_data02 = QToolButton(self.frame_23)
        self.zoom_out_data02.setObjectName(u"zoom_out_data02")
        self.zoom_out_data02.setIcon(icon5)

        self.horizontalLayout_10.addWidget(self.zoom_out_data02)


        self.gridLayout_50.addLayout(self.horizontalLayout_10, 2, 6, 1, 1)

        self.fit_to_zoom_data02 = QPushButton(self.frame_23)
        self.fit_to_zoom_data02.setObjectName(u"fit_to_zoom_data02")
        self.fit_to_zoom_data02.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data02.setAutoDefault(False)
        self.fit_to_zoom_data02.setFlat(False)

        self.gridLayout_50.addWidget(self.fit_to_zoom_data02, 1, 0, 2, 1)

        self.vtkWidget_data02 = QVTKRenderWindowInteractor(self.frame_23)
        self.vtkWidget_data02.setObjectName(u"vtkWidget_data02")
        self.vtkWidget_data02.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_50.addWidget(self.vtkWidget_data02, 0, 0, 1, 8)


        self.gridLayout_55.addWidget(self.frame_23, 0, 0, 1, 2)


        self.gridLayout_data0.addWidget(self.groupBox_time02, 0, 2, 1, 1)

        self.groupBox_25 = QGroupBox(self.page_4Ddata0)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.groupBox_25.setMinimumSize(QSize(400, 100))
        self.groupBox_25.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_32 = QGridLayout(self.groupBox_25)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(-1, -1, 9, 9)
        self.tableintensity_data0 = QTableWidget(self.groupBox_25)
        if (self.tableintensity_data0.columnCount() < 4):
            self.tableintensity_data0.setColumnCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        self.tableintensity_data0.setObjectName(u"tableintensity_data0")
        sizePolicy3.setHeightForWidth(self.tableintensity_data0.sizePolicy().hasHeightForWidth())
        self.tableintensity_data0.setSizePolicy(sizePolicy3)
        self.tableintensity_data0.setMaximumSize(QSize(16777215, 1677))
        self.tableintensity_data0.setContextMenuPolicy(Qt.NoContextMenu)
        self.tableintensity_data0.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableintensity_data0.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableintensity_data0.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableintensity_data0.horizontalHeader().setDefaultSectionSize(67)

        self.gridLayout_32.addWidget(self.tableintensity_data0, 1, 0, 1, 1)


        self.gridLayout_data0.addWidget(self.groupBox_25, 2, 2, 1, 1)

        self.groupbox_legend0 = QGroupBox(self.page_4Ddata0)
        self.groupbox_legend0.setObjectName(u"groupbox_legend0")
        self.groupbox_legend0.setMaximumSize(QSize(16777215, 120))
        self.gridLayout_64 = QGridLayout(self.groupbox_legend0)
        self.gridLayout_64.setObjectName(u"gridLayout_64")
        self.frame_27 = QFrame(self.groupbox_legend0)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setEnabled(True)
        self.frame_27.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_27.setFrameShape(QFrame.NoFrame)
        self.gridLayout_47 = QGridLayout(self.frame_27)
        self.gridLayout_47.setSpacing(0)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(4, 4, 4, 4)
        self.vtkWidget_legend0 = QVTKRenderWindowInteractor(self.frame_27)
        self.vtkWidget_legend0.setObjectName(u"vtkWidget_legend0")
        self.vtkWidget_legend0.setEnabled(True)
        self.vtkWidget_legend0.setMinimumSize(QSize(0, 30))
        self.vtkWidget_legend0.setMaximumSize(QSize(16777215, 167))
        self.vtkWidget_legend0.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_47.addWidget(self.vtkWidget_legend0, 0, 0, 1, 1)


        self.gridLayout_64.addWidget(self.frame_27, 0, 1, 1, 1)


        self.gridLayout_data0.addWidget(self.groupbox_legend0, 2, 3, 1, 1)

        self.gridLayout_data0.setRowStretch(0, 1)
        self.gridLayout_data0.setColumnStretch(0, 1)
        self.gridLayout_data0.setColumnStretch(1, 1)
        self.gridLayout_data0.setColumnStretch(2, 1)
        self.gridLayout_data0.setColumnMinimumWidth(0, 1)
        self.gridLayout_data0.setColumnMinimumWidth(1, 1)
        self.gridLayout_data0.setColumnMinimumWidth(2, 1)
        self.gridLayout_data0.setRowMinimumHeight(0, 1)
        self.data_4d_3d.addWidget(self.page_4Ddata0)
        self.page_3D = QWidget()
        self.page_3D.setObjectName(u"page_3D")
        self.gridLayout_106 = QGridLayout(self.page_3D)
        self.gridLayout_106.setObjectName(u"gridLayout_106")
        self.stackedWidget_3d = QStackedWidget(self.page_3D)
        self.stackedWidget_3d.setObjectName(u"stackedWidget_3d")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_141 = QGridLayout(self.page)
        self.gridLayout_141.setObjectName(u"gridLayout_141")
        self.frame_trajectory = QFrame(self.page)
        self.frame_trajectory.setObjectName(u"frame_trajectory")
        self.frame_trajectory.setFrameShape(QFrame.StyledPanel)
        self.frame_trajectory.setFrameShadow(QFrame.Raised)
        self.gridLayout_137 = QGridLayout(self.frame_trajectory)
        self.gridLayout_137.setObjectName(u"gridLayout_137")
        self.stackedWidget_trajectoryplanning = QStackedWidget(self.frame_trajectory)
        self.stackedWidget_trajectoryplanning.setObjectName(u"stackedWidget_trajectoryplanning")
        self.stackedWidget_trajectoryplanning.setMaximumSize(QSize(500, 16777215))
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_75 = QGridLayout(self.page_5)
        self.gridLayout_75.setObjectName(u"gridLayout_75")
        self.groupBox_21 = QGroupBox(self.page_5)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.gridLayout_176 = QGridLayout(self.groupBox_21)
        self.gridLayout_176.setObjectName(u"gridLayout_176")
        self.lineEdit_58 = QLineEdit(self.groupBox_21)
        self.lineEdit_58.setObjectName(u"lineEdit_58")
        self.lineEdit_58.setReadOnly(True)

        self.gridLayout_176.addWidget(self.lineEdit_58, 1, 1, 1, 3)

        self.doubleSpinBox_d_lambdax = QDoubleSpinBox(self.groupBox_21)
        self.doubleSpinBox_d_lambdax.setObjectName(u"doubleSpinBox_d_lambdax")
        self.doubleSpinBox_d_lambdax.setReadOnly(True)
        self.doubleSpinBox_d_lambdax.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_lambdax.setMaximum(1500.000000000000000)

        self.gridLayout_176.addWidget(self.doubleSpinBox_d_lambdax, 7, 1, 1, 1)

        self.spinBox_tp_lambda_y = QSpinBox(self.groupBox_21)
        self.spinBox_tp_lambda_y.setObjectName(u"spinBox_tp_lambda_y")

        self.gridLayout_176.addWidget(self.spinBox_tp_lambda_y, 3, 2, 1, 1)

        self.spinBox_atlas_lambda_x = QSpinBox(self.groupBox_21)
        self.spinBox_atlas_lambda_x.setObjectName(u"spinBox_atlas_lambda_x")
        self.spinBox_atlas_lambda_x.setReadOnly(True)
        self.spinBox_atlas_lambda_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_lambda_x.setMaximum(1000)

        self.gridLayout_176.addWidget(self.spinBox_atlas_lambda_x, 5, 1, 1, 1)

        self.textEdit = QTextEdit(self.groupBox_21)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QSize(16777215, 50))
        self.textEdit.setReadOnly(True)

        self.gridLayout_176.addWidget(self.textEdit, 6, 1, 1, 3)

        self.pushButton_tp_lambda = QPushButton(self.groupBox_21)
        self.pushButton_tp_lambda.setObjectName(u"pushButton_tp_lambda")
        self.pushButton_tp_lambda.setMinimumSize(QSize(0, 50))
        self.pushButton_tp_lambda.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_tp_lambda.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_176.addWidget(self.pushButton_tp_lambda, 0, 1, 1, 3)

        self.lineEdit_20 = QLineEdit(self.groupBox_21)
        self.lineEdit_20.setObjectName(u"lineEdit_20")
        self.lineEdit_20.setReadOnly(True)

        self.gridLayout_176.addWidget(self.lineEdit_20, 4, 1, 1, 3)

        self.spinBox_atlas_lambda_z = QSpinBox(self.groupBox_21)
        self.spinBox_atlas_lambda_z.setObjectName(u"spinBox_atlas_lambda_z")
        self.spinBox_atlas_lambda_z.setReadOnly(True)
        self.spinBox_atlas_lambda_z.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_lambda_z.setMaximum(1000)

        self.gridLayout_176.addWidget(self.spinBox_atlas_lambda_z, 5, 3, 1, 1)

        self.doubleSpinBox_d_lambday = QDoubleSpinBox(self.groupBox_21)
        self.doubleSpinBox_d_lambday.setObjectName(u"doubleSpinBox_d_lambday")
        self.doubleSpinBox_d_lambday.setReadOnly(True)
        self.doubleSpinBox_d_lambday.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_lambday.setMaximum(1500.000000000000000)

        self.gridLayout_176.addWidget(self.doubleSpinBox_d_lambday, 7, 2, 1, 1)

        self.doubleSpinBox_d_lambdaz = QDoubleSpinBox(self.groupBox_21)
        self.doubleSpinBox_d_lambdaz.setObjectName(u"doubleSpinBox_d_lambdaz")
        self.doubleSpinBox_d_lambdaz.setReadOnly(True)
        self.doubleSpinBox_d_lambdaz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_lambdaz.setMaximum(1500.000000000000000)

        self.gridLayout_176.addWidget(self.doubleSpinBox_d_lambdaz, 7, 3, 1, 1)

        self.spinBox_tp_lambda_x = QSpinBox(self.groupBox_21)
        self.spinBox_tp_lambda_x.setObjectName(u"spinBox_tp_lambda_x")

        self.gridLayout_176.addWidget(self.spinBox_tp_lambda_x, 3, 1, 1, 1)

        self.spinBox_atlas_lambda_y = QSpinBox(self.groupBox_21)
        self.spinBox_atlas_lambda_y.setObjectName(u"spinBox_atlas_lambda_y")
        self.spinBox_atlas_lambda_y.setReadOnly(True)
        self.spinBox_atlas_lambda_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_lambda_y.setMaximum(1000)

        self.gridLayout_176.addWidget(self.spinBox_atlas_lambda_y, 5, 2, 1, 1)

        self.spinBox_tp_lambda_z = QSpinBox(self.groupBox_21)
        self.spinBox_tp_lambda_z.setObjectName(u"spinBox_tp_lambda_z")

        self.gridLayout_176.addWidget(self.spinBox_tp_lambda_z, 3, 3, 1, 1)

        self.lineEdit_95 = QLineEdit(self.groupBox_21)
        self.lineEdit_95.setObjectName(u"lineEdit_95")

        self.gridLayout_176.addWidget(self.lineEdit_95, 2, 1, 1, 1)

        self.lineEdit_96 = QLineEdit(self.groupBox_21)
        self.lineEdit_96.setObjectName(u"lineEdit_96")

        self.gridLayout_176.addWidget(self.lineEdit_96, 2, 2, 1, 1)

        self.lineEdit_97 = QLineEdit(self.groupBox_21)
        self.lineEdit_97.setObjectName(u"lineEdit_97")

        self.gridLayout_176.addWidget(self.lineEdit_97, 2, 3, 1, 1)


        self.gridLayout_75.addWidget(self.groupBox_21, 3, 0, 1, 2)

        self.groupBox_12 = QGroupBox(self.page_5)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.gridLayout_136 = QGridLayout(self.groupBox_12)
        self.gridLayout_136.setObjectName(u"gridLayout_136")
        self.spinBox_atlas_bregma_x = QSpinBox(self.groupBox_12)
        self.spinBox_atlas_bregma_x.setObjectName(u"spinBox_atlas_bregma_x")
        self.spinBox_atlas_bregma_x.setReadOnly(True)
        self.spinBox_atlas_bregma_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_bregma_x.setMaximum(1000)

        self.gridLayout_136.addWidget(self.spinBox_atlas_bregma_x, 5, 1, 1, 1)

        self.lineEdit_29 = QLineEdit(self.groupBox_12)
        self.lineEdit_29.setObjectName(u"lineEdit_29")
        self.lineEdit_29.setReadOnly(True)

        self.gridLayout_136.addWidget(self.lineEdit_29, 4, 1, 1, 3)

        self.textEdit_4 = QTextEdit(self.groupBox_12)
        self.textEdit_4.setObjectName(u"textEdit_4")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.textEdit_4.sizePolicy().hasHeightForWidth())
        self.textEdit_4.setSizePolicy(sizePolicy5)
        self.textEdit_4.setMaximumSize(QSize(16777215, 50))
        self.textEdit_4.setReadOnly(True)

        self.gridLayout_136.addWidget(self.textEdit_4, 6, 1, 1, 3)

        self.pushButton_tp_bregma = QPushButton(self.groupBox_12)
        self.pushButton_tp_bregma.setObjectName(u"pushButton_tp_bregma")
        self.pushButton_tp_bregma.setMinimumSize(QSize(0, 50))
        self.pushButton_tp_bregma.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_tp_bregma.setAutoFillBackground(False)
        self.pushButton_tp_bregma.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_136.addWidget(self.pushButton_tp_bregma, 0, 1, 1, 3)

        self.spinBox_tp_bregma_x = QSpinBox(self.groupBox_12)
        self.spinBox_tp_bregma_x.setObjectName(u"spinBox_tp_bregma_x")

        self.gridLayout_136.addWidget(self.spinBox_tp_bregma_x, 3, 1, 1, 1)

        self.doubleSpinBox_d_bregmax = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_d_bregmax.setObjectName(u"doubleSpinBox_d_bregmax")
        self.doubleSpinBox_d_bregmax.setReadOnly(True)
        self.doubleSpinBox_d_bregmax.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_bregmax.setMaximum(1500.000000000000000)

        self.gridLayout_136.addWidget(self.doubleSpinBox_d_bregmax, 8, 1, 1, 1)

        self.doubleSpinBox_d_bregmaz = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_d_bregmaz.setObjectName(u"doubleSpinBox_d_bregmaz")
        self.doubleSpinBox_d_bregmaz.setReadOnly(True)
        self.doubleSpinBox_d_bregmaz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_bregmaz.setMaximum(1500.000000000000000)

        self.gridLayout_136.addWidget(self.doubleSpinBox_d_bregmaz, 8, 3, 1, 1)

        self.spinBox_tp_bregma_z = QSpinBox(self.groupBox_12)
        self.spinBox_tp_bregma_z.setObjectName(u"spinBox_tp_bregma_z")

        self.gridLayout_136.addWidget(self.spinBox_tp_bregma_z, 3, 3, 1, 1)

        self.spinBox_tp_bregma_y = QSpinBox(self.groupBox_12)
        self.spinBox_tp_bregma_y.setObjectName(u"spinBox_tp_bregma_y")

        self.gridLayout_136.addWidget(self.spinBox_tp_bregma_y, 3, 2, 1, 1)

        self.spinBox_atlas_bregma_z = QSpinBox(self.groupBox_12)
        self.spinBox_atlas_bregma_z.setObjectName(u"spinBox_atlas_bregma_z")
        self.spinBox_atlas_bregma_z.setReadOnly(True)
        self.spinBox_atlas_bregma_z.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_bregma_z.setMaximum(1000)

        self.gridLayout_136.addWidget(self.spinBox_atlas_bregma_z, 5, 3, 1, 1)

        self.spinBox_atlas_bregma_y = QSpinBox(self.groupBox_12)
        self.spinBox_atlas_bregma_y.setObjectName(u"spinBox_atlas_bregma_y")
        self.spinBox_atlas_bregma_y.setReadOnly(True)
        self.spinBox_atlas_bregma_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_bregma_y.setMaximum(1000)

        self.gridLayout_136.addWidget(self.spinBox_atlas_bregma_y, 5, 2, 1, 1)

        self.lineEdit_24 = QLineEdit(self.groupBox_12)
        self.lineEdit_24.setObjectName(u"lineEdit_24")
        self.lineEdit_24.setReadOnly(True)

        self.gridLayout_136.addWidget(self.lineEdit_24, 1, 1, 1, 3)

        self.doubleSpinBox_d_bregmay = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_d_bregmay.setObjectName(u"doubleSpinBox_d_bregmay")
        self.doubleSpinBox_d_bregmay.setReadOnly(True)
        self.doubleSpinBox_d_bregmay.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_bregmay.setMaximum(1500.000000000000000)

        self.gridLayout_136.addWidget(self.doubleSpinBox_d_bregmay, 8, 2, 1, 1)

        self.lineEdit_92 = QLineEdit(self.groupBox_12)
        self.lineEdit_92.setObjectName(u"lineEdit_92")

        self.gridLayout_136.addWidget(self.lineEdit_92, 2, 1, 1, 1)

        self.lineEdit_93 = QLineEdit(self.groupBox_12)
        self.lineEdit_93.setObjectName(u"lineEdit_93")

        self.gridLayout_136.addWidget(self.lineEdit_93, 2, 2, 1, 1)

        self.lineEdit_94 = QLineEdit(self.groupBox_12)
        self.lineEdit_94.setObjectName(u"lineEdit_94")

        self.gridLayout_136.addWidget(self.lineEdit_94, 2, 3, 1, 1)


        self.gridLayout_75.addWidget(self.groupBox_12, 1, 0, 1, 2)

        self.groupBox_22 = QGroupBox(self.page_5)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.groupBox_22.setMaximumSize(QSize(16777215, 150))
        self.gridLayout_20 = QGridLayout(self.groupBox_22)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.lineEdit_31 = QLineEdit(self.groupBox_22)
        self.lineEdit_31.setObjectName(u"lineEdit_31")
        self.lineEdit_31.setReadOnly(True)

        self.gridLayout_20.addWidget(self.lineEdit_31, 0, 0, 1, 1)

        self.lineEdit_43 = QLineEdit(self.groupBox_22)
        self.lineEdit_43.setObjectName(u"lineEdit_43")
        self.lineEdit_43.setReadOnly(True)

        self.gridLayout_20.addWidget(self.lineEdit_43, 2, 0, 1, 1)

        self.lineEdit_33 = QLineEdit(self.groupBox_22)
        self.lineEdit_33.setObjectName(u"lineEdit_33")
        self.lineEdit_33.setReadOnly(True)

        self.gridLayout_20.addWidget(self.lineEdit_33, 1, 0, 1, 1)

        self.doubleSpinBox_distanceAtlas = QDoubleSpinBox(self.groupBox_22)
        self.doubleSpinBox_distanceAtlas.setObjectName(u"doubleSpinBox_distanceAtlas")
        self.doubleSpinBox_distanceAtlas.setReadOnly(True)
        self.doubleSpinBox_distanceAtlas.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_20.addWidget(self.doubleSpinBox_distanceAtlas, 1, 1, 1, 1)

        self.doubleSpinBox_tp_ratio = QDoubleSpinBox(self.groupBox_22)
        self.doubleSpinBox_tp_ratio.setObjectName(u"doubleSpinBox_tp_ratio")
        self.doubleSpinBox_tp_ratio.setReadOnly(True)
        self.doubleSpinBox_tp_ratio.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_20.addWidget(self.doubleSpinBox_tp_ratio, 2, 1, 1, 1)

        self.doubleSpinBox_distance = QDoubleSpinBox(self.groupBox_22)
        self.doubleSpinBox_distance.setObjectName(u"doubleSpinBox_distance")
        self.doubleSpinBox_distance.setEnabled(True)
        self.doubleSpinBox_distance.setReadOnly(True)
        self.doubleSpinBox_distance.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_20.addWidget(self.doubleSpinBox_distance, 0, 1, 1, 1)


        self.gridLayout_75.addWidget(self.groupBox_22, 4, 0, 1, 2)

        self.textEdit_2 = QTextEdit(self.page_5)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setMaximumSize(QSize(16777215, 50))
        self.textEdit_2.setReadOnly(True)

        self.gridLayout_75.addWidget(self.textEdit_2, 0, 0, 1, 2)

        self.pushButton_tp_next0 = QPushButton(self.page_5)
        self.pushButton_tp_next0.setObjectName(u"pushButton_tp_next0")
        self.pushButton_tp_next0.setEnabled(False)
        self.pushButton_tp_next0.setMinimumSize(QSize(0, 50))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(230, 126, 34, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        brush2 = QBrush(QColor(255, 255, 255, 128))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        brush3 = QBrush(QColor(204, 204, 204, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush3)
        brush4 = QBrush(QColor(169, 113, 63, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush4)
        brush5 = QBrush(QColor(204, 204, 204, 128))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush5)
#endif
        self.pushButton_tp_next0.setPalette(palette)
        self.pushButton_tp_next0.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_75.addWidget(self.pushButton_tp_next0, 12, 0, 1, 2)

        self.groupBox_80 = QGroupBox(self.page_5)
        self.groupBox_80.setObjectName(u"groupBox_80")
        self.gridLayout_219 = QGridLayout(self.groupBox_80)
        self.gridLayout_219.setObjectName(u"gridLayout_219")
        self.dial_missalignment = QDial(self.groupBox_80)
        self.dial_missalignment.setObjectName(u"dial_missalignment")

        self.gridLayout_219.addWidget(self.dial_missalignment, 0, 3, 1, 2)

        self.doubleSpinBox_missalignment = QDoubleSpinBox(self.groupBox_80)
        self.doubleSpinBox_missalignment.setObjectName(u"doubleSpinBox_missalignment")

        self.gridLayout_219.addWidget(self.doubleSpinBox_missalignment, 0, 0, 1, 1)


        self.gridLayout_75.addWidget(self.groupBox_80, 11, 0, 1, 2)

        self.stackedWidget_trajectoryplanning.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.gridLayout_187 = QGridLayout(self.page_6)
        self.gridLayout_187.setObjectName(u"gridLayout_187")
        self.pushButton_PyLdetection = QPushButton(self.page_6)
        self.pushButton_PyLdetection.setObjectName(u"pushButton_PyLdetection")
        self.pushButton_PyLdetection.setEnabled(False)
        self.pushButton_PyLdetection.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_187.addWidget(self.pushButton_PyLdetection, 14, 0, 1, 2)

        self.pushButton_SaveTraj = QPushButton(self.page_6)
        self.pushButton_SaveTraj.setObjectName(u"pushButton_SaveTraj")
        self.pushButton_SaveTraj.setMinimumSize(QSize(0, 50))
        self.pushButton_SaveTraj.setAutoFillBackground(False)
        self.pushButton_SaveTraj.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_187.addWidget(self.pushButton_SaveTraj, 15, 0, 1, 2)

        self.groupBox_shank = QGroupBox(self.page_6)
        self.groupBox_shank.setObjectName(u"groupBox_shank")
        self.gridLayout_179 = QGridLayout(self.groupBox_shank)
        self.gridLayout_179.setObjectName(u"gridLayout_179")
        self.widget_tp_sidebar = QWidget(self.groupBox_shank)
        self.widget_tp_sidebar.setObjectName(u"widget_tp_sidebar")

        self.gridLayout_179.addWidget(self.widget_tp_sidebar, 1, 0, 1, 2)

        self.stackedWidget_geometry = QStackedWidget(self.groupBox_shank)
        self.stackedWidget_geometry.setObjectName(u"stackedWidget_geometry")
        self.stackedWidget_geometry.setMaximumSize(QSize(16777215, 100))
        self.page_25 = QWidget()
        self.page_25.setObjectName(u"page_25")
        self.gridLayout_210 = QGridLayout(self.page_25)
        self.gridLayout_210.setObjectName(u"gridLayout_210")
        self.pushButton_geometry_dfx = QPushButton(self.page_25)
        self.pushButton_geometry_dfx.setObjectName(u"pushButton_geometry_dfx")
        self.pushButton_geometry_dfx.setMinimumSize(QSize(0, 50))
        self.pushButton_geometry_dfx.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_210.addWidget(self.pushButton_geometry_dfx, 0, 0, 1, 1)

        self.stackedWidget_geometry.addWidget(self.page_25)
        self.page_26 = QWidget()
        self.page_26.setObjectName(u"page_26")
        self.gridLayout_209 = QGridLayout(self.page_26)
        self.gridLayout_209.setObjectName(u"gridLayout_209")
        self.lineEdit_21 = QLineEdit(self.page_26)
        self.lineEdit_21.setObjectName(u"lineEdit_21")
        self.lineEdit_21.setReadOnly(True)

        self.gridLayout_209.addWidget(self.lineEdit_21, 0, 0, 1, 1)

        self.spinBox_tp_channels = QSpinBox(self.page_26)
        self.spinBox_tp_channels.setObjectName(u"spinBox_tp_channels")
        self.spinBox_tp_channels.setMaximum(1024)
        self.spinBox_tp_channels.setValue(64)

        self.gridLayout_209.addWidget(self.spinBox_tp_channels, 0, 1, 1, 1)

        self.lineEdit_22 = QLineEdit(self.page_26)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        self.lineEdit_22.setReadOnly(True)

        self.gridLayout_209.addWidget(self.lineEdit_22, 1, 0, 1, 1)

        self.spinBox_tp_separation = QSpinBox(self.page_26)
        self.spinBox_tp_separation.setObjectName(u"spinBox_tp_separation")
        self.spinBox_tp_separation.setMaximum(1000)
        self.spinBox_tp_separation.setValue(50)

        self.gridLayout_209.addWidget(self.spinBox_tp_separation, 1, 1, 1, 1)

        self.stackedWidget_geometry.addWidget(self.page_26)

        self.gridLayout_179.addWidget(self.stackedWidget_geometry, 0, 0, 1, 2)

        self.gridLayout_179.setRowStretch(1, 1)

        self.gridLayout_187.addWidget(self.groupBox_shank, 11, 0, 1, 2)

        self.pushButton_tp_3d = QPushButton(self.page_6)
        self.pushButton_tp_3d.setObjectName(u"pushButton_tp_3d")
        self.pushButton_tp_3d.setMinimumSize(QSize(0, 50))
        self.pushButton_tp_3d.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_187.addWidget(self.pushButton_tp_3d, 0, 0, 1, 2)

        self.stackedWidget_trajectoryplanning.addWidget(self.page_6)
        self.page_31 = QWidget()
        self.page_31.setObjectName(u"page_31")
        self.gridLayout_222 = QGridLayout(self.page_31)
        self.gridLayout_222.setObjectName(u"gridLayout_222")
        self.groupBox_79 = QGroupBox(self.page_31)
        self.groupBox_79.setObjectName(u"groupBox_79")
        self.gridLayout_221 = QGridLayout(self.groupBox_79)
        self.gridLayout_221.setObjectName(u"gridLayout_221")
        self.pushButton_insertionPoint = QPushButton(self.groupBox_79)
        self.pushButton_insertionPoint.setObjectName(u"pushButton_insertionPoint")
        self.pushButton_insertionPoint.setMinimumSize(QSize(0, 50))
        self.pushButton_insertionPoint.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_insertionPoint.setAutoFillBackground(False)
        self.pushButton_insertionPoint.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_221.addWidget(self.pushButton_insertionPoint, 1, 1, 1, 3)

        self.spinBox_depth = QDoubleSpinBox(self.groupBox_79)
        self.spinBox_depth.setObjectName(u"spinBox_depth")
        self.spinBox_depth.setReadOnly(True)
        self.spinBox_depth.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_depth.setMaximum(1500.000000000000000)

        self.gridLayout_221.addWidget(self.spinBox_depth, 6, 1, 1, 3)

        self.spinBox_insertion_y = QSpinBox(self.groupBox_79)
        self.spinBox_insertion_y.setObjectName(u"spinBox_insertion_y")

        self.gridLayout_221.addWidget(self.spinBox_insertion_y, 3, 2, 1, 1)

        self.lineEdit_107 = QLineEdit(self.groupBox_79)
        self.lineEdit_107.setObjectName(u"lineEdit_107")

        self.gridLayout_221.addWidget(self.lineEdit_107, 2, 2, 1, 1)

        self.spinBox_insertion_z = QSpinBox(self.groupBox_79)
        self.spinBox_insertion_z.setObjectName(u"spinBox_insertion_z")

        self.gridLayout_221.addWidget(self.spinBox_insertion_z, 3, 3, 1, 1)

        self.spinBox_insertion_x = QSpinBox(self.groupBox_79)
        self.spinBox_insertion_x.setObjectName(u"spinBox_insertion_x")

        self.gridLayout_221.addWidget(self.spinBox_insertion_x, 3, 1, 1, 1)

        self.comboBox_insertion_shank = QComboBox(self.groupBox_79)
        self.comboBox_insertion_shank.addItem("")
        self.comboBox_insertion_shank.setObjectName(u"comboBox_insertion_shank")
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(False)
        self.comboBox_insertion_shank.setFont(font3)

        self.gridLayout_221.addWidget(self.comboBox_insertion_shank, 0, 1, 1, 3)

        self.pushButton_nextShank = QPushButton(self.groupBox_79)
        self.pushButton_nextShank.setObjectName(u"pushButton_nextShank")
        self.pushButton_nextShank.setMinimumSize(QSize(50, 50))
        self.pushButton_nextShank.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_221.addWidget(self.pushButton_nextShank, 7, 1, 1, 3)

        self.lineEdit_108 = QLineEdit(self.groupBox_79)
        self.lineEdit_108.setObjectName(u"lineEdit_108")

        self.gridLayout_221.addWidget(self.lineEdit_108, 2, 3, 1, 1)

        self.lineEdit_106 = QLineEdit(self.groupBox_79)
        self.lineEdit_106.setObjectName(u"lineEdit_106")

        self.gridLayout_221.addWidget(self.lineEdit_106, 2, 1, 1, 1)

        self.textEdit_14 = QTextEdit(self.groupBox_79)
        self.textEdit_14.setObjectName(u"textEdit_14")
        sizePolicy5.setHeightForWidth(self.textEdit_14.sizePolicy().hasHeightForWidth())
        self.textEdit_14.setSizePolicy(sizePolicy5)
        self.textEdit_14.setMaximumSize(QSize(16777215, 50))
        self.textEdit_14.setReadOnly(True)

        self.gridLayout_221.addWidget(self.textEdit_14, 4, 1, 1, 3)


        self.gridLayout_222.addWidget(self.groupBox_79, 1, 0, 1, 1)

        self.textEdit_5 = QTextEdit(self.page_31)
        self.textEdit_5.setObjectName(u"textEdit_5")
        self.textEdit_5.setMinimumSize(QSize(0, 50))
        self.textEdit_5.setMaximumSize(QSize(16777215, 100))
        self.textEdit_5.setReadOnly(True)

        self.gridLayout_222.addWidget(self.textEdit_5, 0, 0, 1, 1)

        self.stackedWidget_trajectoryplanning.addWidget(self.page_31)

        self.gridLayout_137.addWidget(self.stackedWidget_trajectoryplanning, 0, 0, 1, 1)


        self.gridLayout_141.addWidget(self.frame_trajectory, 0, 0, 1, 1)

        self.stackedWidget_3d.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_142 = QGridLayout(self.page_2)
        self.gridLayout_142.setObjectName(u"gridLayout_142")
        self.lineEdit_vis3D = QLineEdit(self.page_2)
        self.lineEdit_vis3D.setObjectName(u"lineEdit_vis3D")
        font4 = QFont()
        font4.setPointSize(16)
        font4.setBold(False)
        self.lineEdit_vis3D.setFont(font4)
        self.lineEdit_vis3D.setReadOnly(True)

        self.gridLayout_142.addWidget(self.lineEdit_vis3D, 0, 0, 1, 1)

        self.frame_vis3D = QFrame(self.page_2)
        self.frame_vis3D.setObjectName(u"frame_vis3D")
        self.frame_vis3D.setMinimumSize(QSize(0, 0))
        self.frame_vis3D.setFrameShape(QFrame.StyledPanel)
        self.frame_vis3D.setFrameShadow(QFrame.Raised)
        self.gridLayout_81 = QGridLayout(self.frame_vis3D)
        self.gridLayout_81.setObjectName(u"gridLayout_81")
        self.vtkWidget_data_seg3D = QVTKRenderWindowInteractor(self.frame_vis3D)
        self.vtkWidget_data_seg3D.setObjectName(u"vtkWidget_data_seg3D")
        self.vtkWidget_data_seg3D.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_81.addWidget(self.vtkWidget_data_seg3D, 0, 0, 1, 1)

        self.pushButton_seg3D = QPushButton(self.frame_vis3D)
        self.pushButton_seg3D.setObjectName(u"pushButton_seg3D")

        self.gridLayout_81.addWidget(self.pushButton_seg3D, 1, 0, 1, 1)


        self.gridLayout_142.addWidget(self.frame_vis3D, 1, 0, 1, 1)

        self.stackedWidget_3d.addWidget(self.page_2)

        self.gridLayout_106.addWidget(self.stackedWidget_3d, 1, 3, 3, 1)

        self.stackedWidget_dfx = QStackedWidget(self.page_3D)
        self.stackedWidget_dfx.setObjectName(u"stackedWidget_dfx")
        font5 = QFont()
        font5.setPointSize(13)
        font5.setBold(False)
        self.stackedWidget_dfx.setFont(font5)
        self.page_23 = QWidget()
        self.page_23.setObjectName(u"page_23")
        self.gridLayout_143 = QGridLayout(self.page_23)
        self.gridLayout_143.setObjectName(u"gridLayout_143")
        self.stackedWidget_sagittal = QStackedWidget(self.page_23)
        self.stackedWidget_sagittal.setObjectName(u"stackedWidget_sagittal")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_175 = QGridLayout(self.page_3)
        self.gridLayout_175.setObjectName(u"gridLayout_175")
        self.gridLayout_175.setContentsMargins(0, 0, 0, 0)
        self.textEdit_8 = QTextEdit(self.page_3)
        self.textEdit_8.setObjectName(u"textEdit_8")
        self.textEdit_8.setMinimumSize(QSize(0, 30))
        self.textEdit_8.setMaximumSize(QSize(16777215, 30))
        self.textEdit_8.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_8.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_8.setReadOnly(True)

        self.gridLayout_175.addWidget(self.textEdit_8, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.page_3)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 200))
        self.frame_9.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.gridLayout_144 = QGridLayout(self.frame_9)
        self.gridLayout_144.setSpacing(0)
        self.gridLayout_144.setObjectName(u"gridLayout_144")
        self.gridLayout_144.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.zoom_in_data3d1 = QToolButton(self.frame_9)
        self.zoom_in_data3d1.setObjectName(u"zoom_in_data3d1")
        self.zoom_in_data3d1.setIcon(icon4)

        self.horizontalLayout_33.addWidget(self.zoom_in_data3d1)

        self.zoom_out_data3d1 = QToolButton(self.frame_9)
        self.zoom_out_data3d1.setObjectName(u"zoom_out_data3d1")
        self.zoom_out_data3d1.setIcon(icon5)

        self.horizontalLayout_33.addWidget(self.zoom_out_data3d1)


        self.gridLayout_144.addLayout(self.horizontalLayout_33, 3, 7, 1, 1)

        self.fit_to_zoom_data3d1 = QPushButton(self.frame_9)
        self.fit_to_zoom_data3d1.setObjectName(u"fit_to_zoom_data3d1")
        self.fit_to_zoom_data3d1.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data3d1.setAutoDefault(False)
        self.fit_to_zoom_data3d1.setFlat(False)

        self.gridLayout_144.addWidget(self.fit_to_zoom_data3d1, 2, 0, 2, 1)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.go_down_data3d1 = QToolButton(self.frame_9)
        self.go_down_data3d1.setObjectName(u"go_down_data3d1")
        self.go_down_data3d1.setIcon(icon)

        self.horizontalLayout_32.addWidget(self.go_down_data3d1)

        self.go_up_data3d1 = QToolButton(self.frame_9)
        self.go_up_data3d1.setObjectName(u"go_up_data3d1")
        self.go_up_data3d1.setIcon(icon1)

        self.horizontalLayout_32.addWidget(self.go_up_data3d1)

        self.go_left_data3d1 = QToolButton(self.frame_9)
        self.go_left_data3d1.setObjectName(u"go_left_data3d1")
        self.go_left_data3d1.setIcon(icon2)

        self.horizontalLayout_32.addWidget(self.go_left_data3d1)

        self.go_right_data3d1 = QToolButton(self.frame_9)
        self.go_right_data3d1.setObjectName(u"go_right_data3d1")
        self.go_right_data3d1.setIcon(icon3)

        self.horizontalLayout_32.addWidget(self.go_right_data3d1)


        self.gridLayout_144.addLayout(self.horizontalLayout_32, 3, 8, 1, 1)

        self.vtkWidget_data_sagittal = QVTKRenderWindowInteractor(self.frame_9)
        self.vtkWidget_data_sagittal.setObjectName(u"vtkWidget_data_sagittal")
        self.vtkWidget_data_sagittal.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_144.addWidget(self.vtkWidget_data_sagittal, 1, 0, 1, 9)

        self.Scroll_data3d1 = QScrollBar(self.frame_9)
        self.Scroll_data3d1.setObjectName(u"Scroll_data3d1")
        self.Scroll_data3d1.setPageStep(10)

        self.gridLayout_144.addWidget(self.Scroll_data3d1, 1, 9, 1, 1)

        self.vtkWidget_data_sagittal.raise_()
        self.Scroll_data3d1.raise_()
        self.fit_to_zoom_data3d1.raise_()

        self.gridLayout_175.addWidget(self.frame_9, 1, 0, 1, 1)

        self.stackedWidget_sagittal.addWidget(self.page_3)
        self.page_33 = QWidget()
        self.page_33.setObjectName(u"page_33")
        self.gridLayout_229 = QGridLayout(self.page_33)
        self.gridLayout_229.setObjectName(u"gridLayout_229")
        self.gridLayout_229.setContentsMargins(0, 0, 0, 0)
        self.textEdit_16 = QTextEdit(self.page_33)
        self.textEdit_16.setObjectName(u"textEdit_16")
        self.textEdit_16.setMinimumSize(QSize(0, 30))
        self.textEdit_16.setMaximumSize(QSize(16777215, 30))
        self.textEdit_16.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_16.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_16.setReadOnly(True)

        self.gridLayout_229.addWidget(self.textEdit_16, 0, 0, 1, 1)

        self.frame_16 = QFrame(self.page_33)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 200))
        self.frame_16.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.gridLayout_228 = QGridLayout(self.frame_16)
        self.gridLayout_228.setSpacing(0)
        self.gridLayout_228.setObjectName(u"gridLayout_228")
        self.gridLayout_228.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.zoom_in_data3d1_3 = QToolButton(self.frame_16)
        self.zoom_in_data3d1_3.setObjectName(u"zoom_in_data3d1_3")
        self.zoom_in_data3d1_3.setIcon(icon4)

        self.horizontalLayout_44.addWidget(self.zoom_in_data3d1_3)

        self.zoom_out_data3d1_3 = QToolButton(self.frame_16)
        self.zoom_out_data3d1_3.setObjectName(u"zoom_out_data3d1_3")
        self.zoom_out_data3d1_3.setIcon(icon5)

        self.horizontalLayout_44.addWidget(self.zoom_out_data3d1_3)


        self.gridLayout_228.addLayout(self.horizontalLayout_44, 3, 7, 1, 1)

        self.fit_to_zoom_data3d1_3 = QPushButton(self.frame_16)
        self.fit_to_zoom_data3d1_3.setObjectName(u"fit_to_zoom_data3d1_3")
        self.fit_to_zoom_data3d1_3.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data3d1_3.setAutoDefault(False)
        self.fit_to_zoom_data3d1_3.setFlat(False)

        self.gridLayout_228.addWidget(self.fit_to_zoom_data3d1_3, 2, 0, 2, 1)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.go_down_data3d1_3 = QToolButton(self.frame_16)
        self.go_down_data3d1_3.setObjectName(u"go_down_data3d1_3")
        self.go_down_data3d1_3.setIcon(icon)

        self.horizontalLayout_45.addWidget(self.go_down_data3d1_3)

        self.go_up_data3d1_3 = QToolButton(self.frame_16)
        self.go_up_data3d1_3.setObjectName(u"go_up_data3d1_3")
        self.go_up_data3d1_3.setIcon(icon1)

        self.horizontalLayout_45.addWidget(self.go_up_data3d1_3)

        self.go_left_data3d1_3 = QToolButton(self.frame_16)
        self.go_left_data3d1_3.setObjectName(u"go_left_data3d1_3")
        self.go_left_data3d1_3.setIcon(icon2)

        self.horizontalLayout_45.addWidget(self.go_left_data3d1_3)

        self.go_right_data3d1_3 = QToolButton(self.frame_16)
        self.go_right_data3d1_3.setObjectName(u"go_right_data3d1_3")
        self.go_right_data3d1_3.setIcon(icon3)

        self.horizontalLayout_45.addWidget(self.go_right_data3d1_3)


        self.gridLayout_228.addLayout(self.horizontalLayout_45, 3, 8, 1, 1)

        self.vtkWidget_data_sagittal_3 = QVTKRenderWindowInteractor(self.frame_16)
        self.vtkWidget_data_sagittal_3.setObjectName(u"vtkWidget_data_sagittal_3")
        self.vtkWidget_data_sagittal_3.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_228.addWidget(self.vtkWidget_data_sagittal_3, 1, 0, 1, 9)

        self.Scroll_data3d1_3 = QScrollBar(self.frame_16)
        self.Scroll_data3d1_3.setObjectName(u"Scroll_data3d1_3")
        self.Scroll_data3d1_3.setPageStep(10)

        self.gridLayout_228.addWidget(self.Scroll_data3d1_3, 1, 9, 1, 1)


        self.gridLayout_229.addWidget(self.frame_16, 1, 0, 1, 1)

        self.stackedWidget_sagittal.addWidget(self.page_33)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_174 = QGridLayout(self.page_4)
        self.gridLayout_174.setObjectName(u"gridLayout_174")
        self.gridLayout_174.setContentsMargins(0, 0, 0, 0)
        self.textEdit_11 = QTextEdit(self.page_4)
        self.textEdit_11.setObjectName(u"textEdit_11")
        self.textEdit_11.setMinimumSize(QSize(0, 30))
        self.textEdit_11.setMaximumSize(QSize(16777215, 30))
        self.textEdit_11.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_11.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_11.setReadOnly(True)

        self.gridLayout_174.addWidget(self.textEdit_11, 0, 0, 1, 2)

        self.vtkWidget_trajPlan_2 = QVTKRenderWindowInteractor(self.page_4)
        self.vtkWidget_trajPlan_2.setObjectName(u"vtkWidget_trajPlan_2")
        self.vtkWidget_trajPlan_2.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_174.addWidget(self.vtkWidget_trajPlan_2, 1, 0, 1, 2)

        self.pushButton_resetSagittal = QPushButton(self.page_4)
        self.pushButton_resetSagittal.setObjectName(u"pushButton_resetSagittal")

        self.gridLayout_174.addWidget(self.pushButton_resetSagittal, 2, 0, 1, 2)

        self.stackedWidget_sagittal.addWidget(self.page_4)

        self.gridLayout_143.addWidget(self.stackedWidget_sagittal, 0, 1, 1, 1)

        self.stackedWidget_coronal = QStackedWidget(self.page_23)
        self.stackedWidget_coronal.setObjectName(u"stackedWidget_coronal")
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_182 = QGridLayout(self.page_7)
        self.gridLayout_182.setObjectName(u"gridLayout_182")
        self.gridLayout_182.setHorizontalSpacing(6)
        self.gridLayout_182.setContentsMargins(-1, 0, 0, 0)
        self.textEdit_9 = QTextEdit(self.page_7)
        self.textEdit_9.setObjectName(u"textEdit_9")
        self.textEdit_9.setMinimumSize(QSize(0, 30))
        self.textEdit_9.setMaximumSize(QSize(16777215, 30))
        self.textEdit_9.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_9.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_9.setReadOnly(True)

        self.gridLayout_182.addWidget(self.textEdit_9, 0, 0, 1, 1)

        self.frame_10 = QFrame(self.page_7)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 200))
        self.frame_10.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.gridLayout_145 = QGridLayout(self.frame_10)
        self.gridLayout_145.setSpacing(0)
        self.gridLayout_145.setObjectName(u"gridLayout_145")
        self.gridLayout_145.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.zoom_in_data3d2 = QToolButton(self.frame_10)
        self.zoom_in_data3d2.setObjectName(u"zoom_in_data3d2")
        self.zoom_in_data3d2.setIcon(icon4)

        self.horizontalLayout_35.addWidget(self.zoom_in_data3d2)

        self.zoom_out_data3d2 = QToolButton(self.frame_10)
        self.zoom_out_data3d2.setObjectName(u"zoom_out_data3d2")
        self.zoom_out_data3d2.setIcon(icon5)

        self.horizontalLayout_35.addWidget(self.zoom_out_data3d2)


        self.gridLayout_145.addLayout(self.horizontalLayout_35, 2, 7, 1, 1)

        self.fit_to_zoom_data3d2 = QPushButton(self.frame_10)
        self.fit_to_zoom_data3d2.setObjectName(u"fit_to_zoom_data3d2")
        self.fit_to_zoom_data3d2.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data3d2.setAutoDefault(False)
        self.fit_to_zoom_data3d2.setFlat(False)

        self.gridLayout_145.addWidget(self.fit_to_zoom_data3d2, 1, 0, 2, 1)

        self.vtkWidget_data_coronal = QVTKRenderWindowInteractor(self.frame_10)
        self.vtkWidget_data_coronal.setObjectName(u"vtkWidget_data_coronal")
        self.vtkWidget_data_coronal.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_145.addWidget(self.vtkWidget_data_coronal, 0, 0, 1, 9)

        self.Scroll_data3d2 = QScrollBar(self.frame_10)
        self.Scroll_data3d2.setObjectName(u"Scroll_data3d2")
        self.Scroll_data3d2.setPageStep(10)

        self.gridLayout_145.addWidget(self.Scroll_data3d2, 0, 9, 1, 1)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.go_down_data3d2 = QToolButton(self.frame_10)
        self.go_down_data3d2.setObjectName(u"go_down_data3d2")
        self.go_down_data3d2.setIcon(icon)

        self.horizontalLayout_34.addWidget(self.go_down_data3d2)

        self.go_up_data3d2 = QToolButton(self.frame_10)
        self.go_up_data3d2.setObjectName(u"go_up_data3d2")
        self.go_up_data3d2.setIcon(icon1)

        self.horizontalLayout_34.addWidget(self.go_up_data3d2)

        self.go_left_data3d2 = QToolButton(self.frame_10)
        self.go_left_data3d2.setObjectName(u"go_left_data3d2")
        self.go_left_data3d2.setIcon(icon2)

        self.horizontalLayout_34.addWidget(self.go_left_data3d2)

        self.go_right_data3d2 = QToolButton(self.frame_10)
        self.go_right_data3d2.setObjectName(u"go_right_data3d2")
        self.go_right_data3d2.setIcon(icon3)

        self.horizontalLayout_34.addWidget(self.go_right_data3d2)


        self.gridLayout_145.addLayout(self.horizontalLayout_34, 2, 8, 1, 1)

        self.vtkWidget_data_coronal.raise_()
        self.Scroll_data3d2.raise_()
        self.fit_to_zoom_data3d2.raise_()

        self.gridLayout_182.addWidget(self.frame_10, 1, 0, 1, 1)

        self.stackedWidget_coronal.addWidget(self.page_7)
        self.page_32 = QWidget()
        self.page_32.setObjectName(u"page_32")
        self.gridLayout_227 = QGridLayout(self.page_32)
        self.gridLayout_227.setObjectName(u"gridLayout_227")
        self.gridLayout_227.setContentsMargins(0, 0, 0, 0)
        self.textEdit_15 = QTextEdit(self.page_32)
        self.textEdit_15.setObjectName(u"textEdit_15")
        self.textEdit_15.setMinimumSize(QSize(0, 30))
        self.textEdit_15.setMaximumSize(QSize(16777215, 30))
        self.textEdit_15.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_15.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_15.setReadOnly(True)

        self.gridLayout_227.addWidget(self.textEdit_15, 0, 0, 1, 1)

        self.frame_14 = QFrame(self.page_32)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(0, 200))
        self.frame_14.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.gridLayout_226 = QGridLayout(self.frame_14)
        self.gridLayout_226.setSpacing(0)
        self.gridLayout_226.setObjectName(u"gridLayout_226")
        self.gridLayout_226.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.zoom_in_data3d2_3 = QToolButton(self.frame_14)
        self.zoom_in_data3d2_3.setObjectName(u"zoom_in_data3d2_3")
        self.zoom_in_data3d2_3.setIcon(icon4)

        self.horizontalLayout_42.addWidget(self.zoom_in_data3d2_3)

        self.zoom_out_data3d2_3 = QToolButton(self.frame_14)
        self.zoom_out_data3d2_3.setObjectName(u"zoom_out_data3d2_3")
        self.zoom_out_data3d2_3.setIcon(icon5)

        self.horizontalLayout_42.addWidget(self.zoom_out_data3d2_3)


        self.gridLayout_226.addLayout(self.horizontalLayout_42, 2, 7, 1, 1)

        self.fit_to_zoom_data3d2_3 = QPushButton(self.frame_14)
        self.fit_to_zoom_data3d2_3.setObjectName(u"fit_to_zoom_data3d2_3")
        self.fit_to_zoom_data3d2_3.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data3d2_3.setAutoDefault(False)
        self.fit_to_zoom_data3d2_3.setFlat(False)

        self.gridLayout_226.addWidget(self.fit_to_zoom_data3d2_3, 1, 0, 2, 1)

        self.vtkWidget_data_coronal_3 = QVTKRenderWindowInteractor(self.frame_14)
        self.vtkWidget_data_coronal_3.setObjectName(u"vtkWidget_data_coronal_3")
        self.vtkWidget_data_coronal_3.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_226.addWidget(self.vtkWidget_data_coronal_3, 0, 0, 1, 9)

        self.Scroll_data3d2_3 = QScrollBar(self.frame_14)
        self.Scroll_data3d2_3.setObjectName(u"Scroll_data3d2_3")
        self.Scroll_data3d2_3.setPageStep(10)

        self.gridLayout_226.addWidget(self.Scroll_data3d2_3, 0, 9, 1, 1)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.go_down_data3d2_3 = QToolButton(self.frame_14)
        self.go_down_data3d2_3.setObjectName(u"go_down_data3d2_3")
        self.go_down_data3d2_3.setIcon(icon)

        self.horizontalLayout_43.addWidget(self.go_down_data3d2_3)

        self.go_up_data3d2_3 = QToolButton(self.frame_14)
        self.go_up_data3d2_3.setObjectName(u"go_up_data3d2_3")
        self.go_up_data3d2_3.setIcon(icon1)

        self.horizontalLayout_43.addWidget(self.go_up_data3d2_3)

        self.go_left_data3d2_3 = QToolButton(self.frame_14)
        self.go_left_data3d2_3.setObjectName(u"go_left_data3d2_3")
        self.go_left_data3d2_3.setIcon(icon2)

        self.horizontalLayout_43.addWidget(self.go_left_data3d2_3)

        self.go_right_data3d2_3 = QToolButton(self.frame_14)
        self.go_right_data3d2_3.setObjectName(u"go_right_data3d2_3")
        self.go_right_data3d2_3.setIcon(icon3)

        self.horizontalLayout_43.addWidget(self.go_right_data3d2_3)


        self.gridLayout_226.addLayout(self.horizontalLayout_43, 2, 8, 1, 1)


        self.gridLayout_227.addWidget(self.frame_14, 1, 0, 1, 1)

        self.stackedWidget_coronal.addWidget(self.page_32)
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.gridLayout_184 = QGridLayout(self.page_10)
        self.gridLayout_184.setObjectName(u"gridLayout_184")
        self.gridLayout_184.setContentsMargins(0, 0, 0, 0)
        self.vtkWidget_trajPlan_1 = QVTKRenderWindowInteractor(self.page_10)
        self.vtkWidget_trajPlan_1.setObjectName(u"vtkWidget_trajPlan_1")
        self.vtkWidget_trajPlan_1.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_184.addWidget(self.vtkWidget_trajPlan_1, 1, 0, 1, 2)

        self.textEdit_10 = QTextEdit(self.page_10)
        self.textEdit_10.setObjectName(u"textEdit_10")
        self.textEdit_10.setMinimumSize(QSize(0, 30))
        self.textEdit_10.setMaximumSize(QSize(16777215, 30))
        self.textEdit_10.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_10.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_10.setReadOnly(True)

        self.gridLayout_184.addWidget(self.textEdit_10, 0, 0, 1, 2)

        self.pushButton_resetCoronal = QPushButton(self.page_10)
        self.pushButton_resetCoronal.setObjectName(u"pushButton_resetCoronal")

        self.gridLayout_184.addWidget(self.pushButton_resetCoronal, 2, 0, 1, 2)

        self.stackedWidget_coronal.addWidget(self.page_10)

        self.gridLayout_143.addWidget(self.stackedWidget_coronal, 0, 2, 1, 1)

        self.stackedWidget_axial = QStackedWidget(self.page_23)
        self.stackedWidget_axial.setObjectName(u"stackedWidget_axial")
        self.page_11 = QWidget()
        self.page_11.setObjectName(u"page_11")
        self.gridLayout_178 = QGridLayout(self.page_11)
        self.gridLayout_178.setObjectName(u"gridLayout_178")
        self.gridLayout_178.setContentsMargins(0, 0, 0, 0)
        self.textEdit_7 = QTextEdit(self.page_11)
        self.textEdit_7.setObjectName(u"textEdit_7")
        self.textEdit_7.setMinimumSize(QSize(0, 30))
        self.textEdit_7.setMaximumSize(QSize(16777215, 30))
        self.textEdit_7.setLayoutDirection(Qt.LeftToRight)
        self.textEdit_7.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_7.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_7.setReadOnly(True)

        self.gridLayout_178.addWidget(self.textEdit_7, 0, 0, 1, 1)

        self.frame_11 = QFrame(self.page_11)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 200))
        self.frame_11.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.gridLayout_146 = QGridLayout(self.frame_11)
        self.gridLayout_146.setSpacing(0)
        self.gridLayout_146.setObjectName(u"gridLayout_146")
        self.gridLayout_146.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.go_down_data3d0 = QToolButton(self.frame_11)
        self.go_down_data3d0.setObjectName(u"go_down_data3d0")
        self.go_down_data3d0.setIcon(icon)

        self.horizontalLayout_36.addWidget(self.go_down_data3d0)

        self.go_up_data3d0 = QToolButton(self.frame_11)
        self.go_up_data3d0.setObjectName(u"go_up_data3d0")
        self.go_up_data3d0.setIcon(icon1)

        self.horizontalLayout_36.addWidget(self.go_up_data3d0)

        self.go_left_data3d0 = QToolButton(self.frame_11)
        self.go_left_data3d0.setObjectName(u"go_left_data3d0")
        self.go_left_data3d0.setIcon(icon2)

        self.horizontalLayout_36.addWidget(self.go_left_data3d0)

        self.go_right_data3d0 = QToolButton(self.frame_11)
        self.go_right_data3d0.setObjectName(u"go_right_data3d0")
        self.go_right_data3d0.setIcon(icon3)

        self.horizontalLayout_36.addWidget(self.go_right_data3d0)


        self.gridLayout_146.addLayout(self.horizontalLayout_36, 2, 8, 1, 1)

        self.fit_to_zoom_data3d0 = QPushButton(self.frame_11)
        self.fit_to_zoom_data3d0.setObjectName(u"fit_to_zoom_data3d0")
        self.fit_to_zoom_data3d0.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data3d0.setAutoDefault(False)
        self.fit_to_zoom_data3d0.setFlat(False)

        self.gridLayout_146.addWidget(self.fit_to_zoom_data3d0, 1, 0, 2, 1)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.zoom_in_data3d0 = QToolButton(self.frame_11)
        self.zoom_in_data3d0.setObjectName(u"zoom_in_data3d0")
        self.zoom_in_data3d0.setIcon(icon4)

        self.horizontalLayout_37.addWidget(self.zoom_in_data3d0)

        self.zoom_out_data3d0 = QToolButton(self.frame_11)
        self.zoom_out_data3d0.setObjectName(u"zoom_out_data3d0")
        self.zoom_out_data3d0.setIcon(icon5)

        self.horizontalLayout_37.addWidget(self.zoom_out_data3d0)


        self.gridLayout_146.addLayout(self.horizontalLayout_37, 2, 7, 1, 1)

        self.Scroll_data3d0 = QScrollBar(self.frame_11)
        self.Scroll_data3d0.setObjectName(u"Scroll_data3d0")
        self.Scroll_data3d0.setPageStep(10)

        self.gridLayout_146.addWidget(self.Scroll_data3d0, 0, 9, 1, 1)

        self.vtkWidget_data_axial = QVTKRenderWindowInteractor(self.frame_11)
        self.vtkWidget_data_axial.setObjectName(u"vtkWidget_data_axial")
        self.vtkWidget_data_axial.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_146.addWidget(self.vtkWidget_data_axial, 0, 0, 1, 9)

        self.vtkWidget_data_axial.raise_()
        self.Scroll_data3d0.raise_()
        self.fit_to_zoom_data3d0.raise_()

        self.gridLayout_178.addWidget(self.frame_11, 1, 0, 1, 1)

        self.stackedWidget_axial.addWidget(self.page_11)
        self.page_14 = QWidget()
        self.page_14.setObjectName(u"page_14")
        self.gridLayout_196 = QGridLayout(self.page_14)
        self.gridLayout_196.setObjectName(u"gridLayout_196")
        self.gridLayout_196.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget_sagittal_2 = QStackedWidget(self.page_14)
        self.stackedWidget_sagittal_2.setObjectName(u"stackedWidget_sagittal_2")
        self.page_19 = QWidget()
        self.page_19.setObjectName(u"page_19")
        self.gridLayout_193 = QGridLayout(self.page_19)
        self.gridLayout_193.setObjectName(u"gridLayout_193")
        self.gridLayout_193.setContentsMargins(0, 0, 0, 0)
        self.textEdit_12 = QTextEdit(self.page_19)
        self.textEdit_12.setObjectName(u"textEdit_12")
        self.textEdit_12.setMinimumSize(QSize(0, 30))
        self.textEdit_12.setMaximumSize(QSize(16777215, 30))
        self.textEdit_12.setReadOnly(True)

        self.gridLayout_193.addWidget(self.textEdit_12, 0, 0, 1, 1)

        self.frame_12 = QFrame(self.page_19)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 200))
        self.frame_12.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.gridLayout_194 = QGridLayout(self.frame_12)
        self.gridLayout_194.setSpacing(0)
        self.gridLayout_194.setObjectName(u"gridLayout_194")
        self.gridLayout_194.setContentsMargins(4, 4, 4, 4)
        self.vtkWidget_data_sagittal_2 = QVTKRenderWindowInteractor(self.frame_12)
        self.vtkWidget_data_sagittal_2.setObjectName(u"vtkWidget_data_sagittal_2")
        self.vtkWidget_data_sagittal_2.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_194.addWidget(self.vtkWidget_data_sagittal_2, 1, 0, 1, 9)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.go_down_data3d1_2 = QToolButton(self.frame_12)
        self.go_down_data3d1_2.setObjectName(u"go_down_data3d1_2")
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.go_down_data3d1_2.setIcon(icon6)

        self.horizontalLayout_38.addWidget(self.go_down_data3d1_2)

        self.go_up_data3d1_2 = QToolButton(self.frame_12)
        self.go_up_data3d1_2.setObjectName(u"go_up_data3d1_2")
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.go_up_data3d1_2.setIcon(icon7)

        self.horizontalLayout_38.addWidget(self.go_up_data3d1_2)

        self.go_left_data3d1_2 = QToolButton(self.frame_12)
        self.go_left_data3d1_2.setObjectName(u"go_left_data3d1_2")

        self.horizontalLayout_38.addWidget(self.go_left_data3d1_2)

        self.go_right_data3d1_2 = QToolButton(self.frame_12)
        self.go_right_data3d1_2.setObjectName(u"go_right_data3d1_2")

        self.horizontalLayout_38.addWidget(self.go_right_data3d1_2)


        self.gridLayout_194.addLayout(self.horizontalLayout_38, 3, 8, 1, 1)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.zoom_in_data3d1_2 = QToolButton(self.frame_12)
        self.zoom_in_data3d1_2.setObjectName(u"zoom_in_data3d1_2")

        self.horizontalLayout_39.addWidget(self.zoom_in_data3d1_2)

        self.zoom_out_data3d1_2 = QToolButton(self.frame_12)
        self.zoom_out_data3d1_2.setObjectName(u"zoom_out_data3d1_2")

        self.horizontalLayout_39.addWidget(self.zoom_out_data3d1_2)


        self.gridLayout_194.addLayout(self.horizontalLayout_39, 3, 7, 1, 1)

        self.fit_to_zoom_data3d1_2 = QPushButton(self.frame_12)
        self.fit_to_zoom_data3d1_2.setObjectName(u"fit_to_zoom_data3d1_2")
        self.fit_to_zoom_data3d1_2.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data3d1_2.setAutoDefault(False)
        self.fit_to_zoom_data3d1_2.setFlat(False)

        self.gridLayout_194.addWidget(self.fit_to_zoom_data3d1_2, 2, 0, 2, 1)

        self.Scroll_data3d1_2 = QScrollBar(self.frame_12)
        self.Scroll_data3d1_2.setObjectName(u"Scroll_data3d1_2")
        self.Scroll_data3d1_2.setPageStep(10)

        self.gridLayout_194.addWidget(self.Scroll_data3d1_2, 1, 9, 1, 1)


        self.gridLayout_193.addWidget(self.frame_12, 1, 0, 1, 1)

        self.stackedWidget_sagittal_2.addWidget(self.page_19)
        self.page_20 = QWidget()
        self.page_20.setObjectName(u"page_20")
        self.gridLayout_195 = QGridLayout(self.page_20)
        self.gridLayout_195.setObjectName(u"gridLayout_195")
        self.gridLayout_195.setContentsMargins(0, 0, 0, 0)
        self.vtkWidget_trajPlan_3 = QVTKRenderWindowInteractor(self.page_20)
        self.vtkWidget_trajPlan_3.setObjectName(u"vtkWidget_trajPlan_3")
        self.vtkWidget_trajPlan_3.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_195.addWidget(self.vtkWidget_trajPlan_3, 2, 0, 1, 2)

        self.pushButton_resetAxial = QPushButton(self.page_20)
        self.pushButton_resetAxial.setObjectName(u"pushButton_resetAxial")

        self.gridLayout_195.addWidget(self.pushButton_resetAxial, 5, 0, 1, 2)

        self.lineEdit_59 = QLineEdit(self.page_20)
        self.lineEdit_59.setObjectName(u"lineEdit_59")
        self.lineEdit_59.setMaximumSize(QSize(1677215, 16777215))
        self.lineEdit_59.setReadOnly(True)

        self.gridLayout_195.addWidget(self.lineEdit_59, 3, 0, 1, 1)

        self.horizontalSlider_axial3D = QSlider(self.page_20)
        self.horizontalSlider_axial3D.setObjectName(u"horizontalSlider_axial3D")
        self.horizontalSlider_axial3D.setSingleStep(10)
        self.horizontalSlider_axial3D.setOrientation(Qt.Horizontal)

        self.gridLayout_195.addWidget(self.horizontalSlider_axial3D, 3, 1, 1, 1)

        self.textEdit_13 = QTextEdit(self.page_20)
        self.textEdit_13.setObjectName(u"textEdit_13")
        self.textEdit_13.setMinimumSize(QSize(0, 30))
        self.textEdit_13.setMaximumSize(QSize(16777215, 30))
        self.textEdit_13.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_13.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_13.setReadOnly(True)

        self.gridLayout_195.addWidget(self.textEdit_13, 1, 0, 1, 2)

        self.stackedWidget_sagittal_2.addWidget(self.page_20)

        self.gridLayout_196.addWidget(self.stackedWidget_sagittal_2, 0, 0, 1, 1)

        self.stackedWidget_axial.addWidget(self.page_14)

        self.gridLayout_143.addWidget(self.stackedWidget_axial, 0, 0, 1, 1)

        self.stackedWidget_3d_tp = QStackedWidget(self.page_23)
        self.stackedWidget_3d_tp.setObjectName(u"stackedWidget_3d_tp")
        self.stackedWidget_3d_tp.setMaximumSize(QSize(16777215, 300))
        self.page_29 = QWidget()
        self.page_29.setObjectName(u"page_29")
        self.page_29.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_211 = QGridLayout(self.page_29)
        self.gridLayout_211.setObjectName(u"gridLayout_211")
        self.gridLayout_211.setHorizontalSpacing(6)
        self.gridLayout_211.setVerticalSpacing(0)
        self.gridLayout_211.setContentsMargins(0, 0, 0, 0)
        self.groupBox_68 = QGroupBox(self.page_29)
        self.groupBox_68.setObjectName(u"groupBox_68")
        self.groupBox_68.setMaximumSize(QSize(16777215, 300))
        self.gridLayout_157 = QGridLayout(self.groupBox_68)
        self.gridLayout_157.setObjectName(u"gridLayout_157")
        self.lineEdit_68 = QLineEdit(self.groupBox_68)
        self.lineEdit_68.setObjectName(u"lineEdit_68")
        self.lineEdit_68.setReadOnly(True)

        self.gridLayout_157.addWidget(self.lineEdit_68, 0, 2, 1, 1)

        self.spinBox_y_data3d = QSpinBox(self.groupBox_68)
        self.spinBox_y_data3d.setObjectName(u"spinBox_y_data3d")
        self.spinBox_y_data3d.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data3d.setMinimum(1)
        self.spinBox_y_data3d.setMaximum(120)

        self.gridLayout_157.addWidget(self.spinBox_y_data3d, 1, 2, 1, 1)

        self.spinBox_z_data3d = QSpinBox(self.groupBox_68)
        self.spinBox_z_data3d.setObjectName(u"spinBox_z_data3d")
        self.spinBox_z_data3d.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data3d.setMinimum(1)
        self.spinBox_z_data3d.setMaximum(60)

        self.gridLayout_157.addWidget(self.spinBox_z_data3d, 1, 3, 1, 1)

        self.spinBox_x_data3d = QSpinBox(self.groupBox_68)
        self.spinBox_x_data3d.setObjectName(u"spinBox_x_data3d")
        self.spinBox_x_data3d.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_data3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_x_data3d.setMinimum(1)
        self.spinBox_x_data3d.setMaximum(120)

        self.gridLayout_157.addWidget(self.spinBox_x_data3d, 1, 1, 1, 1)

        self.lineEdit_67 = QLineEdit(self.groupBox_68)
        self.lineEdit_67.setObjectName(u"lineEdit_67")
        self.lineEdit_67.setReadOnly(True)

        self.gridLayout_157.addWidget(self.lineEdit_67, 0, 1, 1, 1)

        self.lineEdit_77 = QLineEdit(self.groupBox_68)
        self.lineEdit_77.setObjectName(u"lineEdit_77")
        self.lineEdit_77.setReadOnly(True)

        self.gridLayout_157.addWidget(self.lineEdit_77, 0, 3, 1, 1)


        self.gridLayout_211.addWidget(self.groupBox_68, 0, 0, 1, 1)

        self.groupBox_contrast = QGroupBox(self.page_29)
        self.groupBox_contrast.setObjectName(u"groupBox_contrast")
        self.groupBox_contrast.setMinimumSize(QSize(0, 0))
        self.groupBox_contrast.setMaximumSize(QSize(16777215, 300))
        self.gridLayout_162 = QGridLayout(self.groupBox_contrast)
        self.gridLayout_162.setObjectName(u"gridLayout_162")
        self.changeContrast_data3d = QSlider(self.groupBox_contrast)
        self.changeContrast_data3d.setObjectName(u"changeContrast_data3d")
        self.changeContrast_data3d.setStyleSheet(u"")
        self.changeContrast_data3d.setMaximum(99)
        self.changeContrast_data3d.setSingleStep(1)
        self.changeContrast_data3d.setPageStep(10)
        self.changeContrast_data3d.setValue(0)
        self.changeContrast_data3d.setOrientation(Qt.Horizontal)

        self.gridLayout_162.addWidget(self.changeContrast_data3d, 5, 0, 1, 2)

        self.label_35 = QLabel(self.groupBox_contrast)
        self.label_35.setObjectName(u"label_35")
        font6 = QFont()
        font6.setPointSize(10)
        font6.setBold(False)
        self.label_35.setFont(font6)

        self.gridLayout_162.addWidget(self.label_35, 2, 3, 1, 1)

        self.display_window_data3d = QSpinBox(self.groupBox_contrast)
        self.display_window_data3d.setObjectName(u"display_window_data3d")
        self.display_window_data3d.setEnabled(True)
        self.display_window_data3d.setReadOnly(True)
        self.display_window_data3d.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_162.addWidget(self.display_window_data3d, 2, 1, 1, 1)

        self.changeBrightness_data3d = QSlider(self.groupBox_contrast)
        self.changeBrightness_data3d.setObjectName(u"changeBrightness_data3d")
        self.changeBrightness_data3d.setMaximum(99)
        self.changeBrightness_data3d.setSingleStep(1)
        self.changeBrightness_data3d.setPageStep(10)
        self.changeBrightness_data3d.setValue(0)
        self.changeBrightness_data3d.setOrientation(Qt.Horizontal)

        self.gridLayout_162.addWidget(self.changeBrightness_data3d, 5, 3, 1, 2)

        self.pushButton_auto_data3d = QPushButton(self.groupBox_contrast)
        self.pushButton_auto_data3d.setObjectName(u"pushButton_auto_data3d")

        self.gridLayout_162.addWidget(self.pushButton_auto_data3d, 1, 3, 1, 2)

        self.pushButton_reset_data3d = QPushButton(self.groupBox_contrast)
        self.pushButton_reset_data3d.setObjectName(u"pushButton_reset_data3d")

        self.gridLayout_162.addWidget(self.pushButton_reset_data3d, 1, 0, 1, 2)

        self.display_level_data3d = QSpinBox(self.groupBox_contrast)
        self.display_level_data3d.setObjectName(u"display_level_data3d")
        self.display_level_data3d.setReadOnly(True)
        self.display_level_data3d.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_162.addWidget(self.display_level_data3d, 2, 4, 1, 1)

        self.label_36 = QLabel(self.groupBox_contrast)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font6)

        self.gridLayout_162.addWidget(self.label_36, 2, 0, 1, 1)

        self.comboBox_Contrastimage = QComboBox(self.groupBox_contrast)
        self.comboBox_Contrastimage.setObjectName(u"comboBox_Contrastimage")

        self.gridLayout_162.addWidget(self.comboBox_Contrastimage, 0, 0, 1, 5)

        self.gridLayout_162.setColumnStretch(0, 1)
        self.gridLayout_162.setColumnStretch(3, 1)

        self.gridLayout_211.addWidget(self.groupBox_contrast, 0, 1, 1, 1)

        self.groupBox_40 = QGroupBox(self.page_29)
        self.groupBox_40.setObjectName(u"groupBox_40")
        self.groupBox_40.setMinimumSize(QSize(100, 100))
        self.groupBox_40.setMaximumSize(QSize(16777215, 300))
        self.gridLayout_156 = QGridLayout(self.groupBox_40)
        self.gridLayout_156.setObjectName(u"gridLayout_156")
        self.gridLayout_156.setContentsMargins(-1, -1, 9, 9)
        self.tableintensity_data3d = QTableWidget(self.groupBox_40)
        if (self.tableintensity_data3d.columnCount() < 4):
            self.tableintensity_data3d.setColumnCount(4)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(3, __qtablewidgetitem11)
        self.tableintensity_data3d.setObjectName(u"tableintensity_data3d")
        sizePolicy3.setHeightForWidth(self.tableintensity_data3d.sizePolicy().hasHeightForWidth())
        self.tableintensity_data3d.setSizePolicy(sizePolicy3)
        self.tableintensity_data3d.setMaximumSize(QSize(700, 1677))
        self.tableintensity_data3d.setContextMenuPolicy(Qt.NoContextMenu)
        self.tableintensity_data3d.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableintensity_data3d.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableintensity_data3d.horizontalHeader().setDefaultSectionSize(67)

        self.gridLayout_156.addWidget(self.tableintensity_data3d, 1, 0, 1, 1)


        self.gridLayout_211.addWidget(self.groupBox_40, 0, 2, 1, 1)

        self.gridLayout_211.setColumnStretch(0, 1)
        self.gridLayout_211.setColumnStretch(1, 1)
        self.gridLayout_211.setColumnStretch(2, 1)
        self.stackedWidget_3d_tp.addWidget(self.page_29)
        self.page_30 = QWidget()
        self.page_30.setObjectName(u"page_30")
        self.gridLayout_214 = QGridLayout(self.page_30)
        self.gridLayout_214.setObjectName(u"gridLayout_214")
        self.gridLayout_214.setHorizontalSpacing(6)
        self.gridLayout_214.setContentsMargins(0, 0, 0, 0)
        self.groupBox_70 = QGroupBox(self.page_30)
        self.groupBox_70.setObjectName(u"groupBox_70")
        self.groupBox_70.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_212 = QGridLayout(self.groupBox_70)
        self.gridLayout_212.setObjectName(u"gridLayout_212")
        self.spinBox_x_data3d_2 = QSpinBox(self.groupBox_70)
        self.spinBox_x_data3d_2.setObjectName(u"spinBox_x_data3d_2")
        self.spinBox_x_data3d_2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_data3d_2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_x_data3d_2.setMinimum(1)
        self.spinBox_x_data3d_2.setMaximum(512)

        self.gridLayout_212.addWidget(self.spinBox_x_data3d_2, 1, 1, 1, 1)

        self.lineEdit_80 = QLineEdit(self.groupBox_70)
        self.lineEdit_80.setObjectName(u"lineEdit_80")
        self.lineEdit_80.setReadOnly(True)

        self.gridLayout_212.addWidget(self.lineEdit_80, 0, 3, 1, 1)

        self.spinBox_z_data3d_2 = QSpinBox(self.groupBox_70)
        self.spinBox_z_data3d_2.setObjectName(u"spinBox_z_data3d_2")
        self.spinBox_z_data3d_2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data3d_2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data3d_2.setMinimum(1)
        self.spinBox_z_data3d_2.setMaximum(512)

        self.gridLayout_212.addWidget(self.spinBox_z_data3d_2, 1, 3, 1, 1)

        self.spinBox_y_data3d_2 = QSpinBox(self.groupBox_70)
        self.spinBox_y_data3d_2.setObjectName(u"spinBox_y_data3d_2")
        self.spinBox_y_data3d_2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data3d_2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data3d_2.setMinimum(1)
        self.spinBox_y_data3d_2.setMaximum(1024)

        self.gridLayout_212.addWidget(self.spinBox_y_data3d_2, 1, 2, 1, 1)

        self.lineEdit_78 = QLineEdit(self.groupBox_70)
        self.lineEdit_78.setObjectName(u"lineEdit_78")
        self.lineEdit_78.setReadOnly(True)

        self.gridLayout_212.addWidget(self.lineEdit_78, 0, 2, 1, 1)

        self.lineEdit_79 = QLineEdit(self.groupBox_70)
        self.lineEdit_79.setObjectName(u"lineEdit_79")
        self.lineEdit_79.setReadOnly(True)

        self.gridLayout_212.addWidget(self.lineEdit_79, 0, 1, 1, 1)


        self.gridLayout_214.addWidget(self.groupBox_70, 0, 0, 1, 1)

        self.groupBox_72 = QGroupBox(self.page_30)
        self.groupBox_72.setObjectName(u"groupBox_72")
        self.gridLayout_215 = QGridLayout(self.groupBox_72)
        self.gridLayout_215.setObjectName(u"gridLayout_215")
        self.doubleSpinBox_distance_shank = QDoubleSpinBox(self.groupBox_72)
        self.doubleSpinBox_distance_shank.setObjectName(u"doubleSpinBox_distance_shank")
        self.doubleSpinBox_distance_shank.setEnabled(False)
        self.doubleSpinBox_distance_shank.setReadOnly(True)
        self.doubleSpinBox_distance_shank.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_distance_shank.setMaximum(99.000000000000000)

        self.gridLayout_215.addWidget(self.doubleSpinBox_distance_shank, 3, 0, 1, 2)

        self.textEdit_distance_shank = QTextEdit(self.groupBox_72)
        self.textEdit_distance_shank.setObjectName(u"textEdit_distance_shank")
        self.textEdit_distance_shank.setEnabled(False)
        self.textEdit_distance_shank.setMinimumSize(QSize(0, 50))
        self.textEdit_distance_shank.setReadOnly(True)

        self.gridLayout_215.addWidget(self.textEdit_distance_shank, 2, 0, 1, 2)


        self.gridLayout_214.addWidget(self.groupBox_72, 3, 3, 1, 1)

        self.groupBox_74 = QGroupBox(self.page_30)
        self.groupBox_74.setObjectName(u"groupBox_74")
        self.gridLayout_188 = QGridLayout(self.groupBox_74)
        self.gridLayout_188.setObjectName(u"gridLayout_188")
        self.pushButton_tp_deep = QPushButton(self.groupBox_74)
        self.pushButton_tp_deep.setObjectName(u"pushButton_tp_deep")
        self.pushButton_tp_deep.setMinimumSize(QSize(0, 50))
        self.pushButton_tp_deep.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_tp_deep.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_188.addWidget(self.pushButton_tp_deep, 0, 0, 1, 3)

        self.spinBox_tp_deep_z = QSpinBox(self.groupBox_74)
        self.spinBox_tp_deep_z.setObjectName(u"spinBox_tp_deep_z")
        self.spinBox_tp_deep_z.setMaximum(1000)

        self.gridLayout_188.addWidget(self.spinBox_tp_deep_z, 2, 2, 1, 1)

        self.spinBox_tp_deep_x = QSpinBox(self.groupBox_74)
        self.spinBox_tp_deep_x.setObjectName(u"spinBox_tp_deep_x")
        self.spinBox_tp_deep_x.setMaximum(1000)

        self.gridLayout_188.addWidget(self.spinBox_tp_deep_x, 2, 0, 1, 1)

        self.spinBox_tp_deep_y = QSpinBox(self.groupBox_74)
        self.spinBox_tp_deep_y.setObjectName(u"spinBox_tp_deep_y")
        self.spinBox_tp_deep_y.setMaximum(1000)

        self.gridLayout_188.addWidget(self.spinBox_tp_deep_y, 2, 1, 1, 1)

        self.lineEdit_89 = QLineEdit(self.groupBox_74)
        self.lineEdit_89.setObjectName(u"lineEdit_89")
        self.lineEdit_89.setReadOnly(True)

        self.gridLayout_188.addWidget(self.lineEdit_89, 1, 0, 1, 1)

        self.lineEdit_90 = QLineEdit(self.groupBox_74)
        self.lineEdit_90.setObjectName(u"lineEdit_90")
        self.lineEdit_90.setReadOnly(True)

        self.gridLayout_188.addWidget(self.lineEdit_90, 1, 1, 1, 1)

        self.lineEdit_91 = QLineEdit(self.groupBox_74)
        self.lineEdit_91.setObjectName(u"lineEdit_91")
        self.lineEdit_91.setReadOnly(True)

        self.gridLayout_188.addWidget(self.lineEdit_91, 1, 2, 1, 1)


        self.gridLayout_214.addWidget(self.groupBox_74, 1, 2, 3, 1)

        self.groupBox_71 = QGroupBox(self.page_30)
        self.groupBox_71.setObjectName(u"groupBox_71")
        self.groupBox_71.setMinimumSize(QSize(100, 100))
        self.groupBox_71.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_213 = QGridLayout(self.groupBox_71)
        self.gridLayout_213.setObjectName(u"gridLayout_213")
        self.gridLayout_213.setContentsMargins(-1, -1, 9, 9)
        self.tableintensity_data3d_2 = QTableWidget(self.groupBox_71)
        if (self.tableintensity_data3d_2.columnCount() < 4):
            self.tableintensity_data3d_2.setColumnCount(4)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableintensity_data3d_2.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableintensity_data3d_2.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableintensity_data3d_2.setHorizontalHeaderItem(2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableintensity_data3d_2.setHorizontalHeaderItem(3, __qtablewidgetitem15)
        self.tableintensity_data3d_2.setObjectName(u"tableintensity_data3d_2")
        sizePolicy3.setHeightForWidth(self.tableintensity_data3d_2.sizePolicy().hasHeightForWidth())
        self.tableintensity_data3d_2.setSizePolicy(sizePolicy3)
        self.tableintensity_data3d_2.setMaximumSize(QSize(700, 1677))
        self.tableintensity_data3d_2.setContextMenuPolicy(Qt.NoContextMenu)
        self.tableintensity_data3d_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableintensity_data3d_2.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableintensity_data3d_2.horizontalHeader().setDefaultSectionSize(67)

        self.gridLayout_213.addWidget(self.tableintensity_data3d_2, 1, 0, 1, 1)

        self.pushButton_contrastAdjustments = QPushButton(self.groupBox_71)
        self.pushButton_contrastAdjustments.setObjectName(u"pushButton_contrastAdjustments")

        self.gridLayout_213.addWidget(self.pushButton_contrastAdjustments, 2, 0, 1, 1)


        self.gridLayout_214.addWidget(self.groupBox_71, 1, 0, 3, 1)

        self.checkBox_brain_region = QCheckBox(self.page_30)
        self.checkBox_brain_region.setObjectName(u"checkBox_brain_region")
        self.checkBox_brain_region.setChecked(True)

        self.gridLayout_214.addWidget(self.checkBox_brain_region, 2, 3, 1, 1)

        self.groupBox_75 = QGroupBox(self.page_30)
        self.groupBox_75.setObjectName(u"groupBox_75")
        self.gridLayout_189 = QGridLayout(self.groupBox_75)
        self.gridLayout_189.setObjectName(u"gridLayout_189")
        self.pushButton_tp_insert = QPushButton(self.groupBox_75)
        self.pushButton_tp_insert.setObjectName(u"pushButton_tp_insert")
        self.pushButton_tp_insert.setMinimumSize(QSize(0, 50))
        self.pushButton_tp_insert.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_tp_insert.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_189.addWidget(self.pushButton_tp_insert, 0, 1, 1, 3)

        self.spinBox_tp_insert_x = QSpinBox(self.groupBox_75)
        self.spinBox_tp_insert_x.setObjectName(u"spinBox_tp_insert_x")
        self.spinBox_tp_insert_x.setReadOnly(True)
        self.spinBox_tp_insert_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_tp_insert_x.setMaximum(1000)

        self.gridLayout_189.addWidget(self.spinBox_tp_insert_x, 2, 1, 1, 1)

        self.spinBox_tp_insert_y = QSpinBox(self.groupBox_75)
        self.spinBox_tp_insert_y.setObjectName(u"spinBox_tp_insert_y")
        self.spinBox_tp_insert_y.setReadOnly(True)
        self.spinBox_tp_insert_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_tp_insert_y.setMaximum(1000)

        self.gridLayout_189.addWidget(self.spinBox_tp_insert_y, 2, 2, 1, 1)

        self.spinBox_tp_insert_z = QSpinBox(self.groupBox_75)
        self.spinBox_tp_insert_z.setObjectName(u"spinBox_tp_insert_z")
        self.spinBox_tp_insert_z.setReadOnly(True)
        self.spinBox_tp_insert_z.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_tp_insert_z.setMaximum(1000)

        self.gridLayout_189.addWidget(self.spinBox_tp_insert_z, 2, 3, 1, 1)

        self.lineEdit_19 = QLineEdit(self.groupBox_75)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        self.lineEdit_19.setReadOnly(True)

        self.gridLayout_189.addWidget(self.lineEdit_19, 1, 1, 1, 1)

        self.lineEdit_30 = QLineEdit(self.groupBox_75)
        self.lineEdit_30.setObjectName(u"lineEdit_30")
        self.lineEdit_30.setReadOnly(True)

        self.gridLayout_189.addWidget(self.lineEdit_30, 1, 2, 1, 1)

        self.lineEdit_88 = QLineEdit(self.groupBox_75)
        self.lineEdit_88.setObjectName(u"lineEdit_88")
        self.lineEdit_88.setReadOnly(True)

        self.gridLayout_189.addWidget(self.lineEdit_88, 1, 3, 1, 1)


        self.gridLayout_214.addWidget(self.groupBox_75, 0, 2, 1, 1)

        self.groupBox_73 = QGroupBox(self.page_30)
        self.groupBox_73.setObjectName(u"groupBox_73")
        self.gridLayout_216 = QGridLayout(self.groupBox_73)
        self.gridLayout_216.setObjectName(u"gridLayout_216")
        self.pushButton_removeShank = QPushButton(self.groupBox_73)
        self.pushButton_removeShank.setObjectName(u"pushButton_removeShank")
        self.pushButton_removeShank.setMaximumSize(QSize(16777215, 40))
        self.pushButton_removeShank.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_216.addWidget(self.pushButton_removeShank, 5, 0, 1, 1)

        self.comboBox_Shanks = QComboBox(self.groupBox_73)
        self.comboBox_Shanks.setObjectName(u"comboBox_Shanks")
        self.comboBox_Shanks.setMinimumSize(QSize(0, 50))
        self.comboBox_Shanks.setFont(font3)

        self.gridLayout_216.addWidget(self.comboBox_Shanks, 1, 0, 1, 1)

        self.comboBox_tpColor = QComboBox(self.groupBox_73)
        self.comboBox_tpColor.setObjectName(u"comboBox_tpColor")
        self.comboBox_tpColor.setMinimumSize(QSize(0, 50))
        self.comboBox_tpColor.setFont(font3)

        self.gridLayout_216.addWidget(self.comboBox_tpColor, 3, 0, 1, 1)

        self.pushButton_addShank = QPushButton(self.groupBox_73)
        self.pushButton_addShank.setObjectName(u"pushButton_addShank")
        self.pushButton_addShank.setMaximumSize(QSize(16777215, 40))
        self.pushButton_addShank.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_216.addWidget(self.pushButton_addShank, 4, 0, 1, 1)


        self.gridLayout_214.addWidget(self.groupBox_73, 0, 1, 4, 1)

        self.frame = QFrame(self.page_30)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_177 = QGridLayout(self.frame)
        self.gridLayout_177.setObjectName(u"gridLayout_177")
        self.pushButton_sagittalView = QPushButton(self.frame)
        self.pushButton_sagittalView.setObjectName(u"pushButton_sagittalView")
        self.pushButton_sagittalView.setEnabled(False)
        self.pushButton_sagittalView.setCheckable(True)
        self.pushButton_sagittalView.setChecked(True)

        self.gridLayout_177.addWidget(self.pushButton_sagittalView, 2, 1, 1, 1)

        self.pushButton_coronalView = QPushButton(self.frame)
        self.pushButton_coronalView.setObjectName(u"pushButton_coronalView")
        self.pushButton_coronalView.setEnabled(False)
        self.pushButton_coronalView.setCheckable(True)
        self.pushButton_coronalView.setChecked(True)

        self.gridLayout_177.addWidget(self.pushButton_coronalView, 2, 2, 1, 1)

        self.checkBox_constraint_90deg_coronal = QCheckBox(self.frame)
        self.checkBox_constraint_90deg_coronal.setObjectName(u"checkBox_constraint_90deg_coronal")
        font7 = QFont()
        font7.setPointSize(13)
        self.checkBox_constraint_90deg_coronal.setFont(font7)

        self.gridLayout_177.addWidget(self.checkBox_constraint_90deg_coronal, 1, 0, 1, 3)

        self.checkBox_constraint_90deg = QCheckBox(self.frame)
        self.checkBox_constraint_90deg.setObjectName(u"checkBox_constraint_90deg")
        self.checkBox_constraint_90deg.setEnabled(True)
        self.checkBox_constraint_90deg.setFont(font7)

        self.gridLayout_177.addWidget(self.checkBox_constraint_90deg, 0, 0, 1, 3)

        self.pushButton_axialView = QPushButton(self.frame)
        self.pushButton_axialView.setObjectName(u"pushButton_axialView")
        self.pushButton_axialView.setEnabled(False)
        self.pushButton_axialView.setCheckable(True)
        self.pushButton_axialView.setChecked(True)

        self.gridLayout_177.addWidget(self.pushButton_axialView, 2, 0, 1, 1)

        self.gridLayout_177.setColumnStretch(0, 1)
        self.gridLayout_177.setColumnStretch(1, 1)
        self.gridLayout_177.setColumnStretch(2, 1)

        self.gridLayout_214.addWidget(self.frame, 0, 3, 1, 1)

        self.gridLayout_214.setColumnStretch(0, 1)
        self.gridLayout_214.setColumnStretch(1, 1)
        self.gridLayout_214.setColumnStretch(2, 1)
        self.gridLayout_214.setColumnStretch(3, 1)
        self.stackedWidget_3d_tp.addWidget(self.page_30)

        self.gridLayout_143.addWidget(self.stackedWidget_3d_tp, 2, 0, 1, 3)

        self.gridLayout_143.setColumnStretch(0, 1)
        self.gridLayout_143.setColumnStretch(1, 1)
        self.gridLayout_143.setColumnStretch(2, 1)
        self.stackedWidget_dfx.addWidget(self.page_23)
        self.page_24 = QWidget()
        self.page_24.setObjectName(u"page_24")
        self.gridLayout_149 = QGridLayout(self.page_24)
        self.gridLayout_149.setObjectName(u"gridLayout_149")
        self.widget_dfx = QWidget(self.page_24)
        self.widget_dfx.setObjectName(u"widget_dfx")

        self.gridLayout_149.addWidget(self.widget_dfx, 1, 1, 1, 2)

        self.pushButton_dfx_ok = QPushButton(self.page_24)
        self.pushButton_dfx_ok.setObjectName(u"pushButton_dfx_ok")
        self.pushButton_dfx_ok.setMinimumSize(QSize(0, 50))
        self.pushButton_dfx_ok.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")
        self.pushButton_dfx_ok.setIconSize(QSize(20, 20))

        self.gridLayout_149.addWidget(self.pushButton_dfx_ok, 2, 2, 1, 1)

        self.pushButton_plot_probe = QPushButton(self.page_24)
        self.pushButton_plot_probe.setObjectName(u"pushButton_plot_probe")
        self.pushButton_plot_probe.setMinimumSize(QSize(0, 50))
        self.pushButton_plot_probe.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_149.addWidget(self.pushButton_plot_probe, 2, 1, 1, 1)

        self.groupBox_69 = QGroupBox(self.page_24)
        self.groupBox_69.setObjectName(u"groupBox_69")
        self.gridLayout_208 = QGridLayout(self.groupBox_69)
        self.gridLayout_208.setObjectName(u"gridLayout_208")
        self.doubleSpinBox_bundle_ratio = QDoubleSpinBox(self.groupBox_69)
        self.doubleSpinBox_bundle_ratio.setObjectName(u"doubleSpinBox_bundle_ratio")
        self.doubleSpinBox_bundle_ratio.setValue(0.100000000000000)

        self.gridLayout_208.addWidget(self.doubleSpinBox_bundle_ratio, 5, 2, 1, 1)

        self.pushButton_xml = QPushButton(self.groupBox_69)
        self.pushButton_xml.setObjectName(u"pushButton_xml")
        self.pushButton_xml.setMinimumSize(QSize(0, 50))
        self.pushButton_xml.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_208.addWidget(self.pushButton_xml, 10, 0, 1, 3)

        self.pushButton_dfx_run = QPushButton(self.groupBox_69)
        self.pushButton_dfx_run.setObjectName(u"pushButton_dfx_run")
        self.pushButton_dfx_run.setMinimumSize(QSize(0, 50))
        self.pushButton_dfx_run.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_208.addWidget(self.pushButton_dfx_run, 12, 0, 1, 1)

        self.lineEdit_76 = QLineEdit(self.groupBox_69)
        self.lineEdit_76.setObjectName(u"lineEdit_76")
        self.lineEdit_76.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_76, 4, 0, 1, 1)

        self.lineEdit_73 = QLineEdit(self.groupBox_69)
        self.lineEdit_73.setObjectName(u"lineEdit_73")
        self.lineEdit_73.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_73, 2, 0, 1, 1)

        self.textEdit_channels_xml = QTextEdit(self.groupBox_69)
        self.textEdit_channels_xml.setObjectName(u"textEdit_channels_xml")

        self.gridLayout_208.addWidget(self.textEdit_channels_xml, 11, 0, 1, 3)

        self.spinBox_max_bend_angle = QSpinBox(self.groupBox_69)
        self.spinBox_max_bend_angle.setObjectName(u"spinBox_max_bend_angle")
        self.spinBox_max_bend_angle.setMaximum(1000)
        self.spinBox_max_bend_angle.setValue(50)

        self.gridLayout_208.addWidget(self.spinBox_max_bend_angle, 4, 2, 1, 1)

        self.lineEdit_74 = QLineEdit(self.groupBox_69)
        self.lineEdit_74.setObjectName(u"lineEdit_74")
        self.lineEdit_74.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_74, 5, 0, 1, 1)

        self.lineEdit_72 = QLineEdit(self.groupBox_69)
        self.lineEdit_72.setObjectName(u"lineEdit_72")
        self.lineEdit_72.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_72, 6, 0, 1, 1)

        self.lineEdit_70 = QLineEdit(self.groupBox_69)
        self.lineEdit_70.setObjectName(u"lineEdit_70")
        self.lineEdit_70.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_70, 8, 0, 1, 1)

        self.lineEdit_69 = QLineEdit(self.groupBox_69)
        self.lineEdit_69.setObjectName(u"lineEdit_69")
        self.lineEdit_69.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_69, 1, 0, 1, 1)

        self.spinBox_bend_r1 = QSpinBox(self.groupBox_69)
        self.spinBox_bend_r1.setObjectName(u"spinBox_bend_r1")
        self.spinBox_bend_r1.setMaximum(1000)
        self.spinBox_bend_r1.setValue(400)

        self.gridLayout_208.addWidget(self.spinBox_bend_r1, 6, 2, 1, 1)

        self.spinBox_first_bend_distance = QSpinBox(self.groupBox_69)
        self.spinBox_first_bend_distance.setObjectName(u"spinBox_first_bend_distance")
        self.spinBox_first_bend_distance.setMaximum(1000)
        self.spinBox_first_bend_distance.setValue(200)

        self.gridLayout_208.addWidget(self.spinBox_first_bend_distance, 3, 2, 1, 1)

        self.pushButton_export = QPushButton(self.groupBox_69)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setMinimumSize(QSize(0, 50))

        self.gridLayout_208.addWidget(self.pushButton_export, 12, 2, 1, 1)

        self.spinBox_um_per_unit = QSpinBox(self.groupBox_69)
        self.spinBox_um_per_unit.setObjectName(u"spinBox_um_per_unit")
        self.spinBox_um_per_unit.setValue(1)

        self.gridLayout_208.addWidget(self.spinBox_um_per_unit, 1, 2, 1, 1)

        self.spinBox_bend_r2 = QSpinBox(self.groupBox_69)
        self.spinBox_bend_r2.setObjectName(u"spinBox_bend_r2")
        self.spinBox_bend_r2.setMaximum(1000)
        self.spinBox_bend_r2.setValue(400)

        self.gridLayout_208.addWidget(self.spinBox_bend_r2, 7, 2, 1, 1)

        self.checkBox_defaultchannels = QCheckBox(self.groupBox_69)
        self.checkBox_defaultchannels.setObjectName(u"checkBox_defaultchannels")
        self.checkBox_defaultchannels.setChecked(True)

        self.gridLayout_208.addWidget(self.checkBox_defaultchannels, 9, 0, 1, 3)

        self.spinBox_arc_points = QSpinBox(self.groupBox_69)
        self.spinBox_arc_points.setObjectName(u"spinBox_arc_points")
        self.spinBox_arc_points.setMaximum(1000)
        self.spinBox_arc_points.setValue(200)

        self.gridLayout_208.addWidget(self.spinBox_arc_points, 8, 2, 1, 1)

        self.lineEdit_71 = QLineEdit(self.groupBox_69)
        self.lineEdit_71.setObjectName(u"lineEdit_71")
        self.lineEdit_71.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_71, 7, 0, 1, 1)

        self.spinBox_artificial_extension = QSpinBox(self.groupBox_69)
        self.spinBox_artificial_extension.setObjectName(u"spinBox_artificial_extension")
        self.spinBox_artificial_extension.setMaximum(10000)
        self.spinBox_artificial_extension.setValue(3000)

        self.gridLayout_208.addWidget(self.spinBox_artificial_extension, 2, 2, 1, 1)

        self.lineEdit_75 = QLineEdit(self.groupBox_69)
        self.lineEdit_75.setObjectName(u"lineEdit_75")
        self.lineEdit_75.setReadOnly(True)

        self.gridLayout_208.addWidget(self.lineEdit_75, 3, 0, 1, 1)

        self.pushButton_dfx = QPushButton(self.groupBox_69)
        self.pushButton_dfx.setObjectName(u"pushButton_dfx")
        self.pushButton_dfx.setMinimumSize(QSize(0, 50))
        self.pushButton_dfx.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_208.addWidget(self.pushButton_dfx, 0, 0, 1, 3)


        self.gridLayout_149.addWidget(self.groupBox_69, 0, 0, 3, 1)

        self.comboBox_geometry_shanks = QComboBox(self.page_24)
        self.comboBox_geometry_shanks.setObjectName(u"comboBox_geometry_shanks")
        self.comboBox_geometry_shanks.setMinimumSize(QSize(0, 50))
        self.comboBox_geometry_shanks.setFont(font5)

        self.gridLayout_149.addWidget(self.comboBox_geometry_shanks, 0, 1, 1, 2)

        self.gridLayout_149.setColumnStretch(0, 2)
        self.gridLayout_149.setColumnStretch(1, 1)
        self.gridLayout_149.setColumnStretch(2, 1)
        self.stackedWidget_dfx.addWidget(self.page_24)

        self.gridLayout_106.addWidget(self.stackedWidget_dfx, 1, 0, 1, 3)

        self.gridLayout_106.setColumnStretch(0, 1)
        self.data_4d_3d.addWidget(self.page_3D)

        self.gridLayout_7.addWidget(self.data_4d_3d, 0, 0, 1, 1)

        self.gridLayout_7.setRowStretch(0, 1)

        self.gridLayout_70.addWidget(self.groupBox_data0, 1, 1, 1, 4)

        self.pushButton_metadata = QPushButton(self.PostSurgery)
        self.pushButton_metadata.setObjectName(u"pushButton_metadata")
        self.pushButton_metadata.setMaximumSize(QSize(50, 16777215))
        icon8 = QIcon()
        icon8.addFile(u"Icons/mri/person14.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_metadata.setIcon(icon8)
        self.pushButton_metadata.setIconSize(QSize(32, 32))

        self.gridLayout_70.addWidget(self.pushButton_metadata, 0, 4, 1, 1)

        self.groupBox_data1 = QGroupBox(self.PostSurgery)
        self.groupBox_data1.setObjectName(u"groupBox_data1")
        self.gridLayout_89 = QGridLayout(self.groupBox_data1)
        self.gridLayout_89.setObjectName(u"gridLayout_89")
        self.groupbox_legend1 = QGroupBox(self.groupBox_data1)
        self.groupbox_legend1.setObjectName(u"groupbox_legend1")
        self.groupbox_legend1.setMaximumSize(QSize(16777215, 120))
        self.gridLayout_113 = QGridLayout(self.groupbox_legend1)
        self.gridLayout_113.setObjectName(u"gridLayout_113")
        self.frame_30 = QFrame(self.groupbox_legend1)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setEnabled(True)
        self.frame_30.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_30.setFrameShape(QFrame.NoFrame)
        self.gridLayout_114 = QGridLayout(self.frame_30)
        self.gridLayout_114.setSpacing(0)
        self.gridLayout_114.setObjectName(u"gridLayout_114")
        self.gridLayout_114.setContentsMargins(4, 4, 4, 4)
        self.vtkWidget_legend1 = QVTKRenderWindowInteractor(self.frame_30)
        self.vtkWidget_legend1.setObjectName(u"vtkWidget_legend1")
        self.vtkWidget_legend1.setEnabled(True)
        self.vtkWidget_legend1.setMinimumSize(QSize(0, 30))
        self.vtkWidget_legend1.setMaximumSize(QSize(16777215, 167))
        self.vtkWidget_legend1.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_114.addWidget(self.vtkWidget_legend1, 0, 0, 1, 1)


        self.gridLayout_113.addWidget(self.frame_30, 0, 0, 1, 1)


        self.gridLayout_89.addWidget(self.groupbox_legend1, 1, 3, 1, 1)

        self.groupBox_time11 = QGroupBox(self.groupBox_data1)
        self.groupBox_time11.setObjectName(u"groupBox_time11")
        sizePolicy2.setHeightForWidth(self.groupBox_time11.sizePolicy().hasHeightForWidth())
        self.groupBox_time11.setSizePolicy(sizePolicy2)
        self.groupBox_time11.setFont(font1)
        self.gridLayout_85 = QGridLayout(self.groupBox_time11)
        self.gridLayout_85.setObjectName(u"gridLayout_85")
        self.frame_7 = QFrame(self.groupBox_time11)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 200))
        self.frame_7.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.gridLayout_82 = QGridLayout(self.frame_7)
        self.gridLayout_82.setSpacing(0)
        self.gridLayout_82.setObjectName(u"gridLayout_82")
        self.gridLayout_82.setContentsMargins(4, 4, 4, 4)
        self.fit_to_zoom_data11 = QPushButton(self.frame_7)
        self.fit_to_zoom_data11.setObjectName(u"fit_to_zoom_data11")
        self.fit_to_zoom_data11.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data11.setAutoDefault(False)
        self.fit_to_zoom_data11.setFlat(False)

        self.gridLayout_82.addWidget(self.fit_to_zoom_data11, 1, 0, 2, 1)

        self.vtkWidget_data11 = QVTKRenderWindowInteractor(self.frame_7)
        self.vtkWidget_data11.setObjectName(u"vtkWidget_data11")
        self.vtkWidget_data11.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_82.addWidget(self.vtkWidget_data11, 0, 0, 1, 9)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.go_down_data11 = QToolButton(self.frame_7)
        self.go_down_data11.setObjectName(u"go_down_data11")
        self.go_down_data11.setIcon(icon)

        self.horizontalLayout_18.addWidget(self.go_down_data11)

        self.go_up_data11 = QToolButton(self.frame_7)
        self.go_up_data11.setObjectName(u"go_up_data11")
        self.go_up_data11.setIcon(icon1)

        self.horizontalLayout_18.addWidget(self.go_up_data11)

        self.go_left_data11 = QToolButton(self.frame_7)
        self.go_left_data11.setObjectName(u"go_left_data11")
        self.go_left_data11.setIcon(icon2)

        self.horizontalLayout_18.addWidget(self.go_left_data11)

        self.go_right_data11 = QToolButton(self.frame_7)
        self.go_right_data11.setObjectName(u"go_right_data11")
        self.go_right_data11.setIcon(icon3)

        self.horizontalLayout_18.addWidget(self.go_right_data11)


        self.gridLayout_82.addLayout(self.horizontalLayout_18, 2, 8, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.zoom_in_data11 = QToolButton(self.frame_7)
        self.zoom_in_data11.setObjectName(u"zoom_in_data11")
        self.zoom_in_data11.setIcon(icon4)

        self.horizontalLayout_3.addWidget(self.zoom_in_data11)

        self.zoom_out_data11 = QToolButton(self.frame_7)
        self.zoom_out_data11.setObjectName(u"zoom_out_data11")
        self.zoom_out_data11.setIcon(icon5)

        self.horizontalLayout_3.addWidget(self.zoom_out_data11)


        self.gridLayout_82.addLayout(self.horizontalLayout_3, 2, 7, 1, 1)


        self.gridLayout_85.addWidget(self.frame_7, 0, 1, 1, 1)


        self.gridLayout_89.addWidget(self.groupBox_time11, 0, 1, 1, 1)

        self.groupBox_38 = QGroupBox(self.groupBox_data1)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.groupBox_38.setMinimumSize(QSize(400, 100))
        self.groupBox_38.setMaximumSize(QSize(16777215, 180))
        self.gridLayout_105 = QGridLayout(self.groupBox_38)
        self.gridLayout_105.setObjectName(u"gridLayout_105")
        self.gridLayout_105.setContentsMargins(-1, -1, 9, 9)
        self.tableintensity_data1 = QTableWidget(self.groupBox_38)
        if (self.tableintensity_data1.columnCount() < 4):
            self.tableintensity_data1.setColumnCount(4)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(3, __qtablewidgetitem19)
        self.tableintensity_data1.setObjectName(u"tableintensity_data1")
        sizePolicy3.setHeightForWidth(self.tableintensity_data1.sizePolicy().hasHeightForWidth())
        self.tableintensity_data1.setSizePolicy(sizePolicy3)
        self.tableintensity_data1.setMaximumSize(QSize(16777215, 1677))
        self.tableintensity_data1.setContextMenuPolicy(Qt.NoContextMenu)
        self.tableintensity_data1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableintensity_data1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableintensity_data1.horizontalHeader().setDefaultSectionSize(67)

        self.gridLayout_105.addWidget(self.tableintensity_data1, 1, 0, 1, 1)


        self.gridLayout_89.addWidget(self.groupBox_38, 1, 2, 1, 1)

        self.heatmap_data1 = QGroupBox(self.groupBox_data1)
        self.heatmap_data1.setObjectName(u"heatmap_data1")
        self.heatmap_data1.setFont(font1)
        self.gridLayout_87 = QGridLayout(self.heatmap_data1)
        self.gridLayout_87.setObjectName(u"gridLayout_87")
        self.frame_28 = QFrame(self.heatmap_data1)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setEnabled(True)
        self.frame_28.setMinimumSize(QSize(0, 200))
        self.frame_28.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_28.setFrameShape(QFrame.NoFrame)
        self.gridLayout_88 = QGridLayout(self.frame_28)
        self.gridLayout_88.setSpacing(0)
        self.gridLayout_88.setObjectName(u"gridLayout_88")
        self.gridLayout_88.setContentsMargins(4, 4, 4, 4)
        self.vtkWidget_data13 = QVTKRenderWindowInteractor(self.frame_28)
        self.vtkWidget_data13.setObjectName(u"vtkWidget_data13")
        self.vtkWidget_data13.setEnabled(True)
        self.vtkWidget_data13.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_88.addWidget(self.vtkWidget_data13, 0, 0, 1, 8)

        self.fit_to_zoom_data13 = QPushButton(self.frame_28)
        self.fit_to_zoom_data13.setObjectName(u"fit_to_zoom_data13")
        self.fit_to_zoom_data13.setEnabled(True)
        self.fit_to_zoom_data13.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data13.setAutoDefault(False)
        self.fit_to_zoom_data13.setFlat(False)

        self.gridLayout_88.addWidget(self.fit_to_zoom_data13, 1, 0, 2, 1)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.go_down_data13 = QToolButton(self.frame_28)
        self.go_down_data13.setObjectName(u"go_down_data13")
        self.go_down_data13.setEnabled(True)
        self.go_down_data13.setIcon(icon)

        self.horizontalLayout_23.addWidget(self.go_down_data13)

        self.go_up_data13 = QToolButton(self.frame_28)
        self.go_up_data13.setObjectName(u"go_up_data13")
        self.go_up_data13.setEnabled(True)
        self.go_up_data13.setIcon(icon1)

        self.horizontalLayout_23.addWidget(self.go_up_data13)

        self.go_left_data13 = QToolButton(self.frame_28)
        self.go_left_data13.setObjectName(u"go_left_data13")
        self.go_left_data13.setEnabled(True)
        self.go_left_data13.setIcon(icon2)

        self.horizontalLayout_23.addWidget(self.go_left_data13)

        self.go_right_data13 = QToolButton(self.frame_28)
        self.go_right_data13.setObjectName(u"go_right_data13")
        self.go_right_data13.setEnabled(True)
        self.go_right_data13.setIcon(icon3)

        self.horizontalLayout_23.addWidget(self.go_right_data13)


        self.gridLayout_88.addLayout(self.horizontalLayout_23, 2, 7, 1, 1)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.zoom_in_data13 = QToolButton(self.frame_28)
        self.zoom_in_data13.setObjectName(u"zoom_in_data13")
        self.zoom_in_data13.setEnabled(True)
        self.zoom_in_data13.setIcon(icon4)
        self.zoom_in_data13.setIconSize(QSize(14, 16))

        self.horizontalLayout_24.addWidget(self.zoom_in_data13)

        self.zoom_out_data13 = QToolButton(self.frame_28)
        self.zoom_out_data13.setObjectName(u"zoom_out_data13")
        self.zoom_out_data13.setEnabled(True)
        self.zoom_out_data13.setIcon(icon5)

        self.horizontalLayout_24.addWidget(self.zoom_out_data13)


        self.gridLayout_88.addLayout(self.horizontalLayout_24, 2, 6, 1, 1)


        self.gridLayout_87.addWidget(self.frame_28, 1, 0, 1, 1)


        self.gridLayout_89.addWidget(self.heatmap_data1, 0, 3, 1, 1)

        self.groupBox_24 = QGroupBox(self.groupBox_data1)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.groupBox_24.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_35 = QGridLayout(self.groupBox_24)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.spinBox_y_data1 = QSpinBox(self.groupBox_24)
        self.spinBox_y_data1.setObjectName(u"spinBox_y_data1")
        self.spinBox_y_data1.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data1.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data1.setMinimum(1)
        self.spinBox_y_data1.setMaximum(120)

        self.gridLayout_35.addWidget(self.spinBox_y_data1, 1, 1, 1, 1)

        self.spinBox_x_data1 = QSpinBox(self.groupBox_24)
        self.spinBox_x_data1.setObjectName(u"spinBox_x_data1")
        self.spinBox_x_data1.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_data1.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_x_data1.setMinimum(1)
        self.spinBox_x_data1.setMaximum(120)

        self.gridLayout_35.addWidget(self.spinBox_x_data1, 1, 0, 1, 1)

        self.spinBox_z_data1 = QSpinBox(self.groupBox_24)
        self.spinBox_z_data1.setObjectName(u"spinBox_z_data1")
        self.spinBox_z_data1.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data1.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data1.setMinimum(1)
        self.spinBox_z_data1.setMaximum(60)

        self.gridLayout_35.addWidget(self.spinBox_z_data1, 1, 2, 1, 1)

        self.lineEdit_101 = QLineEdit(self.groupBox_24)
        self.lineEdit_101.setObjectName(u"lineEdit_101")
        self.lineEdit_101.setReadOnly(True)

        self.gridLayout_35.addWidget(self.lineEdit_101, 0, 0, 1, 1)

        self.lineEdit_102 = QLineEdit(self.groupBox_24)
        self.lineEdit_102.setObjectName(u"lineEdit_102")
        self.lineEdit_102.setReadOnly(True)

        self.gridLayout_35.addWidget(self.lineEdit_102, 0, 1, 1, 1)

        self.lineEdit_103 = QLineEdit(self.groupBox_24)
        self.lineEdit_103.setObjectName(u"lineEdit_103")
        self.lineEdit_103.setReadOnly(True)

        self.gridLayout_35.addWidget(self.lineEdit_103, 0, 2, 1, 1)


        self.gridLayout_89.addWidget(self.groupBox_24, 1, 0, 1, 1)

        self.groupBox_time12 = QGroupBox(self.groupBox_data1)
        self.groupBox_time12.setObjectName(u"groupBox_time12")
        sizePolicy2.setHeightForWidth(self.groupBox_time12.sizePolicy().hasHeightForWidth())
        self.groupBox_time12.setSizePolicy(sizePolicy2)
        self.groupBox_time12.setFont(font1)
        self.gridLayout_83 = QGridLayout(self.groupBox_time12)
        self.gridLayout_83.setObjectName(u"gridLayout_83")
        self.frame_18 = QFrame(self.groupBox_time12)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 200))
        self.frame_18.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.gridLayout_86 = QGridLayout(self.frame_18)
        self.gridLayout_86.setSpacing(0)
        self.gridLayout_86.setObjectName(u"gridLayout_86")
        self.gridLayout_86.setContentsMargins(4, 4, 4, 4)
        self.fit_to_zoom_data12 = QPushButton(self.frame_18)
        self.fit_to_zoom_data12.setObjectName(u"fit_to_zoom_data12")
        self.fit_to_zoom_data12.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data12.setAutoDefault(False)
        self.fit_to_zoom_data12.setFlat(False)

        self.gridLayout_86.addWidget(self.fit_to_zoom_data12, 1, 0, 2, 1)

        self.vtkWidget_data12 = QVTKRenderWindowInteractor(self.frame_18)
        self.vtkWidget_data12.setObjectName(u"vtkWidget_data12")
        self.vtkWidget_data12.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_86.addWidget(self.vtkWidget_data12, 0, 0, 1, 11)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.go_down_data12 = QToolButton(self.frame_18)
        self.go_down_data12.setObjectName(u"go_down_data12")
        self.go_down_data12.setIcon(icon)

        self.horizontalLayout_21.addWidget(self.go_down_data12)

        self.go_up_data12 = QToolButton(self.frame_18)
        self.go_up_data12.setObjectName(u"go_up_data12")
        self.go_up_data12.setIcon(icon1)

        self.horizontalLayout_21.addWidget(self.go_up_data12)

        self.go_left_data12 = QToolButton(self.frame_18)
        self.go_left_data12.setObjectName(u"go_left_data12")
        self.go_left_data12.setIcon(icon2)

        self.horizontalLayout_21.addWidget(self.go_left_data12)

        self.go_right_data12 = QToolButton(self.frame_18)
        self.go_right_data12.setObjectName(u"go_right_data12")
        self.go_right_data12.setIcon(icon3)

        self.horizontalLayout_21.addWidget(self.go_right_data12)


        self.gridLayout_86.addLayout(self.horizontalLayout_21, 1, 10, 1, 1)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.zoom_in_data12 = QToolButton(self.frame_18)
        self.zoom_in_data12.setObjectName(u"zoom_in_data12")
        self.zoom_in_data12.setIcon(icon4)

        self.horizontalLayout_22.addWidget(self.zoom_in_data12)

        self.zoom_out_data12 = QToolButton(self.frame_18)
        self.zoom_out_data12.setObjectName(u"zoom_out_data12")
        self.zoom_out_data12.setIcon(icon5)

        self.horizontalLayout_22.addWidget(self.zoom_out_data12)


        self.gridLayout_86.addLayout(self.horizontalLayout_22, 1, 9, 1, 1)


        self.gridLayout_83.addWidget(self.frame_18, 0, 0, 1, 1)


        self.gridLayout_89.addWidget(self.groupBox_time12, 0, 2, 1, 1)

        self.tabWidget_time1 = QTabWidget(self.groupBox_data1)
        self.tabWidget_time1.setObjectName(u"tabWidget_time1")
        self.tabWidget_time12 = QWidget()
        self.tabWidget_time12.setObjectName(u"tabWidget_time12")
        self.gridLayout_78 = QGridLayout(self.tabWidget_time12)
        self.gridLayout_78.setObjectName(u"gridLayout_78")
        self.groupBox_51 = QGroupBox(self.tabWidget_time12)
        self.groupBox_51.setObjectName(u"groupBox_51")
        self.groupBox_51.setFont(font2)
        self.gridLayout_63 = QGridLayout(self.groupBox_51)
        self.gridLayout_63.setObjectName(u"gridLayout_63")
        self.changetimestamp_data10 = QSlider(self.groupBox_51)
        self.changetimestamp_data10.setObjectName(u"changetimestamp_data10")
        self.changetimestamp_data10.setStyleSheet(u"")
        self.changetimestamp_data10.setMaximum(99)
        self.changetimestamp_data10.setSingleStep(1)
        self.changetimestamp_data10.setPageStep(1)
        self.changetimestamp_data10.setValue(0)
        self.changetimestamp_data10.setOrientation(Qt.Horizontal)

        self.gridLayout_63.addWidget(self.changetimestamp_data10, 0, 0, 1, 1)

        self.displaytimestamp_data10 = QSpinBox(self.groupBox_51)
        self.displaytimestamp_data10.setObjectName(u"displaytimestamp_data10")
        self.displaytimestamp_data10.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data10.setMinimum(1)
        self.displaytimestamp_data10.setMaximum(120)

        self.gridLayout_63.addWidget(self.displaytimestamp_data10, 0, 1, 1, 1)


        self.gridLayout_78.addWidget(self.groupBox_51, 1, 0, 1, 1)

        self.groupBox_53 = QGroupBox(self.tabWidget_time12)
        self.groupBox_53.setObjectName(u"groupBox_53")
        self.groupBox_53.setFont(font2)
        self.gridLayout_65 = QGridLayout(self.groupBox_53)
        self.gridLayout_65.setObjectName(u"gridLayout_65")
        self.pushButton_reset_data10 = QPushButton(self.groupBox_53)
        self.pushButton_reset_data10.setObjectName(u"pushButton_reset_data10")

        self.gridLayout_65.addWidget(self.pushButton_reset_data10, 0, 0, 1, 1)

        self.pushButton_auto_data10 = QPushButton(self.groupBox_53)
        self.pushButton_auto_data10.setObjectName(u"pushButton_auto_data10")

        self.gridLayout_65.addWidget(self.pushButton_auto_data10, 0, 1, 1, 1)


        self.gridLayout_78.addWidget(self.groupBox_53, 1, 1, 1, 1)

        self.tabWidget_time1.addTab(self.tabWidget_time12, "")
        self.tabWidget_time10 = QWidget()
        self.tabWidget_time10.setObjectName(u"tabWidget_time10")
        self.gridLayout_107 = QGridLayout(self.tabWidget_time10)
        self.gridLayout_107.setObjectName(u"gridLayout_107")
        self.groupBox_45 = QGroupBox(self.tabWidget_time10)
        self.groupBox_45.setObjectName(u"groupBox_45")
        self.groupBox_45.setFont(font2)
        self.gridLayout_108 = QGridLayout(self.groupBox_45)
        self.gridLayout_108.setObjectName(u"gridLayout_108")
        self.changetimestamp_data11 = QSlider(self.groupBox_45)
        self.changetimestamp_data11.setObjectName(u"changetimestamp_data11")
        self.changetimestamp_data11.setStyleSheet(u"")
        self.changetimestamp_data11.setMaximum(99)
        self.changetimestamp_data11.setSingleStep(1)
        self.changetimestamp_data11.setPageStep(1)
        self.changetimestamp_data11.setValue(0)
        self.changetimestamp_data11.setOrientation(Qt.Horizontal)

        self.gridLayout_108.addWidget(self.changetimestamp_data11, 0, 0, 1, 1)

        self.displaytimestamp_data11 = QSpinBox(self.groupBox_45)
        self.displaytimestamp_data11.setObjectName(u"displaytimestamp_data11")
        self.displaytimestamp_data11.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data11.setMinimum(1)
        self.displaytimestamp_data11.setMaximum(120)

        self.gridLayout_108.addWidget(self.displaytimestamp_data11, 0, 1, 1, 1)


        self.gridLayout_107.addWidget(self.groupBox_45, 0, 0, 1, 1)

        self.groupBox_54 = QGroupBox(self.tabWidget_time10)
        self.groupBox_54.setObjectName(u"groupBox_54")
        self.groupBox_54.setFont(font2)
        self.gridLayout_109 = QGridLayout(self.groupBox_54)
        self.gridLayout_109.setObjectName(u"gridLayout_109")
        self.pushButton_auto_data11 = QPushButton(self.groupBox_54)
        self.pushButton_auto_data11.setObjectName(u"pushButton_auto_data11")

        self.gridLayout_109.addWidget(self.pushButton_auto_data11, 0, 1, 1, 1)

        self.pushButton_reset_data11 = QPushButton(self.groupBox_54)
        self.pushButton_reset_data11.setObjectName(u"pushButton_reset_data11")

        self.gridLayout_109.addWidget(self.pushButton_reset_data11, 0, 0, 1, 1)


        self.gridLayout_107.addWidget(self.groupBox_54, 0, 1, 1, 1)

        self.tabWidget_time1.addTab(self.tabWidget_time10, "")
        self.tabWidget_time11 = QWidget()
        self.tabWidget_time11.setObjectName(u"tabWidget_time11")
        self.gridLayout_110 = QGridLayout(self.tabWidget_time11)
        self.gridLayout_110.setObjectName(u"gridLayout_110")
        self.groupBox_55 = QGroupBox(self.tabWidget_time11)
        self.groupBox_55.setObjectName(u"groupBox_55")
        self.groupBox_55.setFont(font2)
        self.gridLayout_111 = QGridLayout(self.groupBox_55)
        self.gridLayout_111.setObjectName(u"gridLayout_111")
        self.changetimestamp_data12 = QSlider(self.groupBox_55)
        self.changetimestamp_data12.setObjectName(u"changetimestamp_data12")
        self.changetimestamp_data12.setStyleSheet(u"")
        self.changetimestamp_data12.setMaximum(99)
        self.changetimestamp_data12.setSingleStep(1)
        self.changetimestamp_data12.setPageStep(1)
        self.changetimestamp_data12.setValue(0)
        self.changetimestamp_data12.setOrientation(Qt.Horizontal)

        self.gridLayout_111.addWidget(self.changetimestamp_data12, 0, 0, 1, 1)

        self.displaytimestamp_data12 = QSpinBox(self.groupBox_55)
        self.displaytimestamp_data12.setObjectName(u"displaytimestamp_data12")
        self.displaytimestamp_data12.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.displaytimestamp_data12.setMinimum(1)
        self.displaytimestamp_data12.setMaximum(120)

        self.gridLayout_111.addWidget(self.displaytimestamp_data12, 0, 1, 1, 1)


        self.gridLayout_110.addWidget(self.groupBox_55, 0, 0, 1, 1)

        self.groupBox_56 = QGroupBox(self.tabWidget_time11)
        self.groupBox_56.setObjectName(u"groupBox_56")
        self.groupBox_56.setFont(font2)
        self.gridLayout_112 = QGridLayout(self.groupBox_56)
        self.gridLayout_112.setObjectName(u"gridLayout_112")
        self.pushButton_reset_data12 = QPushButton(self.groupBox_56)
        self.pushButton_reset_data12.setObjectName(u"pushButton_reset_data12")

        self.gridLayout_112.addWidget(self.pushButton_reset_data12, 0, 0, 1, 1)

        self.pushButton_auto_data12 = QPushButton(self.groupBox_56)
        self.pushButton_auto_data12.setObjectName(u"pushButton_auto_data12")

        self.gridLayout_112.addWidget(self.pushButton_auto_data12, 0, 1, 1, 1)


        self.gridLayout_110.addWidget(self.groupBox_56, 0, 1, 1, 1)

        self.tabWidget_time1.addTab(self.tabWidget_time11, "")

        self.gridLayout_89.addWidget(self.tabWidget_time1, 1, 1, 1, 1)

        self.groupBox_time10 = QGroupBox(self.groupBox_data1)
        self.groupBox_time10.setObjectName(u"groupBox_time10")
        sizePolicy2.setHeightForWidth(self.groupBox_time10.sizePolicy().hasHeightForWidth())
        self.groupBox_time10.setSizePolicy(sizePolicy2)
        self.groupBox_time10.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_time10.setFont(font1)
        self.groupBox_time10.setStyleSheet(u"")
        self.gridLayout_66 = QGridLayout(self.groupBox_time10)
        self.gridLayout_66.setObjectName(u"gridLayout_66")
        self.frame_24 = QFrame(self.groupBox_time10)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(0, 200))
        self.frame_24.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.gridLayout_84 = QGridLayout(self.frame_24)
        self.gridLayout_84.setSpacing(0)
        self.gridLayout_84.setObjectName(u"gridLayout_84")
        self.gridLayout_84.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.zoom_in_data10 = QToolButton(self.frame_24)
        self.zoom_in_data10.setObjectName(u"zoom_in_data10")
        self.zoom_in_data10.setIcon(icon4)
        self.zoom_in_data10.setIconSize(QSize(14, 16))

        self.horizontalLayout_20.addWidget(self.zoom_in_data10)

        self.zoom_out_data10 = QToolButton(self.frame_24)
        self.zoom_out_data10.setObjectName(u"zoom_out_data10")
        self.zoom_out_data10.setIcon(icon5)

        self.horizontalLayout_20.addWidget(self.zoom_out_data10)


        self.gridLayout_84.addLayout(self.horizontalLayout_20, 2, 6, 1, 1)

        self.fit_to_zoom_data10 = QPushButton(self.frame_24)
        self.fit_to_zoom_data10.setObjectName(u"fit_to_zoom_data10")
        self.fit_to_zoom_data10.setStyleSheet(u"\n"
"background-color: rgb(0, 153, 255);")
        self.fit_to_zoom_data10.setAutoDefault(False)
        self.fit_to_zoom_data10.setFlat(False)

        self.gridLayout_84.addWidget(self.fit_to_zoom_data10, 1, 0, 2, 1)

        self.vtkWidget_data10 = QVTKRenderWindowInteractor(self.frame_24)
        self.vtkWidget_data10.setObjectName(u"vtkWidget_data10")
        self.vtkWidget_data10.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_84.addWidget(self.vtkWidget_data10, 0, 0, 1, 8)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.go_down_data10 = QToolButton(self.frame_24)
        self.go_down_data10.setObjectName(u"go_down_data10")
        self.go_down_data10.setIcon(icon)

        self.horizontalLayout_19.addWidget(self.go_down_data10)

        self.go_up_data10 = QToolButton(self.frame_24)
        self.go_up_data10.setObjectName(u"go_up_data10")
        self.go_up_data10.setIcon(icon1)

        self.horizontalLayout_19.addWidget(self.go_up_data10)

        self.go_left_data10 = QToolButton(self.frame_24)
        self.go_left_data10.setObjectName(u"go_left_data10")
        self.go_left_data10.setIcon(icon2)

        self.horizontalLayout_19.addWidget(self.go_left_data10)

        self.go_right_data10 = QToolButton(self.frame_24)
        self.go_right_data10.setObjectName(u"go_right_data10")
        self.go_right_data10.setIcon(icon3)

        self.horizontalLayout_19.addWidget(self.go_right_data10)


        self.gridLayout_84.addLayout(self.horizontalLayout_19, 2, 7, 1, 1)

        self.Scroll_data1 = QScrollBar(self.frame_24)
        self.Scroll_data1.setObjectName(u"Scroll_data1")
        self.Scroll_data1.setPageStep(10)

        self.gridLayout_84.addWidget(self.Scroll_data1, 0, 8, 1, 1)


        self.gridLayout_66.addWidget(self.frame_24, 0, 1, 1, 1)


        self.gridLayout_89.addWidget(self.groupBox_time10, 0, 0, 1, 1)

        self.gridLayout_89.setColumnStretch(0, 1)
        self.gridLayout_89.setColumnStretch(1, 1)
        self.gridLayout_89.setColumnStretch(2, 1)

        self.gridLayout_70.addWidget(self.groupBox_data1, 2, 1, 1, 4)

        self.file_name_displayed = QLabel(self.PostSurgery)
        self.file_name_displayed.setObjectName(u"file_name_displayed")
        self.file_name_displayed.setMinimumSize(QSize(800, 0))

        self.gridLayout_70.addWidget(self.file_name_displayed, 0, 1, 1, 1)

        self.groupBox_barcode = QGroupBox(self.PostSurgery)
        self.groupBox_barcode.setObjectName(u"groupBox_barcode")
        self.gridLayout_8 = QGridLayout(self.groupBox_barcode)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.tableWidget_barcode = QTableWidget(self.groupBox_barcode)
        if (self.tableWidget_barcode.columnCount() < 4):
            self.tableWidget_barcode.setColumnCount(4)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(2, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(3, __qtablewidgetitem23)
        if (self.tableWidget_barcode.rowCount() < 2):
            self.tableWidget_barcode.setRowCount(2)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_barcode.setVerticalHeaderItem(0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget_barcode.setVerticalHeaderItem(1, __qtablewidgetitem25)
        self.tableWidget_barcode.setObjectName(u"tableWidget_barcode")
        sizePolicy3.setHeightForWidth(self.tableWidget_barcode.sizePolicy().hasHeightForWidth())
        self.tableWidget_barcode.setSizePolicy(sizePolicy3)
        self.tableWidget_barcode.setMinimumSize(QSize(300, 100))
        self.tableWidget_barcode.setMaximumSize(QSize(2000, 383))
        self.tableWidget_barcode.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_barcode.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_barcode.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_8.addWidget(self.tableWidget_barcode, 2, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox_barcode)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_27 = QGridLayout(self.groupBox_4)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.ca1_signal_widget = MplWidget(self.groupBox_4)
        self.ca1_signal_widget.setObjectName(u"ca1_signal_widget")

        self.gridLayout_27.addWidget(self.ca1_signal_widget, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_4, 5, 0, 1, 1)

        self.groupbox_barcode1 = QGroupBox(self.groupBox_barcode)
        self.groupbox_barcode1.setObjectName(u"groupbox_barcode1")
        self.groupbox_barcode1.setMinimumSize(QSize(0, 200))
        self.groupbox_barcode1.setMaximumSize(QSize(16777215, 1000))
        self.gridLayout_6 = QGridLayout(self.groupbox_barcode1)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.widget_barcode_reconstructed = MplWidget(self.groupbox_barcode1)
        self.widget_barcode_reconstructed.setObjectName(u"widget_barcode_reconstructed")
        self.widget_barcode_reconstructed.setMinimumSize(QSize(0, 100))

        self.gridLayout_6.addWidget(self.widget_barcode_reconstructed, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupbox_barcode1, 3, 0, 1, 1)

        self.comboBox_mridBarcodes = QComboBox(self.groupBox_barcode)
        self.comboBox_mridBarcodes.setObjectName(u"comboBox_mridBarcodes")

        self.gridLayout_8.addWidget(self.comboBox_mridBarcodes, 1, 0, 1, 1)

        self.groupbox_barcode0 = QGroupBox(self.groupBox_barcode)
        self.groupbox_barcode0.setObjectName(u"groupbox_barcode0")
        self.groupbox_barcode0.setMinimumSize(QSize(0, 200))
        self.groupbox_barcode0.setMaximumSize(QSize(16777215, 1000))
        self.gridLayout_67 = QGridLayout(self.groupbox_barcode0)
        self.gridLayout_67.setObjectName(u"gridLayout_67")
        self.widget_barcode_detected = MplWidget(self.groupbox_barcode0)
        self.widget_barcode_detected.setObjectName(u"widget_barcode_detected")
        self.widget_barcode_detected.setMinimumSize(QSize(0, 100))

        self.gridLayout_67.addWidget(self.widget_barcode_detected, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupbox_barcode0, 4, 0, 1, 1)

        self.comboBox_atlasSwitch = QComboBox(self.groupBox_barcode)
        self.comboBox_atlasSwitch.setObjectName(u"comboBox_atlasSwitch")

        self.gridLayout_8.addWidget(self.comboBox_atlasSwitch, 0, 0, 1, 1)


        self.gridLayout_70.addWidget(self.groupBox_barcode, 0, 5, 4, 1)

        self.pushButton_questionmark = QPushButton(self.PostSurgery)
        self.pushButton_questionmark.setObjectName(u"pushButton_questionmark")
        self.pushButton_questionmark.setMaximumSize(QSize(50, 16777215))
        icon9 = QIcon()
        icon9.addFile(u"Icons/mri/question_mark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_questionmark.setIcon(icon9)
        self.pushButton_questionmark.setIconSize(QSize(32, 32))

        self.gridLayout_70.addWidget(self.pushButton_questionmark, 0, 3, 1, 1)

        self.tabWidget.addTab(self.PostSurgery, "")

        self.gridLayout_79.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.tabWidget_visualisation.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_150 = QGridLayout(self.tab_3)
        self.gridLayout_150.setObjectName(u"gridLayout_150")
        self.comboBox_mridTag_vis3D = QComboBox(self.tab_3)
        self.comboBox_mridTag_vis3D.setObjectName(u"comboBox_mridTag_vis3D")
        self.comboBox_mridTag_vis3D.setMinimumSize(QSize(0, 50))

        self.gridLayout_150.addWidget(self.comboBox_mridTag_vis3D, 0, 0, 1, 2)

        self.frame_33 = QFrame(self.tab_3)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setEnabled(True)
        self.frame_33.setMinimumSize(QSize(0, 200))
        self.frame_33.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_33.setFrameShape(QFrame.NoFrame)
        self.gridLayout_147 = QGridLayout(self.frame_33)
        self.gridLayout_147.setSpacing(0)
        self.gridLayout_147.setObjectName(u"gridLayout_147")
        self.gridLayout_147.setContentsMargins(4, 4, 4, 4)
        self.pushButton_slicez_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicez_vis3D.setObjectName(u"pushButton_slicez_vis3D")
        icon10 = QIcon()
        icon10.addFile(u"Icons/ephys/slicing_axial_top.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicez_vis3D.setIcon(icon10)
        self.pushButton_slicez_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_slicez_vis3D, 3, 6, 2, 1)

        self.pushButton_slicey_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicey_vis3D.setObjectName(u"pushButton_slicey_vis3D")
        icon11 = QIcon()
        icon11.addFile(u"Icons/ephys/slicing_coronal_front.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicey_vis3D.setIcon(icon11)
        self.pushButton_slicey_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_slicey_vis3D, 3, 5, 2, 1)

        self.pushButton_slicex_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicex_vis3D.setObjectName(u"pushButton_slicex_vis3D")
        icon12 = QIcon()
        icon12.addFile(u"Icons/ephys/slicing_sagittal_right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicex_vis3D.setIcon(icon12)
        self.pushButton_slicex_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_slicex_vis3D, 3, 4, 2, 1)

        self.pushButton_Noslicing_vis3D = QPushButton(self.frame_33)
        self.pushButton_Noslicing_vis3D.setObjectName(u"pushButton_Noslicing_vis3D")
        icon13 = QIcon()
        icon13.addFile(u"Icons/ephys/no_slicing.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_Noslicing_vis3D.setIcon(icon13)
        self.pushButton_Noslicing_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_Noslicing_vis3D, 3, 3, 2, 1)

        self.change_perspective_vis3D = QPushButton(self.frame_33)
        self.change_perspective_vis3D.setObjectName(u"change_perspective_vis3D")
        self.change_perspective_vis3D.setStyleSheet(u"")
        icon14 = QIcon()
        icon14.addFile(u"Icons/ephys/projection_parallel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.change_perspective_vis3D.setIcon(icon14)
        self.change_perspective_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.change_perspective_vis3D, 3, 2, 2, 1)

        self.resetCamera_vis3D = QPushButton(self.frame_33)
        self.resetCamera_vis3D.setObjectName(u"resetCamera_vis3D")
        self.resetCamera_vis3D.setEnabled(True)
        self.resetCamera_vis3D.setStyleSheet(u"")
        icon15 = QIcon(QIcon.fromTheme(u"go-home"))
        self.resetCamera_vis3D.setIcon(icon15)
        self.resetCamera_vis3D.setIconSize(QSize(40, 40))
        self.resetCamera_vis3D.setAutoDefault(False)
        self.resetCamera_vis3D.setFlat(False)

        self.gridLayout_147.addWidget(self.resetCamera_vis3D, 2, 0, 3, 2)

        self.vtkWidget_vis3D = QVTKRenderWindowInteractor(self.frame_33)
        self.vtkWidget_vis3D.setObjectName(u"vtkWidget_vis3D")
        self.vtkWidget_vis3D.setEnabled(True)
        self.vtkWidget_vis3D.setMinimumSize(QSize(500, 0))
        self.vtkWidget_vis3D.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_147.addWidget(self.vtkWidget_vis3D, 0, 0, 1, 8)

        self.gridLayout_147.setColumnStretch(0, 1)
        self.gridLayout_147.setColumnStretch(1, 1)
        self.gridLayout_147.setColumnStretch(2, 1)
        self.gridLayout_147.setColumnStretch(3, 1)
        self.gridLayout_147.setColumnStretch(4, 1)
        self.gridLayout_147.setColumnStretch(5, 1)
        self.gridLayout_147.setColumnStretch(6, 1)

        self.gridLayout_150.addWidget(self.frame_33, 1, 0, 1, 2)

        self.tableWidget_vis3D = QTableWidget(self.tab_3)
        self.tableWidget_vis3D.setObjectName(u"tableWidget_vis3D")
        self.tableWidget_vis3D.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_vis3D.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_vis3D.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_vis3D.horizontalHeader().setCascadingSectionResizes(False)

        self.gridLayout_150.addWidget(self.tableWidget_vis3D, 0, 2, 4, 1)

        self.gridLayout_150.setColumnStretch(0, 2)
        self.tabWidget_visualisation.addTab(self.tab_3, "")

        self.gridLayout_34.addWidget(self.tabWidget_visualisation, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_ephys = QDockWidget(MainWindow)
        self.dockWidget_ephys.setObjectName(u"dockWidget_ephys")
        self.dockWidget_ephys.setMinimumSize(QSize(663, 1041))
        self.dockWidget_ephys.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidget_ephys)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 2000, 23))
        self.menuGUI = QMenu(self.menubar)
        self.menuGUI.setObjectName(u"menuGUI")
        self.menuTrajectory_Planning = QMenu(self.menuGUI)
        self.menuTrajectory_Planning.setObjectName(u"menuTrajectory_Planning")
        self.menuStructural_Tools = QMenu(self.menubar)
        self.menuStructural_Tools.setObjectName(u"menuStructural_Tools")
        self.menuTime_Series_Tools = QMenu(self.menubar)
        self.menuTime_Series_Tools.setObjectName(u"menuTime_Series_Tools")
        self.menuElectrode_Localization = QMenu(self.menuTime_Series_Tools)
        self.menuElectrode_Localization.setObjectName(u"menuElectrode_Localization")
        self.menuEphys_Analysis = QMenu(self.menubar)
        self.menuEphys_Analysis.setObjectName(u"menuEphys_Analysis")
        MainWindow.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.tabWidget_time0, self.changetimestamp_data00)
        QWidget.setTabOrder(self.changetimestamp_data00, self.displaytimestamp_data00)
        QWidget.setTabOrder(self.displaytimestamp_data00, self.pushButton_reset_data00)
        QWidget.setTabOrder(self.pushButton_reset_data00, self.pushButton_auto_data00)
        QWidget.setTabOrder(self.pushButton_auto_data00, self.changetimestamp_data01)
        QWidget.setTabOrder(self.changetimestamp_data01, self.displaytimestamp_data01)
        QWidget.setTabOrder(self.displaytimestamp_data01, self.pushButton_auto_data01)
        QWidget.setTabOrder(self.pushButton_auto_data01, self.pushButton_reset_data01)
        QWidget.setTabOrder(self.pushButton_reset_data01, self.changetimestamp_data02)
        QWidget.setTabOrder(self.changetimestamp_data02, self.displaytimestamp_data02)
        QWidget.setTabOrder(self.displaytimestamp_data02, self.pushButton_reset_data02)
        QWidget.setTabOrder(self.pushButton_reset_data02, self.spinBox_x_data3d_2)
        QWidget.setTabOrder(self.spinBox_x_data3d_2, self.spinBox_y_data3d_2)
        QWidget.setTabOrder(self.spinBox_y_data3d_2, self.spinBox_z_data3d_2)
        QWidget.setTabOrder(self.spinBox_z_data3d_2, self.spinBox_tp_insert_x)
        QWidget.setTabOrder(self.spinBox_tp_insert_x, self.spinBox_tp_insert_y)
        QWidget.setTabOrder(self.spinBox_tp_insert_y, self.spinBox_tp_insert_z)
        QWidget.setTabOrder(self.spinBox_tp_insert_z, self.go_left_data00)
        QWidget.setTabOrder(self.go_left_data00, self.go_right_data00)
        QWidget.setTabOrder(self.go_right_data00, self.zoom_in_data00)
        QWidget.setTabOrder(self.zoom_in_data00, self.zoom_out_data00)
        QWidget.setTabOrder(self.zoom_out_data00, self.zoom_in_data01)
        QWidget.setTabOrder(self.zoom_in_data01, self.zoom_out_data01)
        QWidget.setTabOrder(self.zoom_out_data01, self.spinBox_tp_deep_x)
        QWidget.setTabOrder(self.spinBox_tp_deep_x, self.spinBox_tp_deep_y)
        QWidget.setTabOrder(self.spinBox_tp_deep_y, self.spinBox_tp_deep_z)
        QWidget.setTabOrder(self.spinBox_tp_deep_z, self.go_left_data01)
        QWidget.setTabOrder(self.go_left_data01, self.go_right_data01)
        QWidget.setTabOrder(self.go_right_data01, self.vtkWidget_data01)
        QWidget.setTabOrder(self.vtkWidget_data01, self.spinBox_y_data0)
        QWidget.setTabOrder(self.spinBox_y_data0, self.spinBox_x_data0)
        QWidget.setTabOrder(self.spinBox_x_data0, self.spinBox_z_data0)
        QWidget.setTabOrder(self.spinBox_z_data0, self.go_down_data02)
        QWidget.setTabOrder(self.go_down_data02, self.go_up_data02)
        QWidget.setTabOrder(self.go_up_data02, self.go_left_data02)
        QWidget.setTabOrder(self.go_left_data02, self.go_right_data02)
        QWidget.setTabOrder(self.go_right_data02, self.zoom_in_data02)
        QWidget.setTabOrder(self.zoom_in_data02, self.zoom_out_data02)
        QWidget.setTabOrder(self.zoom_out_data02, self.fit_to_zoom_data02)
        QWidget.setTabOrder(self.fit_to_zoom_data02, self.vtkWidget_data02)
        QWidget.setTabOrder(self.vtkWidget_data02, self.tableintensity_data0)
        QWidget.setTabOrder(self.tableintensity_data0, self.vtkWidget_legend0)
        QWidget.setTabOrder(self.vtkWidget_legend0, self.spinBox_x_data3d)
        QWidget.setTabOrder(self.spinBox_x_data3d, self.spinBox_y_data3d)
        QWidget.setTabOrder(self.spinBox_y_data3d, self.spinBox_z_data3d)
        QWidget.setTabOrder(self.spinBox_z_data3d, self.spinBox_tp_bregma_x)
        QWidget.setTabOrder(self.spinBox_tp_bregma_x, self.spinBox_tp_bregma_y)
        QWidget.setTabOrder(self.spinBox_tp_bregma_y, self.spinBox_tp_bregma_z)
        QWidget.setTabOrder(self.spinBox_tp_bregma_z, self.spinBox_atlas_bregma_x)
        QWidget.setTabOrder(self.spinBox_atlas_bregma_x, self.spinBox_atlas_bregma_y)
        QWidget.setTabOrder(self.spinBox_atlas_bregma_y, self.spinBox_atlas_bregma_z)
        QWidget.setTabOrder(self.spinBox_atlas_bregma_z, self.spinBox_tp_lambda_x)
        QWidget.setTabOrder(self.spinBox_tp_lambda_x, self.spinBox_tp_lambda_y)
        QWidget.setTabOrder(self.spinBox_tp_lambda_y, self.spinBox_tp_lambda_z)
        QWidget.setTabOrder(self.spinBox_tp_lambda_z, self.spinBox_atlas_lambda_x)
        QWidget.setTabOrder(self.spinBox_atlas_lambda_x, self.spinBox_atlas_lambda_y)
        QWidget.setTabOrder(self.spinBox_atlas_lambda_y, self.spinBox_atlas_lambda_z)
        QWidget.setTabOrder(self.spinBox_atlas_lambda_z, self.lineEdit_31)
        QWidget.setTabOrder(self.lineEdit_31, self.lineEdit_43)
        QWidget.setTabOrder(self.lineEdit_43, self.lineEdit_33)
        QWidget.setTabOrder(self.lineEdit_33, self.doubleSpinBox_distanceAtlas)
        QWidget.setTabOrder(self.doubleSpinBox_distanceAtlas, self.doubleSpinBox_tp_ratio)
        QWidget.setTabOrder(self.doubleSpinBox_tp_ratio, self.doubleSpinBox_distance)
        QWidget.setTabOrder(self.doubleSpinBox_distance, self.textEdit_2)
        QWidget.setTabOrder(self.textEdit_2, self.doubleSpinBox_d_bregmaz)
        QWidget.setTabOrder(self.doubleSpinBox_d_bregmaz, self.pushButton_tp_bregma)
        QWidget.setTabOrder(self.pushButton_tp_bregma, self.lineEdit_24)
        QWidget.setTabOrder(self.lineEdit_24, self.lineEdit_29)
        QWidget.setTabOrder(self.lineEdit_29, self.doubleSpinBox_d_bregmax)
        QWidget.setTabOrder(self.doubleSpinBox_d_bregmax, self.doubleSpinBox_d_bregmay)
        QWidget.setTabOrder(self.doubleSpinBox_d_bregmay, self.pushButton_tp_next0)
        QWidget.setTabOrder(self.pushButton_tp_next0, self.lineEdit_20)
        QWidget.setTabOrder(self.lineEdit_20, self.pushButton_tp_lambda)
        QWidget.setTabOrder(self.pushButton_tp_lambda, self.lineEdit_58)
        QWidget.setTabOrder(self.lineEdit_58, self.doubleSpinBox_d_lambdaz)
        QWidget.setTabOrder(self.doubleSpinBox_d_lambdaz, self.doubleSpinBox_d_lambdax)
        QWidget.setTabOrder(self.doubleSpinBox_d_lambdax, self.doubleSpinBox_d_lambday)
        QWidget.setTabOrder(self.doubleSpinBox_d_lambday, self.pushButton_PyLdetection)
        QWidget.setTabOrder(self.pushButton_PyLdetection, self.lineEdit_vis3D)
        QWidget.setTabOrder(self.lineEdit_vis3D, self.vtkWidget_data_seg3D)
        QWidget.setTabOrder(self.vtkWidget_data_seg3D, self.pushButton_seg3D)
        QWidget.setTabOrder(self.pushButton_seg3D, self.fit_to_zoom_data3d0)
        QWidget.setTabOrder(self.fit_to_zoom_data3d0, self.vtkWidget_data_axial)
        QWidget.setTabOrder(self.vtkWidget_data_axial, self.go_down_data3d0)
        QWidget.setTabOrder(self.go_down_data3d0, self.go_up_data3d0)
        QWidget.setTabOrder(self.go_up_data3d0, self.go_left_data3d0)
        QWidget.setTabOrder(self.go_left_data3d0, self.go_right_data3d0)
        QWidget.setTabOrder(self.go_right_data3d0, self.zoom_in_data3d0)
        QWidget.setTabOrder(self.zoom_in_data3d0, self.zoom_out_data3d0)
        QWidget.setTabOrder(self.zoom_out_data3d0, self.textEdit_8)
        QWidget.setTabOrder(self.textEdit_8, self.vtkWidget_data_sagittal)
        QWidget.setTabOrder(self.vtkWidget_data_sagittal, self.go_down_data3d1)
        QWidget.setTabOrder(self.go_down_data3d1, self.go_up_data3d1)
        QWidget.setTabOrder(self.go_up_data3d1, self.go_left_data3d1)
        QWidget.setTabOrder(self.go_left_data3d1, self.go_right_data3d1)
        QWidget.setTabOrder(self.go_right_data3d1, self.zoom_in_data3d1)
        QWidget.setTabOrder(self.zoom_in_data3d1, self.zoom_out_data3d1)
        QWidget.setTabOrder(self.zoom_out_data3d1, self.fit_to_zoom_data3d1)
        QWidget.setTabOrder(self.fit_to_zoom_data3d1, self.textEdit_11)
        QWidget.setTabOrder(self.textEdit_11, self.vtkWidget_trajPlan_2)
        QWidget.setTabOrder(self.vtkWidget_trajPlan_2, self.pushButton_resetSagittal)
        QWidget.setTabOrder(self.pushButton_resetSagittal, self.textEdit_9)
        QWidget.setTabOrder(self.textEdit_9, self.fit_to_zoom_data3d2)
        QWidget.setTabOrder(self.fit_to_zoom_data3d2, self.vtkWidget_data_coronal)
        QWidget.setTabOrder(self.vtkWidget_data_coronal, self.go_down_data3d2)
        QWidget.setTabOrder(self.go_down_data3d2, self.go_up_data3d2)
        QWidget.setTabOrder(self.go_up_data3d2, self.go_left_data3d2)
        QWidget.setTabOrder(self.go_left_data3d2, self.go_right_data3d2)
        QWidget.setTabOrder(self.go_right_data3d2, self.zoom_in_data3d2)
        QWidget.setTabOrder(self.zoom_in_data3d2, self.zoom_out_data3d2)
        QWidget.setTabOrder(self.zoom_out_data3d2, self.vtkWidget_trajPlan_1)
        QWidget.setTabOrder(self.vtkWidget_trajPlan_1, self.textEdit_10)
        QWidget.setTabOrder(self.textEdit_10, self.pushButton_resetCoronal)
        QWidget.setTabOrder(self.pushButton_resetCoronal, self.changeContrast_data3d)
        QWidget.setTabOrder(self.changeContrast_data3d, self.display_window_data3d)
        QWidget.setTabOrder(self.display_window_data3d, self.changeBrightness_data3d)
        QWidget.setTabOrder(self.changeBrightness_data3d, self.pushButton_auto_data3d)
        QWidget.setTabOrder(self.pushButton_auto_data3d, self.pushButton_reset_data3d)
        QWidget.setTabOrder(self.pushButton_reset_data3d, self.display_level_data3d)
        QWidget.setTabOrder(self.display_level_data3d, self.comboBox_Contrastimage)
        QWidget.setTabOrder(self.comboBox_Contrastimage, self.tableintensity_data3d)
        QWidget.setTabOrder(self.tableintensity_data3d, self.spinBox_x_data1)
        QWidget.setTabOrder(self.spinBox_x_data1, self.spinBox_y_data1)
        QWidget.setTabOrder(self.spinBox_y_data1, self.spinBox_z_data1)
        QWidget.setTabOrder(self.spinBox_z_data1, self.spinBox_x_data2)
        QWidget.setTabOrder(self.spinBox_x_data2, self.spinBox_y_data2)
        QWidget.setTabOrder(self.spinBox_y_data2, self.spinBox_z_data2)
        QWidget.setTabOrder(self.spinBox_z_data2, self.zoom_out_data12)
        QWidget.setTabOrder(self.zoom_out_data12, self.vtkWidget_data13)
        QWidget.setTabOrder(self.vtkWidget_data13, self.fit_to_zoom_data13)
        QWidget.setTabOrder(self.fit_to_zoom_data13, self.go_down_data13)
        QWidget.setTabOrder(self.go_down_data13, self.go_up_data13)
        QWidget.setTabOrder(self.go_up_data13, self.go_left_data13)
        QWidget.setTabOrder(self.go_left_data13, self.go_right_data13)
        QWidget.setTabOrder(self.go_right_data13, self.zoom_in_data13)
        QWidget.setTabOrder(self.zoom_in_data13, self.zoom_out_data13)
        QWidget.setTabOrder(self.zoom_out_data13, self.go_down_data12)
        QWidget.setTabOrder(self.go_down_data12, self.vtkWidget_data12)
        QWidget.setTabOrder(self.vtkWidget_data12, self.go_up_data12)
        QWidget.setTabOrder(self.go_up_data12, self.tabWidget_time1)
        QWidget.setTabOrder(self.tabWidget_time1, self.changetimestamp_data10)
        QWidget.setTabOrder(self.changetimestamp_data10, self.displaytimestamp_data10)
        QWidget.setTabOrder(self.displaytimestamp_data10, self.pushButton_reset_data10)
        QWidget.setTabOrder(self.pushButton_reset_data10, self.pushButton_auto_data10)
        QWidget.setTabOrder(self.pushButton_auto_data10, self.changetimestamp_data11)
        QWidget.setTabOrder(self.changetimestamp_data11, self.displaytimestamp_data11)
        QWidget.setTabOrder(self.displaytimestamp_data11, self.pushButton_auto_data11)
        QWidget.setTabOrder(self.pushButton_auto_data11, self.pushButton_reset_data11)
        QWidget.setTabOrder(self.pushButton_reset_data11, self.changetimestamp_data12)
        QWidget.setTabOrder(self.changetimestamp_data12, self.displaytimestamp_data12)
        QWidget.setTabOrder(self.displaytimestamp_data12, self.pushButton_reset_data12)
        QWidget.setTabOrder(self.pushButton_reset_data12, self.pushButton_auto_data12)
        QWidget.setTabOrder(self.pushButton_auto_data12, self.tableintensity_data1)
        QWidget.setTabOrder(self.tableintensity_data1, self.vtkWidget_legend1)
        QWidget.setTabOrder(self.vtkWidget_legend1, self.go_left_data12)
        QWidget.setTabOrder(self.go_left_data12, self.go_right_data12)
        QWidget.setTabOrder(self.go_right_data12, self.zoom_in_data12)
        QWidget.setTabOrder(self.zoom_in_data12, self.fit_to_zoom_data20)
        QWidget.setTabOrder(self.fit_to_zoom_data20, self.vtkWidget_data20)
        QWidget.setTabOrder(self.vtkWidget_data20, self.go_down_data20)
        QWidget.setTabOrder(self.go_down_data20, self.go_up_data20)
        QWidget.setTabOrder(self.go_up_data20, self.go_left_data20)
        QWidget.setTabOrder(self.go_left_data20, self.go_right_data20)
        QWidget.setTabOrder(self.go_right_data20, self.zoom_in_data20)
        QWidget.setTabOrder(self.zoom_in_data20, self.zoom_out_data20)
        QWidget.setTabOrder(self.zoom_out_data20, self.tabWidget_time2)
        QWidget.setTabOrder(self.tabWidget_time2, self.changetimestamp_data20)
        QWidget.setTabOrder(self.changetimestamp_data20, self.displaytimestamp_data20)
        QWidget.setTabOrder(self.displaytimestamp_data20, self.pushButton_reset_data20)
        QWidget.setTabOrder(self.pushButton_reset_data20, self.pushButton_auto_data20)
        QWidget.setTabOrder(self.pushButton_auto_data20, self.changetimestamp_data21)
        QWidget.setTabOrder(self.changetimestamp_data21, self.displaytimestamp_data21)
        QWidget.setTabOrder(self.displaytimestamp_data21, self.pushButton_auto_data21)
        QWidget.setTabOrder(self.pushButton_auto_data21, self.pushButton_reset_data21)
        QWidget.setTabOrder(self.pushButton_reset_data21, self.changetimestamp_data22)
        QWidget.setTabOrder(self.changetimestamp_data22, self.displaytimestamp_data22)
        QWidget.setTabOrder(self.displaytimestamp_data22, self.pushButton_reset_data22)
        QWidget.setTabOrder(self.pushButton_reset_data22, self.pushButton_auto_data22)
        QWidget.setTabOrder(self.pushButton_auto_data22, self.go_down_data23)
        QWidget.setTabOrder(self.go_down_data23, self.go_up_data23)
        QWidget.setTabOrder(self.go_up_data23, self.go_left_data23)
        QWidget.setTabOrder(self.go_left_data23, self.go_right_data23)
        QWidget.setTabOrder(self.go_right_data23, self.vtkWidget_data23)
        QWidget.setTabOrder(self.vtkWidget_data23, self.fit_to_zoom_data23)
        QWidget.setTabOrder(self.fit_to_zoom_data23, self.zoom_in_data23)
        QWidget.setTabOrder(self.zoom_in_data23, self.zoom_out_data23)
        QWidget.setTabOrder(self.zoom_out_data23, self.tableintensity_data2)
        QWidget.setTabOrder(self.tableintensity_data2, self.fit_to_zoom_data21)
        QWidget.setTabOrder(self.fit_to_zoom_data21, self.vtkWidget_data21)
        QWidget.setTabOrder(self.vtkWidget_data21, self.go_down_data21)
        QWidget.setTabOrder(self.go_down_data21, self.go_up_data21)
        QWidget.setTabOrder(self.go_up_data21, self.go_left_data21)
        QWidget.setTabOrder(self.go_left_data21, self.go_right_data21)
        QWidget.setTabOrder(self.go_right_data21, self.zoom_in_data21)
        QWidget.setTabOrder(self.zoom_in_data21, self.zoom_out_data21)
        QWidget.setTabOrder(self.zoom_out_data21, self.fit_to_zoom_data22)
        QWidget.setTabOrder(self.fit_to_zoom_data22, self.vtkWidget_data22)
        QWidget.setTabOrder(self.vtkWidget_data22, self.go_down_data22)
        QWidget.setTabOrder(self.go_down_data22, self.go_up_data22)
        QWidget.setTabOrder(self.go_up_data22, self.go_left_data22)
        QWidget.setTabOrder(self.go_left_data22, self.go_right_data22)
        QWidget.setTabOrder(self.go_right_data22, self.zoom_in_data22)
        QWidget.setTabOrder(self.zoom_in_data22, self.zoom_out_data22)
        QWidget.setTabOrder(self.zoom_out_data22, self.vtkWidget_legend2)
        QWidget.setTabOrder(self.vtkWidget_legend2, self.zoom_in_data10)
        QWidget.setTabOrder(self.zoom_in_data10, self.zoom_out_data10)
        QWidget.setTabOrder(self.zoom_out_data10, self.go_down_data10)
        QWidget.setTabOrder(self.go_down_data10, self.tableWidget_barcode)
        QWidget.setTabOrder(self.tableWidget_barcode, self.vtkWidget_data10)
        QWidget.setTabOrder(self.vtkWidget_data10, self.fit_to_zoom_data10)
        QWidget.setTabOrder(self.fit_to_zoom_data10, self.go_left_data10)
        QWidget.setTabOrder(self.go_left_data10, self.vtkWidget_data11)
        QWidget.setTabOrder(self.vtkWidget_data11, self.go_right_data10)
        QWidget.setTabOrder(self.go_right_data10, self.go_up_data10)
        QWidget.setTabOrder(self.go_up_data10, self.go_down_data11)
        QWidget.setTabOrder(self.go_down_data11, self.fit_to_zoom_data11)
        QWidget.setTabOrder(self.fit_to_zoom_data11, self.go_up_data11)
        QWidget.setTabOrder(self.go_up_data11, self.go_left_data11)
        QWidget.setTabOrder(self.go_left_data11, self.go_right_data11)
        QWidget.setTabOrder(self.go_right_data11, self.zoom_in_data11)
        QWidget.setTabOrder(self.zoom_in_data11, self.zoom_out_data11)
        QWidget.setTabOrder(self.zoom_out_data11, self.fit_to_zoom_data12)
        QWidget.setTabOrder(self.fit_to_zoom_data12, self.tabWidget_visualisation)
        QWidget.setTabOrder(self.tabWidget_visualisation, self.comboBox_mridBarcodes)
        QWidget.setTabOrder(self.comboBox_mridBarcodes, self.comboBox_mridTag_vis3D)
        QWidget.setTabOrder(self.comboBox_mridTag_vis3D, self.pushButton_slicey_vis3D)
        QWidget.setTabOrder(self.pushButton_slicey_vis3D, self.resetCamera_vis3D)
        QWidget.setTabOrder(self.resetCamera_vis3D, self.pushButton_slicex_vis3D)
        QWidget.setTabOrder(self.pushButton_slicex_vis3D, self.change_perspective_vis3D)
        QWidget.setTabOrder(self.change_perspective_vis3D, self.pushButton_slicez_vis3D)
        QWidget.setTabOrder(self.pushButton_slicez_vis3D, self.vtkWidget_vis3D)
        QWidget.setTabOrder(self.vtkWidget_vis3D, self.pushButton_Noslicing_vis3D)
        QWidget.setTabOrder(self.pushButton_Noslicing_vis3D, self.tableWidget_vis3D)
        QWidget.setTabOrder(self.tableWidget_vis3D, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.lineEdit_98)
        QWidget.setTabOrder(self.lineEdit_98, self.lineEdit_99)
        QWidget.setTabOrder(self.lineEdit_99, self.lineEdit_100)
        QWidget.setTabOrder(self.lineEdit_100, self.lineEdit_87)
        QWidget.setTabOrder(self.lineEdit_87, self.lineEdit_104)
        QWidget.setTabOrder(self.lineEdit_104, self.lineEdit_105)
        QWidget.setTabOrder(self.lineEdit_105, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.lineEdit_95)
        QWidget.setTabOrder(self.lineEdit_95, self.lineEdit_96)
        QWidget.setTabOrder(self.lineEdit_96, self.lineEdit_97)
        QWidget.setTabOrder(self.lineEdit_97, self.textEdit_4)
        QWidget.setTabOrder(self.textEdit_4, self.lineEdit_92)
        QWidget.setTabOrder(self.lineEdit_92, self.lineEdit_93)
        QWidget.setTabOrder(self.lineEdit_93, self.lineEdit_94)
        QWidget.setTabOrder(self.lineEdit_94, self.dial_missalignment)
        QWidget.setTabOrder(self.dial_missalignment, self.doubleSpinBox_missalignment)
        QWidget.setTabOrder(self.doubleSpinBox_missalignment, self.pushButton_SaveTraj)
        QWidget.setTabOrder(self.pushButton_SaveTraj, self.pushButton_geometry_dfx)
        QWidget.setTabOrder(self.pushButton_geometry_dfx, self.lineEdit_21)
        QWidget.setTabOrder(self.lineEdit_21, self.spinBox_tp_channels)
        QWidget.setTabOrder(self.spinBox_tp_channels, self.lineEdit_22)
        QWidget.setTabOrder(self.lineEdit_22, self.spinBox_tp_separation)
        QWidget.setTabOrder(self.spinBox_tp_separation, self.pushButton_tp_3d)
        QWidget.setTabOrder(self.pushButton_tp_3d, self.pushButton_insertionPoint)
        QWidget.setTabOrder(self.pushButton_insertionPoint, self.spinBox_depth)
        QWidget.setTabOrder(self.spinBox_depth, self.spinBox_insertion_y)
        QWidget.setTabOrder(self.spinBox_insertion_y, self.lineEdit_107)
        QWidget.setTabOrder(self.lineEdit_107, self.spinBox_insertion_z)
        QWidget.setTabOrder(self.spinBox_insertion_z, self.spinBox_insertion_x)
        QWidget.setTabOrder(self.spinBox_insertion_x, self.comboBox_insertion_shank)
        QWidget.setTabOrder(self.comboBox_insertion_shank, self.pushButton_nextShank)
        QWidget.setTabOrder(self.pushButton_nextShank, self.lineEdit_108)
        QWidget.setTabOrder(self.lineEdit_108, self.lineEdit_106)
        QWidget.setTabOrder(self.lineEdit_106, self.textEdit_14)
        QWidget.setTabOrder(self.textEdit_14, self.textEdit_5)
        QWidget.setTabOrder(self.textEdit_5, self.textEdit_16)
        QWidget.setTabOrder(self.textEdit_16, self.zoom_in_data3d1_3)
        QWidget.setTabOrder(self.zoom_in_data3d1_3, self.zoom_out_data3d1_3)
        QWidget.setTabOrder(self.zoom_out_data3d1_3, self.fit_to_zoom_data3d1_3)
        QWidget.setTabOrder(self.fit_to_zoom_data3d1_3, self.go_down_data3d1_3)
        QWidget.setTabOrder(self.go_down_data3d1_3, self.go_up_data3d1_3)
        QWidget.setTabOrder(self.go_up_data3d1_3, self.go_left_data3d1_3)
        QWidget.setTabOrder(self.go_left_data3d1_3, self.go_right_data3d1_3)
        QWidget.setTabOrder(self.go_right_data3d1_3, self.vtkWidget_data_sagittal_3)
        QWidget.setTabOrder(self.vtkWidget_data_sagittal_3, self.textEdit_15)
        QWidget.setTabOrder(self.textEdit_15, self.zoom_in_data3d2_3)
        QWidget.setTabOrder(self.zoom_in_data3d2_3, self.zoom_out_data3d2_3)
        QWidget.setTabOrder(self.zoom_out_data3d2_3, self.fit_to_zoom_data3d2_3)
        QWidget.setTabOrder(self.fit_to_zoom_data3d2_3, self.vtkWidget_data_coronal_3)
        QWidget.setTabOrder(self.vtkWidget_data_coronal_3, self.go_down_data3d2_3)
        QWidget.setTabOrder(self.go_down_data3d2_3, self.go_up_data3d2_3)
        QWidget.setTabOrder(self.go_up_data3d2_3, self.go_left_data3d2_3)
        QWidget.setTabOrder(self.go_left_data3d2_3, self.go_right_data3d2_3)
        QWidget.setTabOrder(self.go_right_data3d2_3, self.textEdit_7)
        QWidget.setTabOrder(self.textEdit_7, self.textEdit_12)
        QWidget.setTabOrder(self.textEdit_12, self.vtkWidget_data_sagittal_2)
        QWidget.setTabOrder(self.vtkWidget_data_sagittal_2, self.go_down_data3d1_2)
        QWidget.setTabOrder(self.go_down_data3d1_2, self.go_up_data3d1_2)
        QWidget.setTabOrder(self.go_up_data3d1_2, self.go_left_data3d1_2)
        QWidget.setTabOrder(self.go_left_data3d1_2, self.go_right_data3d1_2)
        QWidget.setTabOrder(self.go_right_data3d1_2, self.zoom_in_data3d1_2)
        QWidget.setTabOrder(self.zoom_in_data3d1_2, self.zoom_out_data3d1_2)
        QWidget.setTabOrder(self.zoom_out_data3d1_2, self.fit_to_zoom_data3d1_2)
        QWidget.setTabOrder(self.fit_to_zoom_data3d1_2, self.vtkWidget_trajPlan_3)
        QWidget.setTabOrder(self.vtkWidget_trajPlan_3, self.pushButton_resetAxial)
        QWidget.setTabOrder(self.pushButton_resetAxial, self.lineEdit_59)
        QWidget.setTabOrder(self.lineEdit_59, self.horizontalSlider_axial3D)
        QWidget.setTabOrder(self.horizontalSlider_axial3D, self.textEdit_13)
        QWidget.setTabOrder(self.textEdit_13, self.lineEdit_68)
        QWidget.setTabOrder(self.lineEdit_68, self.lineEdit_67)
        QWidget.setTabOrder(self.lineEdit_67, self.lineEdit_77)
        QWidget.setTabOrder(self.lineEdit_77, self.pushButton_auto_data02)
        QWidget.setTabOrder(self.pushButton_auto_data02, self.lineEdit_80)
        QWidget.setTabOrder(self.lineEdit_80, self.fit_to_zoom_data00)
        QWidget.setTabOrder(self.fit_to_zoom_data00, self.vtkWidget_data03)
        QWidget.setTabOrder(self.vtkWidget_data03, self.lineEdit_78)
        QWidget.setTabOrder(self.lineEdit_78, self.lineEdit_79)
        QWidget.setTabOrder(self.lineEdit_79, self.doubleSpinBox_distance_shank)
        QWidget.setTabOrder(self.doubleSpinBox_distance_shank, self.textEdit_distance_shank)
        QWidget.setTabOrder(self.textEdit_distance_shank, self.pushButton_tp_deep)
        QWidget.setTabOrder(self.pushButton_tp_deep, self.go_up_data01)
        QWidget.setTabOrder(self.go_up_data01, self.fit_to_zoom_data01)
        QWidget.setTabOrder(self.fit_to_zoom_data01, self.go_down_data01)
        QWidget.setTabOrder(self.go_down_data01, self.lineEdit_89)
        QWidget.setTabOrder(self.lineEdit_89, self.lineEdit_90)
        QWidget.setTabOrder(self.lineEdit_90, self.lineEdit_91)
        QWidget.setTabOrder(self.lineEdit_91, self.tableintensity_data3d_2)
        QWidget.setTabOrder(self.tableintensity_data3d_2, self.pushButton_contrastAdjustments)
        QWidget.setTabOrder(self.pushButton_contrastAdjustments, self.checkBox_brain_region)
        QWidget.setTabOrder(self.checkBox_brain_region, self.pushButton_tp_insert)
        QWidget.setTabOrder(self.pushButton_tp_insert, self.vtkWidget_data00)
        QWidget.setTabOrder(self.vtkWidget_data00, self.go_down_data00)
        QWidget.setTabOrder(self.go_down_data00, self.go_up_data00)
        QWidget.setTabOrder(self.go_up_data00, self.lineEdit_19)
        QWidget.setTabOrder(self.lineEdit_19, self.lineEdit_30)
        QWidget.setTabOrder(self.lineEdit_30, self.lineEdit_88)
        QWidget.setTabOrder(self.lineEdit_88, self.pushButton_removeShank)
        QWidget.setTabOrder(self.pushButton_removeShank, self.comboBox_Shanks)
        QWidget.setTabOrder(self.comboBox_Shanks, self.comboBox_tpColor)
        QWidget.setTabOrder(self.comboBox_tpColor, self.pushButton_addShank)
        QWidget.setTabOrder(self.pushButton_addShank, self.pushButton_axialView)
        QWidget.setTabOrder(self.pushButton_axialView, self.checkBox_constraint_90deg)
        QWidget.setTabOrder(self.checkBox_constraint_90deg, self.pushButton_coronalView)
        QWidget.setTabOrder(self.pushButton_coronalView, self.pushButton_sagittalView)
        QWidget.setTabOrder(self.pushButton_sagittalView, self.checkBox_constraint_90deg_coronal)
        QWidget.setTabOrder(self.checkBox_constraint_90deg_coronal, self.pushButton_dfx_ok)
        QWidget.setTabOrder(self.pushButton_dfx_ok, self.pushButton_plot_probe)
        QWidget.setTabOrder(self.pushButton_plot_probe, self.doubleSpinBox_bundle_ratio)
        QWidget.setTabOrder(self.doubleSpinBox_bundle_ratio, self.pushButton_xml)
        QWidget.setTabOrder(self.pushButton_xml, self.pushButton_dfx_run)
        QWidget.setTabOrder(self.pushButton_dfx_run, self.lineEdit_76)
        QWidget.setTabOrder(self.lineEdit_76, self.lineEdit_73)
        QWidget.setTabOrder(self.lineEdit_73, self.textEdit_channels_xml)
        QWidget.setTabOrder(self.textEdit_channels_xml, self.spinBox_max_bend_angle)
        QWidget.setTabOrder(self.spinBox_max_bend_angle, self.lineEdit_74)
        QWidget.setTabOrder(self.lineEdit_74, self.lineEdit_72)
        QWidget.setTabOrder(self.lineEdit_72, self.lineEdit_70)
        QWidget.setTabOrder(self.lineEdit_70, self.lineEdit_69)
        QWidget.setTabOrder(self.lineEdit_69, self.spinBox_bend_r1)
        QWidget.setTabOrder(self.spinBox_bend_r1, self.spinBox_first_bend_distance)
        QWidget.setTabOrder(self.spinBox_first_bend_distance, self.pushButton_export)
        QWidget.setTabOrder(self.pushButton_export, self.spinBox_um_per_unit)
        QWidget.setTabOrder(self.spinBox_um_per_unit, self.spinBox_bend_r2)
        QWidget.setTabOrder(self.spinBox_bend_r2, self.checkBox_defaultchannels)
        QWidget.setTabOrder(self.checkBox_defaultchannels, self.spinBox_arc_points)
        QWidget.setTabOrder(self.spinBox_arc_points, self.lineEdit_71)
        QWidget.setTabOrder(self.lineEdit_71, self.spinBox_artificial_extension)
        QWidget.setTabOrder(self.spinBox_artificial_extension, self.lineEdit_75)
        QWidget.setTabOrder(self.lineEdit_75, self.pushButton_dfx)
        QWidget.setTabOrder(self.pushButton_dfx, self.comboBox_geometry_shanks)
        QWidget.setTabOrder(self.comboBox_geometry_shanks, self.pushButton_metadata)
        QWidget.setTabOrder(self.pushButton_metadata, self.lineEdit_101)
        QWidget.setTabOrder(self.lineEdit_101, self.lineEdit_102)
        QWidget.setTabOrder(self.lineEdit_102, self.lineEdit_103)
        QWidget.setTabOrder(self.lineEdit_103, self.pushButton_questionmark)

        self.menubar.addAction(self.menuGUI.menuAction())
        self.menubar.addAction(self.menuStructural_Tools.menuAction())
        self.menubar.addAction(self.menuTime_Series_Tools.menuAction())
        self.menubar.addAction(self.menuEphys_Analysis.menuAction())
        self.menuGUI.addAction(self.actionStart_SAMRI_process)
        self.menuGUI.addAction(self.menuTrajectory_Planning.menuAction())
        self.menuGUI.addAction(self.actionOpen)
        self.menuGUI.addAction(self.actionOpen_ephys_Data)
        self.menuGUI.addSeparator()
        self.menuGUI.addAction(self.actionAddViewImage)
        self.menuGUI.addSeparator()
        self.menuGUI.addAction(self.actionLoad_Prev_Session)
        self.menuGUI.addSeparator()
        self.menuGUI.addAction(self.actionQuit)
        self.menuGUI.addAction(self.actionNew_Window)
        self.menuTrajectory_Planning.addAction(self.actionTrajectory_Planning_2)
        self.menuTrajectory_Planning.addAction(self.actionIntraoperative)
        self.menuStructural_Tools.addAction(self.actionOpen_Session_2)
        self.menuStructural_Tools.addSeparator()
        self.menuStructural_Tools.addAction(self.actionPaintbrush)
        self.menuStructural_Tools.addAction(self.actionMeasurement)
        self.menuStructural_Tools.addSeparator()
        self.menuStructural_Tools.addAction(self.actionResample)
        self.menuStructural_Tools.addAction(self.actionRegister)
        self.menuStructural_Tools.addSeparator()
        self.menuStructural_Tools.addAction(self.actionSegmentation)
        self.menuStructural_Tools.addSeparator()
        self.menuTime_Series_Tools.addAction(self.actionOpen_Session)
        self.menuTime_Series_Tools.addSeparator()
        self.menuTime_Series_Tools.addAction(self.actionStart_MRIDlabels)
        self.menuTime_Series_Tools.addAction(self.menuElectrode_Localization.menuAction())
        self.menuTime_Series_Tools.addSeparator()
        self.menuTime_Series_Tools.addSeparator()
        self.menuTime_Series_Tools.addAction(self.actionContrast_Adjustments)
        self.menuTime_Series_Tools.addSeparator()
        self.menuElectrode_Localization.addAction(self.actionGaussian_Centers)
        self.menuElectrode_Localization.addAction(self.actionGet_Coordinates)
        self.menuEphys_Analysis.addAction(self.actionOpen_Session_3)
        self.menuEphys_Analysis.addSeparator()
        self.menuEphys_Analysis.addAction(self.actionRippl_AI)
        self.menuEphys_Analysis.addAction(self.actionTheta_Detection)
        self.menuEphys_Analysis.addAction(self.actionLoad_Spike_Sorting)
        self.menuEphys_Analysis.addSeparator()

        self.retranslateUi(MainWindow)

        self.tabWidget_visualisation.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.fit_to_zoom_data20.setDefault(False)
        self.tabWidget_time2.setCurrentIndex(0)
        self.fit_to_zoom_data23.setDefault(False)
        self.fit_to_zoom_data21.setDefault(False)
        self.fit_to_zoom_data22.setDefault(False)
        self.data_4d_3d.setCurrentIndex(1)
        self.tabWidget_time0.setCurrentIndex(0)
        self.fit_to_zoom_data00.setDefault(False)
        self.fit_to_zoom_data01.setDefault(False)
        self.fit_to_zoom_data02.setDefault(False)
        self.stackedWidget_3d.setCurrentIndex(1)
        self.stackedWidget_trajectoryplanning.setCurrentIndex(0)
        self.stackedWidget_dfx.setCurrentIndex(0)
        self.stackedWidget_sagittal.setCurrentIndex(1)
        self.fit_to_zoom_data3d1.setDefault(False)
        self.fit_to_zoom_data3d1_3.setDefault(False)
        self.stackedWidget_coronal.setCurrentIndex(1)
        self.fit_to_zoom_data3d2.setDefault(False)
        self.fit_to_zoom_data3d2_3.setDefault(False)
        self.stackedWidget_axial.setCurrentIndex(0)
        self.fit_to_zoom_data3d0.setDefault(False)
        self.stackedWidget_sagittal_2.setCurrentIndex(1)
        self.fit_to_zoom_data3d1_2.setDefault(False)
        self.stackedWidget_3d_tp.setCurrentIndex(1)
        self.fit_to_zoom_data11.setDefault(False)
        self.fit_to_zoom_data13.setDefault(False)
        self.fit_to_zoom_data12.setDefault(False)
        self.tabWidget_time1.setCurrentIndex(0)
        self.fit_to_zoom_data10.setDefault(False)
        self.resetCamera_vis3D.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(accessibility)
        MainWindow.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Load MRI Image", None))
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Open a NIfTI (.nii.gz) file as the main MRI dataset for a new session.", None))
#endif // QT_CONFIG(tooltip)
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"Add Another Image (3D)", None))
        self.actionSave_Image.setText(QCoreApplication.translate("MainWindow", u"Save Image", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionPaintbrush.setText(QCoreApplication.translate("MainWindow", u"Paintbrush", None))
#if QT_CONFIG(tooltip)
        self.actionPaintbrush.setToolTip(QCoreApplication.translate("MainWindow", u"Open the paintbrush tool to manually draw or edit a label volume.", None))
#endif // QT_CONFIG(tooltip)
        self.actionmain_code_2.setText(QCoreApplication.translate("MainWindow", u"main code 2", None))
        self.actionGaussian_Centers.setText(QCoreApplication.translate("MainWindow", u"Warping and Gaussian Centres Extraction", None))
#if QT_CONFIG(tooltip)
        self.actionGaussian_Centers.setToolTip(QCoreApplication.translate("MainWindow", u"Open warping and Gaussian-centre extraction for electrode localisation.", None))
#endif // QT_CONFIG(tooltip)
        self.actionGet_Coordinates.setText(QCoreApplication.translate("MainWindow", u"Final Localization", None))
#if QT_CONFIG(tooltip)
        self.actionGet_Coordinates.setToolTip(QCoreApplication.translate("MainWindow", u"Compute the final electrode localisation from the extracted coordinates.", None))
#endif // QT_CONFIG(tooltip)
        self.actionStart_with_Labels.setText(QCoreApplication.translate("MainWindow", u"Start with Labels", None))
        self.actionAddViewImage.setText(QCoreApplication.translate("MainWindow", u"Load Another MRI Image", None))
#if QT_CONFIG(tooltip)
        self.actionAddViewImage.setToolTip(QCoreApplication.translate("MainWindow", u"Add another NIfTI file as an overlay layer on top of the current volume.", None))
#endif // QT_CONFIG(tooltip)
        self.actionContrast_Adjustments.setText(QCoreApplication.translate("MainWindow", u"Contrast Adjustments", None))
#if QT_CONFIG(tooltip)
        self.actionContrast_Adjustments.setToolTip(QCoreApplication.translate("MainWindow", u"Open contrast/brightness controls for 4D data.", None))
#endif // QT_CONFIG(tooltip)
        self.actionResample.setText(QCoreApplication.translate("MainWindow", u"Resample", None))
#if QT_CONFIG(tooltip)
        self.actionResample.setToolTip(QCoreApplication.translate("MainWindow", u"Open the resampling controls to change this volume's voxel spacing.", None))
#endif // QT_CONFIG(tooltip)
        self.actionRegister.setText(QCoreApplication.translate("MainWindow", u"Registration", None))
#if QT_CONFIG(tooltip)
        self.actionRegister.setToolTip(QCoreApplication.translate("MainWindow", u"Open the registration workflow to align this volume to a reference/atlas.", None))
#endif // QT_CONFIG(tooltip)
        self.actionContrast_Adjustments_2.setText(QCoreApplication.translate("MainWindow", u"Measurement", None))
        self.actionStart_MRIDlabels.setText(QCoreApplication.translate("MainWindow", u"MRID-tag label creation", None))
#if QT_CONFIG(tooltip)
        self.actionStart_MRIDlabels.setToolTip(QCoreApplication.translate("MainWindow", u"Open the dialog to define MRID tags and start creating anatomical region labels.", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_ephys_Data.setText(QCoreApplication.translate("MainWindow", u"Load ephys Data", None))
#if QT_CONFIG(tooltip)
        self.actionOpen_ephys_Data.setToolTip(QCoreApplication.translate("MainWindow", u"Open a .dat electrophysiology recording (requires a matching .xml file in the same folder).", None))
#endif // QT_CONFIG(tooltip)
        self.actionSegmentation.setText(QCoreApplication.translate("MainWindow", u"Segmentation", None))
#if QT_CONFIG(tooltip)
        self.actionSegmentation.setToolTip(QCoreApplication.translate("MainWindow", u"Open the segmentation tool for this volume.", None))
#endif // QT_CONFIG(tooltip)
        self.actionGet_Position_in_HPC.setText(QCoreApplication.translate("MainWindow", u"Get Position in HPC", None))
        self.actionMeasurement.setText(QCoreApplication.translate("MainWindow", u"Measurement", None))
#if QT_CONFIG(tooltip)
        self.actionMeasurement.setToolTip(QCoreApplication.translate("MainWindow", u"Toggle distance-measurement mode on the MRI views.", None))
#endif // QT_CONFIG(tooltip)
        self.actionVisualize_3D_data.setText(QCoreApplication.translate("MainWindow", u"Visualize 3D data", None))
        self.actionStart_SAMRI_process.setText(QCoreApplication.translate("MainWindow", u"Start SAMRI process", None))
#if QT_CONFIG(tooltip)
        self.actionStart_SAMRI_process.setToolTip(QCoreApplication.translate("MainWindow", u"Start the SAMRI fetch / bias-correction / registration workflow for an animal ID.", None))
#endif // QT_CONFIG(tooltip)
        self.actionTd.setText(QCoreApplication.translate("MainWindow", u"Trajectory Planning", None))
        self.actionNew_Window.setText(QCoreApplication.translate("MainWindow", u"New Window", None))
#if QT_CONFIG(tooltip)
        self.actionNew_Window.setToolTip(QCoreApplication.translate("MainWindow", u"Launch a second, independent copy of this application in a separate process.", None))
#endif // QT_CONFIG(tooltip)
        self.actionRippl_AI.setText(QCoreApplication.translate("MainWindow", u"Rippl AI", None))
#if QT_CONFIG(tooltip)
        self.actionRippl_AI.setToolTip(QCoreApplication.translate("MainWindow", u"Run Rippl-AI ripple (SWR) detection on the loaded recording.", None))
#endif // QT_CONFIG(tooltip)
        self.actionTheta_Detection.setText(QCoreApplication.translate("MainWindow", u"Theta Detection", None))
#if QT_CONFIG(tooltip)
        self.actionTheta_Detection.setToolTip(QCoreApplication.translate("MainWindow", u"Run theta-event detection on the loaded recording.", None))
#endif // QT_CONFIG(tooltip)
        self.actionLoad_Spike_Sorting.setText(QCoreApplication.translate("MainWindow", u"Show Spiking Raster Plot", None))
#if QT_CONFIG(tooltip)
        self.actionLoad_Spike_Sorting.setToolTip(QCoreApplication.translate("MainWindow", u"Show the spike-sorting raster plot for this recording.", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_Session.setText(QCoreApplication.translate("MainWindow", u"Open Session", None))
#if QT_CONFIG(tooltip)
        self.actionOpen_Session.setToolTip(QCoreApplication.translate("MainWindow", u"Reopen a previously loaded 4D MRI session, or load a new one.", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_Session_2.setText(QCoreApplication.translate("MainWindow", u"Open Session", None))
#if QT_CONFIG(tooltip)
        self.actionOpen_Session_2.setToolTip(QCoreApplication.translate("MainWindow", u"Reopen a previously loaded 3D MRI session, or load a new one.", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_Session_3.setText(QCoreApplication.translate("MainWindow", u"Open Session", None))
#if QT_CONFIG(tooltip)
        self.actionOpen_Session_3.setToolTip(QCoreApplication.translate("MainWindow", u"Reopen a previously loaded ephys recording, or load a new one.", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_Session_4.setText(QCoreApplication.translate("MainWindow", u"Open Session", None))
#if QT_CONFIG(tooltip)
        self.actionOpen_Session_4.setToolTip(QCoreApplication.translate("MainWindow", u"Reopen a previous SAMRI animal ID, or start a new one.", None))
#endif // QT_CONFIG(tooltip)
        self.actionLoad_Prev_Session.setText(QCoreApplication.translate("MainWindow", u"Load Prev. File", None))
#if QT_CONFIG(tooltip)
        self.actionLoad_Prev_Session.setToolTip(QCoreApplication.translate("MainWindow", u"Reopen any previously loaded MRI file, ephys recording, or SAMRI animal ID.", None))
#endif // QT_CONFIG(tooltip)
        self.actionIntraoperative.setText(QCoreApplication.translate("MainWindow", u"Intraoperative", None))
        self.actionTrajectory_Planning_2.setText(QCoreApplication.translate("MainWindow", u"Pre-surgery Planning", None))
#if QT_CONFIG(tooltip)
        self.actionTrajectory_Planning_2.setToolTip(QCoreApplication.translate("MainWindow", u"Open pre-surgery trajectory planning for the loaded MRI volume.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_data2.setToolTip(QCoreApplication.translate("MainWindow", u"Axial view comparison panel: one or more 4D echoes of the axial slice shown side by side, each with its own cursor, pan/zoom, and contrast controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_data2.setTitle(QCoreApplication.translate("MainWindow", u"View AXIAL", None))
#if QT_CONFIG(tooltip)
        self.groupBox_32.setToolTip(QCoreApplication.translate("MainWindow", u"Cursor position (x, y, z) for this comparison panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"Cursor position (x,y,z)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_x_data2.setToolTip(QCoreApplication.translate("MainWindow", u"X voxel coordinate of the cursor for this comparison panel; type a value to move the crosshair there.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_y_data2.setToolTip(QCoreApplication.translate("MainWindow", u"Y voxel coordinate of the cursor for this comparison panel; type a value to move the crosshair there.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_z_data2.setToolTip(QCoreApplication.translate("MainWindow", u"Z voxel coordinate of the cursor for this comparison panel; type a value to move the crosshair there.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_98.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_99.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_100.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
#if QT_CONFIG(tooltip)
        self.groupBox_time20.setToolTip(QCoreApplication.translate("MainWindow", u"Echo panel for one 4D frame: the title updates to the frame's actual echo, and it holds this frame's own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time20.setTitle(QCoreApplication.translate("MainWindow", u"Echo 0", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data20.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data20.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data20.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data20.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data20.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data20.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data20.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.groupBox_57.setToolTip(QCoreApplication.translate("MainWindow", u"Choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_57.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Slide to choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Index of the 4D echo (frame) currently displayed in this panel; type a value to jump to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_58.setToolTip(QCoreApplication.translate("MainWindow", u"Auto-compute or reset the window/level (brightness/contrast) for this panel's image.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_58.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the window/level (brightness/contrast) to its initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data20.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data20.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute the window/level (brightness/contrast) from the image data.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data20.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time2.setTabText(self.tabWidget_time2.indexOf(self.tabWidget_time20), QCoreApplication.translate("MainWindow", u"Echo 1", None))
#if QT_CONFIG(tooltip)
        self.groupBox_59.setToolTip(QCoreApplication.translate("MainWindow", u"Choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_59.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Slide to choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Index of the 4D echo (frame) currently displayed in this panel; type a value to jump to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_60.setToolTip(QCoreApplication.translate("MainWindow", u"Auto-compute or reset the window/level (brightness/contrast) for this panel's image.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_60.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute the window/level (brightness/contrast) from the image data.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data21.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the window/level (brightness/contrast) to its initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data21.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.tabWidget_time2.setTabText(self.tabWidget_time2.indexOf(self.tabWidget_time21), QCoreApplication.translate("MainWindow", u"Echo 2", None))
#if QT_CONFIG(tooltip)
        self.groupBox_61.setToolTip(QCoreApplication.translate("MainWindow", u"Choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_61.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Slide to choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Index of the 4D echo (frame) currently displayed in this panel; type a value to jump to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_62.setToolTip(QCoreApplication.translate("MainWindow", u"Auto-compute or reset the window/level (brightness/contrast) for this panel's image.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_62.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the window/level (brightness/contrast) to its initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data22.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute the window/level (brightness/contrast) from the image data.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data22.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time2.setTabText(self.tabWidget_time2.indexOf(self.tabWidget_time22), QCoreApplication.translate("MainWindow", u"Echo 3", None))
#if QT_CONFIG(tooltip)
        self.heatmap_data2.setToolTip(QCoreApplication.translate("MainWindow", u"Heatmap overlay for this view, made visible once MRID-tag segmentation/tagging has been run.", None))
#endif // QT_CONFIG(tooltip)
        self.heatmap_data2.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap", None))
#if QT_CONFIG(tooltip)
        self.go_down_data23.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data23.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data23.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data23.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data23.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data23.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data23.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data23.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data23.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data23.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data23.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data23.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data23.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data23.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.groupBox_39.setToolTip(QCoreApplication.translate("MainWindow", u"Shows the image intensity value at the cursor's current position in this panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_39.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem = self.tableintensity_data2.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem1 = self.tableintensity_data2.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem2 = self.tableintensity_data2.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
#if QT_CONFIG(tooltip)
        self.groupBox_time21.setToolTip(QCoreApplication.translate("MainWindow", u"Echo panel for one 4D frame: the title updates to the frame's actual echo, and it holds this frame's own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time21.setTitle(QCoreApplication.translate("MainWindow", u"Echo 4", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data21.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data21.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data21.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data21.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data21.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data21.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data21.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data21.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_time22.setTitle(QCoreApplication.translate("MainWindow", u"Echo 8", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Reset zoom and pan to fit the whole image in this view.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data22.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data22.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data22.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data22.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data22.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data22.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data22.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data22.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.groupbox_legend2.setToolTip(QCoreApplication.translate("MainWindow", u"Color scale for the electrode/shank heatmap overlay; only shown while heatmap mode is active.", None))
#endif // QT_CONFIG(tooltip)
        self.groupbox_legend2.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap Intensities", None))
#if QT_CONFIG(tooltip)
        self.groupBox_data0.setToolTip(QCoreApplication.translate("MainWindow", u"This dataset's coronal/sagittal/axial panels, each with its own timepoint, contrast, and cursor controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_data0.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
#if QT_CONFIG(tooltip)
        self.groupBox_46.setToolTip(QCoreApplication.translate("MainWindow", u"Scrub through this panel's timepoint independently of the other two orthogonal views, so you can compare different frames of the same 4D scan side by side.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_46.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Drag to jump to a different timepoint (frame) of the 4D scan for this panel; stays synced with the spin box next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Current timepoint (frame) index shown in this panel; stays synced with the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_49.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust this panel's window/level (contrast/brightness) with the sliders, or use Auto/Reset.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_49.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Reset this panel's contrast/brightness (window/level) back to the volume's initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data00.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute contrast/brightness (window/level) from this panel's intensity range (Ctrl+J does this for every panel at once).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data00.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time0.setTabText(self.tabWidget_time0.indexOf(self.tabWidget_time00), QCoreApplication.translate("MainWindow", u"Echo 0", None))
#if QT_CONFIG(tooltip)
        self.groupBox_41.setToolTip(QCoreApplication.translate("MainWindow", u"Scrub through this panel's timepoint independently of the other two orthogonal views, so you can compare different frames of the same 4D scan side by side.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_41.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Drag to jump to a different timepoint (frame) of the 4D scan for this panel; stays synced with the spin box next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Current timepoint (frame) index shown in this panel; stays synced with the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_42.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust this panel's window/level (contrast/brightness) with the sliders, or use Auto/Reset.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_42.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute contrast/brightness (window/level) from this panel's intensity range (Ctrl+J does this for every panel at once).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data01.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Reset this panel's contrast/brightness (window/level) back to the volume's initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data01.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.tabWidget_time0.setTabText(self.tabWidget_time0.indexOf(self.tabWidget_time01), QCoreApplication.translate("MainWindow", u"Echo 4", None))
#if QT_CONFIG(tooltip)
        self.groupBox_44.setToolTip(QCoreApplication.translate("MainWindow", u"Scrub through this panel's timepoint independently of the other two orthogonal views, so you can compare different frames of the same 4D scan side by side.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_44.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Drag to jump to a different timepoint (frame) of the 4D scan for this panel; stays synced with the spin box next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Current timepoint (frame) index shown in this panel; stays synced with the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_43.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust this panel's window/level (contrast/brightness) with the sliders, or use Auto/Reset.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_43.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Reset this panel's contrast/brightness (window/level) back to the volume's initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data02.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute contrast/brightness (window/level) from this panel's intensity range (Ctrl+J does this for every panel at once).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data02.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time0.setTabText(self.tabWidget_time0.indexOf(self.tabWidget_time02), QCoreApplication.translate("MainWindow", u"Echo 8", None))
#if QT_CONFIG(tooltip)
        self.heatmap_data0.setToolTip(QCoreApplication.translate("MainWindow", u"Computed MRID-tag heatmap for this dataset; appears once the heatmap/segmentation analysis has been run.", None))
#endif // QT_CONFIG(tooltip)
        self.heatmap_data0.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap", None))
#if QT_CONFIG(tooltip)
        self.groupBox_time00.setToolTip(QCoreApplication.translate("MainWindow", u"Coronal/sagittal/axial panel currently showing timepoint 0 of the 4D scan, with its own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time00.setTitle(QCoreApplication.translate("MainWindow", u"Echo 0", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Fit this view to the window, resetting pan and zoom.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data00.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data00.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data00.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data00.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data00.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data00.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data00.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data00.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.groupBox_time01.setToolTip(QCoreApplication.translate("MainWindow", u"Coronal/sagittal/axial panel currently showing timepoint 4 of the 4D scan, with its own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time01.setTitle(QCoreApplication.translate("MainWindow", u"Echo 4", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data01.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data01.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Fit this view to the window, resetting pan and zoom.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data01.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data01.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data01.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data01.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data01.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data01.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.groupBox_34.setToolTip(QCoreApplication.translate("MainWindow", u"Live crosshair cursor position for this dataset, in voxel coordinates.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"Cursor Position (x,y,z)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_x_data0.setToolTip(QCoreApplication.translate("MainWindow", u"Voxel x-coordinate of the cursor; type a value to move the cursor there, or it updates as you move the cursor in the views.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_z_data0.setToolTip(QCoreApplication.translate("MainWindow", u"Voxel z-coordinate of the cursor; type a value to move the cursor there, or it updates as you move the cursor in the views.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_y_data0.setToolTip(QCoreApplication.translate("MainWindow", u"Voxel y-coordinate of the cursor; type a value to move the cursor there, or it updates as you move the cursor in the views.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_87.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_104.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_105.setText(QCoreApplication.translate("MainWindow", u"axial", None))
#if QT_CONFIG(tooltip)
        self.groupBox_time02.setToolTip(QCoreApplication.translate("MainWindow", u"Coronal/sagittal/axial panel currently showing timepoint 8 of the 4D scan, with its own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time02.setTitle(QCoreApplication.translate("MainWindow", u"Echo 8", None))
#if QT_CONFIG(tooltip)
        self.go_down_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data02.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data02.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data02.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data02.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data02.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data02.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data02.setToolTip(QCoreApplication.translate("MainWindow", u"Fit this view to the window, resetting pan and zoom.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data02.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.groupBox_25.setToolTip(QCoreApplication.translate("MainWindow", u"Live voxel intensity value at the current cursor position.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem3 = self.tableintensity_data0.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem4 = self.tableintensity_data0.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem5 = self.tableintensity_data0.horizontalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
#if QT_CONFIG(tooltip)
        self.groupbox_legend0.setToolTip(QCoreApplication.translate("MainWindow", u"Color scale (colorbar) for interpreting the heatmap's intensity values.", None))
#endif // QT_CONFIG(tooltip)
        self.groupbox_legend0.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap Intensities", None))
#if QT_CONFIG(tooltip)
        self.groupBox_21.setToolTip(QCoreApplication.translate("MainWindow", u"Lambda position marked on this animal's own scan, alongside where it lands in the atlas after registration.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"Lambda Coordinates xyz", None))
        self.lineEdit_58.setText(QCoreApplication.translate("MainWindow", u"Animal Lambda Coordinates [xyz]", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_d_lambdax.setToolTip(QCoreApplication.translate("MainWindow", u"Per-axis offset between your picked lambda and the atlas-predicted location", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_d_lambdax.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_lambda_y.setToolTip(QCoreApplication.translate("MainWindow", u"Lambda coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_atlas_lambda_x.setToolTip(QCoreApplication.translate("MainWindow", u"Where the atlas predicts lambda to be, in this animal's MRI (read-only)", None))
#endif // QT_CONFIG(tooltip)
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Absolute Distance between Animal and Atlas Lambda</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_tp_lambda.setToolTip(QCoreApplication.translate("MainWindow", u"Pick the lambda point by clicking it in the MRI view", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_tp_lambda.setText(QCoreApplication.translate("MainWindow", u"Save Cursor Position \n"
" as Lambda", None))
        self.lineEdit_20.setText(QCoreApplication.translate("MainWindow", u"Atlas registered Lambda [xyz]", None))
#if QT_CONFIG(tooltip)
        self.spinBox_atlas_lambda_z.setToolTip(QCoreApplication.translate("MainWindow", u"Where the atlas predicts lambda to be, in this animal's MRI (read-only)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_d_lambday.setToolTip(QCoreApplication.translate("MainWindow", u"Per-axis offset between your picked lambda and the atlas-predicted location", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_d_lambday.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_d_lambdaz.setToolTip(QCoreApplication.translate("MainWindow", u"Per-axis offset between your picked lambda and the atlas-predicted location", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_d_lambdaz.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_lambda_x.setToolTip(QCoreApplication.translate("MainWindow", u"Lambda coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_atlas_lambda_y.setToolTip(QCoreApplication.translate("MainWindow", u"Where the atlas predicts lambda to be, in this animal's MRI (read-only)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_tp_lambda_z.setToolTip(QCoreApplication.translate("MainWindow", u"Lambda coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_95.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_96.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_97.setText(QCoreApplication.translate("MainWindow", u"axial", None))
#if QT_CONFIG(tooltip)
        self.groupBox_12.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma position marked on this animal's own scan, alongside where it lands in the atlas after registration.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Bregma Coordinates xyz ", None))
#if QT_CONFIG(tooltip)
        self.spinBox_atlas_bregma_x.setToolTip(QCoreApplication.translate("MainWindow", u"Where the atlas predicts bregma to be, in this animal's MRI (read-only)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_29.setText(QCoreApplication.translate("MainWindow", u"Atlas registered Bregma [xyz]", None))
        self.textEdit_4.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Absolute Distance between Animal and Atlas Bregma</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_tp_bregma.setToolTip(QCoreApplication.translate("MainWindow", u"Pick the bregma point by clicking it in the MRI view", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_tp_bregma.setText(QCoreApplication.translate("MainWindow", u"Save Cursor Position \n"
" as Bregma", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_bregma_x.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_d_bregmax.setToolTip(QCoreApplication.translate("MainWindow", u"Per-axis offset between your picked bregma and the atlas-predicted location", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_d_bregmax.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_d_bregmaz.setToolTip(QCoreApplication.translate("MainWindow", u"Per-axis offset between your picked bregma and the atlas-predicted location", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_d_bregmaz.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_bregma_z.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_tp_bregma_y.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_atlas_bregma_z.setToolTip(QCoreApplication.translate("MainWindow", u"Where the atlas predicts bregma to be, in this animal's MRI (read-only)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_atlas_bregma_y.setToolTip(QCoreApplication.translate("MainWindow", u"Where the atlas predicts bregma to be, in this animal's MRI (read-only)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_24.setText(QCoreApplication.translate("MainWindow", u"Animal Bregma Coordinates [xyz]", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_d_bregmay.setToolTip(QCoreApplication.translate("MainWindow", u"Per-axis offset between your picked bregma and the atlas-predicted location", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_d_bregmay.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.lineEdit_92.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_93.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_94.setText(QCoreApplication.translate("MainWindow", u"axial", None))
#if QT_CONFIG(tooltip)
        self.groupBox_22.setToolTip(QCoreApplication.translate("MainWindow", u"Compares the Bregma-Lambda distance measured on this animal's scan to the atlas, and the scaling ratio between them.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"Distances  between Bregma and Lambda", None))
        self.lineEdit_31.setText(QCoreApplication.translate("MainWindow", u"Animal MRI", None))
        self.lineEdit_43.setText(QCoreApplication.translate("MainWindow", u"Ratio: Animal / Atlas", None))
        self.lineEdit_33.setText(QCoreApplication.translate("MainWindow", u"Atlas registered points", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_distanceAtlas.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma-lambda distance in the atlas template", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_distanceAtlas.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_tp_ratio.setToolTip(QCoreApplication.translate("MainWindow", u"Ratio of this animal's bregma-lambda distance to the atlas's -- a scaling sanity check", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_tp_ratio.setSuffix("")
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_distance.setToolTip(QCoreApplication.translate("MainWindow", u"Distance between your picked bregma and lambda, in this animal's MRI", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_distance.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.textEdit_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Please select Bregma and Lambda in the MRI Image</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_tp_next0.setToolTip(QCoreApplication.translate("MainWindow", u"Continue to the next step (mark forbidden regions)", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_tp_next0.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.groupBox_80.setTitle(QCoreApplication.translate("MainWindow", u"Misalignment of Coronal Slice [Degree]", None))
#if QT_CONFIG(tooltip)
        self.pushButton_PyLdetection.setToolTip(QCoreApplication.translate("MainWindow", u"Channel in CA1 needed", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_PyLdetection.setText(QCoreApplication.translate("MainWindow", u"Detect PyL using DWI", None))
#if QT_CONFIG(tooltip)
        self.pushButton_SaveTraj.setToolTip(QCoreApplication.translate("MainWindow", u"Save the planned trajectories", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_SaveTraj.setText(QCoreApplication.translate("MainWindow", u"Save Trajectory", None))
#if QT_CONFIG(tooltip)
        self.groupBox_shank.setToolTip(QCoreApplication.translate("MainWindow", u"Electrode geometry summary for the selected shank (channel count and spacing), plus a button to define a custom, non-standard layout.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_shank.setTitle(QCoreApplication.translate("MainWindow", u"Shank Info", None))
#if QT_CONFIG(tooltip)
        self.pushButton_geometry_dfx.setToolTip(QCoreApplication.translate("MainWindow", u"Open the panel for defining custom (bent) shank geometry from a DXF file", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_geometry_dfx.setText(QCoreApplication.translate("MainWindow", u"Edit User-defined Shank Geometry", None))
        self.lineEdit_21.setText(QCoreApplication.translate("MainWindow", u"Total Channels", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_channels.setToolTip(QCoreApplication.translate("MainWindow", u"Number of electrode contacts on this shank", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_22.setText(QCoreApplication.translate("MainWindow", u"Channel Separation", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_separation.setToolTip(QCoreApplication.translate("MainWindow", u"Distance between adjacent contacts", None))
#endif // QT_CONFIG(tooltip)
        self.spinBox_tp_separation.setSuffix(QCoreApplication.translate("MainWindow", u"um", None))
#if QT_CONFIG(tooltip)
        self.pushButton_tp_3d.setToolTip(QCoreApplication.translate("MainWindow", u"Open a 3D view of the atlas and planned shanks alongside this window", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_tp_3d.setText(QCoreApplication.translate("MainWindow", u"3D Visualilsation", None))
#if QT_CONFIG(tooltip)
        self.groupBox_79.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma position marked on this animal's own scan, alongside where it lands in the atlas after registration.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_79.setTitle(QCoreApplication.translate("MainWindow", u"Skull Insertion Point Coordinates xyz ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_insertionPoint.setToolTip(QCoreApplication.translate("MainWindow", u"Pick the bregma point by clicking it in the MRI view", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_insertionPoint.setText(QCoreApplication.translate("MainWindow", u"Save Cursor Position \n"
" as Skull Insertion Point", None))
#if QT_CONFIG(tooltip)
        self.spinBox_depth.setToolTip(QCoreApplication.translate("MainWindow", u"Per-axis offset between your picked bregma and the atlas-predicted location", None))
#endif // QT_CONFIG(tooltip)
        self.spinBox_depth.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.spinBox_insertion_y.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_107.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
#if QT_CONFIG(tooltip)
        self.spinBox_insertion_z.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_insertion_x.setToolTip(QCoreApplication.translate("MainWindow", u"Bregma coordinate in the subject's own MRI (voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_insertion_shank.setItemText(0, QCoreApplication.translate("MainWindow", u"test", None))

        self.pushButton_nextShank.setText(QCoreApplication.translate("MainWindow", u"NEXT", None))
        self.lineEdit_108.setText(QCoreApplication.translate("MainWindow", u"axial", None))
        self.lineEdit_106.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.textEdit_14.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Depth between Insertion and deepest Point</p></body></html>", None))
        self.textEdit_5.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Please select Skull Insertion Point of each shank</span></p></body></html>", None))
        self.lineEdit_vis3D.setText(QCoreApplication.translate("MainWindow", u"3D Visualisation", None))
#if QT_CONFIG(tooltip)
        self.pushButton_seg3D.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the 3D camera view", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_seg3D.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.textEdit_8.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">SAGITTAL</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data3d1.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data3d1.setText("")
#if QT_CONFIG(tooltip)
        self.zoom_out_data3d1.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data3d1.setText("")
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d1.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d1.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data3d1.setToolTip(QCoreApplication.translate("MainWindow", u"Pan down", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data3d1.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data3d1.setToolTip(QCoreApplication.translate("MainWindow", u"Pan up", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data3d1.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data3d1.setToolTip(QCoreApplication.translate("MainWindow", u"Pan left", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data3d1.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data3d1.setToolTip(QCoreApplication.translate("MainWindow", u"Pan right", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data3d1.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.textEdit_16.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">SAGITTAL (constraint)</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data3d1_3.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data3d1_3.setText("")
#if QT_CONFIG(tooltip)
        self.zoom_out_data3d1_3.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data3d1_3.setText("")
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d1_3.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d1_3.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data3d1_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan down", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data3d1_3.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data3d1_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan up", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data3d1_3.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data3d1_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan left", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data3d1_3.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data3d1_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan right", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data3d1_3.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.textEdit_11.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">3D View (Sagittal)</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_resetSagittal.setToolTip(QCoreApplication.translate("MainWindow", u"Reset this view's zoom/pan to default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resetSagittal.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.textEdit_9.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">CORONAL</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data3d2.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data3d2.setText("")
#if QT_CONFIG(tooltip)
        self.zoom_out_data3d2.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data3d2.setText("")
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d2.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d2.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data3d2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan down", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data3d2.setText("")
#if QT_CONFIG(tooltip)
        self.go_up_data3d2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan up", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data3d2.setText("")
#if QT_CONFIG(tooltip)
        self.go_left_data3d2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan left", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data3d2.setText("")
#if QT_CONFIG(tooltip)
        self.go_right_data3d2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan right", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data3d2.setText("")
        self.textEdit_15.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">CORONAL (constraint)</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data3d2_3.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data3d2_3.setText("")
#if QT_CONFIG(tooltip)
        self.zoom_out_data3d2_3.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data3d2_3.setText("")
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d2_3.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d2_3.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data3d2_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan down", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data3d2_3.setText("")
#if QT_CONFIG(tooltip)
        self.go_up_data3d2_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan up", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data3d2_3.setText("")
#if QT_CONFIG(tooltip)
        self.go_left_data3d2_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan left", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data3d2_3.setText("")
#if QT_CONFIG(tooltip)
        self.go_right_data3d2_3.setToolTip(QCoreApplication.translate("MainWindow", u"Pan right", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data3d2_3.setText("")
        self.textEdit_10.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">3D View (Coronal)</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_resetCoronal.setToolTip(QCoreApplication.translate("MainWindow", u"Reset this view's zoom/pan to default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resetCoronal.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.textEdit_7.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">AXIAL</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.go_down_data3d0.setToolTip(QCoreApplication.translate("MainWindow", u"Pan down", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data3d0.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data3d0.setToolTip(QCoreApplication.translate("MainWindow", u"Pan up", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data3d0.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data3d0.setToolTip(QCoreApplication.translate("MainWindow", u"Pan left", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data3d0.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data3d0.setToolTip(QCoreApplication.translate("MainWindow", u"Pan right", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data3d0.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d0.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d0.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data3d0.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data3d0.setText("")
#if QT_CONFIG(tooltip)
        self.zoom_out_data3d0.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data3d0.setText("")
        self.textEdit_12.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">SAGITTAL</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.go_down_data3d1_2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan down", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data3d1_2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan up", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data3d1_2.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data3d1_2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan left", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data3d1_2.setToolTip(QCoreApplication.translate("MainWindow", u"Pan right", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data3d1_2.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data3d1_2.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data3d1_2.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d1_2.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.pushButton_resetAxial.setToolTip(QCoreApplication.translate("MainWindow", u"Reset this view's zoom/pan to default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resetAxial.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.lineEdit_59.setText(QCoreApplication.translate("MainWindow", u"Change Depth of Slicing", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider_axial3D.setToolTip(QCoreApplication.translate("MainWindow", u"Change which axial slice depth is shown", None))
#endif // QT_CONFIG(tooltip)
        self.textEdit_13.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">3D View (Axial)</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.groupBox_68.setToolTip(QCoreApplication.translate("MainWindow", u"Live cursor position in this view, reported separately for the coronal, sagittal, and axial planes.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_68.setTitle(QCoreApplication.translate("MainWindow", u"Cursor Position (x,y,z)", None))
        self.lineEdit_68.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
#if QT_CONFIG(tooltip)
        self.spinBox_y_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Cursor position (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_z_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Cursor position (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_x_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Cursor position (voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_67.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_77.setText(QCoreApplication.translate("MainWindow", u"axial", None))
#if QT_CONFIG(tooltip)
        self.groupBox_contrast.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust this 3D view's window/level (contrast/brightness) with the sliders, or use Auto/Reset.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_contrast.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustments", None))
#if QT_CONFIG(tooltip)
        self.changeContrast_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust contrast (window width)", None))
#endif // QT_CONFIG(tooltip)
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_window_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Current contrast (window width) value", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeBrightness_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust brightness (window level)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Auto-adjust contrast/brightness", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data3d.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Reset contrast/brightness to default", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data3d.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.display_level_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Current brightness (window level) value", None))
#endif // QT_CONFIG(tooltip)
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.comboBox_Contrastimage.setToolTip(QCoreApplication.translate("MainWindow", u"Select which loaded layer these contrast controls adjust", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_40.setToolTip(QCoreApplication.translate("MainWindow", u"Live voxel intensity value at the current cursor position.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_40.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem6 = self.tableintensity_data3d.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem7 = self.tableintensity_data3d.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem8 = self.tableintensity_data3d.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
#if QT_CONFIG(tooltip)
        self.tableintensity_data3d.setToolTip(QCoreApplication.translate("MainWindow", u"Loaded layers: toggle visibility, view name/intensity, adjust opacity", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_70.setToolTip(QCoreApplication.translate("MainWindow", u"Live cursor position in this view, reported separately for the coronal, sagittal, and axial planes.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_70.setTitle(QCoreApplication.translate("MainWindow", u"Cursor Position (x,y,z)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_x_data3d_2.setToolTip(QCoreApplication.translate("MainWindow", u"Cursor position (voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_80.setText(QCoreApplication.translate("MainWindow", u"axial", None))
#if QT_CONFIG(tooltip)
        self.spinBox_z_data3d_2.setToolTip(QCoreApplication.translate("MainWindow", u"Cursor position (voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_y_data3d_2.setToolTip(QCoreApplication.translate("MainWindow", u"Cursor position (voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_78.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_79.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.groupBox_72.setTitle("")
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_distance_shank.setToolTip(QCoreApplication.translate("MainWindow", u"Length of this shank's trajectory", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_distance_shank.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.textEdit_distance_shank.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Distance between Insertion Point and Deepest Point  in MRI space</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.groupBox_74.setToolTip(QCoreApplication.translate("MainWindow", u"Marks the electrode's deepest point at the current cursor position for the selected shank.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_74.setTitle(QCoreApplication.translate("MainWindow", u"Deepest Point", None))
#if QT_CONFIG(tooltip)
        self.pushButton_tp_deep.setToolTip(QCoreApplication.translate("MainWindow", u"Pick this shank's deepest point by clicking it in the MRI view", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_tp_deep.setText(QCoreApplication.translate("MainWindow", u"Save Cursor Position \n"
" as Deepest-Point", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_deep_z.setToolTip(QCoreApplication.translate("MainWindow", u"Deepest point coordinate (atlas voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_tp_deep_x.setToolTip(QCoreApplication.translate("MainWindow", u"Deepest point coordinate (atlas voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_tp_deep_y.setToolTip(QCoreApplication.translate("MainWindow", u"Deepest point coordinate (atlas voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_89.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_90.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_91.setText(QCoreApplication.translate("MainWindow", u"axial", None))
#if QT_CONFIG(tooltip)
        self.groupBox_71.setToolTip(QCoreApplication.translate("MainWindow", u"Live voxel intensity value at the current cursor position.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_71.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem9 = self.tableintensity_data3d_2.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem10 = self.tableintensity_data3d_2.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem11 = self.tableintensity_data3d_2.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
#if QT_CONFIG(tooltip)
        self.tableintensity_data3d_2.setToolTip(QCoreApplication.translate("MainWindow", u"Loaded layers (mirrors the table above during this step)", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_contrastAdjustments.setText(QCoreApplication.translate("MainWindow", u"Contrast Adjustments", None))
#if QT_CONFIG(tooltip)
        self.checkBox_brain_region.setToolTip(QCoreApplication.translate("MainWindow", u"Show the anatomical region name next to the shank line", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_brain_region.setText(QCoreApplication.translate("MainWindow", u"Show Brain Region while Hovering", None))
#if QT_CONFIG(tooltip)
        self.groupBox_75.setToolTip(QCoreApplication.translate("MainWindow", u"Marks the electrode's brain-surface insertion point, snapped to the nearest edge in the view you click, for the selected shank.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_75.setTitle(QCoreApplication.translate("MainWindow", u"Insertion Point", None))
#if QT_CONFIG(tooltip)
        self.pushButton_tp_insert.setToolTip(QCoreApplication.translate("MainWindow", u"Pick this shank's insertion point by clicking it in the MRI view", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_tp_insert.setText(QCoreApplication.translate("MainWindow", u"Save Edge Point vertically above \n"
" Cursor Position as Insert-Point", None))
#if QT_CONFIG(tooltip)
        self.spinBox_tp_insert_x.setToolTip(QCoreApplication.translate("MainWindow", u"Insertion point coordinate (atlas voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_tp_insert_y.setToolTip(QCoreApplication.translate("MainWindow", u"Insertion point coordinate (atlas voxel index)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_tp_insert_z.setToolTip(QCoreApplication.translate("MainWindow", u"Insertion point coordinate (atlas voxel index)", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_19.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_30.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_88.setText(QCoreApplication.translate("MainWindow", u"axial", None))
        self.groupBox_73.setTitle("")
#if QT_CONFIG(tooltip)
        self.pushButton_removeShank.setToolTip(QCoreApplication.translate("MainWindow", u"Remove the currently selected shank", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_removeShank.setText(QCoreApplication.translate("MainWindow", u"Remove  \n"
" Shank", None))
#if QT_CONFIG(tooltip)
        self.comboBox_Shanks.setToolTip(QCoreApplication.translate("MainWindow", u"Select which shank to edit", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox_tpColor.setToolTip(QCoreApplication.translate("MainWindow", u"Change the selected shank's display color", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_addShank.setToolTip(QCoreApplication.translate("MainWindow", u"Add a new shank", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_addShank.setText(QCoreApplication.translate("MainWindow", u"Add Another \n"
" Shank", None))
#if QT_CONFIG(tooltip)
        self.pushButton_sagittalView.setToolTip(QCoreApplication.translate("MainWindow", u"Switch this panel between the 2D slice and a 3D view clipped along the trajectory", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_sagittalView.setText(QCoreApplication.translate("MainWindow", u"Change \n"
" Sagittal View", None))
#if QT_CONFIG(tooltip)
        self.pushButton_coronalView.setToolTip(QCoreApplication.translate("MainWindow", u"Switch this panel between the 2D slice and a 3D view clipped along the trajectory", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_coronalView.setText(QCoreApplication.translate("MainWindow", u"Change \n"
" Coronal View", None))
        self.checkBox_constraint_90deg_coronal.setText(QCoreApplication.translate("MainWindow", u"Constraint Angle in Coronal to 0deg ", None))
        self.checkBox_constraint_90deg.setText(QCoreApplication.translate("MainWindow", u"Constraint Angle in Sagittal to 90deg ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_axialView.setToolTip(QCoreApplication.translate("MainWindow", u"Switch this panel between the 2D slice and a 3D view clipped along the trajectory", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_axialView.setText(QCoreApplication.translate("MainWindow", u"Change \n"
" Axial View", None))
#if QT_CONFIG(tooltip)
        self.pushButton_dfx_ok.setToolTip(QCoreApplication.translate("MainWindow", u"Close this panel", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_dfx_ok.setText(QCoreApplication.translate("MainWindow", u"OK", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_probe.setToolTip(QCoreApplication.translate("MainWindow", u"Add a new shank using the geometry computed above", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_probe.setText(QCoreApplication.translate("MainWindow", u"Add current \n"
" run as shank", None))
        self.groupBox_69.setTitle("")
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_bundle_ratio.setToolTip(QCoreApplication.translate("MainWindow", u"Fraction of the probe's channels bundled together at the base (0-1)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_xml.setToolTip(QCoreApplication.translate("MainWindow", u"Browse for a Neuroscope XML file to read this probe's channel groups", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_xml.setText(QCoreApplication.translate("MainWindow", u"Please load .xml file for selected Shank", None))
#if QT_CONFIG(tooltip)
        self.pushButton_dfx_run.setToolTip(QCoreApplication.translate("MainWindow", u"Compute the bent shank geometry from the loaded DXF file", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_dfx_run.setText(QCoreApplication.translate("MainWindow", u"Run bending model", None))
        self.lineEdit_76.setText(QCoreApplication.translate("MainWindow", u"Max bend angle (deg)", None))
        self.lineEdit_73.setText(QCoreApplication.translate("MainWindow", u"Artificial extension (um)", None))
        self.textEdit_channels_xml.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Please load dxf file to see channel list</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.spinBox_max_bend_angle.setToolTip(QCoreApplication.translate("MainWindow", u"Maximum angle allowed for a single bend", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_74.setText(QCoreApplication.translate("MainWindow", u"Bundle ratio (0-1)", None))
        self.lineEdit_72.setText(QCoreApplication.translate("MainWindow", u"Bend radius 1 (um)", None))
        self.lineEdit_70.setText(QCoreApplication.translate("MainWindow", u"Arc points", None))
        self.lineEdit_69.setText(QCoreApplication.translate("MainWindow", u"Um per DFX unit", None))
#if QT_CONFIG(tooltip)
        self.spinBox_bend_r1.setToolTip(QCoreApplication.translate("MainWindow", u"Radius of the first bend", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_first_bend_distance.setToolTip(QCoreApplication.translate("MainWindow", u"Distance from the tip to where the first bend starts", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_export.setToolTip(QCoreApplication.translate("MainWindow", u"Export this shank's bent geometry to a JSON file", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export.setText(QCoreApplication.translate("MainWindow", u"Export as \n"
" .json", None))
#if QT_CONFIG(tooltip)
        self.spinBox_um_per_unit.setToolTip(QCoreApplication.translate("MainWindow", u"Scale: micrometers per unit in the DXF drawing", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_bend_r2.setToolTip(QCoreApplication.translate("MainWindow", u"Radius of the second bend", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkBox_defaultchannels.setToolTip(QCoreApplication.translate("MainWindow", u"Use sequential channel numbering (0..N-1) instead of a custom list", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_defaultchannels.setText(QCoreApplication.translate("MainWindow", u"Use default Channel IDs", None))
#if QT_CONFIG(tooltip)
        self.spinBox_arc_points.setToolTip(QCoreApplication.translate("MainWindow", u"Number of points used to approximate each curved bend", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_71.setText(QCoreApplication.translate("MainWindow", u"Bend radius 2 (um)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_artificial_extension.setToolTip(QCoreApplication.translate("MainWindow", u"Extra shank length added beyond the DXF geometry's own end", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_75.setText(QCoreApplication.translate("MainWindow", u"First bend distance (um)", None))
#if QT_CONFIG(tooltip)
        self.pushButton_dfx.setToolTip(QCoreApplication.translate("MainWindow", u"Browse for a DXF file describing this probe's custom (bent) geometry", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_dfx.setText(QCoreApplication.translate("MainWindow", u"Please load dxf File", None))
#if QT_CONFIG(tooltip)
        self.comboBox_geometry_shanks.setToolTip(QCoreApplication.translate("MainWindow", u"Select which shank's custom geometry to edit", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_metadata.setToolTip(QCoreApplication.translate("MainWindow", u"Metadata of Files", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_metadata.setText("")
#if QT_CONFIG(tooltip)
        self.groupBox_data1.setToolTip(QCoreApplication.translate("MainWindow", u"This dataset's coronal/sagittal/axial panels, each with its own timepoint, contrast, and cursor controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_data1.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
#if QT_CONFIG(tooltip)
        self.groupbox_legend1.setToolTip(QCoreApplication.translate("MainWindow", u"Color scale (colorbar) for interpreting the heatmap's intensity values.", None))
#endif // QT_CONFIG(tooltip)
        self.groupbox_legend1.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap Intensities", None))
#if QT_CONFIG(tooltip)
        self.groupBox_time11.setToolTip(QCoreApplication.translate("MainWindow", u"Coronal/sagittal/axial panel currently showing timepoint 4 of the 4D scan, with its own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time11.setTitle(QCoreApplication.translate("MainWindow", u"Echo 4", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Fit this view to the window, resetting pan and zoom.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data11.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data11.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data11.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data11.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data11.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data11.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data11.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.groupBox_38.setToolTip(QCoreApplication.translate("MainWindow", u"Live voxel intensity value at the current cursor position.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_38.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem12 = self.tableintensity_data1.horizontalHeaderItem(1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem13 = self.tableintensity_data1.horizontalHeaderItem(2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem14 = self.tableintensity_data1.horizontalHeaderItem(3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
#if QT_CONFIG(tooltip)
        self.heatmap_data1.setToolTip(QCoreApplication.translate("MainWindow", u"Computed MRID-tag heatmap for this dataset; appears once the heatmap/segmentation analysis has been run.", None))
#endif // QT_CONFIG(tooltip)
        self.heatmap_data1.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data13.setToolTip(QCoreApplication.translate("MainWindow", u"Fit this view to the window, resetting pan and zoom.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data13.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data13.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data13.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data13.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data13.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data13.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data13.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data13.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data13.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data13.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data13.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data13.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data13.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.groupBox_24.setToolTip(QCoreApplication.translate("MainWindow", u"Live crosshair cursor position for this dataset, in voxel coordinates.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Cursor position (x,y,z)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_y_data1.setToolTip(QCoreApplication.translate("MainWindow", u"Y voxel coordinate of the cursor for this comparison panel; type a value to move the crosshair there.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_x_data1.setToolTip(QCoreApplication.translate("MainWindow", u"X voxel coordinate of the cursor for this comparison panel; type a value to move the crosshair there.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_z_data1.setToolTip(QCoreApplication.translate("MainWindow", u"Z voxel coordinate of the cursor for this comparison panel; type a value to move the crosshair there.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_101.setText(QCoreApplication.translate("MainWindow", u"sagittal", None))
        self.lineEdit_102.setText(QCoreApplication.translate("MainWindow", u"coronal", None))
        self.lineEdit_103.setText(QCoreApplication.translate("MainWindow", u"axial", None))
#if QT_CONFIG(tooltip)
        self.groupBox_time12.setToolTip(QCoreApplication.translate("MainWindow", u"Echo panel for one 4D frame: the title updates to the frame's actual echo, and it holds this frame's own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time12.setTitle(QCoreApplication.translate("MainWindow", u"Echo 8", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data12.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data12.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data12.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data12.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data12.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data12.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data12.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.groupBox_51.setToolTip(QCoreApplication.translate("MainWindow", u"Choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_51.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Slide to choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Index of the 4D echo (frame) currently displayed in this panel; type a value to jump to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_53.setToolTip(QCoreApplication.translate("MainWindow", u"Auto-compute or reset the window/level (brightness/contrast) for this panel's image.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_53.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the window/level (brightness/contrast) to its initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data10.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute the window/level (brightness/contrast) from the image data.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data10.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time1.setTabText(self.tabWidget_time1.indexOf(self.tabWidget_time12), QCoreApplication.translate("MainWindow", u"Echo 1", None))
#if QT_CONFIG(tooltip)
        self.groupBox_45.setToolTip(QCoreApplication.translate("MainWindow", u"Choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_45.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Slide to choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Index of the 4D echo (frame) currently displayed in this panel; type a value to jump to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_54.setToolTip(QCoreApplication.translate("MainWindow", u"Auto-compute or reset the window/level (brightness/contrast) for this panel's image.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_54.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute the window/level (brightness/contrast) from the image data.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data11.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data11.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the window/level (brightness/contrast) to its initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data11.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.tabWidget_time1.setTabText(self.tabWidget_time1.indexOf(self.tabWidget_time10), QCoreApplication.translate("MainWindow", u"Echo 2", None))
#if QT_CONFIG(tooltip)
        self.groupBox_55.setToolTip(QCoreApplication.translate("MainWindow", u"Choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_55.setTitle(QCoreApplication.translate("MainWindow", u"Echo Slider", None))
#if QT_CONFIG(tooltip)
        self.changetimestamp_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Slide to choose which 4D echo (frame) is displayed in this panel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.displaytimestamp_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Index of the 4D echo (frame) currently displayed in this panel; type a value to jump to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_56.setToolTip(QCoreApplication.translate("MainWindow", u"Auto-compute or reset the window/level (brightness/contrast) for this panel's image.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_56.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the window/level (brightness/contrast) to its initial values.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_data12.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_auto_data12.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically compute the window/level (brightness/contrast) from the image data.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_auto_data12.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time1.setTabText(self.tabWidget_time1.indexOf(self.tabWidget_time11), QCoreApplication.translate("MainWindow", u"Echo 3", None))
#if QT_CONFIG(tooltip)
        self.groupBox_time10.setToolTip(QCoreApplication.translate("MainWindow", u"Echo panel for one 4D frame: the title updates to the frame's actual echo, and it holds this frame's own pan/zoom controls.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_time10.setTitle(QCoreApplication.translate("MainWindow", u"Echo 0", None))
#if QT_CONFIG(tooltip)
        self.zoom_in_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_in_data10.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.zoom_out_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on this view.", None))
#endif // QT_CONFIG(tooltip)
        self.zoom_out_data10.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(tooltip)
        self.fit_to_zoom_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Fit the image to the window.", None))
#endif // QT_CONFIG(tooltip)
        self.fit_to_zoom_data10.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
#if QT_CONFIG(tooltip)
        self.go_down_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view down.", None))
#endif // QT_CONFIG(tooltip)
        self.go_down_data10.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_up_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view up.", None))
#endif // QT_CONFIG(tooltip)
        self.go_up_data10.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(tooltip)
        self.go_left_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view left.", None))
#endif // QT_CONFIG(tooltip)
        self.go_left_data10.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(tooltip)
        self.go_right_data10.setToolTip(QCoreApplication.translate("MainWindow", u"Pan the view right.", None))
#endif // QT_CONFIG(tooltip)
        self.go_right_data10.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.file_name_displayed.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_barcode.setTitle(QCoreApplication.translate("MainWindow", u"MRID Barcode", None))
        ___qtablewidgetitem15 = self.tableWidget_barcode.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Duo", None));
        ___qtablewidgetitem16 = self.tableWidget_barcode.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Trio", None));
        ___qtablewidgetitem17 = self.tableWidget_barcode.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Quad", None));
        ___qtablewidgetitem18 = self.tableWidget_barcode.horizontalHeaderItem(3)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Penta", None));
        ___qtablewidgetitem19 = self.tableWidget_barcode.verticalHeaderItem(0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Probabilities", None));
        ___qtablewidgetitem20 = self.tableWidget_barcode.verticalHeaderItem(1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Similarities", None));
#if QT_CONFIG(tooltip)
        self.groupBox_4.setToolTip(QCoreApplication.translate("MainWindow", u"1D intensity profile along the selected shank's channels, colored by anatomical region with the pyramidal layer marked; shown only for shanks that cross CA1.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"CA1 Signal", None))
#if QT_CONFIG(tooltip)
        self.groupbox_barcode1.setToolTip(QCoreApplication.translate("MainWindow", u"The barcode re-derived from the assigned MRID tag, for comparison against the detected barcode above.", None))
#endif // QT_CONFIG(tooltip)
        self.groupbox_barcode1.setTitle(QCoreApplication.translate("MainWindow", u"Barcode reconstructed", None))
#if QT_CONFIG(tooltip)
        self.comboBox_mridBarcodes.setToolTip(QCoreApplication.translate("MainWindow", u"Select which shank/tag's barcode and CA1 signal to display below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupbox_barcode0.setToolTip(QCoreApplication.translate("MainWindow", u"The raw MRID barcode pattern as detected directly from the scan.", None))
#endif // QT_CONFIG(tooltip)
        self.groupbox_barcode0.setTitle(QCoreApplication.translate("MainWindow", u"Barcode detected", None))
#if QT_CONFIG(tooltip)
        self.pushButton_questionmark.setToolTip(QCoreApplication.translate("MainWindow", u"Re-show the current workflow's step-by-step instructions.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_questionmark.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PostSurgery), QCoreApplication.translate("MainWindow", u"MRI Images", None))
        self.tabWidget_visualisation.setTabText(self.tabWidget_visualisation.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u" MRID Location", None))
#if QT_CONFIG(tooltip)
        self.comboBox_mridTag_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Switch which MRID timepoint tag is shown in this 3D view.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_slicez_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Slicing in Axial Direction", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicez_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicey_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Slicing in Coronal Direction", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicey_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicex_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Slicing in Sagittal Direction", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicex_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_Noslicing_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Exit Slicing Mode", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Noslicing_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.change_perspective_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Change Perspective", None))
#endif // QT_CONFIG(tooltip)
        self.change_perspective_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.resetCamera_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Reset Camera View", None))
#endif // QT_CONFIG(tooltip)
        self.resetCamera_vis3D.setText("")
        self.tabWidget_visualisation.setTabText(self.tabWidget_visualisation.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"3D Visualisation", None))
        self.menuGUI.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTrajectory_Planning.setTitle(QCoreApplication.translate("MainWindow", u"Trajectory Planning", None))
        self.menuStructural_Tools.setTitle(QCoreApplication.translate("MainWindow", u"Structural Tools", None))
        self.menuTime_Series_Tools.setTitle(QCoreApplication.translate("MainWindow", u"Time-Series Tools", None))
        self.menuElectrode_Localization.setTitle(QCoreApplication.translate("MainWindow", u"Electrode Localization", None))
        self.menuEphys_Analysis.setTitle(QCoreApplication.translate("MainWindow", u"Ephys Analysis", None))
    # retranslateUi

