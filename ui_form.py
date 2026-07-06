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
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox,
    QApplication, QCheckBox, QComboBox, QDialogButtonBox,
    QDockWidget, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QRadioButton,
    QScrollBar, QSizePolicy, QSlider, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QTableView,
    QTableWidget, QTableWidgetItem, QTextBrowser, QTextEdit,
    QToolBox, QToolButton, QWidget)

from mplwidget import MplWidget
from pgwidget import PgWidget
from pyqtgraph import PlotWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(2184, 2156)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1600, 0))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
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
        self.actionTrajectory_Planning = QAction(MainWindow)
        self.actionTrajectory_Planning.setObjectName(u"actionTrajectory_Planning")
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
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabBarAutoHide(False)
        self.PostSurgery = QWidget()
        self.PostSurgery.setObjectName(u"PostSurgery")
        self.gridLayout_70 = QGridLayout(self.PostSurgery)
        self.gridLayout_70.setObjectName(u"gridLayout_70")
        self.gridLayout_70.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.groupBox_barcode = QGroupBox(self.PostSurgery)
        self.groupBox_barcode.setObjectName(u"groupBox_barcode")
        self.gridLayout_8 = QGridLayout(self.groupBox_barcode)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
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


        self.gridLayout_8.addWidget(self.groupbox_barcode1, 2, 0, 1, 1)

        self.comboBox_mridBarcodes = QComboBox(self.groupBox_barcode)
        self.comboBox_mridBarcodes.setObjectName(u"comboBox_mridBarcodes")

        self.gridLayout_8.addWidget(self.comboBox_mridBarcodes, 0, 0, 1, 1)

        self.tableWidget_barcode = QTableWidget(self.groupBox_barcode)
        if (self.tableWidget_barcode.columnCount() < 4):
            self.tableWidget_barcode.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_barcode.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget_barcode.rowCount() < 2):
            self.tableWidget_barcode.setRowCount(2)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_barcode.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_barcode.setVerticalHeaderItem(1, __qtablewidgetitem5)
        self.tableWidget_barcode.setObjectName(u"tableWidget_barcode")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget_barcode.sizePolicy().hasHeightForWidth())
        self.tableWidget_barcode.setSizePolicy(sizePolicy2)
        self.tableWidget_barcode.setMinimumSize(QSize(300, 76))
        self.tableWidget_barcode.setMaximumSize(QSize(721, 383))
        self.tableWidget_barcode.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_barcode.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_barcode.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_8.addWidget(self.tableWidget_barcode, 1, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox_barcode)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_27 = QGridLayout(self.groupBox_4)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.ca1_signal_widget = MplWidget(self.groupBox_4)
        self.ca1_signal_widget.setObjectName(u"ca1_signal_widget")

        self.gridLayout_27.addWidget(self.ca1_signal_widget, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_4, 4, 0, 1, 1)

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


        self.gridLayout_8.addWidget(self.groupbox_barcode0, 3, 0, 1, 1)


        self.gridLayout_70.addWidget(self.groupBox_barcode, 0, 4, 4, 1)

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
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_time11.sizePolicy().hasHeightForWidth())
        self.groupBox_time11.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
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
        icon = QIcon()
        icon.addFile(u"Icons/mri/downArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_down_data11.setIcon(icon)

        self.horizontalLayout_18.addWidget(self.go_down_data11)

        self.go_up_data11 = QToolButton(self.frame_7)
        self.go_up_data11.setObjectName(u"go_up_data11")
        icon1 = QIcon()
        icon1.addFile(u"Icons/mri/upArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_up_data11.setIcon(icon1)

        self.horizontalLayout_18.addWidget(self.go_up_data11)

        self.go_left_data11 = QToolButton(self.frame_7)
        self.go_left_data11.setObjectName(u"go_left_data11")
        icon2 = QIcon()
        icon2.addFile(u"Icons/mri/leftArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_left_data11.setIcon(icon2)

        self.horizontalLayout_18.addWidget(self.go_left_data11)

        self.go_right_data11 = QToolButton(self.frame_7)
        self.go_right_data11.setObjectName(u"go_right_data11")
        icon3 = QIcon()
        icon3.addFile(u"Icons/mri/rightArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_right_data11.setIcon(icon3)

        self.horizontalLayout_18.addWidget(self.go_right_data11)


        self.gridLayout_82.addLayout(self.horizontalLayout_18, 2, 8, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.zoom_in_data11 = QToolButton(self.frame_7)
        self.zoom_in_data11.setObjectName(u"zoom_in_data11")
        icon4 = QIcon()
        icon4.addFile(u"Icons/mri/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoom_in_data11.setIcon(icon4)

        self.horizontalLayout_3.addWidget(self.zoom_in_data11)

        self.zoom_out_data11 = QToolButton(self.frame_7)
        self.zoom_out_data11.setObjectName(u"zoom_out_data11")
        icon5 = QIcon()
        icon5.addFile(u"Icons/mri/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableintensity_data1.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        self.tableintensity_data1.setObjectName(u"tableintensity_data1")
        sizePolicy2.setHeightForWidth(self.tableintensity_data1.sizePolicy().hasHeightForWidth())
        self.tableintensity_data1.setSizePolicy(sizePolicy2)
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


        self.gridLayout_89.addWidget(self.groupBox_24, 1, 0, 1, 1)

        self.groupBox_time12 = QGroupBox(self.groupBox_data1)
        self.groupBox_time12.setObjectName(u"groupBox_time12")
        sizePolicy3.setHeightForWidth(self.groupBox_time12.sizePolicy().hasHeightForWidth())
        self.groupBox_time12.setSizePolicy(sizePolicy3)
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
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
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
        sizePolicy3.setHeightForWidth(self.groupBox_time10.sizePolicy().hasHeightForWidth())
        self.groupBox_time10.setSizePolicy(sizePolicy3)
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

        self.gridLayout_70.addWidget(self.groupBox_data1, 2, 1, 1, 3)

        self.file_name_displayed_4d = QTextEdit(self.PostSurgery)
        self.file_name_displayed_4d.setObjectName(u"file_name_displayed_4d")
        self.file_name_displayed_4d.setMinimumSize(QSize(56, 10))
        self.file_name_displayed_4d.setMaximumSize(QSize(16777215, 70))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.file_name_displayed_4d.setFont(font3)
        self.file_name_displayed_4d.setReadOnly(True)

        self.gridLayout_70.addWidget(self.file_name_displayed_4d, 0, 1, 1, 1)

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

        self.gridLayout_33.addWidget(self.spinBox_x_data2, 0, 0, 1, 1)

        self.spinBox_y_data2 = QSpinBox(self.groupBox_32)
        self.spinBox_y_data2.setObjectName(u"spinBox_y_data2")
        self.spinBox_y_data2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data2.setMinimum(1)
        self.spinBox_y_data2.setMaximum(120)

        self.gridLayout_33.addWidget(self.spinBox_y_data2, 0, 1, 1, 1)

        self.spinBox_z_data2 = QSpinBox(self.groupBox_32)
        self.spinBox_z_data2.setObjectName(u"spinBox_z_data2")
        self.spinBox_z_data2.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data2.setMinimum(1)
        self.spinBox_z_data2.setMaximum(60)

        self.gridLayout_33.addWidget(self.spinBox_z_data2, 0, 2, 1, 1)


        self.gridLayout_99.addWidget(self.groupBox_32, 1, 0, 1, 1)

        self.groupBox_time20 = QGroupBox(self.groupBox_data2)
        self.groupBox_time20.setObjectName(u"groupBox_time20")
        sizePolicy3.setHeightForWidth(self.groupBox_time20.sizePolicy().hasHeightForWidth())
        self.groupBox_time20.setSizePolicy(sizePolicy3)
        self.groupBox_time20.setMaximumSize(QSize(16777215, 16777215))
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
        self.go_down_data20.setIcon(icon)

        self.horizontalLayout_31.addWidget(self.go_down_data20)

        self.go_up_data20 = QToolButton(self.frame_8)
        self.go_up_data20.setObjectName(u"go_up_data20")
        self.go_up_data20.setIcon(icon1)

        self.horizontalLayout_31.addWidget(self.go_up_data20)

        self.go_left_data20 = QToolButton(self.frame_8)
        self.go_left_data20.setObjectName(u"go_left_data20")
        self.go_left_data20.setIcon(icon2)

        self.horizontalLayout_31.addWidget(self.go_left_data20)

        self.go_right_data20 = QToolButton(self.frame_8)
        self.go_right_data20.setObjectName(u"go_right_data20")
        self.go_right_data20.setIcon(icon3)

        self.horizontalLayout_31.addWidget(self.go_right_data20)


        self.gridLayout_98.addLayout(self.horizontalLayout_31, 2, 8, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.zoom_in_data20 = QToolButton(self.frame_8)
        self.zoom_in_data20.setObjectName(u"zoom_in_data20")
        self.zoom_in_data20.setIcon(icon4)

        self.horizontalLayout_4.addWidget(self.zoom_in_data20)

        self.zoom_out_data20 = QToolButton(self.frame_8)
        self.zoom_out_data20.setObjectName(u"zoom_out_data20")
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
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableintensity_data2.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        self.tableintensity_data2.setObjectName(u"tableintensity_data2")
        sizePolicy2.setHeightForWidth(self.tableintensity_data2.sizePolicy().hasHeightForWidth())
        self.tableintensity_data2.setSizePolicy(sizePolicy2)
        self.tableintensity_data2.setMaximumSize(QSize(16777215, 1677))
        self.tableintensity_data2.setContextMenuPolicy(Qt.NoContextMenu)
        self.tableintensity_data2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableintensity_data2.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableintensity_data2.horizontalHeader().setDefaultSectionSize(67)

        self.gridLayout_133.addWidget(self.tableintensity_data2, 1, 0, 1, 1)


        self.gridLayout_99.addWidget(self.groupBox_39, 1, 2, 1, 1)

        self.groupBox_time21 = QGroupBox(self.groupBox_data2)
        self.groupBox_time21.setObjectName(u"groupBox_time21")
        sizePolicy3.setHeightForWidth(self.groupBox_time21.sizePolicy().hasHeightForWidth())
        self.groupBox_time21.setSizePolicy(sizePolicy3)
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
        sizePolicy3.setHeightForWidth(self.groupBox_time22.sizePolicy().hasHeightForWidth())
        self.groupBox_time22.setSizePolicy(sizePolicy3)
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
        self.gridLayout_99.setColumnStretch(3, 1)

        self.gridLayout_70.addWidget(self.groupBox_data2, 3, 1, 1, 3)

        self.pushButton_metadata = QPushButton(self.PostSurgery)
        self.pushButton_metadata.setObjectName(u"pushButton_metadata")
        icon6 = QIcon()
        icon6.addFile(u"Icons/mri/person14.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_metadata.setIcon(icon6)
        self.pushButton_metadata.setIconSize(QSize(32, 32))

        self.gridLayout_70.addWidget(self.pushButton_metadata, 0, 2, 1, 1)

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
        sizePolicy3.setHeightForWidth(self.groupBox_time00.sizePolicy().hasHeightForWidth())
        self.groupBox_time00.setSizePolicy(sizePolicy3)
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
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.go_down_data00.setIcon(icon7)

        self.horizontalLayout_9.addWidget(self.go_down_data00)

        self.go_up_data00 = QToolButton(self.frame_3)
        self.go_up_data00.setObjectName(u"go_up_data00")
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.go_up_data00.setIcon(icon8)

        self.horizontalLayout_9.addWidget(self.go_up_data00)

        self.go_left_data00 = QToolButton(self.frame_3)
        self.go_left_data00.setObjectName(u"go_left_data00")

        self.horizontalLayout_9.addWidget(self.go_left_data00)

        self.go_right_data00 = QToolButton(self.frame_3)
        self.go_right_data00.setObjectName(u"go_right_data00")

        self.horizontalLayout_9.addWidget(self.go_right_data00)


        self.gridLayout_52.addLayout(self.horizontalLayout_9, 2, 8, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.zoom_in_data00 = QToolButton(self.frame_3)
        self.zoom_in_data00.setObjectName(u"zoom_in_data00")

        self.horizontalLayout_2.addWidget(self.zoom_in_data00)

        self.zoom_out_data00 = QToolButton(self.frame_3)
        self.zoom_out_data00.setObjectName(u"zoom_out_data00")

        self.horizontalLayout_2.addWidget(self.zoom_out_data00)


        self.gridLayout_52.addLayout(self.horizontalLayout_2, 2, 7, 1, 1)

        self.fit_to_zoom_data00.raise_()
        self.Scroll_data0.raise_()
        self.vtkWidget_data00.raise_()

        self.gridLayout_53.addWidget(self.frame_3, 0, 0, 1, 2)


        self.gridLayout_data0.addWidget(self.groupBox_time00, 0, 0, 1, 1)

        self.groupBox_time01 = QGroupBox(self.page_4Ddata0)
        self.groupBox_time01.setObjectName(u"groupBox_time01")
        sizePolicy3.setHeightForWidth(self.groupBox_time01.sizePolicy().hasHeightForWidth())
        self.groupBox_time01.setSizePolicy(sizePolicy3)
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

        self.horizontalLayout_14.addWidget(self.zoom_in_data01)

        self.zoom_out_data01 = QToolButton(self.frame_17)
        self.zoom_out_data01.setObjectName(u"zoom_out_data01")

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
        self.go_down_data01.setIcon(icon7)

        self.horizontalLayout_15.addWidget(self.go_down_data01)

        self.go_up_data01 = QToolButton(self.frame_17)
        self.go_up_data01.setObjectName(u"go_up_data01")
        self.go_up_data01.setIcon(icon8)

        self.horizontalLayout_15.addWidget(self.go_up_data01)

        self.go_left_data01 = QToolButton(self.frame_17)
        self.go_left_data01.setObjectName(u"go_left_data01")

        self.horizontalLayout_15.addWidget(self.go_left_data01)

        self.go_right_data01 = QToolButton(self.frame_17)
        self.go_right_data01.setObjectName(u"go_right_data01")

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
        self.spinBox_y_data0 = QSpinBox(self.groupBox_34)
        self.spinBox_y_data0.setObjectName(u"spinBox_y_data0")
        self.spinBox_y_data0.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data0.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data0.setMinimum(1)
        self.spinBox_y_data0.setMaximum(120)

        self.gridLayout_71.addWidget(self.spinBox_y_data0, 0, 2, 1, 1)

        self.spinBox_x_data0 = QSpinBox(self.groupBox_34)
        self.spinBox_x_data0.setObjectName(u"spinBox_x_data0")
        self.spinBox_x_data0.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_data0.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_x_data0.setMinimum(1)
        self.spinBox_x_data0.setMaximum(120)

        self.gridLayout_71.addWidget(self.spinBox_x_data0, 0, 1, 1, 1)

        self.spinBox_z_data0 = QSpinBox(self.groupBox_34)
        self.spinBox_z_data0.setObjectName(u"spinBox_z_data0")
        self.spinBox_z_data0.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data0.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data0.setMinimum(1)
        self.spinBox_z_data0.setMaximum(60)

        self.gridLayout_71.addWidget(self.spinBox_z_data0, 0, 3, 1, 1)


        self.gridLayout_data0.addWidget(self.groupBox_34, 2, 0, 1, 1)

        self.groupBox_time02 = QGroupBox(self.page_4Ddata0)
        self.groupBox_time02.setObjectName(u"groupBox_time02")
        sizePolicy3.setHeightForWidth(self.groupBox_time02.sizePolicy().hasHeightForWidth())
        self.groupBox_time02.setSizePolicy(sizePolicy3)
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
        self.go_down_data02.setIcon(icon7)

        self.horizontalLayout_13.addWidget(self.go_down_data02)

        self.go_up_data02 = QToolButton(self.frame_23)
        self.go_up_data02.setObjectName(u"go_up_data02")
        self.go_up_data02.setIcon(icon8)

        self.horizontalLayout_13.addWidget(self.go_up_data02)

        self.go_left_data02 = QToolButton(self.frame_23)
        self.go_left_data02.setObjectName(u"go_left_data02")

        self.horizontalLayout_13.addWidget(self.go_left_data02)

        self.go_right_data02 = QToolButton(self.frame_23)
        self.go_right_data02.setObjectName(u"go_right_data02")

        self.horizontalLayout_13.addWidget(self.go_right_data02)


        self.gridLayout_50.addLayout(self.horizontalLayout_13, 2, 7, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.zoom_in_data02 = QToolButton(self.frame_23)
        self.zoom_in_data02.setObjectName(u"zoom_in_data02")
        self.zoom_in_data02.setIconSize(QSize(14, 16))

        self.horizontalLayout_10.addWidget(self.zoom_in_data02)

        self.zoom_out_data02 = QToolButton(self.frame_23)
        self.zoom_out_data02.setObjectName(u"zoom_out_data02")

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
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableintensity_data0.setHorizontalHeaderItem(3, __qtablewidgetitem17)
        self.tableintensity_data0.setObjectName(u"tableintensity_data0")
        sizePolicy2.setHeightForWidth(self.tableintensity_data0.sizePolicy().hasHeightForWidth())
        self.tableintensity_data0.setSizePolicy(sizePolicy2)
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
        self.groupBox_40 = QGroupBox(self.page_3D)
        self.groupBox_40.setObjectName(u"groupBox_40")
        self.groupBox_40.setMinimumSize(QSize(100, 100))
        self.groupBox_40.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_156 = QGridLayout(self.groupBox_40)
        self.gridLayout_156.setObjectName(u"gridLayout_156")
        self.gridLayout_156.setContentsMargins(-1, -1, 9, 9)
        self.tableintensity_data3d = QTableWidget(self.groupBox_40)
        if (self.tableintensity_data3d.columnCount() < 4):
            self.tableintensity_data3d.setColumnCount(4)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableintensity_data3d.setHorizontalHeaderItem(3, __qtablewidgetitem21)
        self.tableintensity_data3d.setObjectName(u"tableintensity_data3d")
        sizePolicy2.setHeightForWidth(self.tableintensity_data3d.sizePolicy().hasHeightForWidth())
        self.tableintensity_data3d.setSizePolicy(sizePolicy2)
        self.tableintensity_data3d.setMaximumSize(QSize(700, 1677))
        self.tableintensity_data3d.setContextMenuPolicy(Qt.NoContextMenu)
        self.tableintensity_data3d.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableintensity_data3d.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableintensity_data3d.horizontalHeader().setDefaultSectionSize(67)

        self.gridLayout_156.addWidget(self.tableintensity_data3d, 1, 0, 1, 1)


        self.gridLayout_106.addWidget(self.groupBox_40, 5, 2, 1, 1)

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
        self.groupBox_22 = QGroupBox(self.page_5)
        self.groupBox_22.setObjectName(u"groupBox_22")
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

        self.pushButton_redAreas = QPushButton(self.page_5)
        self.pushButton_redAreas.setObjectName(u"pushButton_redAreas")
        self.pushButton_redAreas.setEnabled(False)

        self.gridLayout_75.addWidget(self.pushButton_redAreas, 11, 0, 1, 2)

        self.textEdit_2 = QTextEdit(self.page_5)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setMaximumSize(QSize(16777215, 50))
        self.textEdit_2.setReadOnly(True)

        self.gridLayout_75.addWidget(self.textEdit_2, 0, 0, 1, 2)

        self.groupBox_12 = QGroupBox(self.page_5)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.gridLayout_136 = QGridLayout(self.groupBox_12)
        self.gridLayout_136.setObjectName(u"gridLayout_136")
        self.doubleSpinBox_d_bregmaz = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_d_bregmaz.setObjectName(u"doubleSpinBox_d_bregmaz")
        self.doubleSpinBox_d_bregmaz.setReadOnly(True)
        self.doubleSpinBox_d_bregmaz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_bregmaz.setMaximum(1500.000000000000000)

        self.gridLayout_136.addWidget(self.doubleSpinBox_d_bregmaz, 7, 3, 1, 1)

        self.pushButton_tp_bregma = QPushButton(self.groupBox_12)
        self.pushButton_tp_bregma.setObjectName(u"pushButton_tp_bregma")
        self.pushButton_tp_bregma.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_136.addWidget(self.pushButton_tp_bregma, 0, 1, 1, 3)

        self.spinBox_tp_bregma_y = QSpinBox(self.groupBox_12)
        self.spinBox_tp_bregma_y.setObjectName(u"spinBox_tp_bregma_y")

        self.gridLayout_136.addWidget(self.spinBox_tp_bregma_y, 2, 2, 1, 1)

        self.lineEdit_24 = QLineEdit(self.groupBox_12)
        self.lineEdit_24.setObjectName(u"lineEdit_24")
        self.lineEdit_24.setReadOnly(True)

        self.gridLayout_136.addWidget(self.lineEdit_24, 1, 1, 1, 3)

        self.lineEdit_19 = QLineEdit(self.groupBox_12)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        self.lineEdit_19.setReadOnly(True)

        self.gridLayout_136.addWidget(self.lineEdit_19, 5, 1, 1, 3)

        self.spinBox_tp_bregma_z = QSpinBox(self.groupBox_12)
        self.spinBox_tp_bregma_z.setObjectName(u"spinBox_tp_bregma_z")

        self.gridLayout_136.addWidget(self.spinBox_tp_bregma_z, 2, 3, 1, 1)

        self.lineEdit_29 = QLineEdit(self.groupBox_12)
        self.lineEdit_29.setObjectName(u"lineEdit_29")
        self.lineEdit_29.setReadOnly(True)

        self.gridLayout_136.addWidget(self.lineEdit_29, 3, 1, 1, 3)

        self.doubleSpinBox_d_bregmax = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_d_bregmax.setObjectName(u"doubleSpinBox_d_bregmax")
        self.doubleSpinBox_d_bregmax.setReadOnly(True)
        self.doubleSpinBox_d_bregmax.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_bregmax.setMaximum(1500.000000000000000)

        self.gridLayout_136.addWidget(self.doubleSpinBox_d_bregmax, 7, 1, 1, 1)

        self.doubleSpinBox_d_bregmay = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBox_d_bregmay.setObjectName(u"doubleSpinBox_d_bregmay")
        self.doubleSpinBox_d_bregmay.setReadOnly(True)
        self.doubleSpinBox_d_bregmay.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_bregmay.setMaximum(1500.000000000000000)

        self.gridLayout_136.addWidget(self.doubleSpinBox_d_bregmay, 7, 2, 1, 1)

        self.spinBox_atlas_bregma_z = QSpinBox(self.groupBox_12)
        self.spinBox_atlas_bregma_z.setObjectName(u"spinBox_atlas_bregma_z")
        self.spinBox_atlas_bregma_z.setReadOnly(True)
        self.spinBox_atlas_bregma_z.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_bregma_z.setMaximum(1000)

        self.gridLayout_136.addWidget(self.spinBox_atlas_bregma_z, 4, 3, 1, 1)

        self.spinBox_tp_bregma_x = QSpinBox(self.groupBox_12)
        self.spinBox_tp_bregma_x.setObjectName(u"spinBox_tp_bregma_x")

        self.gridLayout_136.addWidget(self.spinBox_tp_bregma_x, 2, 1, 1, 1)

        self.spinBox_atlas_bregma_y = QSpinBox(self.groupBox_12)
        self.spinBox_atlas_bregma_y.setObjectName(u"spinBox_atlas_bregma_y")
        self.spinBox_atlas_bregma_y.setReadOnly(True)
        self.spinBox_atlas_bregma_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_bregma_y.setMaximum(1000)

        self.gridLayout_136.addWidget(self.spinBox_atlas_bregma_y, 4, 2, 1, 1)

        self.spinBox_atlas_bregma_x = QSpinBox(self.groupBox_12)
        self.spinBox_atlas_bregma_x.setObjectName(u"spinBox_atlas_bregma_x")
        self.spinBox_atlas_bregma_x.setReadOnly(True)
        self.spinBox_atlas_bregma_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_bregma_x.setMaximum(1000)

        self.gridLayout_136.addWidget(self.spinBox_atlas_bregma_x, 4, 1, 1, 1)


        self.gridLayout_75.addWidget(self.groupBox_12, 1, 0, 1, 2)

        self.pushButton_tp_next0 = QPushButton(self.page_5)
        self.pushButton_tp_next0.setObjectName(u"pushButton_tp_next0")
        self.pushButton_tp_next0.setEnabled(False)

        self.gridLayout_75.addWidget(self.pushButton_tp_next0, 12, 0, 1, 2)

        self.groupBox_21 = QGroupBox(self.page_5)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.gridLayout_176 = QGridLayout(self.groupBox_21)
        self.gridLayout_176.setObjectName(u"gridLayout_176")
        self.lineEdit_20 = QLineEdit(self.groupBox_21)
        self.lineEdit_20.setObjectName(u"lineEdit_20")
        self.lineEdit_20.setReadOnly(True)

        self.gridLayout_176.addWidget(self.lineEdit_20, 3, 1, 1, 3)

        self.pushButton_tp_lambda = QPushButton(self.groupBox_21)
        self.pushButton_tp_lambda.setObjectName(u"pushButton_tp_lambda")
        self.pushButton_tp_lambda.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_176.addWidget(self.pushButton_tp_lambda, 0, 1, 1, 3)

        self.spinBox_tp_lambda_y = QSpinBox(self.groupBox_21)
        self.spinBox_tp_lambda_y.setObjectName(u"spinBox_tp_lambda_y")

        self.gridLayout_176.addWidget(self.spinBox_tp_lambda_y, 2, 2, 1, 1)

        self.lineEdit_58 = QLineEdit(self.groupBox_21)
        self.lineEdit_58.setObjectName(u"lineEdit_58")
        self.lineEdit_58.setReadOnly(True)

        self.gridLayout_176.addWidget(self.lineEdit_58, 1, 1, 1, 3)

        self.spinBox_atlas_lambda_y = QSpinBox(self.groupBox_21)
        self.spinBox_atlas_lambda_y.setObjectName(u"spinBox_atlas_lambda_y")
        self.spinBox_atlas_lambda_y.setReadOnly(True)
        self.spinBox_atlas_lambda_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_lambda_y.setMaximum(1000)

        self.gridLayout_176.addWidget(self.spinBox_atlas_lambda_y, 4, 2, 1, 1)

        self.spinBox_tp_lambda_z = QSpinBox(self.groupBox_21)
        self.spinBox_tp_lambda_z.setObjectName(u"spinBox_tp_lambda_z")

        self.gridLayout_176.addWidget(self.spinBox_tp_lambda_z, 2, 3, 1, 1)

        self.doubleSpinBox_d_lambdaz = QDoubleSpinBox(self.groupBox_21)
        self.doubleSpinBox_d_lambdaz.setObjectName(u"doubleSpinBox_d_lambdaz")
        self.doubleSpinBox_d_lambdaz.setReadOnly(True)
        self.doubleSpinBox_d_lambdaz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_lambdaz.setMaximum(1500.000000000000000)

        self.gridLayout_176.addWidget(self.doubleSpinBox_d_lambdaz, 6, 3, 1, 1)

        self.spinBox_tp_lambda_x = QSpinBox(self.groupBox_21)
        self.spinBox_tp_lambda_x.setObjectName(u"spinBox_tp_lambda_x")

        self.gridLayout_176.addWidget(self.spinBox_tp_lambda_x, 2, 1, 1, 1)

        self.doubleSpinBox_d_lambdax = QDoubleSpinBox(self.groupBox_21)
        self.doubleSpinBox_d_lambdax.setObjectName(u"doubleSpinBox_d_lambdax")
        self.doubleSpinBox_d_lambdax.setReadOnly(True)
        self.doubleSpinBox_d_lambdax.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_lambdax.setMaximum(1500.000000000000000)

        self.gridLayout_176.addWidget(self.doubleSpinBox_d_lambdax, 6, 1, 1, 1)

        self.lineEdit_30 = QLineEdit(self.groupBox_21)
        self.lineEdit_30.setObjectName(u"lineEdit_30")
        self.lineEdit_30.setReadOnly(True)

        self.gridLayout_176.addWidget(self.lineEdit_30, 5, 1, 1, 3)

        self.doubleSpinBox_d_lambday = QDoubleSpinBox(self.groupBox_21)
        self.doubleSpinBox_d_lambday.setObjectName(u"doubleSpinBox_d_lambday")
        self.doubleSpinBox_d_lambday.setReadOnly(True)
        self.doubleSpinBox_d_lambday.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_d_lambday.setMaximum(1500.000000000000000)

        self.gridLayout_176.addWidget(self.doubleSpinBox_d_lambday, 6, 2, 1, 1)

        self.spinBox_atlas_lambda_z = QSpinBox(self.groupBox_21)
        self.spinBox_atlas_lambda_z.setObjectName(u"spinBox_atlas_lambda_z")
        self.spinBox_atlas_lambda_z.setReadOnly(True)
        self.spinBox_atlas_lambda_z.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_lambda_z.setMaximum(1000)

        self.gridLayout_176.addWidget(self.spinBox_atlas_lambda_z, 4, 3, 1, 1)

        self.spinBox_atlas_lambda_x = QSpinBox(self.groupBox_21)
        self.spinBox_atlas_lambda_x.setObjectName(u"spinBox_atlas_lambda_x")
        self.spinBox_atlas_lambda_x.setReadOnly(True)
        self.spinBox_atlas_lambda_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_atlas_lambda_x.setMaximum(1000)

        self.gridLayout_176.addWidget(self.spinBox_atlas_lambda_x, 4, 1, 1, 1)


        self.gridLayout_75.addWidget(self.groupBox_21, 3, 0, 1, 2)

        self.stackedWidget_trajectoryplanning.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.gridLayout_187 = QGridLayout(self.page_6)
        self.gridLayout_187.setObjectName(u"gridLayout_187")
        self.comboBox_Shanks = QComboBox(self.page_6)
        self.comboBox_Shanks.setObjectName(u"comboBox_Shanks")

        self.gridLayout_187.addWidget(self.comboBox_Shanks, 0, 1, 2, 1)

        self.pushButton_PyLdetection = QPushButton(self.page_6)
        self.pushButton_PyLdetection.setObjectName(u"pushButton_PyLdetection")
        self.pushButton_PyLdetection.setEnabled(False)

        self.gridLayout_187.addWidget(self.pushButton_PyLdetection, 10, 0, 1, 2)

        self.pushButton_edgemask = QPushButton(self.page_6)
        self.pushButton_edgemask.setObjectName(u"pushButton_edgemask")
        self.pushButton_edgemask.setCheckable(True)

        self.gridLayout_187.addWidget(self.pushButton_edgemask, 3, 0, 1, 1)

        self.pushButton_addShank = QPushButton(self.page_6)
        self.pushButton_addShank.setObjectName(u"pushButton_addShank")

        self.gridLayout_187.addWidget(self.pushButton_addShank, 0, 0, 1, 1)

        self.pushButton_SaveTraj = QPushButton(self.page_6)
        self.pushButton_SaveTraj.setObjectName(u"pushButton_SaveTraj")

        self.gridLayout_187.addWidget(self.pushButton_SaveTraj, 11, 0, 1, 2)

        self.doubleSpinBox_distance_shank = QDoubleSpinBox(self.page_6)
        self.doubleSpinBox_distance_shank.setObjectName(u"doubleSpinBox_distance_shank")
        self.doubleSpinBox_distance_shank.setEnabled(False)
        self.doubleSpinBox_distance_shank.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_distance_shank.setMaximum(99.000000000000000)

        self.gridLayout_187.addWidget(self.doubleSpinBox_distance_shank, 6, 1, 1, 1)

        self.groupBox_75 = QGroupBox(self.page_6)
        self.groupBox_75.setObjectName(u"groupBox_75")
        self.gridLayout_189 = QGridLayout(self.groupBox_75)
        self.gridLayout_189.setObjectName(u"gridLayout_189")
        self.spinBox_tp_deep_x = QSpinBox(self.groupBox_75)
        self.spinBox_tp_deep_x.setObjectName(u"spinBox_tp_deep_x")
        self.spinBox_tp_deep_x.setMaximum(1000)

        self.gridLayout_189.addWidget(self.spinBox_tp_deep_x, 0, 0, 1, 1)

        self.spinBox_tp_deep_y = QSpinBox(self.groupBox_75)
        self.spinBox_tp_deep_y.setObjectName(u"spinBox_tp_deep_y")
        self.spinBox_tp_deep_y.setMaximum(1000)

        self.gridLayout_189.addWidget(self.spinBox_tp_deep_y, 0, 1, 1, 1)

        self.spinBox_tp_deep_z = QSpinBox(self.groupBox_75)
        self.spinBox_tp_deep_z.setObjectName(u"spinBox_tp_deep_z")
        self.spinBox_tp_deep_z.setMaximum(1000)

        self.gridLayout_189.addWidget(self.spinBox_tp_deep_z, 0, 2, 1, 1)


        self.gridLayout_187.addWidget(self.groupBox_75, 5, 1, 1, 1)

        self.groupBox_74 = QGroupBox(self.page_6)
        self.groupBox_74.setObjectName(u"groupBox_74")
        self.gridLayout_188 = QGridLayout(self.groupBox_74)
        self.gridLayout_188.setObjectName(u"gridLayout_188")
        self.spinBox_tp_insert_x = QSpinBox(self.groupBox_74)
        self.spinBox_tp_insert_x.setObjectName(u"spinBox_tp_insert_x")
        self.spinBox_tp_insert_x.setReadOnly(True)
        self.spinBox_tp_insert_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_tp_insert_x.setMaximum(1000)

        self.gridLayout_188.addWidget(self.spinBox_tp_insert_x, 0, 0, 1, 1)

        self.spinBox_tp_insert_y = QSpinBox(self.groupBox_74)
        self.spinBox_tp_insert_y.setObjectName(u"spinBox_tp_insert_y")
        self.spinBox_tp_insert_y.setReadOnly(True)
        self.spinBox_tp_insert_y.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_tp_insert_y.setMaximum(1000)

        self.gridLayout_188.addWidget(self.spinBox_tp_insert_y, 0, 1, 1, 1)

        self.spinBox_tp_insert_z = QSpinBox(self.groupBox_74)
        self.spinBox_tp_insert_z.setObjectName(u"spinBox_tp_insert_z")
        self.spinBox_tp_insert_z.setReadOnly(True)
        self.spinBox_tp_insert_z.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_tp_insert_z.setMaximum(1000)

        self.gridLayout_188.addWidget(self.spinBox_tp_insert_z, 0, 2, 1, 1)


        self.gridLayout_187.addWidget(self.groupBox_74, 4, 1, 1, 1)

        self.pushButton_tp_deep = QPushButton(self.page_6)
        self.pushButton_tp_deep.setObjectName(u"pushButton_tp_deep")
        self.pushButton_tp_deep.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_187.addWidget(self.pushButton_tp_deep, 5, 0, 1, 1)

        self.checkBox_brain_region = QCheckBox(self.page_6)
        self.checkBox_brain_region.setObjectName(u"checkBox_brain_region")
        self.checkBox_brain_region.setChecked(True)

        self.gridLayout_187.addWidget(self.checkBox_brain_region, 3, 1, 1, 1)

        self.textEdit = QTextEdit(self.page_6)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 100))
        self.textEdit.setReadOnly(True)

        self.gridLayout_187.addWidget(self.textEdit, 2, 0, 1, 2)

        self.textEdit_distance_shank = QTextEdit(self.page_6)
        self.textEdit_distance_shank.setObjectName(u"textEdit_distance_shank")
        self.textEdit_distance_shank.setEnabled(False)
        self.textEdit_distance_shank.setMaximumSize(QSize(200, 50))
        self.textEdit_distance_shank.setReadOnly(True)

        self.gridLayout_187.addWidget(self.textEdit_distance_shank, 6, 0, 1, 1)

        self.pushButton_tp_insert = QPushButton(self.page_6)
        self.pushButton_tp_insert.setObjectName(u"pushButton_tp_insert")
        self.pushButton_tp_insert.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_187.addWidget(self.pushButton_tp_insert, 4, 0, 1, 1)

        self.frame = QFrame(self.page_6)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_177 = QGridLayout(self.frame)
        self.gridLayout_177.setObjectName(u"gridLayout_177")
        self.pushButton_coronalView = QPushButton(self.frame)
        self.pushButton_coronalView.setObjectName(u"pushButton_coronalView")
        self.pushButton_coronalView.setEnabled(False)
        self.pushButton_coronalView.setCheckable(True)
        self.pushButton_coronalView.setChecked(True)

        self.gridLayout_177.addWidget(self.pushButton_coronalView, 0, 2, 1, 1)

        self.pushButton_axialView = QPushButton(self.frame)
        self.pushButton_axialView.setObjectName(u"pushButton_axialView")
        self.pushButton_axialView.setEnabled(False)
        self.pushButton_axialView.setCheckable(True)
        self.pushButton_axialView.setChecked(True)

        self.gridLayout_177.addWidget(self.pushButton_axialView, 0, 0, 1, 1)

        self.pushButton_sagittalView = QPushButton(self.frame)
        self.pushButton_sagittalView.setObjectName(u"pushButton_sagittalView")
        self.pushButton_sagittalView.setEnabled(False)
        self.pushButton_sagittalView.setCheckable(True)
        self.pushButton_sagittalView.setChecked(True)

        self.gridLayout_177.addWidget(self.pushButton_sagittalView, 0, 1, 1, 1)


        self.gridLayout_187.addWidget(self.frame, 9, 0, 1, 2)

        self.groupBox_shank = QGroupBox(self.page_6)
        self.groupBox_shank.setObjectName(u"groupBox_shank")
        self.groupBox_shank.setEnabled(False)
        self.gridLayout_179 = QGridLayout(self.groupBox_shank)
        self.gridLayout_179.setObjectName(u"gridLayout_179")
        self.lineEdit_21 = QLineEdit(self.groupBox_shank)
        self.lineEdit_21.setObjectName(u"lineEdit_21")
        self.lineEdit_21.setReadOnly(True)

        self.gridLayout_179.addWidget(self.lineEdit_21, 0, 0, 1, 1)

        self.lineEdit_22 = QLineEdit(self.groupBox_shank)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        self.lineEdit_22.setReadOnly(True)

        self.gridLayout_179.addWidget(self.lineEdit_22, 1, 0, 1, 1)

        self.spinBox_tp_channels = QSpinBox(self.groupBox_shank)
        self.spinBox_tp_channels.setObjectName(u"spinBox_tp_channels")
        self.spinBox_tp_channels.setMaximum(1024)
        self.spinBox_tp_channels.setValue(64)

        self.gridLayout_179.addWidget(self.spinBox_tp_channels, 0, 1, 1, 1)

        self.spinBox_tp_separation = QSpinBox(self.groupBox_shank)
        self.spinBox_tp_separation.setObjectName(u"spinBox_tp_separation")
        self.spinBox_tp_separation.setMaximum(1000)
        self.spinBox_tp_separation.setValue(50)

        self.gridLayout_179.addWidget(self.spinBox_tp_separation, 1, 1, 1, 1)

        self.tableWidget_shank_info = QTableWidget(self.groupBox_shank)
        if (self.tableWidget_shank_info.columnCount() < 2):
            self.tableWidget_shank_info.setColumnCount(2)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_shank_info.setHorizontalHeaderItem(0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_shank_info.setHorizontalHeaderItem(1, __qtablewidgetitem23)
        self.tableWidget_shank_info.setObjectName(u"tableWidget_shank_info")

        self.gridLayout_179.addWidget(self.tableWidget_shank_info, 2, 0, 1, 2)


        self.gridLayout_187.addWidget(self.groupBox_shank, 7, 0, 1, 2)

        self.pushButton_removeShank = QPushButton(self.page_6)
        self.pushButton_removeShank.setObjectName(u"pushButton_removeShank")

        self.gridLayout_187.addWidget(self.pushButton_removeShank, 1, 0, 1, 1)

        self.stackedWidget_trajectoryplanning.addWidget(self.page_6)

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

        self.gridLayout_106.addWidget(self.stackedWidget_3d, 1, 3, 5, 1)

        self.groupBox_68 = QGroupBox(self.page_3D)
        self.groupBox_68.setObjectName(u"groupBox_68")
        self.groupBox_68.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_157 = QGridLayout(self.groupBox_68)
        self.gridLayout_157.setObjectName(u"gridLayout_157")
        self.spinBox_y_data3d = QSpinBox(self.groupBox_68)
        self.spinBox_y_data3d.setObjectName(u"spinBox_y_data3d")
        self.spinBox_y_data3d.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_data3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_y_data3d.setMinimum(1)
        self.spinBox_y_data3d.setMaximum(120)

        self.gridLayout_157.addWidget(self.spinBox_y_data3d, 0, 2, 1, 1)

        self.spinBox_x_data3d = QSpinBox(self.groupBox_68)
        self.spinBox_x_data3d.setObjectName(u"spinBox_x_data3d")
        self.spinBox_x_data3d.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_data3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_x_data3d.setMinimum(1)
        self.spinBox_x_data3d.setMaximum(120)

        self.gridLayout_157.addWidget(self.spinBox_x_data3d, 0, 1, 1, 1)

        self.spinBox_z_data3d = QSpinBox(self.groupBox_68)
        self.spinBox_z_data3d.setObjectName(u"spinBox_z_data3d")
        self.spinBox_z_data3d.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_data3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_z_data3d.setMinimum(1)
        self.spinBox_z_data3d.setMaximum(60)

        self.gridLayout_157.addWidget(self.spinBox_z_data3d, 0, 3, 1, 1)


        self.gridLayout_106.addWidget(self.groupBox_68, 5, 0, 1, 1)

        self.groupBox_contrast = QGroupBox(self.page_3D)
        self.groupBox_contrast.setObjectName(u"groupBox_contrast")
        self.groupBox_contrast.setMinimumSize(QSize(0, 0))
        self.groupBox_contrast.setMaximumSize(QSize(16777215, 200))
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
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_35.setFont(font5)

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
        self.label_36.setFont(font5)

        self.gridLayout_162.addWidget(self.label_36, 2, 0, 1, 1)

        self.comboBox_Contrastimage = QComboBox(self.groupBox_contrast)
        self.comboBox_Contrastimage.setObjectName(u"comboBox_Contrastimage")

        self.gridLayout_162.addWidget(self.comboBox_Contrastimage, 0, 0, 1, 5)

        self.gridLayout_162.setColumnStretch(0, 1)
        self.gridLayout_162.setColumnStretch(3, 1)

        self.gridLayout_106.addWidget(self.groupBox_contrast, 5, 1, 1, 1)

        self.stackedWidget_sagittal = QStackedWidget(self.page_3D)
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
        self.vtkWidget_data_sagittal = QVTKRenderWindowInteractor(self.frame_9)
        self.vtkWidget_data_sagittal.setObjectName(u"vtkWidget_data_sagittal")
        self.vtkWidget_data_sagittal.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_144.addWidget(self.vtkWidget_data_sagittal, 1, 0, 1, 9)

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

        self.Scroll_data3d1 = QScrollBar(self.frame_9)
        self.Scroll_data3d1.setObjectName(u"Scroll_data3d1")
        self.Scroll_data3d1.setPageStep(10)

        self.gridLayout_144.addWidget(self.Scroll_data3d1, 1, 9, 1, 1)

        self.vtkWidget_data_sagittal.raise_()
        self.Scroll_data3d1.raise_()
        self.fit_to_zoom_data3d1.raise_()

        self.gridLayout_175.addWidget(self.frame_9, 1, 0, 1, 1)

        self.stackedWidget_sagittal.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_174 = QGridLayout(self.page_4)
        self.gridLayout_174.setObjectName(u"gridLayout_174")
        self.gridLayout_174.setContentsMargins(0, 0, 0, 0)
        self.textEdit_11 = QTextEdit(self.page_4)
        self.textEdit_11.setObjectName(u"textEdit_11")
        self.textEdit_11.setMinimumSize(QSize(0, 30))
        self.textEdit_11.setMaximumSize(QSize(16777215, 30))
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

        self.gridLayout_106.addWidget(self.stackedWidget_sagittal, 1, 1, 4, 1)

        self.stackedWidget_coronal = QStackedWidget(self.page_3D)
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
        icon9 = QIcon()
        icon9.addFile(u"../../Downloads/leftArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_left_data3d2.setIcon(icon9)

        self.horizontalLayout_34.addWidget(self.go_left_data3d2)

        self.go_right_data3d2 = QToolButton(self.frame_10)
        self.go_right_data3d2.setObjectName(u"go_right_data3d2")
        icon10 = QIcon()
        icon10.addFile(u"../../Downloads/rightArrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.go_right_data3d2.setIcon(icon10)

        self.horizontalLayout_34.addWidget(self.go_right_data3d2)


        self.gridLayout_145.addLayout(self.horizontalLayout_34, 2, 8, 1, 1)

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

        self.vtkWidget_data_coronal.raise_()
        self.Scroll_data3d2.raise_()
        self.fit_to_zoom_data3d2.raise_()

        self.gridLayout_182.addWidget(self.frame_10, 1, 0, 1, 1)

        self.stackedWidget_coronal.addWidget(self.page_7)
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
        self.textEdit_10.setReadOnly(True)

        self.gridLayout_184.addWidget(self.textEdit_10, 0, 0, 1, 2)

        self.pushButton_resetCoronal = QPushButton(self.page_10)
        self.pushButton_resetCoronal.setObjectName(u"pushButton_resetCoronal")

        self.gridLayout_184.addWidget(self.pushButton_resetCoronal, 2, 0, 1, 2)

        self.stackedWidget_coronal.addWidget(self.page_10)

        self.gridLayout_106.addWidget(self.stackedWidget_coronal, 1, 2, 4, 1)

        self.stackedWidget_axial = QStackedWidget(self.page_3D)
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
        self.go_down_data3d1_2.setIcon(icon7)

        self.horizontalLayout_38.addWidget(self.go_down_data3d1_2)

        self.go_up_data3d1_2 = QToolButton(self.frame_12)
        self.go_up_data3d1_2.setObjectName(u"go_up_data3d1_2")
        self.go_up_data3d1_2.setIcon(icon8)

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
        self.textEdit_13.setReadOnly(True)

        self.gridLayout_195.addWidget(self.textEdit_13, 1, 0, 1, 2)

        self.stackedWidget_sagittal_2.addWidget(self.page_20)

        self.gridLayout_196.addWidget(self.stackedWidget_sagittal_2, 0, 0, 1, 1)

        self.stackedWidget_axial.addWidget(self.page_14)

        self.gridLayout_106.addWidget(self.stackedWidget_axial, 1, 0, 4, 1)

        self.gridLayout_106.setColumnStretch(0, 1)
        self.data_4d_3d.addWidget(self.page_3D)

        self.gridLayout_7.addWidget(self.data_4d_3d, 0, 0, 1, 1)


        self.gridLayout_70.addWidget(self.groupBox_data0, 1, 1, 1, 3)

        self.tabWidget.addTab(self.PostSurgery, "")
        self.tab_15 = QWidget()
        self.tab_15.setObjectName(u"tab_15")
        self.gridLayout_104 = QGridLayout(self.tab_15)
        self.gridLayout_104.setObjectName(u"gridLayout_104")
        self.groupBox_measurement = QGroupBox(self.tab_15)
        self.groupBox_measurement.setObjectName(u"groupBox_measurement")
        self.gridLayout_9 = QGridLayout(self.groupBox_measurement)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.checkBox_measurement = QCheckBox(self.groupBox_measurement)
        self.checkBox_measurement.setObjectName(u"checkBox_measurement")
        self.checkBox_measurement.setEnabled(True)
        font6 = QFont()
        font6.setPointSize(25)
        font6.setBold(False)
        self.checkBox_measurement.setFont(font6)
        icon11 = QIcon()
        icon11.addFile(u":/Icons/nternet/Icons/Internet/measure.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.checkBox_measurement.setIcon(icon11)
        self.checkBox_measurement.setIconSize(QSize(50, 50))
        self.checkBox_measurement.setChecked(True)

        self.gridLayout_9.addWidget(self.checkBox_measurement, 0, 0, 1, 1)

        self.groupBox_ = QGroupBox(self.groupBox_measurement)
        self.groupBox_.setObjectName(u"groupBox_")
        self.gridLayout_19 = QGridLayout(self.groupBox_)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.comboBox_measurementColors = QComboBox(self.groupBox_)
        self.comboBox_measurementColors.addItem("")
        self.comboBox_measurementColors.addItem("")
        self.comboBox_measurementColors.addItem("")
        self.comboBox_measurementColors.addItem("")
        self.comboBox_measurementColors.addItem("")
        self.comboBox_measurementColors.setObjectName(u"comboBox_measurementColors")

        self.gridLayout_19.addWidget(self.comboBox_measurementColors, 1, 0, 1, 1)

        self.pushButton_deleteMeasurement = QPushButton(self.groupBox_)
        self.pushButton_deleteMeasurement.setObjectName(u"pushButton_deleteMeasurement")

        self.gridLayout_19.addWidget(self.pushButton_deleteMeasurement, 1, 1, 1, 1)

        self.tableWidget_meaurement = QTableWidget(self.groupBox_)
        self.tableWidget_meaurement.setObjectName(u"tableWidget_meaurement")
        self.tableWidget_meaurement.setMinimumSize(QSize(280, 0))
        self.tableWidget_meaurement.setMaximumSize(QSize(280, 16777215))
        self.tableWidget_meaurement.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout_19.addWidget(self.tableWidget_meaurement, 0, 0, 1, 2)


        self.gridLayout_9.addWidget(self.groupBox_, 1, 0, 1, 1)


        self.gridLayout_104.addWidget(self.groupBox_measurement, 1, 3, 1, 1)

        self.groupBox_23 = QGroupBox(self.tab_15)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.gridLayout_158 = QGridLayout(self.groupBox_23)
        self.gridLayout_158.setObjectName(u"gridLayout_158")
        self.tabWidget_4 = QTabWidget(self.groupBox_23)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tab_28 = QWidget()
        self.tab_28.setObjectName(u"tab_28")
        self.gridLayout_148 = QGridLayout(self.tab_28)
        self.gridLayout_148.setObjectName(u"gridLayout_148")
        self.display_level_data3d0 = QSpinBox(self.tab_28)
        self.display_level_data3d0.setObjectName(u"display_level_data3d0")
        self.display_level_data3d0.setMaximumSize(QSize(16777215, 100))
        self.display_level_data3d0.setAutoFillBackground(False)
        self.display_level_data3d0.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data3d0.setReadOnly(True)
        self.display_level_data3d0.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_148.addWidget(self.display_level_data3d0, 2, 1, 1, 1)

        self.label_30 = QLabel(self.tab_28)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font5)

        self.gridLayout_148.addWidget(self.label_30, 0, 0, 1, 1)

        self.display_window_data3d0 = QSpinBox(self.tab_28)
        self.display_window_data3d0.setObjectName(u"display_window_data3d0")
        self.display_window_data3d0.setMaximumSize(QSize(70, 100))
        self.display_window_data3d0.setAutoFillBackground(False)
        self.display_window_data3d0.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data3d0.setReadOnly(True)
        self.display_window_data3d0.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_148.addWidget(self.display_window_data3d0, 0, 1, 1, 1)

        self.changeContrast_data3d0 = QSlider(self.tab_28)
        self.changeContrast_data3d0.setObjectName(u"changeContrast_data3d0")
        self.changeContrast_data3d0.setOrientation(Qt.Horizontal)

        self.gridLayout_148.addWidget(self.changeContrast_data3d0, 1, 0, 1, 2)

        self.label_29 = QLabel(self.tab_28)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font5)

        self.gridLayout_148.addWidget(self.label_29, 2, 0, 1, 1)

        self.changeBrightness_data3d0 = QSlider(self.tab_28)
        self.changeBrightness_data3d0.setObjectName(u"changeBrightness_data3d0")
        self.changeBrightness_data3d0.setOrientation(Qt.Horizontal)

        self.gridLayout_148.addWidget(self.changeBrightness_data3d0, 3, 0, 1, 2)

        self.tabWidget_4.addTab(self.tab_28, "")
        self.tab_29 = QWidget()
        self.tab_29.setObjectName(u"tab_29")
        self.gridLayout_151 = QGridLayout(self.tab_29)
        self.gridLayout_151.setObjectName(u"gridLayout_151")
        self.display_level_data3d1 = QSpinBox(self.tab_29)
        self.display_level_data3d1.setObjectName(u"display_level_data3d1")
        self.display_level_data3d1.setMaximumSize(QSize(16777215, 100))
        self.display_level_data3d1.setAutoFillBackground(False)
        self.display_level_data3d1.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data3d1.setReadOnly(True)
        self.display_level_data3d1.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_151.addWidget(self.display_level_data3d1, 2, 1, 1, 1)

        self.changeContrast_data3d1 = QSlider(self.tab_29)
        self.changeContrast_data3d1.setObjectName(u"changeContrast_data3d1")
        self.changeContrast_data3d1.setOrientation(Qt.Horizontal)

        self.gridLayout_151.addWidget(self.changeContrast_data3d1, 1, 0, 1, 2)

        self.label_31 = QLabel(self.tab_29)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font5)

        self.gridLayout_151.addWidget(self.label_31, 0, 0, 1, 1)

        self.display_window_data3d1 = QSpinBox(self.tab_29)
        self.display_window_data3d1.setObjectName(u"display_window_data3d1")
        self.display_window_data3d1.setMaximumSize(QSize(70, 100))
        self.display_window_data3d1.setAutoFillBackground(False)
        self.display_window_data3d1.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data3d1.setReadOnly(True)
        self.display_window_data3d1.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_151.addWidget(self.display_window_data3d1, 0, 1, 1, 1)

        self.label_32 = QLabel(self.tab_29)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font5)

        self.gridLayout_151.addWidget(self.label_32, 2, 0, 1, 1)

        self.changeBrightness_data3d1 = QSlider(self.tab_29)
        self.changeBrightness_data3d1.setObjectName(u"changeBrightness_data3d1")
        self.changeBrightness_data3d1.setOrientation(Qt.Horizontal)

        self.gridLayout_151.addWidget(self.changeBrightness_data3d1, 3, 0, 1, 2)

        self.tabWidget_4.addTab(self.tab_29, "")
        self.tab_30 = QWidget()
        self.tab_30.setObjectName(u"tab_30")
        self.gridLayout_154 = QGridLayout(self.tab_30)
        self.gridLayout_154.setObjectName(u"gridLayout_154")
        self.display_window_data3d2 = QSpinBox(self.tab_30)
        self.display_window_data3d2.setObjectName(u"display_window_data3d2")
        self.display_window_data3d2.setMaximumSize(QSize(70, 100))
        self.display_window_data3d2.setAutoFillBackground(False)
        self.display_window_data3d2.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data3d2.setReadOnly(True)
        self.display_window_data3d2.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_154.addWidget(self.display_window_data3d2, 0, 1, 1, 1)

        self.label_34 = QLabel(self.tab_30)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font5)

        self.gridLayout_154.addWidget(self.label_34, 2, 0, 1, 1)

        self.label_33 = QLabel(self.tab_30)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font5)

        self.gridLayout_154.addWidget(self.label_33, 0, 0, 1, 1)

        self.changeBrightness_data3d2 = QSlider(self.tab_30)
        self.changeBrightness_data3d2.setObjectName(u"changeBrightness_data3d2")
        self.changeBrightness_data3d2.setOrientation(Qt.Horizontal)

        self.gridLayout_154.addWidget(self.changeBrightness_data3d2, 3, 0, 1, 2)

        self.display_level_data3d2 = QSpinBox(self.tab_30)
        self.display_level_data3d2.setObjectName(u"display_level_data3d2")
        self.display_level_data3d2.setMaximumSize(QSize(16777215, 100))
        self.display_level_data3d2.setAutoFillBackground(False)
        self.display_level_data3d2.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data3d2.setReadOnly(True)
        self.display_level_data3d2.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_154.addWidget(self.display_level_data3d2, 2, 1, 1, 1)

        self.changeContrast_data3d2 = QSlider(self.tab_30)
        self.changeContrast_data3d2.setObjectName(u"changeContrast_data3d2")
        self.changeContrast_data3d2.setOrientation(Qt.Horizontal)

        self.gridLayout_154.addWidget(self.changeContrast_data3d2, 1, 0, 1, 2)

        self.tabWidget_4.addTab(self.tab_30, "")

        self.gridLayout_158.addWidget(self.tabWidget_4, 0, 0, 1, 1)


        self.gridLayout_104.addWidget(self.groupBox_23, 0, 0, 1, 1)

        self.ManualContrastAdjustments = QGroupBox(self.tab_15)
        self.ManualContrastAdjustments.setObjectName(u"ManualContrastAdjustments")
        sizePolicy1.setHeightForWidth(self.ManualContrastAdjustments.sizePolicy().hasHeightForWidth())
        self.ManualContrastAdjustments.setSizePolicy(sizePolicy1)
        self.ManualContrastAdjustments.setMinimumSize(QSize(400, 400))
        self.ManualContrastAdjustments.setMaximumSize(QSize(283, 350))
        self.gridLayout_100 = QGridLayout(self.ManualContrastAdjustments)
        self.gridLayout_100.setObjectName(u"gridLayout_100")
        self.contrast_data = QToolBox(self.ManualContrastAdjustments)
        self.contrast_data.setObjectName(u"contrast_data")
        self.contrast_data.setEnabled(True)
        self.contrast_data0 = QWidget()
        self.contrast_data0.setObjectName(u"contrast_data0")
        self.contrast_data0.setGeometry(QRect(0, 0, 376, 259))
        self.gridLayout_115 = QGridLayout(self.contrast_data0)
        self.gridLayout_115.setObjectName(u"gridLayout_115")
        self.tabWidget_3 = QTabWidget(self.contrast_data0)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.gridLayout_101 = QGridLayout(self.tab_10)
        self.gridLayout_101.setObjectName(u"gridLayout_101")
        self.changeBrightness_data00 = QSlider(self.tab_10)
        self.changeBrightness_data00.setObjectName(u"changeBrightness_data00")
        self.changeBrightness_data00.setMaximum(99)
        self.changeBrightness_data00.setSingleStep(1)
        self.changeBrightness_data00.setPageStep(10)
        self.changeBrightness_data00.setValue(0)
        self.changeBrightness_data00.setOrientation(Qt.Horizontal)

        self.gridLayout_101.addWidget(self.changeBrightness_data00, 3, 0, 1, 2)

        self.display_level_data00 = QSpinBox(self.tab_10)
        self.display_level_data00.setObjectName(u"display_level_data00")
        self.display_level_data00.setMaximumSize(QSize(16777215, 100))
        self.display_level_data00.setAutoFillBackground(False)
        self.display_level_data00.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data00.setReadOnly(True)
        self.display_level_data00.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_101.addWidget(self.display_level_data00, 2, 1, 1, 1)

        self.label_11 = QLabel(self.tab_10)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font5)

        self.gridLayout_101.addWidget(self.label_11, 2, 0, 1, 1)

        self.display_window_data00 = QSpinBox(self.tab_10)
        self.display_window_data00.setObjectName(u"display_window_data00")
        self.display_window_data00.setMaximumSize(QSize(70, 100))
        self.display_window_data00.setAutoFillBackground(False)
        self.display_window_data00.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data00.setReadOnly(True)
        self.display_window_data00.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_101.addWidget(self.display_window_data00, 0, 1, 1, 1)

        self.changeContrast_data00 = QSlider(self.tab_10)
        self.changeContrast_data00.setObjectName(u"changeContrast_data00")
        self.changeContrast_data00.setStyleSheet(u"")
        self.changeContrast_data00.setMaximum(99)
        self.changeContrast_data00.setSingleStep(1)
        self.changeContrast_data00.setPageStep(10)
        self.changeContrast_data00.setValue(0)
        self.changeContrast_data00.setOrientation(Qt.Horizontal)

        self.gridLayout_101.addWidget(self.changeContrast_data00, 1, 0, 1, 2)

        self.label_12 = QLabel(self.tab_10)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font5)

        self.gridLayout_101.addWidget(self.label_12, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_10, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_102 = QGridLayout(self.tab_11)
        self.gridLayout_102.setObjectName(u"gridLayout_102")
        self.label_17 = QLabel(self.tab_11)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font5)

        self.gridLayout_102.addWidget(self.label_17, 0, 0, 1, 1)

        self.display_window_data01 = QSpinBox(self.tab_11)
        self.display_window_data01.setObjectName(u"display_window_data01")
        self.display_window_data01.setMaximumSize(QSize(70, 100))
        self.display_window_data01.setAutoFillBackground(False)
        self.display_window_data01.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data01.setReadOnly(True)
        self.display_window_data01.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_102.addWidget(self.display_window_data01, 0, 1, 1, 1)

        self.changeContrast_data01 = QSlider(self.tab_11)
        self.changeContrast_data01.setObjectName(u"changeContrast_data01")
        self.changeContrast_data01.setStyleSheet(u"")
        self.changeContrast_data01.setMaximum(99)
        self.changeContrast_data01.setSingleStep(1)
        self.changeContrast_data01.setPageStep(10)
        self.changeContrast_data01.setValue(0)
        self.changeContrast_data01.setOrientation(Qt.Horizontal)

        self.gridLayout_102.addWidget(self.changeContrast_data01, 1, 0, 1, 2)

        self.label_18 = QLabel(self.tab_11)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font5)

        self.gridLayout_102.addWidget(self.label_18, 2, 0, 1, 1)

        self.display_level_data01 = QSpinBox(self.tab_11)
        self.display_level_data01.setObjectName(u"display_level_data01")
        self.display_level_data01.setMaximumSize(QSize(16777215, 100))
        self.display_level_data01.setAutoFillBackground(False)
        self.display_level_data01.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data01.setReadOnly(True)
        self.display_level_data01.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_102.addWidget(self.display_level_data01, 2, 1, 1, 1)

        self.changeBrightness_data01 = QSlider(self.tab_11)
        self.changeBrightness_data01.setObjectName(u"changeBrightness_data01")
        self.changeBrightness_data01.setMaximum(99)
        self.changeBrightness_data01.setSingleStep(1)
        self.changeBrightness_data01.setPageStep(10)
        self.changeBrightness_data01.setValue(0)
        self.changeBrightness_data01.setOrientation(Qt.Horizontal)

        self.gridLayout_102.addWidget(self.changeBrightness_data01, 3, 0, 1, 2)

        self.tabWidget_3.addTab(self.tab_11, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_103 = QGridLayout(self.tab_12)
        self.gridLayout_103.setObjectName(u"gridLayout_103")
        self.label_19 = QLabel(self.tab_12)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font5)

        self.gridLayout_103.addWidget(self.label_19, 0, 0, 1, 1)

        self.display_window_data02 = QSpinBox(self.tab_12)
        self.display_window_data02.setObjectName(u"display_window_data02")
        self.display_window_data02.setMaximumSize(QSize(70, 100))
        self.display_window_data02.setAutoFillBackground(False)
        self.display_window_data02.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data02.setReadOnly(True)
        self.display_window_data02.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_103.addWidget(self.display_window_data02, 0, 1, 1, 1)

        self.changeContrast_data02 = QSlider(self.tab_12)
        self.changeContrast_data02.setObjectName(u"changeContrast_data02")
        self.changeContrast_data02.setStyleSheet(u"")
        self.changeContrast_data02.setMaximum(99)
        self.changeContrast_data02.setSingleStep(1)
        self.changeContrast_data02.setPageStep(10)
        self.changeContrast_data02.setValue(0)
        self.changeContrast_data02.setOrientation(Qt.Horizontal)

        self.gridLayout_103.addWidget(self.changeContrast_data02, 1, 0, 1, 2)

        self.label_20 = QLabel(self.tab_12)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font5)

        self.gridLayout_103.addWidget(self.label_20, 2, 0, 1, 1)

        self.display_level_data02 = QSpinBox(self.tab_12)
        self.display_level_data02.setObjectName(u"display_level_data02")
        self.display_level_data02.setMaximumSize(QSize(16777215, 100))
        self.display_level_data02.setAutoFillBackground(False)
        self.display_level_data02.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data02.setReadOnly(True)
        self.display_level_data02.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_103.addWidget(self.display_level_data02, 2, 1, 1, 1)

        self.changeBrightness_data02 = QSlider(self.tab_12)
        self.changeBrightness_data02.setObjectName(u"changeBrightness_data02")
        self.changeBrightness_data02.setMaximum(99)
        self.changeBrightness_data02.setSingleStep(1)
        self.changeBrightness_data02.setPageStep(10)
        self.changeBrightness_data02.setValue(0)
        self.changeBrightness_data02.setOrientation(Qt.Horizontal)

        self.gridLayout_103.addWidget(self.changeBrightness_data02, 3, 0, 1, 2)

        self.tabWidget_3.addTab(self.tab_12, "")

        self.gridLayout_115.addWidget(self.tabWidget_3, 0, 0, 1, 1)

        self.contrast_data.addItem(self.contrast_data0, u"Data 0")
        self.contrast_data1 = QWidget()
        self.contrast_data1.setObjectName(u"contrast_data1")
        self.contrast_data1.setEnabled(True)
        self.contrast_data1.setGeometry(QRect(0, 0, 184, 164))
        self.gridLayout_120 = QGridLayout(self.contrast_data1)
        self.gridLayout_120.setObjectName(u"gridLayout_120")
        self.tabWidget_5 = QTabWidget(self.contrast_data1)
        self.tabWidget_5.setObjectName(u"tabWidget_5")
        self.tabWidget_5.setEnabled(True)
        self.tab_16 = QWidget()
        self.tab_16.setObjectName(u"tab_16")
        self.gridLayout_117 = QGridLayout(self.tab_16)
        self.gridLayout_117.setObjectName(u"gridLayout_117")
        self.changeBrightness_data10 = QSlider(self.tab_16)
        self.changeBrightness_data10.setObjectName(u"changeBrightness_data10")
        self.changeBrightness_data10.setMaximum(99)
        self.changeBrightness_data10.setSingleStep(1)
        self.changeBrightness_data10.setPageStep(10)
        self.changeBrightness_data10.setValue(0)
        self.changeBrightness_data10.setOrientation(Qt.Horizontal)

        self.gridLayout_117.addWidget(self.changeBrightness_data10, 3, 0, 1, 2)

        self.display_level_data10 = QSpinBox(self.tab_16)
        self.display_level_data10.setObjectName(u"display_level_data10")
        self.display_level_data10.setMaximumSize(QSize(16777215, 100))
        self.display_level_data10.setAutoFillBackground(False)
        self.display_level_data10.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data10.setReadOnly(True)
        self.display_level_data10.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_117.addWidget(self.display_level_data10, 2, 1, 1, 1)

        self.label_13 = QLabel(self.tab_16)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font5)

        self.gridLayout_117.addWidget(self.label_13, 2, 0, 1, 1)

        self.display_window_data10 = QSpinBox(self.tab_16)
        self.display_window_data10.setObjectName(u"display_window_data10")
        self.display_window_data10.setMaximumSize(QSize(70, 100))
        self.display_window_data10.setAutoFillBackground(False)
        self.display_window_data10.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data10.setReadOnly(True)
        self.display_window_data10.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_117.addWidget(self.display_window_data10, 0, 1, 1, 1)

        self.changeContrast_data10 = QSlider(self.tab_16)
        self.changeContrast_data10.setObjectName(u"changeContrast_data10")
        self.changeContrast_data10.setStyleSheet(u"")
        self.changeContrast_data10.setMaximum(99)
        self.changeContrast_data10.setSingleStep(1)
        self.changeContrast_data10.setPageStep(10)
        self.changeContrast_data10.setValue(0)
        self.changeContrast_data10.setOrientation(Qt.Horizontal)

        self.gridLayout_117.addWidget(self.changeContrast_data10, 1, 0, 1, 2)

        self.label_14 = QLabel(self.tab_16)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setEnabled(True)
        self.label_14.setFont(font5)

        self.gridLayout_117.addWidget(self.label_14, 0, 0, 1, 1)

        self.tabWidget_5.addTab(self.tab_16, "")
        self.tab_17 = QWidget()
        self.tab_17.setObjectName(u"tab_17")
        self.gridLayout_118 = QGridLayout(self.tab_17)
        self.gridLayout_118.setObjectName(u"gridLayout_118")
        self.label_21 = QLabel(self.tab_17)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font5)

        self.gridLayout_118.addWidget(self.label_21, 0, 0, 1, 1)

        self.display_window_data11 = QSpinBox(self.tab_17)
        self.display_window_data11.setObjectName(u"display_window_data11")
        self.display_window_data11.setMaximumSize(QSize(70, 100))
        self.display_window_data11.setAutoFillBackground(False)
        self.display_window_data11.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data11.setReadOnly(True)
        self.display_window_data11.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_118.addWidget(self.display_window_data11, 0, 1, 1, 1)

        self.changeContrast_data11 = QSlider(self.tab_17)
        self.changeContrast_data11.setObjectName(u"changeContrast_data11")
        self.changeContrast_data11.setStyleSheet(u"")
        self.changeContrast_data11.setMaximum(99)
        self.changeContrast_data11.setSingleStep(1)
        self.changeContrast_data11.setPageStep(10)
        self.changeContrast_data11.setValue(0)
        self.changeContrast_data11.setOrientation(Qt.Horizontal)

        self.gridLayout_118.addWidget(self.changeContrast_data11, 1, 0, 1, 2)

        self.label_22 = QLabel(self.tab_17)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font5)

        self.gridLayout_118.addWidget(self.label_22, 2, 0, 1, 1)

        self.display_level_data11 = QSpinBox(self.tab_17)
        self.display_level_data11.setObjectName(u"display_level_data11")
        self.display_level_data11.setMaximumSize(QSize(16777215, 100))
        self.display_level_data11.setAutoFillBackground(False)
        self.display_level_data11.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data11.setReadOnly(True)
        self.display_level_data11.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_118.addWidget(self.display_level_data11, 2, 1, 1, 1)

        self.changeBrightness_data11 = QSlider(self.tab_17)
        self.changeBrightness_data11.setObjectName(u"changeBrightness_data11")
        self.changeBrightness_data11.setMaximum(99)
        self.changeBrightness_data11.setSingleStep(1)
        self.changeBrightness_data11.setPageStep(10)
        self.changeBrightness_data11.setValue(0)
        self.changeBrightness_data11.setOrientation(Qt.Horizontal)

        self.gridLayout_118.addWidget(self.changeBrightness_data11, 3, 0, 1, 2)

        self.tabWidget_5.addTab(self.tab_17, "")
        self.tab_18 = QWidget()
        self.tab_18.setObjectName(u"tab_18")
        self.gridLayout_119 = QGridLayout(self.tab_18)
        self.gridLayout_119.setObjectName(u"gridLayout_119")
        self.label_23 = QLabel(self.tab_18)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font5)

        self.gridLayout_119.addWidget(self.label_23, 0, 0, 1, 1)

        self.display_window_data12 = QSpinBox(self.tab_18)
        self.display_window_data12.setObjectName(u"display_window_data12")
        self.display_window_data12.setMaximumSize(QSize(70, 100))
        self.display_window_data12.setAutoFillBackground(False)
        self.display_window_data12.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data12.setReadOnly(True)
        self.display_window_data12.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_119.addWidget(self.display_window_data12, 0, 1, 1, 1)

        self.changeContrast_data12 = QSlider(self.tab_18)
        self.changeContrast_data12.setObjectName(u"changeContrast_data12")
        self.changeContrast_data12.setStyleSheet(u"")
        self.changeContrast_data12.setMaximum(99)
        self.changeContrast_data12.setSingleStep(1)
        self.changeContrast_data12.setPageStep(10)
        self.changeContrast_data12.setValue(0)
        self.changeContrast_data12.setOrientation(Qt.Horizontal)

        self.gridLayout_119.addWidget(self.changeContrast_data12, 1, 0, 1, 2)

        self.label_24 = QLabel(self.tab_18)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font5)

        self.gridLayout_119.addWidget(self.label_24, 2, 0, 1, 1)

        self.display_level_data12 = QSpinBox(self.tab_18)
        self.display_level_data12.setObjectName(u"display_level_data12")
        self.display_level_data12.setMaximumSize(QSize(16777215, 100))
        self.display_level_data12.setAutoFillBackground(False)
        self.display_level_data12.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data12.setReadOnly(True)
        self.display_level_data12.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_119.addWidget(self.display_level_data12, 2, 1, 1, 1)

        self.changeBrightness_data12 = QSlider(self.tab_18)
        self.changeBrightness_data12.setObjectName(u"changeBrightness_data12")
        self.changeBrightness_data12.setMaximum(99)
        self.changeBrightness_data12.setSingleStep(1)
        self.changeBrightness_data12.setPageStep(10)
        self.changeBrightness_data12.setValue(0)
        self.changeBrightness_data12.setOrientation(Qt.Horizontal)

        self.gridLayout_119.addWidget(self.changeBrightness_data12, 3, 0, 1, 2)

        self.tabWidget_5.addTab(self.tab_18, "")

        self.gridLayout_120.addWidget(self.tabWidget_5, 0, 0, 1, 1)

        self.contrast_data.addItem(self.contrast_data1, u"Data 1")
        self.contrast_data2 = QWidget()
        self.contrast_data2.setObjectName(u"contrast_data2")
        self.contrast_data2.setEnabled(True)
        self.contrast_data2.setGeometry(QRect(0, 0, 184, 164))
        self.gridLayout_124 = QGridLayout(self.contrast_data2)
        self.gridLayout_124.setObjectName(u"gridLayout_124")
        self.tabWidget_6 = QTabWidget(self.contrast_data2)
        self.tabWidget_6.setObjectName(u"tabWidget_6")
        self.tabWidget_6.setEnabled(True)
        self.tab_19 = QWidget()
        self.tab_19.setObjectName(u"tab_19")
        self.gridLayout_121 = QGridLayout(self.tab_19)
        self.gridLayout_121.setObjectName(u"gridLayout_121")
        self.changeBrightness_data20 = QSlider(self.tab_19)
        self.changeBrightness_data20.setObjectName(u"changeBrightness_data20")
        self.changeBrightness_data20.setMaximum(99)
        self.changeBrightness_data20.setSingleStep(1)
        self.changeBrightness_data20.setPageStep(10)
        self.changeBrightness_data20.setValue(0)
        self.changeBrightness_data20.setOrientation(Qt.Horizontal)

        self.gridLayout_121.addWidget(self.changeBrightness_data20, 3, 0, 1, 2)

        self.display_level_data20 = QSpinBox(self.tab_19)
        self.display_level_data20.setObjectName(u"display_level_data20")
        self.display_level_data20.setMaximumSize(QSize(16777215, 100))
        self.display_level_data20.setAutoFillBackground(False)
        self.display_level_data20.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data20.setReadOnly(True)
        self.display_level_data20.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_121.addWidget(self.display_level_data20, 2, 1, 1, 1)

        self.label_15 = QLabel(self.tab_19)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font5)

        self.gridLayout_121.addWidget(self.label_15, 2, 0, 1, 1)

        self.display_window_data20 = QSpinBox(self.tab_19)
        self.display_window_data20.setObjectName(u"display_window_data20")
        self.display_window_data20.setMaximumSize(QSize(70, 100))
        self.display_window_data20.setAutoFillBackground(False)
        self.display_window_data20.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data20.setReadOnly(True)
        self.display_window_data20.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_121.addWidget(self.display_window_data20, 0, 1, 1, 1)

        self.changeContrast_data20 = QSlider(self.tab_19)
        self.changeContrast_data20.setObjectName(u"changeContrast_data20")
        self.changeContrast_data20.setStyleSheet(u"")
        self.changeContrast_data20.setMaximum(99)
        self.changeContrast_data20.setSingleStep(1)
        self.changeContrast_data20.setPageStep(10)
        self.changeContrast_data20.setValue(0)
        self.changeContrast_data20.setOrientation(Qt.Horizontal)

        self.gridLayout_121.addWidget(self.changeContrast_data20, 1, 0, 1, 2)

        self.label_16 = QLabel(self.tab_19)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font5)

        self.gridLayout_121.addWidget(self.label_16, 0, 0, 1, 1)

        self.tabWidget_6.addTab(self.tab_19, "")
        self.tab_20 = QWidget()
        self.tab_20.setObjectName(u"tab_20")
        self.gridLayout_122 = QGridLayout(self.tab_20)
        self.gridLayout_122.setObjectName(u"gridLayout_122")
        self.label_25 = QLabel(self.tab_20)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font5)

        self.gridLayout_122.addWidget(self.label_25, 0, 0, 1, 1)

        self.display_window_data21 = QSpinBox(self.tab_20)
        self.display_window_data21.setObjectName(u"display_window_data21")
        self.display_window_data21.setMaximumSize(QSize(70, 100))
        self.display_window_data21.setAutoFillBackground(False)
        self.display_window_data21.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data21.setReadOnly(True)
        self.display_window_data21.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_122.addWidget(self.display_window_data21, 0, 1, 1, 1)

        self.changeContrast_data21 = QSlider(self.tab_20)
        self.changeContrast_data21.setObjectName(u"changeContrast_data21")
        self.changeContrast_data21.setStyleSheet(u"")
        self.changeContrast_data21.setMaximum(99)
        self.changeContrast_data21.setSingleStep(1)
        self.changeContrast_data21.setPageStep(10)
        self.changeContrast_data21.setValue(0)
        self.changeContrast_data21.setOrientation(Qt.Horizontal)

        self.gridLayout_122.addWidget(self.changeContrast_data21, 1, 0, 1, 2)

        self.label_26 = QLabel(self.tab_20)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font5)

        self.gridLayout_122.addWidget(self.label_26, 2, 0, 1, 1)

        self.display_level_data21 = QSpinBox(self.tab_20)
        self.display_level_data21.setObjectName(u"display_level_data21")
        self.display_level_data21.setMaximumSize(QSize(16777215, 100))
        self.display_level_data21.setAutoFillBackground(False)
        self.display_level_data21.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data21.setReadOnly(True)
        self.display_level_data21.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_122.addWidget(self.display_level_data21, 2, 1, 1, 1)

        self.changeBrightness_data21 = QSlider(self.tab_20)
        self.changeBrightness_data21.setObjectName(u"changeBrightness_data21")
        self.changeBrightness_data21.setMaximum(99)
        self.changeBrightness_data21.setSingleStep(1)
        self.changeBrightness_data21.setPageStep(10)
        self.changeBrightness_data21.setValue(0)
        self.changeBrightness_data21.setOrientation(Qt.Horizontal)

        self.gridLayout_122.addWidget(self.changeBrightness_data21, 3, 0, 1, 2)

        self.tabWidget_6.addTab(self.tab_20, "")
        self.tab_21 = QWidget()
        self.tab_21.setObjectName(u"tab_21")
        self.gridLayout_123 = QGridLayout(self.tab_21)
        self.gridLayout_123.setObjectName(u"gridLayout_123")
        self.label_27 = QLabel(self.tab_21)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font5)

        self.gridLayout_123.addWidget(self.label_27, 0, 0, 1, 1)

        self.display_window_data22 = QSpinBox(self.tab_21)
        self.display_window_data22.setObjectName(u"display_window_data22")
        self.display_window_data22.setMaximumSize(QSize(70, 100))
        self.display_window_data22.setAutoFillBackground(False)
        self.display_window_data22.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_window_data22.setReadOnly(True)
        self.display_window_data22.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_123.addWidget(self.display_window_data22, 0, 1, 1, 1)

        self.changeContrast_data22 = QSlider(self.tab_21)
        self.changeContrast_data22.setObjectName(u"changeContrast_data22")
        self.changeContrast_data22.setStyleSheet(u"")
        self.changeContrast_data22.setMaximum(99)
        self.changeContrast_data22.setSingleStep(1)
        self.changeContrast_data22.setPageStep(10)
        self.changeContrast_data22.setValue(0)
        self.changeContrast_data22.setOrientation(Qt.Horizontal)

        self.gridLayout_123.addWidget(self.changeContrast_data22, 1, 0, 1, 2)

        self.label_28 = QLabel(self.tab_21)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font5)

        self.gridLayout_123.addWidget(self.label_28, 2, 0, 1, 1)

        self.display_level_data22 = QSpinBox(self.tab_21)
        self.display_level_data22.setObjectName(u"display_level_data22")
        self.display_level_data22.setMaximumSize(QSize(16777215, 100))
        self.display_level_data22.setAutoFillBackground(False)
        self.display_level_data22.setStyleSheet(u"color: rgb(0, 0, 0); background-color: white;")
        self.display_level_data22.setReadOnly(True)
        self.display_level_data22.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_123.addWidget(self.display_level_data22, 2, 1, 1, 1)

        self.changeBrightness_data22 = QSlider(self.tab_21)
        self.changeBrightness_data22.setObjectName(u"changeBrightness_data22")
        self.changeBrightness_data22.setMaximum(99)
        self.changeBrightness_data22.setSingleStep(1)
        self.changeBrightness_data22.setPageStep(10)
        self.changeBrightness_data22.setValue(0)
        self.changeBrightness_data22.setOrientation(Qt.Horizontal)

        self.gridLayout_123.addWidget(self.changeBrightness_data22, 3, 0, 1, 2)

        self.tabWidget_6.addTab(self.tab_21, "")

        self.gridLayout_124.addWidget(self.tabWidget_6, 0, 0, 1, 1)

        self.contrast_data.addItem(self.contrast_data2, u"Data 2")

        self.gridLayout_100.addWidget(self.contrast_data, 0, 0, 1, 1)


        self.gridLayout_104.addWidget(self.ManualContrastAdjustments, 1, 2, 1, 1)

        self.groupBox_register = QGroupBox(self.tab_15)
        self.groupBox_register.setObjectName(u"groupBox_register")
        self.gridLayout_14 = QGridLayout(self.groupBox_register)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.groupBox_26 = QGroupBox(self.groupBox_register)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.gridLayout_3 = QGridLayout(self.groupBox_26)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.comboBox_finest = QComboBox(self.groupBox_26)
        self.comboBox_finest.addItem("")
        self.comboBox_finest.addItem("")
        self.comboBox_finest.addItem("")
        self.comboBox_finest.setObjectName(u"comboBox_finest")
        self.comboBox_finest.setEnabled(True)

        self.gridLayout_3.addWidget(self.comboBox_finest, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_26, 1, 1, 1, 1)

        self.groupBox_27 = QGroupBox(self.groupBox_register)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.groupBox_27.setEnabled(True)
        self.gridLayout_2 = QGridLayout(self.groupBox_27)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.textEdit_6 = QTextEdit(self.groupBox_27)
        self.textEdit_6.setObjectName(u"textEdit_6")
        self.textEdit_6.setMaximumSize(QSize(16777215, 50))

        self.gridLayout_2.addWidget(self.textEdit_6, 0, 1, 1, 1)

        self.comboBox_movingimg = QComboBox(self.groupBox_27)
        self.comboBox_movingimg.setObjectName(u"comboBox_movingimg")
        self.comboBox_movingimg.setEnabled(True)

        self.gridLayout_2.addWidget(self.comboBox_movingimg, 1, 1, 1, 1)

        self.textEdit_pixels = QTextEdit(self.groupBox_27)
        self.textEdit_pixels.setObjectName(u"textEdit_pixels")
        self.textEdit_pixels.setMaximumSize(QSize(16777215, 50))
        self.textEdit_pixels.setStyleSheet(u"color: rgb(170, 0, 0);")

        self.gridLayout_2.addWidget(self.textEdit_pixels, 2, 1, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_27, 0, 0, 1, 2)

        self.pushButton_registration = QPushButton(self.groupBox_register)
        self.pushButton_registration.setObjectName(u"pushButton_registration")
        self.pushButton_registration.setEnabled(False)
        self.pushButton_registration.setAcceptDrops(False)

        self.gridLayout_14.addWidget(self.pushButton_registration, 2, 1, 1, 1)

        self.pushButton_regCancel = QPushButton(self.groupBox_register)
        self.pushButton_regCancel.setObjectName(u"pushButton_regCancel")

        self.gridLayout_14.addWidget(self.pushButton_regCancel, 2, 0, 1, 1)

        self.groupBox_17 = QGroupBox(self.groupBox_register)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.gridLayout_4 = QGridLayout(self.groupBox_17)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.comboBox_coarest = QComboBox(self.groupBox_17)
        self.comboBox_coarest.addItem("")
        self.comboBox_coarest.addItem("")
        self.comboBox_coarest.addItem("")
        self.comboBox_coarest.addItem("")
        self.comboBox_coarest.setObjectName(u"comboBox_coarest")
        self.comboBox_coarest.setEnabled(True)

        self.gridLayout_4.addWidget(self.comboBox_coarest, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_17, 1, 0, 1, 1)


        self.gridLayout_104.addWidget(self.groupBox_register, 1, 0, 1, 1)

        self.groupBox_segmentation = QGroupBox(self.tab_15)
        self.groupBox_segmentation.setObjectName(u"groupBox_segmentation")
        self.gridLayout_5 = QGridLayout(self.groupBox_segmentation)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.stackedWidget_segmentation = QStackedWidget(self.groupBox_segmentation)
        self.stackedWidget_segmentation.setObjectName(u"stackedWidget_segmentation")
        self.stackedWidget_segmentation.setEnabled(True)
        self.stackedWidget_segmentation.setMaximumSize(QSize(215, 16777215))
        self.page_13 = QWidget()
        self.page_13.setObjectName(u"page_13")
        self.gridLayout_152 = QGridLayout(self.page_13)
        self.gridLayout_152.setObjectName(u"gridLayout_152")
        self.textBrowser_5 = QTextBrowser(self.page_13)
        self.textBrowser_5.setObjectName(u"textBrowser_5")
        self.textBrowser_5.setMaximumSize(QSize(16777215, 50))
        self.textBrowser_5.setStyleSheet(u"")
        self.textBrowser_5.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser_5.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gridLayout_152.addWidget(self.textBrowser_5, 0, 0, 1, 2)

        self.checkBox_threshold = QCheckBox(self.page_13)
        self.checkBox_threshold.setObjectName(u"checkBox_threshold")
        self.checkBox_threshold.setEnabled(True)
        self.checkBox_threshold.setChecked(True)

        self.gridLayout_152.addWidget(self.checkBox_threshold, 1, 0, 1, 2)

        self.frame_15 = QFrame(self.page_13)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMaximumSize(QSize(16777215, 300))
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.gridLayout_28 = QGridLayout(self.frame_15)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.groupBox_7 = QGroupBox(self.frame_15)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMaximumSize(QSize(16777215, 100))
        self.gridLayout_29 = QGridLayout(self.groupBox_7)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.radioButton_bounded = QRadioButton(self.groupBox_7)
        self.radioButton_bounded.setObjectName(u"radioButton_bounded")
        self.radioButton_bounded.setChecked(True)

        self.gridLayout_29.addWidget(self.radioButton_bounded, 0, 0, 1, 1)

        self.radioButton_lower = QRadioButton(self.groupBox_7)
        self.radioButton_lower.setObjectName(u"radioButton_lower")

        self.gridLayout_29.addWidget(self.radioButton_lower, 1, 0, 1, 1)

        self.radioButton_upper = QRadioButton(self.groupBox_7)
        self.radioButton_upper.setObjectName(u"radioButton_upper")

        self.gridLayout_29.addWidget(self.radioButton_upper, 2, 0, 1, 1)


        self.gridLayout_28.addWidget(self.groupBox_7, 0, 0, 1, 1)

        self.groupBox_13 = QGroupBox(self.frame_15)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_30 = QGridLayout(self.groupBox_13)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.ScrollBar_lower = QSlider(self.groupBox_13)
        self.ScrollBar_lower.setObjectName(u"ScrollBar_lower")
        self.ScrollBar_lower.setMaximum(105)
        self.ScrollBar_lower.setSingleStep(1)
        self.ScrollBar_lower.setPageStep(10)
        self.ScrollBar_lower.setValue(0)
        self.ScrollBar_lower.setOrientation(Qt.Horizontal)

        self.gridLayout_30.addWidget(self.ScrollBar_lower, 0, 0, 1, 1)

        self.doubleSpinBox_lower = QDoubleSpinBox(self.groupBox_13)
        self.doubleSpinBox_lower.setObjectName(u"doubleSpinBox_lower")
        self.doubleSpinBox_lower.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_lower.setMaximum(105.000000000000000)
        self.doubleSpinBox_lower.setSingleStep(0.100000000000000)

        self.gridLayout_30.addWidget(self.doubleSpinBox_lower, 0, 1, 1, 1)


        self.gridLayout_28.addWidget(self.groupBox_13, 1, 0, 1, 1)

        self.groupBox_63 = QGroupBox(self.frame_15)
        self.groupBox_63.setObjectName(u"groupBox_63")
        self.groupBox_63.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_31 = QGridLayout(self.groupBox_63)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.ScrollBar_upper = QSlider(self.groupBox_63)
        self.ScrollBar_upper.setObjectName(u"ScrollBar_upper")
        self.ScrollBar_upper.setMaximum(105)
        self.ScrollBar_upper.setSingleStep(1)
        self.ScrollBar_upper.setPageStep(10)
        self.ScrollBar_upper.setValue(0)
        self.ScrollBar_upper.setOrientation(Qt.Horizontal)

        self.gridLayout_31.addWidget(self.ScrollBar_upper, 0, 0, 1, 1)

        self.doubleSpinBox_upper = QDoubleSpinBox(self.groupBox_63)
        self.doubleSpinBox_upper.setObjectName(u"doubleSpinBox_upper")
        self.doubleSpinBox_upper.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_upper.setMaximum(105.000000000000000)
        self.doubleSpinBox_upper.setSingleStep(0.100000000000000)

        self.gridLayout_31.addWidget(self.doubleSpinBox_upper, 0, 1, 1, 1)


        self.gridLayout_28.addWidget(self.groupBox_63, 2, 0, 1, 1)


        self.gridLayout_152.addWidget(self.frame_15, 2, 0, 1, 2)

        self.pushButton_Back1 = QPushButton(self.page_13)
        self.pushButton_Back1.setObjectName(u"pushButton_Back1")
        self.pushButton_Back1.setEnabled(False)

        self.gridLayout_152.addWidget(self.pushButton_Back1, 3, 0, 1, 1)

        self.pushButton_Next1 = QPushButton(self.page_13)
        self.pushButton_Next1.setObjectName(u"pushButton_Next1")

        self.gridLayout_152.addWidget(self.pushButton_Next1, 3, 1, 1, 1)

        self.stackedWidget_segmentation.addWidget(self.page_13)
        self.initialization = QWidget()
        self.initialization.setObjectName(u"initialization")
        self.gridLayout_153 = QGridLayout(self.initialization)
        self.gridLayout_153.setObjectName(u"gridLayout_153")
        self.textBrowser_6 = QTextBrowser(self.initialization)
        self.textBrowser_6.setObjectName(u"textBrowser_6")
        self.textBrowser_6.setMaximumSize(QSize(16777215, 50))
        self.textBrowser_6.setStyleSheet(u"")
        self.textBrowser_6.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser_6.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gridLayout_153.addWidget(self.textBrowser_6, 0, 0, 1, 3)

        self.groupBox_10 = QGroupBox(self.initialization)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_155 = QGridLayout(self.groupBox_10)
        self.gridLayout_155.setObjectName(u"gridLayout_155")
        self.doubleSpinBox_Bubradius = QDoubleSpinBox(self.groupBox_10)
        self.doubleSpinBox_Bubradius.setObjectName(u"doubleSpinBox_Bubradius")
        self.doubleSpinBox_Bubradius.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_Bubradius.setFrame(True)
        self.doubleSpinBox_Bubradius.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.doubleSpinBox_Bubradius.setMaximum(105.000000000000000)
        self.doubleSpinBox_Bubradius.setSingleStep(0.100000000000000)

        self.gridLayout_155.addWidget(self.doubleSpinBox_Bubradius, 1, 0, 1, 1)

        self.horizontalSlider_Bubradius = QSlider(self.groupBox_10)
        self.horizontalSlider_Bubradius.setObjectName(u"horizontalSlider_Bubradius")
        self.horizontalSlider_Bubradius.setMaximum(600)
        self.horizontalSlider_Bubradius.setSingleStep(10)
        self.horizontalSlider_Bubradius.setPageStep(10)
        self.horizontalSlider_Bubradius.setValue(0)
        self.horizontalSlider_Bubradius.setOrientation(Qt.Horizontal)

        self.gridLayout_155.addWidget(self.horizontalSlider_Bubradius, 1, 1, 1, 1)


        self.gridLayout_153.addWidget(self.groupBox_10, 2, 0, 1, 3)

        self.pushButton_Back2 = QPushButton(self.initialization)
        self.pushButton_Back2.setObjectName(u"pushButton_Back2")
        self.pushButton_Back2.setEnabled(True)

        self.gridLayout_153.addWidget(self.pushButton_Back2, 5, 0, 1, 2)

        self.pushButton_Next2 = QPushButton(self.initialization)
        self.pushButton_Next2.setObjectName(u"pushButton_Next2")
        self.pushButton_Next2.setEnabled(False)

        self.gridLayout_153.addWidget(self.pushButton_Next2, 5, 2, 1, 1)

        self.pushButton_addBubbles = QPushButton(self.initialization)
        self.pushButton_addBubbles.setObjectName(u"pushButton_addBubbles")

        self.gridLayout_153.addWidget(self.pushButton_addBubbles, 1, 0, 1, 3)

        self.groupBox_16 = QGroupBox(self.initialization)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.gridLayout_159 = QGridLayout(self.groupBox_16)
        self.gridLayout_159.setObjectName(u"gridLayout_159")
        self.tableView_activeBub = QTableView(self.groupBox_16)
        self.tableView_activeBub.setObjectName(u"tableView_activeBub")
        self.tableView_activeBub.setEnabled(True)
        self.tableView_activeBub.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableView_activeBub.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_activeBub.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView_activeBub.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_activeBub.horizontalHeader().setCascadingSectionResizes(False)

        self.gridLayout_159.addWidget(self.tableView_activeBub, 0, 0, 1, 1)


        self.gridLayout_153.addWidget(self.groupBox_16, 3, 0, 1, 3)

        self.pushButton_delete = QPushButton(self.initialization)
        self.pushButton_delete.setObjectName(u"pushButton_delete")

        self.gridLayout_153.addWidget(self.pushButton_delete, 4, 0, 1, 3)

        self.stackedWidget_segmentation.addWidget(self.initialization)
        self.page_16 = QWidget()
        self.page_16.setObjectName(u"page_16")
        self.gridLayout_160 = QGridLayout(self.page_16)
        self.gridLayout_160.setObjectName(u"gridLayout_160")
        self.groupBox_64 = QGroupBox(self.page_16)
        self.groupBox_64.setObjectName(u"groupBox_64")
        self.groupBox_64.setMaximumSize(QSize(16777215, 100))
        self.gridLayout_161 = QGridLayout(self.groupBox_64)
        self.gridLayout_161.setObjectName(u"gridLayout_161")
        self.doubleSpinBox_SegStep = QDoubleSpinBox(self.groupBox_64)
        self.doubleSpinBox_SegStep.setObjectName(u"doubleSpinBox_SegStep")
        self.doubleSpinBox_SegStep.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_SegStep.setFrame(True)
        self.doubleSpinBox_SegStep.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.doubleSpinBox_SegStep.setMaximum(1000.000000000000000)
        self.doubleSpinBox_SegStep.setSingleStep(0.100000000000000)

        self.gridLayout_161.addWidget(self.doubleSpinBox_SegStep, 0, 0, 1, 1)


        self.gridLayout_160.addWidget(self.groupBox_64, 3, 0, 1, 3)

        self.groupBox_65 = QGroupBox(self.page_16)
        self.groupBox_65.setObjectName(u"groupBox_65")
        self.groupBox_65.setMaximumSize(QSize(16777215, 100))
        self.gridLayout_163 = QGridLayout(self.groupBox_65)
        self.gridLayout_163.setObjectName(u"gridLayout_163")
        self.toolButton_forwardEvo = QToolButton(self.groupBox_65)
        self.toolButton_forwardEvo.setObjectName(u"toolButton_forwardEvo")
        self.toolButton_forwardEvo.setEnabled(True)
        icon12 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekForward))
        self.toolButton_forwardEvo.setIcon(icon12)
        self.toolButton_forwardEvo.setIconSize(QSize(20, 20))

        self.gridLayout_163.addWidget(self.toolButton_forwardEvo, 0, 2, 1, 1)

        self.toolButton_runEvo = QToolButton(self.groupBox_65)
        self.toolButton_runEvo.setObjectName(u"toolButton_runEvo")
        icon13 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
        self.toolButton_runEvo.setIcon(icon13)
        self.toolButton_runEvo.setIconSize(QSize(20, 20))
        self.toolButton_runEvo.setCheckable(True)
        self.toolButton_runEvo.setChecked(False)

        self.gridLayout_163.addWidget(self.toolButton_runEvo, 0, 1, 1, 1)

        self.toolButton_backwardEvo = QToolButton(self.groupBox_65)
        self.toolButton_backwardEvo.setObjectName(u"toolButton_backwardEvo")
        self.toolButton_backwardEvo.setEnabled(True)
        icon14 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekBackward))
        self.toolButton_backwardEvo.setIcon(icon14)
        self.toolButton_backwardEvo.setIconSize(QSize(20, 20))

        self.gridLayout_163.addWidget(self.toolButton_backwardEvo, 0, 0, 1, 1)


        self.gridLayout_160.addWidget(self.groupBox_65, 1, 0, 1, 4)

        self.textBrowser_7 = QTextBrowser(self.page_16)
        self.textBrowser_7.setObjectName(u"textBrowser_7")
        self.textBrowser_7.setMinimumSize(QSize(185, 0))
        self.textBrowser_7.setMaximumSize(QSize(200, 50))
        self.textBrowser_7.setStyleSheet(u"")
        self.textBrowser_7.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser_7.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gridLayout_160.addWidget(self.textBrowser_7, 0, 0, 1, 1)

        self.groupBox_66 = QGroupBox(self.page_16)
        self.groupBox_66.setObjectName(u"groupBox_66")
        self.groupBox_66.setMaximumSize(QSize(16777215, 100))
        self.gridLayout_164 = QGridLayout(self.groupBox_66)
        self.gridLayout_164.setObjectName(u"gridLayout_164")
        self.doubleSpinBox_Segiter = QDoubleSpinBox(self.groupBox_66)
        self.doubleSpinBox_Segiter.setObjectName(u"doubleSpinBox_Segiter")
        self.doubleSpinBox_Segiter.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_Segiter.setFrame(True)
        self.doubleSpinBox_Segiter.setReadOnly(True)
        self.doubleSpinBox_Segiter.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_Segiter.setMaximum(20000.000000000000000)
        self.doubleSpinBox_Segiter.setSingleStep(0.100000000000000)

        self.gridLayout_164.addWidget(self.doubleSpinBox_Segiter, 0, 0, 1, 1)


        self.gridLayout_160.addWidget(self.groupBox_66, 3, 3, 1, 1)

        self.pushButton_Finish = QPushButton(self.page_16)
        self.pushButton_Finish.setObjectName(u"pushButton_Finish")
        self.pushButton_Finish.setEnabled(True)

        self.gridLayout_160.addWidget(self.pushButton_Finish, 5, 3, 1, 1)

        self.pushButton_Back3 = QPushButton(self.page_16)
        self.pushButton_Back3.setObjectName(u"pushButton_Back3")
        self.pushButton_Back3.setEnabled(True)

        self.gridLayout_160.addWidget(self.pushButton_Back3, 5, 0, 1, 1)

        self.stackedWidget_segmentation.addWidget(self.page_16)

        self.gridLayout_5.addWidget(self.stackedWidget_segmentation, 1, 0, 1, 1)

        self.textEdit_SAMRI_reg = QTextEdit(self.groupBox_segmentation)
        self.textEdit_SAMRI_reg.setObjectName(u"textEdit_SAMRI_reg")
        self.textEdit_SAMRI_reg.setMaximumSize(QSize(215, 100))

        self.gridLayout_5.addWidget(self.textEdit_SAMRI_reg, 0, 0, 1, 1)


        self.gridLayout_104.addWidget(self.groupBox_segmentation, 0, 2, 1, 2)

        self.groupBox_paintbrush_3d = QGroupBox(self.tab_15)
        self.groupBox_paintbrush_3d.setObjectName(u"groupBox_paintbrush_3d")
        self.gridLayout_18 = QGridLayout(self.groupBox_paintbrush_3d)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.groupBox_20 = QGroupBox(self.groupBox_paintbrush_3d)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.gridLayout_16 = QGridLayout(self.groupBox_20)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.doubleSpinBox_labelOcc3d = QDoubleSpinBox(self.groupBox_20)
        self.doubleSpinBox_labelOcc3d.setObjectName(u"doubleSpinBox_labelOcc3d")
        self.doubleSpinBox_labelOcc3d.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_labelOcc3d.setFrame(True)
        self.doubleSpinBox_labelOcc3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.doubleSpinBox_labelOcc3d.setMaximum(105.000000000000000)
        self.doubleSpinBox_labelOcc3d.setSingleStep(0.050000000000000)

        self.gridLayout_16.addWidget(self.doubleSpinBox_labelOcc3d, 0, 0, 1, 1)

        self.sizeSlider_labelOcc3d = QSlider(self.groupBox_20)
        self.sizeSlider_labelOcc3d.setObjectName(u"sizeSlider_labelOcc3d")
        self.sizeSlider_labelOcc3d.setMaximum(600)
        self.sizeSlider_labelOcc3d.setSingleStep(1)
        self.sizeSlider_labelOcc3d.setPageStep(1)
        self.sizeSlider_labelOcc3d.setValue(0)
        self.sizeSlider_labelOcc3d.setOrientation(Qt.Horizontal)

        self.gridLayout_16.addWidget(self.sizeSlider_labelOcc3d, 0, 1, 1, 1)


        self.gridLayout_18.addWidget(self.groupBox_20, 0, 1, 1, 1)

        self.groupBox_18 = QGroupBox(self.groupBox_paintbrush_3d)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_10 = QGridLayout(self.groupBox_18)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.groupBox_19 = QGroupBox(self.groupBox_18)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.gridLayout_11 = QGridLayout(self.groupBox_19)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.comboBox_paintOver = QComboBox(self.groupBox_19)
        self.comboBox_paintOver.setObjectName(u"comboBox_paintOver")

        self.gridLayout_11.addWidget(self.comboBox_paintOver, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_19, 0, 0, 1, 1)

        self.groupBox_50 = QGroupBox(self.groupBox_18)
        self.groupBox_50.setObjectName(u"groupBox_50")
        self.gridLayout_15 = QGridLayout(self.groupBox_50)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.tableWidget_labels3D = QTableWidget(self.groupBox_50)
        if (self.tableWidget_labels3D.columnCount() < 3):
            self.tableWidget_labels3D.setColumnCount(3)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_labels3D.setHorizontalHeaderItem(0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget_labels3D.setHorizontalHeaderItem(1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget_labels3D.setHorizontalHeaderItem(2, __qtablewidgetitem26)
        self.tableWidget_labels3D.setObjectName(u"tableWidget_labels3D")
        self.tableWidget_labels3D.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_labels3D.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_labels3D.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_labels3D.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_labels3D.horizontalHeader().setVisible(False)
        self.tableWidget_labels3D.horizontalHeader().setMinimumSectionSize(23)
        self.tableWidget_labels3D.horizontalHeader().setDefaultSectionSize(51)
        self.tableWidget_labels3D.verticalHeader().setVisible(False)
        self.tableWidget_labels3D.verticalHeader().setDefaultSectionSize(25)

        self.gridLayout_15.addWidget(self.tableWidget_labels3D, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_50, 1, 0, 1, 1)


        self.gridLayout_18.addWidget(self.groupBox_18, 3, 0, 1, 2)

        self.groupBox_15 = QGroupBox(self.groupBox_paintbrush_3d)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.gridLayout_13 = QGridLayout(self.groupBox_15)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.brush_size3d = QDoubleSpinBox(self.groupBox_15)
        self.brush_size3d.setObjectName(u"brush_size3d")
        self.brush_size3d.setMaximumSize(QSize(16777215, 30))
        self.brush_size3d.setWrapping(False)
        self.brush_size3d.setFrame(True)
        self.brush_size3d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.brush_size3d.setDecimals(0)
        self.brush_size3d.setMaximum(40.000000000000000)
        self.brush_size3d.setSingleStep(1.000000000000000)

        self.gridLayout_13.addWidget(self.brush_size3d, 0, 0, 1, 1)

        self.brush_sizeSlider3d = QSlider(self.groupBox_15)
        self.brush_sizeSlider3d.setObjectName(u"brush_sizeSlider3d")
        self.brush_sizeSlider3d.setMaximum(600)
        self.brush_sizeSlider3d.setSingleStep(1)
        self.brush_sizeSlider3d.setPageStep(1)
        self.brush_sizeSlider3d.setValue(0)
        self.brush_sizeSlider3d.setOrientation(Qt.Horizontal)

        self.gridLayout_13.addWidget(self.brush_sizeSlider3d, 0, 1, 1, 1)


        self.gridLayout_18.addWidget(self.groupBox_15, 1, 1, 1, 1)

        self.checkBox_Brush = QCheckBox(self.groupBox_paintbrush_3d)
        self.checkBox_Brush.setObjectName(u"checkBox_Brush")
        self.checkBox_Brush.setEnabled(True)
        self.checkBox_Brush.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox_Brush.setFont(font1)
        self.checkBox_Brush.setIconSize(QSize(16, 16))
        self.checkBox_Brush.setChecked(True)

        self.gridLayout_18.addWidget(self.checkBox_Brush, 0, 0, 1, 1)

        self.groupBox_14 = QGroupBox(self.groupBox_paintbrush_3d)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.gridLayout_12 = QGridLayout(self.groupBox_14)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.paint_square = QToolButton(self.groupBox_14)
        self.paint_square.setObjectName(u"paint_square")
        icon15 = QIcon()
        icon15.addFile(u"Icons/Internet/square.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paint_square.setIcon(icon15)
        self.paint_square.setIconSize(QSize(20, 20))
        self.paint_square.setCheckable(True)
        self.paint_square.setChecked(True)
        self.paint_square.setAutoExclusive(False)

        self.gridLayout_12.addWidget(self.paint_square, 0, 0, 1, 1)

        self.paint_round = QToolButton(self.groupBox_14)
        self.paint_round.setObjectName(u"paint_round")
        self.paint_round.setEnabled(True)
        icon16 = QIcon()
        icon16.addFile(u"Icons/Internet/circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paint_round.setIcon(icon16)
        self.paint_round.setIconSize(QSize(20, 20))
        self.paint_round.setCheckable(True)
        self.paint_round.setAutoExclusive(False)

        self.gridLayout_12.addWidget(self.paint_round, 0, 1, 1, 1)


        self.gridLayout_18.addWidget(self.groupBox_14, 1, 0, 1, 1)

        self.pushButton_paint_done = QPushButton(self.groupBox_paintbrush_3d)
        self.pushButton_paint_done.setObjectName(u"pushButton_paint_done")

        self.gridLayout_18.addWidget(self.pushButton_paint_done, 4, 0, 1, 2)

        self.gridLayout_18.setColumnStretch(0, 1)
        self.gridLayout_18.setColumnStretch(1, 1)

        self.gridLayout_104.addWidget(self.groupBox_paintbrush_3d, 1, 4, 1, 1)

        self.groupBox_resample = QGroupBox(self.tab_15)
        self.groupBox_resample.setObjectName(u"groupBox_resample")
        self.gridLayout_17 = QGridLayout(self.groupBox_resample)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.pushButton_resample100um = QPushButton(self.groupBox_resample)
        self.pushButton_resample100um.setObjectName(u"pushButton_resample100um")

        self.gridLayout_17.addWidget(self.pushButton_resample100um, 2, 0, 1, 3)

        self.pushButton_openfile100um = QPushButton(self.groupBox_resample)
        self.pushButton_openfile100um.setObjectName(u"pushButton_openfile100um")
        self.pushButton_openfile100um.setEnabled(False)

        self.gridLayout_17.addWidget(self.pushButton_openfile100um, 6, 2, 1, 1)

        self.pushButton_done = QPushButton(self.groupBox_resample)
        self.pushButton_done.setObjectName(u"pushButton_done")

        self.gridLayout_17.addWidget(self.pushButton_done, 6, 0, 1, 2)

        self.pushButton_resample25um = QPushButton(self.groupBox_resample)
        self.pushButton_resample25um.setObjectName(u"pushButton_resample25um")

        self.gridLayout_17.addWidget(self.pushButton_resample25um, 4, 0, 1, 3)

        self.comboBox_resamplefiles = QComboBox(self.groupBox_resample)
        self.comboBox_resamplefiles.setObjectName(u"comboBox_resamplefiles")

        self.gridLayout_17.addWidget(self.comboBox_resamplefiles, 1, 0, 1, 3)

        self.textBrowser_4 = QTextBrowser(self.groupBox_resample)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setMaximumSize(QSize(16777215, 16777215))
        self.textBrowser_4.setStyleSheet(u"")
        self.textBrowser_4.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser_4.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gridLayout_17.addWidget(self.textBrowser_4, 0, 0, 1, 3)

        self.textEdit_resample25 = QTextEdit(self.groupBox_resample)
        self.textEdit_resample25.setObjectName(u"textEdit_resample25")
        self.textEdit_resample25.setEnabled(False)
        self.textEdit_resample25.setMaximumSize(QSize(16777215, 16777215))
        self.textEdit_resample25.setReadOnly(True)

        self.gridLayout_17.addWidget(self.textEdit_resample25, 5, 0, 1, 3)

        self.textEdit_resample100 = QTextEdit(self.groupBox_resample)
        self.textEdit_resample100.setObjectName(u"textEdit_resample100")
        self.textEdit_resample100.setEnabled(False)
        self.textEdit_resample100.setMaximumSize(QSize(16777215, 16777215))
        self.textEdit_resample100.setReadOnly(True)

        self.gridLayout_17.addWidget(self.textEdit_resample100, 3, 0, 1, 3)

        self.gridLayout_17.setColumnStretch(0, 1)

        self.gridLayout_104.addWidget(self.groupBox_resample, 0, 4, 1, 1)

        self.tabWidget.addTab(self.tab_15, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_173 = QGridLayout(self.tab_6)
        self.gridLayout_173.setObjectName(u"gridLayout_173")
        self.groupBox_paintbrush = QGroupBox(self.tab_6)
        self.groupBox_paintbrush.setObjectName(u"groupBox_paintbrush")
        self.groupBox_paintbrush.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_paintbrush.sizePolicy().hasHeightForWidth())
        self.groupBox_paintbrush.setSizePolicy(sizePolicy5)
        self.groupBox_paintbrush.setMinimumSize(QSize(300, 250))
        self.groupBox_paintbrush.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_43 = QGridLayout(self.groupBox_paintbrush)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.stackedWidget_4D = QStackedWidget(self.groupBox_paintbrush)
        self.stackedWidget_4D.setObjectName(u"stackedWidget_4D")
        self.stackedWidget_4D.setMinimumSize(QSize(0, 0))
        self.stackedWidget_4D.setMaximumSize(QSize(16777215, 16777215))
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout = QGridLayout(self.page_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_anatOK = QPushButton(self.page_8)
        self.pushButton_anatOK.setObjectName(u"pushButton_anatOK")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pushButton_anatOK.sizePolicy().hasHeightForWidth())
        self.pushButton_anatOK.setSizePolicy(sizePolicy6)
        self.pushButton_anatOK.setMinimumSize(QSize(100, 80))
        font7 = QFont()
        font7.setBold(False)
        font7.setStyleStrategy(QFont.PreferDefault)
        self.pushButton_anatOK.setFont(font7)
        self.pushButton_anatOK.setStyleSheet(u"background-color: rgb(237, 51, 59);")

        self.gridLayout.addWidget(self.pushButton_anatOK, 1, 1, 1, 1)

        self.plainTextEdit_MRID_2 = QPlainTextEdit(self.page_8)
        self.plainTextEdit_MRID_2.setObjectName(u"plainTextEdit_MRID_2")
        self.plainTextEdit_MRID_2.setMinimumSize(QSize(0, 80))
        self.plainTextEdit_MRID_2.setMaximumSize(QSize(16777215, 16777215))
        self.plainTextEdit_MRID_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.plainTextEdit_MRID_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.plainTextEdit_MRID_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit_MRID_2.setReadOnly(True)

        self.gridLayout.addWidget(self.plainTextEdit_MRID_2, 0, 1, 1, 1)

        self.stackedWidget_4D.addWidget(self.page_8)
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.gridLayout_80 = QGridLayout(self.page_9)
        self.gridLayout_80.setObjectName(u"gridLayout_80")
        self.pushButton_segOK = QPushButton(self.page_9)
        self.pushButton_segOK.setObjectName(u"pushButton_segOK")
        self.pushButton_segOK.setMinimumSize(QSize(100, 80))
        self.pushButton_segOK.setStyleSheet(u"background-color: rgb(237, 51, 59);")

        self.gridLayout_80.addWidget(self.pushButton_segOK, 1, 1, 1, 1)

        self.plainTextEdit_MRID_4 = QPlainTextEdit(self.page_9)
        self.plainTextEdit_MRID_4.setObjectName(u"plainTextEdit_MRID_4")
        self.plainTextEdit_MRID_4.setMinimumSize(QSize(0, 0))
        self.plainTextEdit_MRID_4.setMaximumSize(QSize(16777215, 16777215))
        self.plainTextEdit_MRID_4.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.plainTextEdit_MRID_4.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.plainTextEdit_MRID_4.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit_MRID_4.setReadOnly(True)

        self.gridLayout_80.addWidget(self.plainTextEdit_MRID_4, 0, 1, 1, 1)

        self.stackedWidget_4D.addWidget(self.page_9)

        self.gridLayout_43.addWidget(self.stackedWidget_4D, 1, 0, 3, 1)

        self.checkBox_Brush_MRID = QCheckBox(self.groupBox_paintbrush)
        self.checkBox_Brush_MRID.setObjectName(u"checkBox_Brush_MRID")
        self.checkBox_Brush_MRID.setEnabled(True)
        self.checkBox_Brush_MRID.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox_Brush_MRID.setFont(font1)
        self.checkBox_Brush_MRID.setIconSize(QSize(16, 16))
        self.checkBox_Brush_MRID.setChecked(True)

        self.gridLayout_43.addWidget(self.checkBox_Brush_MRID, 0, 0, 1, 1)

        self.groupBox_28 = QGroupBox(self.groupBox_paintbrush)
        self.groupBox_28.setObjectName(u"groupBox_28")
        self.groupBox_28.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_41 = QGridLayout(self.groupBox_28)
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.groupBox_29 = QGroupBox(self.groupBox_28)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.groupBox_29.setMaximumSize(QSize(16777215, 100))
        self.gridLayout_40 = QGridLayout(self.groupBox_29)
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.paint_square_Post = QToolButton(self.groupBox_29)
        self.paint_square_Post.setObjectName(u"paint_square_Post")
        self.paint_square_Post.setFont(font)
        self.paint_square_Post.setStyleSheet(u"")
        self.paint_square_Post.setIcon(icon15)
        self.paint_square_Post.setIconSize(QSize(20, 20))
        self.paint_square_Post.setCheckable(True)
        self.paint_square_Post.setChecked(True)
        self.paint_square_Post.setAutoExclusive(False)

        self.gridLayout_40.addWidget(self.paint_square_Post, 0, 0, 1, 1)

        self.paint_round_Post = QToolButton(self.groupBox_29)
        self.paint_round_Post.setObjectName(u"paint_round_Post")
        self.paint_round_Post.setEnabled(True)
        self.paint_round_Post.setIcon(icon16)
        self.paint_round_Post.setIconSize(QSize(20, 20))
        self.paint_round_Post.setCheckable(True)
        self.paint_round_Post.setAutoExclusive(False)

        self.gridLayout_40.addWidget(self.paint_round_Post, 0, 1, 1, 1)


        self.gridLayout_41.addWidget(self.groupBox_29, 0, 1, 1, 3)

        self.groupBox_31 = QGroupBox(self.groupBox_28)
        self.groupBox_31.setObjectName(u"groupBox_31")
        self.groupBox_31.setMaximumSize(QSize(16777215, 250))
        self.gridLayout_42 = QGridLayout(self.groupBox_31)
        self.gridLayout_42.setObjectName(u"gridLayout_42")
        self.sizeSlider_labelOcc = QSlider(self.groupBox_31)
        self.sizeSlider_labelOcc.setObjectName(u"sizeSlider_labelOcc")
        self.sizeSlider_labelOcc.setMinimum(1)
        self.sizeSlider_labelOcc.setMaximum(100)
        self.sizeSlider_labelOcc.setSingleStep(1)
        self.sizeSlider_labelOcc.setPageStep(1)
        self.sizeSlider_labelOcc.setValue(1)
        self.sizeSlider_labelOcc.setOrientation(Qt.Horizontal)

        self.gridLayout_42.addWidget(self.sizeSlider_labelOcc, 0, 1, 1, 1)

        self.doubleSpinBox_labelOcc = QDoubleSpinBox(self.groupBox_31)
        self.doubleSpinBox_labelOcc.setObjectName(u"doubleSpinBox_labelOcc")
        self.doubleSpinBox_labelOcc.setMaximum(1.000000000000000)
        self.doubleSpinBox_labelOcc.setSingleStep(0.050000000000000)

        self.gridLayout_42.addWidget(self.doubleSpinBox_labelOcc, 0, 0, 1, 1)


        self.gridLayout_41.addWidget(self.groupBox_31, 2, 1, 1, 3)

        self.groupBox_30 = QGroupBox(self.groupBox_28)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.gridLayout_39 = QGridLayout(self.groupBox_30)
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.brush_size4d = QDoubleSpinBox(self.groupBox_30)
        self.brush_size4d.setObjectName(u"brush_size4d")
        self.brush_size4d.setMaximumSize(QSize(16777215, 30))
        self.brush_size4d.setWrapping(False)
        self.brush_size4d.setFrame(True)
        self.brush_size4d.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.brush_size4d.setDecimals(0)
        self.brush_size4d.setMinimum(1.000000000000000)
        self.brush_size4d.setMaximum(20.000000000000000)
        self.brush_size4d.setSingleStep(1.000000000000000)

        self.gridLayout_39.addWidget(self.brush_size4d, 0, 0, 1, 1)

        self.brush_sizeSlider4d = QSlider(self.groupBox_30)
        self.brush_sizeSlider4d.setObjectName(u"brush_sizeSlider4d")
        self.brush_sizeSlider4d.setMinimum(1)
        self.brush_sizeSlider4d.setMaximum(20)
        self.brush_sizeSlider4d.setSingleStep(1)
        self.brush_sizeSlider4d.setPageStep(1)
        self.brush_sizeSlider4d.setValue(1)
        self.brush_sizeSlider4d.setOrientation(Qt.Horizontal)

        self.gridLayout_39.addWidget(self.brush_sizeSlider4d, 0, 1, 1, 1)


        self.gridLayout_41.addWidget(self.groupBox_30, 1, 1, 1, 3)


        self.gridLayout_43.addWidget(self.groupBox_28, 0, 1, 4, 1)

        self.groupBox_33 = QGroupBox(self.groupBox_paintbrush)
        self.groupBox_33.setObjectName(u"groupBox_33")
        self.groupBox_33.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_38 = QGridLayout(self.groupBox_33)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.groupBox_35 = QGroupBox(self.groupBox_33)
        self.groupBox_35.setObjectName(u"groupBox_35")
        self.gridLayout_36 = QGridLayout(self.groupBox_35)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.comboBox_paintOver_Post = QComboBox(self.groupBox_35)
        self.comboBox_paintOver_Post.setObjectName(u"comboBox_paintOver_Post")
        self.comboBox_paintOver_Post.setEnabled(True)

        self.gridLayout_36.addWidget(self.comboBox_paintOver_Post, 0, 0, 1, 1)


        self.gridLayout_38.addWidget(self.groupBox_35, 0, 0, 1, 1)

        self.groupBox_47 = QGroupBox(self.groupBox_33)
        self.groupBox_47.setObjectName(u"groupBox_47")
        self.gridLayout_37 = QGridLayout(self.groupBox_47)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.tableWidget_labels = QTableWidget(self.groupBox_47)
        if (self.tableWidget_labels.columnCount() < 3):
            self.tableWidget_labels.setColumnCount(3)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget_labels.setHorizontalHeaderItem(0, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget_labels.setHorizontalHeaderItem(1, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget_labels.setHorizontalHeaderItem(2, __qtablewidgetitem29)
        self.tableWidget_labels.setObjectName(u"tableWidget_labels")
        self.tableWidget_labels.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_labels.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_labels.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_labels.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_labels.horizontalHeader().setVisible(False)
        self.tableWidget_labels.horizontalHeader().setMinimumSectionSize(23)
        self.tableWidget_labels.horizontalHeader().setDefaultSectionSize(51)
        self.tableWidget_labels.verticalHeader().setVisible(False)
        self.tableWidget_labels.verticalHeader().setDefaultSectionSize(25)

        self.gridLayout_37.addWidget(self.tableWidget_labels, 0, 0, 1, 1)


        self.gridLayout_38.addWidget(self.groupBox_47, 1, 0, 1, 1)


        self.gridLayout_43.addWidget(self.groupBox_33, 0, 4, 4, 1)

        self.groupBox_36 = QGroupBox(self.groupBox_paintbrush)
        self.groupBox_36.setObjectName(u"groupBox_36")
        self.groupBox_36.setEnabled(True)
        self.groupBox_36.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_44 = QGridLayout(self.groupBox_36)
        self.gridLayout_44.setObjectName(u"gridLayout_44")
        self.groupBox_48 = QGroupBox(self.groupBox_36)
        self.groupBox_48.setObjectName(u"groupBox_48")
        self.groupBox_48.setMaximumSize(QSize(16777215, 60))
        self.gridLayout_45 = QGridLayout(self.groupBox_48)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.histogram_label = QComboBox(self.groupBox_48)
        self.histogram_label.setObjectName(u"histogram_label")
        self.histogram_label.setEnabled(True)

        self.gridLayout_45.addWidget(self.histogram_label, 0, 0, 1, 1)

        self.paintbrush_dataview = QComboBox(self.groupBox_48)
        self.paintbrush_dataview.setObjectName(u"paintbrush_dataview")

        self.gridLayout_45.addWidget(self.paintbrush_dataview, 0, 1, 1, 1)


        self.gridLayout_44.addWidget(self.groupBox_48, 0, 0, 1, 1)

        self.widget_histogram = PlotWidget(self.groupBox_36)
        self.widget_histogram.setObjectName(u"widget_histogram")
        self.widget_histogram.setMaximumSize(QSize(16777215, 1000))

        self.gridLayout_44.addWidget(self.widget_histogram, 0, 1, 1, 1)


        self.gridLayout_43.addWidget(self.groupBox_36, 0, 5, 4, 1)


        self.gridLayout_173.addWidget(self.groupBox_paintbrush, 0, 0, 1, 1)

        self.frame_spacing = QFrame(self.tab_6)
        self.frame_spacing.setObjectName(u"frame_spacing")
        self.frame_spacing.setFrameShape(QFrame.StyledPanel)
        self.frame_spacing.setFrameShadow(QFrame.Raised)
        self.gridLayout_181 = QGridLayout(self.frame_spacing)
        self.gridLayout_181.setObjectName(u"gridLayout_181")
        self.lineEdit_52 = QLineEdit(self.frame_spacing)
        self.lineEdit_52.setObjectName(u"lineEdit_52")
        self.lineEdit_52.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_52.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_52, 1, 5, 1, 1)

        self.doubleSpinBox_fovy = QDoubleSpinBox(self.frame_spacing)
        self.doubleSpinBox_fovy.setObjectName(u"doubleSpinBox_fovy")
        self.doubleSpinBox_fovy.setDecimals(5)
        self.doubleSpinBox_fovy.setMaximum(1000.000000000000000)

        self.gridLayout_181.addWidget(self.doubleSpinBox_fovy, 2, 6, 1, 1)

        self.lineEdit_56 = QLineEdit(self.frame_spacing)
        self.lineEdit_56.setObjectName(u"lineEdit_56")
        self.lineEdit_56.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_56.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_56, 2, 7, 1, 1)

        self.doubleSpinBox_spay = QDoubleSpinBox(self.frame_spacing)
        self.doubleSpinBox_spay.setObjectName(u"doubleSpinBox_spay")
        self.doubleSpinBox_spay.setDecimals(5)
        self.doubleSpinBox_spay.setMaximum(1000.000000000000000)

        self.gridLayout_181.addWidget(self.doubleSpinBox_spay, 3, 6, 1, 1)

        self.spinBox_dimey = QSpinBox(self.frame_spacing)
        self.spinBox_dimey.setObjectName(u"spinBox_dimey")
        self.spinBox_dimey.setReadOnly(True)
        self.spinBox_dimey.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimey.setMaximum(1000)

        self.gridLayout_181.addWidget(self.spinBox_dimey, 1, 6, 1, 1)

        self.pushButton_SaveSpacing = QPushButton(self.frame_spacing)
        self.pushButton_SaveSpacing.setObjectName(u"pushButton_SaveSpacing")

        self.gridLayout_181.addWidget(self.pushButton_SaveSpacing, 5, 4, 1, 5)

        self.lineEdit_55 = QLineEdit(self.frame_spacing)
        self.lineEdit_55.setObjectName(u"lineEdit_55")
        self.lineEdit_55.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_55.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_55, 1, 7, 1, 1)

        self.spinBox_dimez = QSpinBox(self.frame_spacing)
        self.spinBox_dimez.setObjectName(u"spinBox_dimez")
        self.spinBox_dimez.setReadOnly(True)
        self.spinBox_dimez.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimez.setMaximum(1000)

        self.gridLayout_181.addWidget(self.spinBox_dimez, 1, 8, 1, 1)

        self.lineEdit_50 = QLineEdit(self.frame_spacing)
        self.lineEdit_50.setObjectName(u"lineEdit_50")
        self.lineEdit_50.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_50.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_50, 2, 2, 1, 1)

        self.lineEdit_47 = QLineEdit(self.frame_spacing)
        self.lineEdit_47.setObjectName(u"lineEdit_47")
        self.lineEdit_47.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_47, 3, 0, 1, 1)

        self.lineEdit_54 = QLineEdit(self.frame_spacing)
        self.lineEdit_54.setObjectName(u"lineEdit_54")
        self.lineEdit_54.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_54.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_54, 3, 5, 1, 1)

        self.lineEdit_53 = QLineEdit(self.frame_spacing)
        self.lineEdit_53.setObjectName(u"lineEdit_53")
        self.lineEdit_53.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_53.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_53, 2, 5, 1, 1)

        self.lineEdit_48 = QLineEdit(self.frame_spacing)
        self.lineEdit_48.setObjectName(u"lineEdit_48")
        self.lineEdit_48.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_48, 2, 0, 1, 1)

        self.lineEdit_51 = QLineEdit(self.frame_spacing)
        self.lineEdit_51.setObjectName(u"lineEdit_51")
        self.lineEdit_51.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_51.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_51, 3, 2, 1, 1)

        self.lineEdit_46 = QLineEdit(self.frame_spacing)
        self.lineEdit_46.setObjectName(u"lineEdit_46")
        self.lineEdit_46.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_46, 1, 0, 1, 1)

        self.doubleSpinBox_fovz = QDoubleSpinBox(self.frame_spacing)
        self.doubleSpinBox_fovz.setObjectName(u"doubleSpinBox_fovz")
        self.doubleSpinBox_fovz.setDecimals(5)
        self.doubleSpinBox_fovz.setMaximum(1000.000000000000000)

        self.gridLayout_181.addWidget(self.doubleSpinBox_fovz, 2, 8, 1, 1)

        self.doubleSpinBox_spax = QDoubleSpinBox(self.frame_spacing)
        self.doubleSpinBox_spax.setObjectName(u"doubleSpinBox_spax")
        self.doubleSpinBox_spax.setDecimals(5)
        self.doubleSpinBox_spax.setMaximum(1000.000000000000000)

        self.gridLayout_181.addWidget(self.doubleSpinBox_spax, 3, 3, 1, 1)

        self.spinBox_dimex = QSpinBox(self.frame_spacing)
        self.spinBox_dimex.setObjectName(u"spinBox_dimex")
        self.spinBox_dimex.setReadOnly(True)
        self.spinBox_dimex.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimex.setMaximum(1000)

        self.gridLayout_181.addWidget(self.spinBox_dimex, 1, 3, 1, 1)

        self.pushButton_cancel_spacing = QPushButton(self.frame_spacing)
        self.pushButton_cancel_spacing.setObjectName(u"pushButton_cancel_spacing")

        self.gridLayout_181.addWidget(self.pushButton_cancel_spacing, 5, 0, 1, 4)

        self.doubleSpinBox_fovx = QDoubleSpinBox(self.frame_spacing)
        self.doubleSpinBox_fovx.setObjectName(u"doubleSpinBox_fovx")
        self.doubleSpinBox_fovx.setDecimals(5)
        self.doubleSpinBox_fovx.setMaximum(1000.000000000000000)

        self.gridLayout_181.addWidget(self.doubleSpinBox_fovx, 2, 3, 1, 1)

        self.lineEdit_49 = QLineEdit(self.frame_spacing)
        self.lineEdit_49.setObjectName(u"lineEdit_49")
        self.lineEdit_49.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_49.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_49, 1, 2, 1, 1)

        self.lineEdit_57 = QLineEdit(self.frame_spacing)
        self.lineEdit_57.setObjectName(u"lineEdit_57")
        self.lineEdit_57.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_57.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_57, 3, 7, 1, 1)

        self.doubleSpinBox_spaz = QDoubleSpinBox(self.frame_spacing)
        self.doubleSpinBox_spaz.setObjectName(u"doubleSpinBox_spaz")
        self.doubleSpinBox_spaz.setDecimals(5)
        self.doubleSpinBox_spaz.setMaximum(1000.000000000000000)

        self.gridLayout_181.addWidget(self.doubleSpinBox_spaz, 3, 8, 1, 1)


        self.gridLayout_173.addWidget(self.frame_spacing, 1, 1, 1, 1)

        self.frame_metadata = QFrame(self.tab_6)
        self.frame_metadata.setObjectName(u"frame_metadata")
        self.frame_metadata.setFrameShape(QFrame.StyledPanel)
        self.frame_metadata.setFrameShadow(QFrame.Raised)
        self.gridLayout_180 = QGridLayout(self.frame_metadata)
        self.gridLayout_180.setObjectName(u"gridLayout_180")
        self.lineEdit_42 = QLineEdit(self.frame_metadata)
        self.lineEdit_42.setObjectName(u"lineEdit_42")
        self.lineEdit_42.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_42.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_42, 4, 6, 1, 1)

        self.doubleSpinBox_originx = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_originx.setObjectName(u"doubleSpinBox_originx")
        self.doubleSpinBox_originx.setReadOnly(True)
        self.doubleSpinBox_originx.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_originx.setDecimals(5)
        self.doubleSpinBox_originx.setMinimum(-1000.000000000000000)

        self.gridLayout_180.addWidget(self.doubleSpinBox_originx, 4, 2, 1, 1)

        self.lineEdit_28 = QLineEdit(self.frame_metadata)
        self.lineEdit_28.setObjectName(u"lineEdit_28")
        self.lineEdit_28.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_28, 8, 0, 1, 1)

        self.lineEdit_34 = QLineEdit(self.frame_metadata)
        self.lineEdit_34.setObjectName(u"lineEdit_34")
        self.lineEdit_34.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_34.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_34, 2, 1, 1, 1)

        self.pushButton_SaveMetadata = QPushButton(self.frame_metadata)
        self.pushButton_SaveMetadata.setObjectName(u"pushButton_SaveMetadata")

        self.gridLayout_180.addWidget(self.pushButton_SaveMetadata, 9, 3, 1, 5)

        self.lineEdit_23 = QLineEdit(self.frame_metadata)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        self.lineEdit_23.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_23, 2, 0, 1, 1)

        self.lineEdit_37 = QLineEdit(self.frame_metadata)
        self.lineEdit_37.setObjectName(u"lineEdit_37")
        self.lineEdit_37.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_37.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_37, 2, 4, 1, 1)

        self.comboBox = QComboBox(self.frame_metadata)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_180.addWidget(self.comboBox, 0, 0, 1, 8)

        self.pushButton_changeSpacing = QPushButton(self.frame_metadata)
        self.pushButton_changeSpacing.setObjectName(u"pushButton_changeSpacing")

        self.gridLayout_180.addWidget(self.pushButton_changeSpacing, 9, 0, 1, 1)

        self.doubleSpinBox_minIntensity = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_minIntensity.setObjectName(u"doubleSpinBox_minIntensity")
        self.doubleSpinBox_minIntensity.setReadOnly(True)
        self.doubleSpinBox_minIntensity.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_minIntensity.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_minIntensity, 8, 5, 1, 1)

        self.lineEdit_40 = QLineEdit(self.frame_metadata)
        self.lineEdit_40.setObjectName(u"lineEdit_40")
        self.lineEdit_40.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_40.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_40, 2, 6, 1, 1)

        self.lineEdit_39 = QLineEdit(self.frame_metadata)
        self.lineEdit_39.setObjectName(u"lineEdit_39")
        self.lineEdit_39.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_39.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_39, 4, 4, 1, 1)

        self.lineEdit_35 = QLineEdit(self.frame_metadata)
        self.lineEdit_35.setObjectName(u"lineEdit_35")
        self.lineEdit_35.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_35.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_35, 3, 1, 1, 1)

        self.spinBox_dimy = QSpinBox(self.frame_metadata)
        self.spinBox_dimy.setObjectName(u"spinBox_dimy")
        self.spinBox_dimy.setReadOnly(True)
        self.spinBox_dimy.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimy.setMaximum(100000)

        self.gridLayout_180.addWidget(self.spinBox_dimy, 2, 5, 1, 1)

        self.pushButton_cancel_metadata = QPushButton(self.frame_metadata)
        self.pushButton_cancel_metadata.setObjectName(u"pushButton_cancel_metadata")

        self.gridLayout_180.addWidget(self.pushButton_cancel_metadata, 9, 1, 1, 2)

        self.lineEdit_26 = QLineEdit(self.frame_metadata)
        self.lineEdit_26.setObjectName(u"lineEdit_26")
        self.lineEdit_26.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_26, 4, 0, 1, 1)

        self.doubleSpinBox_spacingy = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_spacingy.setObjectName(u"doubleSpinBox_spacingy")
        self.doubleSpinBox_spacingy.setReadOnly(True)
        self.doubleSpinBox_spacingy.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_spacingy.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_spacingy, 3, 5, 1, 1)

        self.lineEdit_44 = QLineEdit(self.frame_metadata)
        self.lineEdit_44.setObjectName(u"lineEdit_44")
        self.lineEdit_44.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_44.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_44, 8, 4, 1, 1)

        self.pushButton_reorient = QPushButton(self.frame_metadata)
        self.pushButton_reorient.setObjectName(u"pushButton_reorient")
        self.pushButton_reorient.setCheckable(True)
        self.pushButton_reorient.setChecked(False)

        self.gridLayout_180.addWidget(self.pushButton_reorient, 5, 7, 1, 1)

        self.doubleSpinBox_originz = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_originz.setObjectName(u"doubleSpinBox_originz")
        self.doubleSpinBox_originz.setReadOnly(True)
        self.doubleSpinBox_originz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_originz.setDecimals(5)
        self.doubleSpinBox_originz.setMinimum(-1000.000000000000000)

        self.gridLayout_180.addWidget(self.doubleSpinBox_originz, 4, 7, 1, 1)

        self.lineEdit_36 = QLineEdit(self.frame_metadata)
        self.lineEdit_36.setObjectName(u"lineEdit_36")
        self.lineEdit_36.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_36.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_36, 4, 1, 1, 1)

        self.lineEdit_41 = QLineEdit(self.frame_metadata)
        self.lineEdit_41.setObjectName(u"lineEdit_41")
        self.lineEdit_41.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_41.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_41, 3, 6, 1, 1)

        self.spinBox_dimx = QSpinBox(self.frame_metadata)
        self.spinBox_dimx.setObjectName(u"spinBox_dimx")
        self.spinBox_dimx.setReadOnly(True)
        self.spinBox_dimx.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimx.setMaximum(100000)

        self.gridLayout_180.addWidget(self.spinBox_dimx, 2, 2, 1, 1)

        self.doubleSpinBox_spacingx = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_spacingx.setObjectName(u"doubleSpinBox_spacingx")
        self.doubleSpinBox_spacingx.setReadOnly(True)
        self.doubleSpinBox_spacingx.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_spacingx.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_spacingx, 3, 2, 1, 1)

        self.lineEdit_32 = QLineEdit(self.frame_metadata)
        self.lineEdit_32.setObjectName(u"lineEdit_32")
        self.lineEdit_32.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_32, 7, 0, 1, 1)

        self.lineEdit_direction = QTextEdit(self.frame_metadata)
        self.lineEdit_direction.setObjectName(u"lineEdit_direction")
        self.lineEdit_direction.setMaximumSize(QSize(500, 100))

        self.gridLayout_180.addWidget(self.lineEdit_direction, 7, 1, 1, 7)

        self.lineEdit_27 = QLineEdit(self.frame_metadata)
        self.lineEdit_27.setObjectName(u"lineEdit_27")
        self.lineEdit_27.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_27, 5, 0, 1, 1)

        self.lineEdit_25 = QLineEdit(self.frame_metadata)
        self.lineEdit_25.setObjectName(u"lineEdit_25")
        self.lineEdit_25.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_25, 3, 0, 1, 1)

        self.doubleSpinBox_originy = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_originy.setObjectName(u"doubleSpinBox_originy")
        self.doubleSpinBox_originy.setReadOnly(True)
        self.doubleSpinBox_originy.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_originy.setDecimals(5)
        self.doubleSpinBox_originy.setMinimum(-1000.000000000000000)

        self.gridLayout_180.addWidget(self.doubleSpinBox_originy, 4, 5, 1, 1)

        self.doubleSpinBox_maxIntensity = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_maxIntensity.setObjectName(u"doubleSpinBox_maxIntensity")
        self.doubleSpinBox_maxIntensity.setReadOnly(True)
        self.doubleSpinBox_maxIntensity.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_maxIntensity.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_maxIntensity, 8, 7, 1, 1)

        self.lineEdit_DicomOrient = QLineEdit(self.frame_metadata)
        self.lineEdit_DicomOrient.setObjectName(u"lineEdit_DicomOrient")
        self.lineEdit_DicomOrient.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_DicomOrient, 5, 4, 1, 3)

        self.lineEdit_38 = QLineEdit(self.frame_metadata)
        self.lineEdit_38.setObjectName(u"lineEdit_38")
        self.lineEdit_38.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_38.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_38, 3, 4, 1, 1)

        self.lineEdit_45 = QLineEdit(self.frame_metadata)
        self.lineEdit_45.setObjectName(u"lineEdit_45")
        self.lineEdit_45.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_45.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_45, 8, 6, 1, 1)

        self.doubleSpinBox_spacingz = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_spacingz.setObjectName(u"doubleSpinBox_spacingz")
        self.doubleSpinBox_spacingz.setReadOnly(True)
        self.doubleSpinBox_spacingz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_spacingz.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_spacingz, 3, 7, 1, 1)

        self.spinBox_dimz = QSpinBox(self.frame_metadata)
        self.spinBox_dimz.setObjectName(u"spinBox_dimz")
        self.spinBox_dimz.setReadOnly(True)
        self.spinBox_dimz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimz.setMaximum(100000)

        self.gridLayout_180.addWidget(self.spinBox_dimz, 2, 7, 1, 1)


        self.gridLayout_173.addWidget(self.frame_metadata, 1, 0, 1, 1)

        self.tp_dwi1D_frame = QFrame(self.tab_6)
        self.tp_dwi1D_frame.setObjectName(u"tp_dwi1D_frame")
        self.tp_dwi1D_frame.setFrameShape(QFrame.StyledPanel)
        self.tp_dwi1D_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_183 = QGridLayout(self.tp_dwi1D_frame)
        self.gridLayout_183.setObjectName(u"gridLayout_183")
        self.tp_dwi1D_widget = MplWidget(self.tp_dwi1D_frame)
        self.tp_dwi1D_widget.setObjectName(u"tp_dwi1D_widget")

        self.gridLayout_183.addWidget(self.tp_dwi1D_widget, 0, 0, 1, 1)


        self.gridLayout_173.addWidget(self.tp_dwi1D_frame, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_ephys = QWidget()
        self.tab_ephys.setObjectName(u"tab_ephys")
        self.gridLayout_22 = QGridLayout(self.tab_ephys)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.pushButton_anatRegion = QPushButton(self.tab_ephys)
        self.pushButton_anatRegion.setObjectName(u"pushButton_anatRegion")
        self.pushButton_anatRegion.setMinimumSize(QSize(0, 72))
        self.pushButton_anatRegion.setFont(font1)
        self.pushButton_anatRegion.setStyleSheet(u"color: rgb(224, 27, 36);")

        self.gridLayout_22.addWidget(self.pushButton_anatRegion, 2, 4, 1, 1)

        self.groupBox_5 = QGroupBox(self.tab_ephys)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_165 = QGridLayout(self.groupBox_5)
        self.gridLayout_165.setObjectName(u"gridLayout_165")
        self.comboBox_mridTag = QComboBox(self.groupBox_5)
        self.comboBox_mridTag.setObjectName(u"comboBox_mridTag")
        self.comboBox_mridTag.setEnabled(False)
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


        self.gridLayout_22.addWidget(self.groupBox_5, 0, 3, 1, 1)

        self.frame_2 = QFrame(self.tab_ephys)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_168 = QGridLayout(self.frame_2)
        self.gridLayout_168.setObjectName(u"gridLayout_168")
        self.pushButton_selectAll = QPushButton(self.frame_2)
        self.pushButton_selectAll.setObjectName(u"pushButton_selectAll")

        self.gridLayout_168.addWidget(self.pushButton_selectAll, 1, 0, 1, 1)

        self.tableWidget_ephys = QTableWidget(self.frame_2)
        self.tableWidget_ephys.setObjectName(u"tableWidget_ephys")
        self.tableWidget_ephys.setFont(font2)
        self.tableWidget_ephys.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_ephys.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_ephys.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.tableWidget_ephys.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_ephys.horizontalHeader().setCascadingSectionResizes(False)

        self.gridLayout_168.addWidget(self.tableWidget_ephys, 0, 0, 1, 2)

        self.pushButton_deselectAll = QPushButton(self.frame_2)
        self.pushButton_deselectAll.setObjectName(u"pushButton_deselectAll")

        self.gridLayout_168.addWidget(self.pushButton_deselectAll, 1, 1, 1, 1)

        self.pushButton_showChannels = QPushButton(self.frame_2)
        self.pushButton_showChannels.setObjectName(u"pushButton_showChannels")
        self.pushButton_showChannels.setCheckable(True)
        self.pushButton_showChannels.setChecked(True)

        self.gridLayout_168.addWidget(self.pushButton_showChannels, 2, 0, 1, 2)


        self.gridLayout_22.addWidget(self.frame_2, 0, 4, 2, 1)

        self.textEdit_ephys = QTextEdit(self.tab_ephys)
        self.textEdit_ephys.setObjectName(u"textEdit_ephys")
        self.textEdit_ephys.setMaximumSize(QSize(16777215, 50))
        self.textEdit_ephys.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_ephys.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_ephys.setReadOnly(True)

        self.gridLayout_22.addWidget(self.textEdit_ephys, 0, 0, 1, 3)

        self.tabWidget_2 = QTabWidget(self.tab_ephys)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
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

        self.spinBox_z_ephys = QSpinBox(self.groupBox_37)
        self.spinBox_z_ephys.setObjectName(u"spinBox_z_ephys")
        self.spinBox_z_ephys.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_ephys.setReadOnly(True)
        self.spinBox_z_ephys.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_z_ephys.setMinimum(1)
        self.spinBox_z_ephys.setMaximum(1000)

        self.gridLayout_74.addWidget(self.spinBox_z_ephys, 0, 3, 1, 1)

        self.spinBox_x_ephys = QSpinBox(self.groupBox_37)
        self.spinBox_x_ephys.setObjectName(u"spinBox_x_ephys")
        self.spinBox_x_ephys.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_ephys.setReadOnly(True)
        self.spinBox_x_ephys.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_x_ephys.setMinimum(1)
        self.spinBox_x_ephys.setMaximum(1000)

        self.gridLayout_74.addWidget(self.spinBox_x_ephys, 0, 1, 1, 1)


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
        self.resetCamera_ephys = QPushButton(self.frame_32)
        self.resetCamera_ephys.setObjectName(u"resetCamera_ephys")
        self.resetCamera_ephys.setEnabled(True)
        self.resetCamera_ephys.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon17 = QIcon(QIcon.fromTheme(u"go-home"))
        self.resetCamera_ephys.setIcon(icon17)
        self.resetCamera_ephys.setIconSize(QSize(60, 40))
        self.resetCamera_ephys.setAutoDefault(False)
        self.resetCamera_ephys.setFlat(False)

        self.gridLayout_68.addWidget(self.resetCamera_ephys, 2, 0, 2, 1)

        self.change_perspective_ephys = QPushButton(self.frame_32)
        self.change_perspective_ephys.setObjectName(u"change_perspective_ephys")
        self.change_perspective_ephys.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon18 = QIcon()
        icon18.addFile(u"Icons/ephys/projection_parallel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.change_perspective_ephys.setIcon(icon18)
        self.change_perspective_ephys.setIconSize(QSize(60, 40))

        self.gridLayout_68.addWidget(self.change_perspective_ephys, 3, 1, 1, 1)

        self.pushButton_slicey = QPushButton(self.frame_32)
        self.pushButton_slicey.setObjectName(u"pushButton_slicey")
        self.pushButton_slicey.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon19 = QIcon()
        icon19.addFile(u"Icons/ephys/slicing_coronal_front.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicey.setIcon(icon19)
        self.pushButton_slicey.setIconSize(QSize(60, 40))
        self.pushButton_slicey.setCheckable(True)

        self.gridLayout_68.addWidget(self.pushButton_slicey, 3, 4, 1, 1)

        self.pushButton_Noslicing = QPushButton(self.frame_32)
        self.pushButton_Noslicing.setObjectName(u"pushButton_Noslicing")
        self.pushButton_Noslicing.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon20 = QIcon()
        icon20.addFile(u"Icons/ephys/no_slicing.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_Noslicing.setIcon(icon20)
        self.pushButton_Noslicing.setIconSize(QSize(60, 40))

        self.gridLayout_68.addWidget(self.pushButton_Noslicing, 3, 2, 1, 1)

        self.pushButton_slicex = QPushButton(self.frame_32)
        self.pushButton_slicex.setObjectName(u"pushButton_slicex")
        self.pushButton_slicex.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon21 = QIcon()
        icon21.addFile(u"Icons/ephys/slicing_sagittal_right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicex.setIcon(icon21)
        self.pushButton_slicex.setIconSize(QSize(60, 40))
        self.pushButton_slicex.setCheckable(True)

        self.gridLayout_68.addWidget(self.pushButton_slicex, 3, 3, 1, 1)

        self.pushButton_slicez = QPushButton(self.frame_32)
        self.pushButton_slicez.setObjectName(u"pushButton_slicez")
        self.pushButton_slicez.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon22 = QIcon()
        icon22.addFile(u"Icons/ephys/slicing_axial_top.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicez.setIcon(icon22)
        self.pushButton_slicez.setIconSize(QSize(60, 40))
        self.pushButton_slicez.setCheckable(True)

        self.gridLayout_68.addWidget(self.pushButton_slicez, 3, 5, 1, 1)

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

        self.gridLayout_68.addWidget(self.groupBox_6, 1, 0, 1, 6)

        self.vtkWidget_ephys = QVTKRenderWindowInteractor(self.frame_32)
        self.vtkWidget_ephys.setObjectName(u"vtkWidget_ephys")
        self.vtkWidget_ephys.setEnabled(True)
        self.vtkWidget_ephys.setMinimumSize(QSize(0, 0))
        self.vtkWidget_ephys.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_68.addWidget(self.vtkWidget_ephys, 0, 0, 1, 6)

        self.gridLayout_68.setColumnStretch(0, 1)
        self.gridLayout_68.setColumnStretch(1, 1)
        self.gridLayout_68.setColumnStretch(2, 1)
        self.gridLayout_68.setColumnStretch(3, 1)
        self.gridLayout_68.setColumnStretch(4, 1)
        self.gridLayout_68.setColumnStretch(5, 1)

        self.gridLayout_46.addWidget(self.frame_32, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_4, "")
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
        icon23 = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.pushButton_videoPlay.setIcon(icon23)
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

        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_185 = QGridLayout(self.tab_7)
        self.gridLayout_185.setObjectName(u"gridLayout_185")
        self.stackedWidget = QStackedWidget(self.tab_7)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_17 = QWidget()
        self.page_17.setObjectName(u"page_17")
        self.gridLayout_186 = QGridLayout(self.page_17)
        self.gridLayout_186.setObjectName(u"gridLayout_186")
        self.widget_cutoff_freq = QWidget(self.page_17)
        self.widget_cutoff_freq.setObjectName(u"widget_cutoff_freq")
        self.widget_cutoff_freq.setMinimumSize(QSize(1000, 100))
        self.groupBox_anatRegion = QGroupBox(self.widget_cutoff_freq)
        self.groupBox_anatRegion.setObjectName(u"groupBox_anatRegion")
        self.groupBox_anatRegion.setGeometry(QRect(20, 160, 1142, 85))
        self.gridLayout_24 = QGridLayout(self.groupBox_anatRegion)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.comboBox_anatRegion = QComboBox(self.groupBox_anatRegion)
        self.comboBox_anatRegion.setObjectName(u"comboBox_anatRegion")
        self.comboBox_anatRegion.setEnabled(False)
        self.comboBox_anatRegion.setMinimumSize(QSize(0, 40))
        self.comboBox_anatRegion.setStyleSheet(u"")

        self.gridLayout_24.addWidget(self.comboBox_anatRegion, 0, 2, 1, 1)

        self.spinBox_channelID = QSpinBox(self.groupBox_anatRegion)
        self.spinBox_channelID.setObjectName(u"spinBox_channelID")
        self.spinBox_channelID.setMinimumSize(QSize(0, 40))
        self.spinBox_channelID.setReadOnly(False)
        self.spinBox_channelID.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_24.addWidget(self.spinBox_channelID, 0, 1, 1, 1)

        self.pushButton_changeTAG = QPushButton(self.widget_cutoff_freq)
        self.pushButton_changeTAG.setObjectName(u"pushButton_changeTAG")
        self.pushButton_changeTAG.setGeometry(QRect(540, 80, 266, 26))
        self.pushButton_changeTAG.setStyleSheet(u"color: rgb(224, 27, 36);")

        self.gridLayout_186.addWidget(self.widget_cutoff_freq, 1, 0, 1, 2)

        self.pushButton_filterpopup = QPushButton(self.page_17)
        self.pushButton_filterpopup.setObjectName(u"pushButton_filterpopup")

        self.gridLayout_186.addWidget(self.pushButton_filterpopup, 0, 0, 1, 2)

        self.stackedWidget.addWidget(self.page_17)
        self.page_18 = QWidget()
        self.page_18.setObjectName(u"page_18")
        self.stackedWidget.addWidget(self.page_18)

        self.gridLayout_185.addWidget(self.stackedWidget, 1, 0, 1, 1)

        self.lineEdit_13 = QLineEdit(self.tab_7)
        self.lineEdit_13.setObjectName(u"lineEdit_13")

        self.gridLayout_185.addWidget(self.lineEdit_13, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_7, "")

        self.gridLayout_22.addWidget(self.tabWidget_2, 1, 0, 2, 4)

        self.tabWidget.addTab(self.tab_ephys, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_21 = QGridLayout(self.tab)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.frame_filterchannels = QFrame(self.tab)
        self.frame_filterchannels.setObjectName(u"frame_filterchannels")
        self.frame_filterchannels.setFrameShape(QFrame.StyledPanel)
        self.frame_filterchannels.setFrameShadow(QFrame.Raised)
        self.gridLayout_192 = QGridLayout(self.frame_filterchannels)
        self.gridLayout_192.setObjectName(u"gridLayout_192")
        self.pushButton_FrequencyResponse = QPushButton(self.frame_filterchannels)
        self.pushButton_FrequencyResponse.setObjectName(u"pushButton_FrequencyResponse")

        self.gridLayout_192.addWidget(self.pushButton_FrequencyResponse, 9, 0, 1, 1)

        self.comboBox_FilterType = QComboBox(self.frame_filterchannels)
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.setObjectName(u"comboBox_FilterType")

        self.gridLayout_192.addWidget(self.comboBox_FilterType, 2, 1, 1, 1)

        self.lineEdit_selectedChannels = QLineEdit(self.frame_filterchannels)
        self.lineEdit_selectedChannels.setObjectName(u"lineEdit_selectedChannels")

        self.gridLayout_192.addWidget(self.lineEdit_selectedChannels, 0, 1, 1, 1)

        self.radioButton_bandPass = QRadioButton(self.frame_filterchannels)
        self.radioButton_bandPass.setObjectName(u"radioButton_bandPass")
        self.radioButton_bandPass.setChecked(True)

        self.gridLayout_192.addWidget(self.radioButton_bandPass, 2, 0, 1, 1)

        self.lineEdit_18 = QLineEdit(self.frame_filterchannels)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        self.lineEdit_18.setReadOnly(True)

        self.gridLayout_192.addWidget(self.lineEdit_18, 0, 0, 1, 1)

        self.radioButton_lowPass = QRadioButton(self.frame_filterchannels)
        self.radioButton_lowPass.setObjectName(u"radioButton_lowPass")

        self.gridLayout_192.addWidget(self.radioButton_lowPass, 4, 0, 1, 1)

        self.pushButton_Filter = QPushButton(self.frame_filterchannels)
        self.pushButton_Filter.setObjectName(u"pushButton_Filter")

        self.gridLayout_192.addWidget(self.pushButton_Filter, 9, 1, 1, 1)

        self.groupBox_upperFreq = QGroupBox(self.frame_filterchannels)
        self.groupBox_upperFreq.setObjectName(u"groupBox_upperFreq")
        self.groupBox_upperFreq.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_191 = QGridLayout(self.groupBox_upperFreq)
        self.gridLayout_191.setObjectName(u"gridLayout_191")
        self.doubleSpinBox_upperFreq = QDoubleSpinBox(self.groupBox_upperFreq)
        self.doubleSpinBox_upperFreq.setObjectName(u"doubleSpinBox_upperFreq")
        self.doubleSpinBox_upperFreq.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_upperFreq.setMinimum(0.010000000000000)
        self.doubleSpinBox_upperFreq.setMaximum(100000000000000000.000000000000000)
        self.doubleSpinBox_upperFreq.setSingleStep(1.000000000000000)

        self.gridLayout_191.addWidget(self.doubleSpinBox_upperFreq, 0, 0, 1, 1)


        self.gridLayout_192.addWidget(self.groupBox_upperFreq, 7, 0, 1, 1)

        self.groupBox_52 = QGroupBox(self.frame_filterchannels)
        self.groupBox_52.setObjectName(u"groupBox_52")
        self.groupBox_52.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_190 = QGridLayout(self.groupBox_52)
        self.gridLayout_190.setObjectName(u"gridLayout_190")
        self.doubleSpinBox_lowerFreq = QDoubleSpinBox(self.groupBox_52)
        self.doubleSpinBox_lowerFreq.setObjectName(u"doubleSpinBox_lowerFreq")
        self.doubleSpinBox_lowerFreq.setMaximumSize(QSize(16777215, 30))
        self.doubleSpinBox_lowerFreq.setMinimum(0.010000000000000)
        self.doubleSpinBox_lowerFreq.setMaximum(100000000000000000.000000000000000)
        self.doubleSpinBox_lowerFreq.setSingleStep(1.000000000000000)

        self.gridLayout_190.addWidget(self.doubleSpinBox_lowerFreq, 0, 0, 1, 1)


        self.gridLayout_192.addWidget(self.groupBox_52, 6, 0, 1, 1)

        self.pushButton_detectFreq = QPushButton(self.frame_filterchannels)
        self.pushButton_detectFreq.setObjectName(u"pushButton_detectFreq")

        self.gridLayout_192.addWidget(self.pushButton_detectFreq, 6, 1, 1, 1)


        self.gridLayout_21.addWidget(self.frame_filterchannels, 0, 0, 1, 1)

        self.groupBox_ChangeanatRegion = QGroupBox(self.tab)
        self.groupBox_ChangeanatRegion.setObjectName(u"groupBox_ChangeanatRegion")
        self.gridLayout_25 = QGridLayout(self.groupBox_ChangeanatRegion)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.groupBox_2 = QGroupBox(self.groupBox_ChangeanatRegion)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_23 = QGridLayout(self.groupBox_2)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.comboBox_ChangeanatRegion = QComboBox(self.groupBox_2)
        self.comboBox_ChangeanatRegion.setObjectName(u"comboBox_ChangeanatRegion")
        self.comboBox_ChangeanatRegion.setEnabled(True)
        self.comboBox_ChangeanatRegion.setStyleSheet(u"")
        self.comboBox_ChangeanatRegion.setEditable(True)

        self.gridLayout_23.addWidget(self.comboBox_ChangeanatRegion, 0, 0, 1, 1)


        self.gridLayout_25.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.groupBox = QGroupBox(self.groupBox_ChangeanatRegion)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_26 = QGridLayout(self.groupBox)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.spinBox_ChangechannelID = QSpinBox(self.groupBox)
        self.spinBox_ChangechannelID.setObjectName(u"spinBox_ChangechannelID")
        self.spinBox_ChangechannelID.setReadOnly(True)
        self.spinBox_ChangechannelID.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_26.addWidget(self.spinBox_ChangechannelID, 0, 0, 1, 1)


        self.gridLayout_25.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox_ChangeanatRegion, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_samri = QWidget()
        self.tab_samri.setObjectName(u"tab_samri")
        self.gridLayout_90 = QGridLayout(self.tab_samri)
        self.gridLayout_90.setObjectName(u"gridLayout_90")
        self.lineEdit_4 = QLineEdit(self.tab_samri)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout_90.addWidget(self.lineEdit_4, 0, 0, 1, 2)

        self.frame_4 = QFrame(self.tab_samri)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_138 = QGridLayout(self.frame_4)
        self.gridLayout_138.setObjectName(u"gridLayout_138")
        self.lineEdit_8 = QLineEdit(self.frame_4)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setReadOnly(True)

        self.gridLayout_138.addWidget(self.lineEdit_8, 1, 0, 1, 1)

        self.pushButton_fetch = QPushButton(self.frame_4)
        self.pushButton_fetch.setObjectName(u"pushButton_fetch")

        self.gridLayout_138.addWidget(self.pushButton_fetch, 5, 0, 1, 1)

        self.lineEdit_server = QLineEdit(self.frame_4)
        self.lineEdit_server.setObjectName(u"lineEdit_server")

        self.gridLayout_138.addWidget(self.lineEdit_server, 1, 1, 1, 2)

        self.lineEdit_animalid = QLineEdit(self.frame_4)
        self.lineEdit_animalid.setObjectName(u"lineEdit_animalid")

        self.gridLayout_138.addWidget(self.lineEdit_animalid, 3, 1, 1, 2)

        self.lineEdit_9 = QLineEdit(self.frame_4)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setReadOnly(True)

        self.gridLayout_138.addWidget(self.lineEdit_9, 2, 0, 1, 1)

        self.lineEdit_rawBase = QLineEdit(self.frame_4)
        self.lineEdit_rawBase.setObjectName(u"lineEdit_rawBase")

        self.gridLayout_138.addWidget(self.lineEdit_rawBase, 0, 1, 1, 1)

        self.checkBox_bidsflag = QCheckBox(self.frame_4)
        self.checkBox_bidsflag.setObjectName(u"checkBox_bidsflag")
        self.checkBox_bidsflag.setChecked(True)

        self.gridLayout_138.addWidget(self.checkBox_bidsflag, 4, 0, 1, 2)

        self.lineEdit_password = QLineEdit(self.frame_4)
        self.lineEdit_password.setObjectName(u"lineEdit_password")

        self.gridLayout_138.addWidget(self.lineEdit_password, 2, 1, 1, 2)

        self.pushButton_browse = QPushButton(self.frame_4)
        self.pushButton_browse.setObjectName(u"pushButton_browse")

        self.gridLayout_138.addWidget(self.pushButton_browse, 0, 2, 1, 1)

        self.lineEdit_6 = QLineEdit(self.frame_4)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setReadOnly(True)

        self.gridLayout_138.addWidget(self.lineEdit_6, 0, 0, 1, 1)

        self.lineEdit_12 = QLineEdit(self.frame_4)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setReadOnly(True)

        self.gridLayout_138.addWidget(self.lineEdit_12, 3, 0, 1, 1)

        self.pushButton_re_fetch = QPushButton(self.frame_4)
        self.pushButton_re_fetch.setObjectName(u"pushButton_re_fetch")
        self.pushButton_re_fetch.setEnabled(False)

        self.gridLayout_138.addWidget(self.pushButton_re_fetch, 6, 0, 1, 1)

        self.pushButton_continue = QPushButton(self.frame_4)
        self.pushButton_continue.setObjectName(u"pushButton_continue")
        self.pushButton_continue.setEnabled(False)

        self.gridLayout_138.addWidget(self.pushButton_continue, 5, 1, 2, 2)


        self.gridLayout_90.addWidget(self.frame_4, 0, 2, 2, 1)

        self.frame_samri = QFrame(self.tab_samri)
        self.frame_samri.setObjectName(u"frame_samri")
        self.frame_samri.setEnabled(False)
        self.frame_samri.setFrameShape(QFrame.StyledPanel)
        self.frame_samri.setFrameShadow(QFrame.Raised)
        self.gridLayout_139 = QGridLayout(self.frame_samri)
        self.gridLayout_139.setObjectName(u"gridLayout_139")
        self.lineEdit_11 = QLineEdit(self.frame_samri)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_11, 12, 1, 1, 1)

        self.checkBox_atlasmask = QCheckBox(self.frame_samri)
        self.checkBox_atlasmask.setObjectName(u"checkBox_atlasmask")
        self.checkBox_atlasmask.setChecked(True)

        self.gridLayout_139.addWidget(self.checkBox_atlasmask, 4, 1, 1, 1)

        self.pushButton_browseAtlas = QPushButton(self.frame_samri)
        self.pushButton_browseAtlas.setObjectName(u"pushButton_browseAtlas")

        self.gridLayout_139.addWidget(self.pushButton_browseAtlas, 3, 3, 1, 1)

        self.lineEdit_10 = QLineEdit(self.frame_samri)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_10, 3, 1, 1, 1)

        self.comboBox_register_key = QComboBox(self.frame_samri)
        self.comboBox_register_key.setObjectName(u"comboBox_register_key")

        self.gridLayout_139.addWidget(self.comboBox_register_key, 7, 2, 1, 2)

        self.spinBox_num_threads = QSpinBox(self.frame_samri)
        self.spinBox_num_threads.setObjectName(u"spinBox_num_threads")

        self.gridLayout_139.addWidget(self.spinBox_num_threads, 8, 2, 1, 2)

        self.comboBox_tasks = QComboBox(self.frame_samri)
        self.comboBox_tasks.setObjectName(u"comboBox_tasks")

        self.gridLayout_139.addWidget(self.comboBox_tasks, 6, 2, 1, 2)

        self.lineEdit_15 = QLineEdit(self.frame_samri)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_15, 5, 1, 1, 1)

        self.lineEdit_atlas_path = QTextEdit(self.frame_samri)
        self.lineEdit_atlas_path.setObjectName(u"lineEdit_atlas_path")
        self.lineEdit_atlas_path.setMaximumSize(QSize(16777215, 70))

        self.gridLayout_139.addWidget(self.lineEdit_atlas_path, 3, 2, 1, 1)

        self.pushButton_browseBase = QPushButton(self.frame_samri)
        self.pushButton_browseBase.setObjectName(u"pushButton_browseBase")

        self.gridLayout_139.addWidget(self.pushButton_browseBase, 2, 3, 1, 1)

        self.checkBox_elastic = QCheckBox(self.frame_samri)
        self.checkBox_elastic.setObjectName(u"checkBox_elastic")
        self.checkBox_elastic.setChecked(True)

        self.gridLayout_139.addWidget(self.checkBox_elastic, 16, 1, 1, 1)

        self.frame_6 = QFrame(self.frame_samri)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_140 = QGridLayout(self.frame_6)
        self.gridLayout_140.setObjectName(u"gridLayout_140")
        self.pushButton_createMovMask = QPushButton(self.frame_6)
        self.pushButton_createMovMask.setObjectName(u"pushButton_createMovMask")

        self.gridLayout_140.addWidget(self.pushButton_createMovMask, 1, 0, 1, 1)

        self.pushButton_browseMov = QPushButton(self.frame_6)
        self.pushButton_browseMov.setObjectName(u"pushButton_browseMov")

        self.gridLayout_140.addWidget(self.pushButton_browseMov, 0, 0, 1, 1)


        self.gridLayout_139.addWidget(self.frame_6, 12, 3, 1, 1)

        self.lineEdit_movMask = QTextEdit(self.frame_samri)
        self.lineEdit_movMask.setObjectName(u"lineEdit_movMask")
        self.lineEdit_movMask.setMaximumSize(QSize(16777215, 100))
        self.lineEdit_movMask.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_movMask, 12, 2, 1, 1)

        self.pushButton_browseBru2 = QPushButton(self.frame_samri)
        self.pushButton_browseBru2.setObjectName(u"pushButton_browseBru2")

        self.gridLayout_139.addWidget(self.pushButton_browseBru2, 1, 3, 1, 1)

        self.lineEdit_animalID = QLineEdit(self.frame_samri)
        self.lineEdit_animalID.setObjectName(u"lineEdit_animalID")
        self.lineEdit_animalID.setStyleSheet(u"color: rgb(224, 27, 36);")
        self.lineEdit_animalID.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_animalID, 0, 1, 1, 3)

        self.lineEdit_5 = QLineEdit(self.frame_samri)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_5, 1, 1, 1, 1)

        self.lineEdit_7 = QLineEdit(self.frame_samri)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_7, 2, 1, 1, 1)

        self.checkBox_mov_mask = QCheckBox(self.frame_samri)
        self.checkBox_mov_mask.setObjectName(u"checkBox_mov_mask")
        self.checkBox_mov_mask.setChecked(True)

        self.gridLayout_139.addWidget(self.checkBox_mov_mask, 9, 1, 1, 1)

        self.lineEdit_16 = QLineEdit(self.frame_samri)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_16, 7, 1, 1, 1)

        self.lineEdit_base_path = QTextEdit(self.frame_samri)
        self.lineEdit_base_path.setObjectName(u"lineEdit_base_path")
        self.lineEdit_base_path.setMaximumSize(QSize(16777215, 70))

        self.gridLayout_139.addWidget(self.lineEdit_base_path, 2, 2, 1, 1)

        self.lineEdit_17 = QLineEdit(self.frame_samri)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_17, 6, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(self.frame_samri)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout_139.addWidget(self.buttonBox, 17, 3, 1, 1)

        self.lineEdit_bru2_path = QTextEdit(self.frame_samri)
        self.lineEdit_bru2_path.setObjectName(u"lineEdit_bru2_path")
        self.lineEdit_bru2_path.setMaximumSize(QSize(16777215, 70))

        self.gridLayout_139.addWidget(self.lineEdit_bru2_path, 1, 2, 1, 1)

        self.checkBox_presurgery = QCheckBox(self.frame_samri)
        self.checkBox_presurgery.setObjectName(u"checkBox_presurgery")

        self.gridLayout_139.addWidget(self.checkBox_presurgery, 15, 1, 1, 1)

        self.lineEdit_14 = QLineEdit(self.frame_samri)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_14, 8, 1, 1, 1)

        self.comboBox_working_session = QComboBox(self.frame_samri)
        self.comboBox_working_session.setObjectName(u"comboBox_working_session")

        self.gridLayout_139.addWidget(self.comboBox_working_session, 5, 2, 1, 2)

        self.checkBox_registration = QCheckBox(self.frame_samri)
        self.checkBox_registration.setObjectName(u"checkBox_registration")

        self.gridLayout_139.addWidget(self.checkBox_registration, 14, 1, 1, 1)

        self.checkBox_biascorrection = QCheckBox(self.frame_samri)
        self.checkBox_biascorrection.setObjectName(u"checkBox_biascorrection")

        self.gridLayout_139.addWidget(self.checkBox_biascorrection, 14, 2, 1, 1)


        self.gridLayout_90.addWidget(self.frame_samri, 2, 2, 1, 1)

        self.plainTextEdit_SAMRI = QPlainTextEdit(self.tab_samri)
        self.plainTextEdit_SAMRI.setObjectName(u"plainTextEdit_SAMRI")

        self.gridLayout_90.addWidget(self.plainTextEdit_SAMRI, 1, 0, 2, 2)

        self.gridLayout_90.setColumnStretch(0, 2)
        self.gridLayout_90.setColumnStretch(2, 1)
        self.tabWidget.addTab(self.tab_samri, "")

        self.gridLayout_79.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.tabWidget_visualisation.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_150 = QGridLayout(self.tab_3)
        self.gridLayout_150.setObjectName(u"gridLayout_150")
        self.textEdit_vis3D = QTextEdit(self.tab_3)
        self.textEdit_vis3D.setObjectName(u"textEdit_vis3D")
        self.textEdit_vis3D.setMaximumSize(QSize(16777215, 50))
        self.textEdit_vis3D.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_vis3D.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_vis3D.setReadOnly(True)

        self.gridLayout_150.addWidget(self.textEdit_vis3D, 0, 0, 1, 1)

        self.comboBox_mridTag_vis3D = QComboBox(self.tab_3)
        self.comboBox_mridTag_vis3D.setObjectName(u"comboBox_mridTag_vis3D")
        self.comboBox_mridTag_vis3D.setMinimumSize(QSize(0, 50))

        self.gridLayout_150.addWidget(self.comboBox_mridTag_vis3D, 0, 1, 1, 1)

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
        self.pushButton_slicey_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicey_vis3D.setObjectName(u"pushButton_slicey_vis3D")
        self.pushButton_slicey_vis3D.setIcon(icon19)
        self.pushButton_slicey_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_slicey_vis3D, 2, 5, 1, 1)

        self.resetCamera_vis3D = QPushButton(self.frame_33)
        self.resetCamera_vis3D.setObjectName(u"resetCamera_vis3D")
        self.resetCamera_vis3D.setEnabled(True)
        self.resetCamera_vis3D.setStyleSheet(u"")
        self.resetCamera_vis3D.setIcon(icon17)
        self.resetCamera_vis3D.setIconSize(QSize(40, 40))
        self.resetCamera_vis3D.setAutoDefault(False)
        self.resetCamera_vis3D.setFlat(False)

        self.gridLayout_147.addWidget(self.resetCamera_vis3D, 1, 0, 2, 2)

        self.pushButton_slicex_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicex_vis3D.setObjectName(u"pushButton_slicex_vis3D")
        self.pushButton_slicex_vis3D.setIcon(icon21)
        self.pushButton_slicex_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_slicex_vis3D, 2, 4, 1, 1)

        self.change_perspective_vis3D = QPushButton(self.frame_33)
        self.change_perspective_vis3D.setObjectName(u"change_perspective_vis3D")
        self.change_perspective_vis3D.setStyleSheet(u"")
        self.change_perspective_vis3D.setIcon(icon18)
        self.change_perspective_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.change_perspective_vis3D, 2, 2, 1, 1)

        self.pushButton_slicez_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicez_vis3D.setObjectName(u"pushButton_slicez_vis3D")
        self.pushButton_slicez_vis3D.setIcon(icon22)
        self.pushButton_slicez_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_slicez_vis3D, 2, 6, 1, 1)

        self.vtkWidget_vis3D = QVTKRenderWindowInteractor(self.frame_33)
        self.vtkWidget_vis3D.setObjectName(u"vtkWidget_vis3D")
        self.vtkWidget_vis3D.setEnabled(True)
        self.vtkWidget_vis3D.setMinimumSize(QSize(500, 0))
        self.vtkWidget_vis3D.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_147.addWidget(self.vtkWidget_vis3D, 0, 0, 1, 7)

        self.pushButton_Noslicing_vis3D = QPushButton(self.frame_33)
        self.pushButton_Noslicing_vis3D.setObjectName(u"pushButton_Noslicing_vis3D")
        self.pushButton_Noslicing_vis3D.setIcon(icon20)
        self.pushButton_Noslicing_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_147.addWidget(self.pushButton_Noslicing_vis3D, 2, 3, 1, 1)


        self.gridLayout_150.addWidget(self.frame_33, 1, 0, 1, 2)

        self.groupBox_anatRegion_3 = QGroupBox(self.tab_3)
        self.groupBox_anatRegion_3.setObjectName(u"groupBox_anatRegion_3")
        self.gridLayout_149 = QGridLayout(self.groupBox_anatRegion_3)
        self.gridLayout_149.setObjectName(u"gridLayout_149")
        self.comboBox_anatRegion_vis3D = QComboBox(self.groupBox_anatRegion_3)
        self.comboBox_anatRegion_vis3D.setObjectName(u"comboBox_anatRegion_vis3D")
        self.comboBox_anatRegion_vis3D.setEnabled(False)
        self.comboBox_anatRegion_vis3D.setMinimumSize(QSize(0, 40))
        self.comboBox_anatRegion_vis3D.setStyleSheet(u"")

        self.gridLayout_149.addWidget(self.comboBox_anatRegion_vis3D, 0, 2, 1, 1)

        self.spinBox_channelID_vis3D = QSpinBox(self.groupBox_anatRegion_3)
        self.spinBox_channelID_vis3D.setObjectName(u"spinBox_channelID_vis3D")
        self.spinBox_channelID_vis3D.setMinimumSize(QSize(0, 40))
        self.spinBox_channelID_vis3D.setReadOnly(False)
        self.spinBox_channelID_vis3D.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout_149.addWidget(self.spinBox_channelID_vis3D, 0, 1, 1, 1)


        self.gridLayout_150.addWidget(self.groupBox_anatRegion_3, 2, 0, 1, 2)

        self.groupBox_69 = QGroupBox(self.tab_3)
        self.groupBox_69.setObjectName(u"groupBox_69")
        self.groupBox_69.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_143 = QGridLayout(self.groupBox_69)
        self.gridLayout_143.setObjectName(u"gridLayout_143")
        self.spinBox_y_vis3D = QSpinBox(self.groupBox_69)
        self.spinBox_y_vis3D.setObjectName(u"spinBox_y_vis3D")
        self.spinBox_y_vis3D.setMaximumSize(QSize(16777215, 30))
        self.spinBox_y_vis3D.setReadOnly(True)
        self.spinBox_y_vis3D.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_y_vis3D.setMinimum(1)
        self.spinBox_y_vis3D.setMaximum(1000)

        self.gridLayout_143.addWidget(self.spinBox_y_vis3D, 0, 2, 1, 1)

        self.spinBox_z_vis3D = QSpinBox(self.groupBox_69)
        self.spinBox_z_vis3D.setObjectName(u"spinBox_z_vis3D")
        self.spinBox_z_vis3D.setMaximumSize(QSize(16777215, 30))
        self.spinBox_z_vis3D.setReadOnly(True)
        self.spinBox_z_vis3D.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_z_vis3D.setMinimum(1)
        self.spinBox_z_vis3D.setMaximum(1000)

        self.gridLayout_143.addWidget(self.spinBox_z_vis3D, 0, 3, 1, 1)

        self.spinBox_x_vis3D = QSpinBox(self.groupBox_69)
        self.spinBox_x_vis3D.setObjectName(u"spinBox_x_vis3D")
        self.spinBox_x_vis3D.setMaximumSize(QSize(16777215, 30))
        self.spinBox_x_vis3D.setReadOnly(True)
        self.spinBox_x_vis3D.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_x_vis3D.setMinimum(1)
        self.spinBox_x_vis3D.setMaximum(1000)

        self.gridLayout_143.addWidget(self.spinBox_x_vis3D, 0, 1, 1, 1)


        self.gridLayout_150.addWidget(self.groupBox_69, 4, 0, 1, 2)

        self.tableWidget_vis3D = QTableWidget(self.tab_3)
        self.tableWidget_vis3D.setObjectName(u"tableWidget_vis3D")
        self.tableWidget_vis3D.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_vis3D.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_vis3D.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_vis3D.horizontalHeader().setCascadingSectionResizes(False)

        self.gridLayout_150.addWidget(self.tableWidget_vis3D, 0, 2, 5, 1)

        self.gridLayout_150.setColumnStretch(0, 2)
        self.gridLayout_150.setColumnStretch(1, 1)
        self.gridLayout_150.setColumnStretch(2, 2)
        self.tabWidget_visualisation.addTab(self.tab_3, "")

        self.gridLayout_34.addWidget(self.tabWidget_visualisation, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 2184, 23))
        self.menuGUI = QMenu(self.menubar)
        self.menuGUI.setObjectName(u"menuGUI")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menu4D_Tools = QMenu(self.menubar)
        self.menu4D_Tools.setObjectName(u"menu4D_Tools")
        self.menuElectrode_Localization = QMenu(self.menu4D_Tools)
        self.menuElectrode_Localization.setObjectName(u"menuElectrode_Localization")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_ephys = QDockWidget(MainWindow)
        self.dockWidget_ephys.setObjectName(u"dockWidget_ephys")
        self.dockWidget_ephys.setMinimumSize(QSize(663, 750))
        self.Dock_ephys = QWidget()
        self.Dock_ephys.setObjectName(u"Dock_ephys")
        self.Dock_ephys.setMinimumSize(QSize(650, 0))
        self.gridLayout_69 = QGridLayout(self.Dock_ephys)
        self.gridLayout_69.setObjectName(u"gridLayout_69")
        self.pushButton_zoomOut = QPushButton(self.Dock_ephys)
        self.pushButton_zoomOut.setObjectName(u"pushButton_zoomOut")
        self.pushButton_zoomOut.setEnabled(True)
        self.pushButton_zoomOut.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon24 = QIcon()
        icon24.addFile(u"Icons/ephys/zoom-out.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_zoomOut.setIcon(icon24)
        self.pushButton_zoomOut.setIconSize(QSize(40, 40))
        self.pushButton_zoomOut.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_zoomOut, 1, 4, 1, 1)

        self.pushButton_selectTime = QPushButton(self.Dock_ephys)
        self.pushButton_selectTime.setObjectName(u"pushButton_selectTime")
        self.pushButton_selectTime.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon25 = QIcon()
        icon25.addFile(u"Icons/ephys/select_time.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_selectTime.setIcon(icon25)
        self.pushButton_selectTime.setIconSize(QSize(40, 40))
        self.pushButton_selectTime.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_selectTime, 1, 5, 1, 1)

        self.pushButton_zoomReset = QPushButton(self.Dock_ephys)
        self.pushButton_zoomReset.setObjectName(u"pushButton_zoomReset")
        self.pushButton_zoomReset.setEnabled(True)
        self.pushButton_zoomReset.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon26 = QIcon()
        icon26.addFile(u"Icons/ephys/zoom-in (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_zoomReset.setIcon(icon26)
        self.pushButton_zoomReset.setIconSize(QSize(40, 40))
        self.pushButton_zoomReset.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_zoomReset, 1, 0, 1, 1)

        self.horizontalSlider_ephys = QSlider(self.Dock_ephys)
        self.horizontalSlider_ephys.setObjectName(u"horizontalSlider_ephys")
        self.horizontalSlider_ephys.setSingleStep(100)
        self.horizontalSlider_ephys.setPageStep(1000)
        self.horizontalSlider_ephys.setOrientation(Qt.Horizontal)

        self.gridLayout_69.addWidget(self.horizontalSlider_ephys, 2, 0, 1, 7)

        self.pushButtonAmp_minus = QPushButton(self.Dock_ephys)
        self.pushButtonAmp_minus.setObjectName(u"pushButtonAmp_minus")
        self.pushButtonAmp_minus.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon27 = QIcon()
        icon27.addFile(u"Icons/ephys/amplitude_minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonAmp_minus.setIcon(icon27)
        self.pushButtonAmp_minus.setIconSize(QSize(40, 40))
        self.pushButtonAmp_minus.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButtonAmp_minus, 1, 3, 1, 1)

        self.pushButton_timeline = QPushButton(self.Dock_ephys)
        self.pushButton_timeline.setObjectName(u"pushButton_timeline")
        self.pushButton_timeline.setEnabled(True)
        self.pushButton_timeline.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon28 = QIcon()
        icon28.addFile(u"Icons/ephys/select_timeline.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_timeline.setIcon(icon28)
        self.pushButton_timeline.setIconSize(QSize(40, 40))
        self.pushButton_timeline.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_timeline, 1, 2, 1, 1)

        self.pushButtonAmp_plus = QPushButton(self.Dock_ephys)
        self.pushButtonAmp_plus.setObjectName(u"pushButtonAmp_plus")
        self.pushButtonAmp_plus.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon29 = QIcon()
        icon29.addFile(u"Icons/ephys/amplitude_plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonAmp_plus.setIcon(icon29)
        self.pushButtonAmp_plus.setIconSize(QSize(40, 40))
        self.pushButtonAmp_plus.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButtonAmp_plus, 1, 1, 1, 1)

        self.pushButton_measurement = QPushButton(self.Dock_ephys)
        self.pushButton_measurement.setObjectName(u"pushButton_measurement")
        self.pushButton_measurement.setEnabled(True)
        self.pushButton_measurement.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon30 = QIcon()
        icon30.addFile(u"Icons/mri/measure.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_measurement.setIcon(icon30)
        self.pushButton_measurement.setIconSize(QSize(40, 40))
        self.pushButton_measurement.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_measurement, 1, 6, 1, 1)

        self.groupBox_3 = QGroupBox(self.Dock_ephys)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.groupBox_3.setFlat(False)
        self.gridLayout_76 = QGridLayout(self.groupBox_3)
        self.gridLayout_76.setObjectName(u"gridLayout_76")
        self.spinBox_startMs = QSpinBox(self.groupBox_3)
        self.spinBox_startMs.setObjectName(u"spinBox_startMs")
        self.spinBox_startMs.setMaximum(1000)

        self.gridLayout_76.addWidget(self.spinBox_startMs, 0, 4, 1, 1)

        self.spinBox_startS = QSpinBox(self.groupBox_3)
        self.spinBox_startS.setObjectName(u"spinBox_startS")
        self.spinBox_startS.setMaximum(60)

        self.gridLayout_76.addWidget(self.spinBox_startS, 0, 3, 1, 1)

        self.lineEdit_2 = QLineEdit(self.groupBox_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_76.addWidget(self.lineEdit_2, 0, 5, 1, 1)

        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_76.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.spinBox_startMin = QSpinBox(self.groupBox_3)
        self.spinBox_startMin.setObjectName(u"spinBox_startMin")

        self.gridLayout_76.addWidget(self.spinBox_startMin, 0, 2, 1, 1)

        self.spinBox_duration = QSpinBox(self.groupBox_3)
        self.spinBox_duration.setObjectName(u"spinBox_duration")
        self.spinBox_duration.setMaximum(1000000)

        self.gridLayout_76.addWidget(self.spinBox_duration, 0, 6, 1, 1)


        self.gridLayout_69.addWidget(self.groupBox_3, 3, 0, 1, 7)

        self.widget_pgEphys = PgWidget(self.Dock_ephys)
        self.widget_pgEphys.setObjectName(u"widget_pgEphys")

        self.gridLayout_69.addWidget(self.widget_pgEphys, 0, 0, 1, 7)

        self.dockWidget_ephys.setWidget(self.Dock_ephys)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidget_ephys)
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
        QWidget.setTabOrder(self.spinBox_atlas_lambda_z, self.spinBox_tp_insert_x)
        QWidget.setTabOrder(self.spinBox_tp_insert_x, self.spinBox_tp_insert_y)
        QWidget.setTabOrder(self.spinBox_tp_insert_y, self.spinBox_tp_insert_z)
        QWidget.setTabOrder(self.spinBox_tp_insert_z, self.spinBox_tp_deep_x)
        QWidget.setTabOrder(self.spinBox_tp_deep_x, self.spinBox_tp_deep_y)
        QWidget.setTabOrder(self.spinBox_tp_deep_y, self.spinBox_tp_deep_z)
        QWidget.setTabOrder(self.spinBox_tp_deep_z, self.spinBox_x_data1)
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
        QWidget.setTabOrder(self.vtkWidget_legend1, self.file_name_displayed_4d)
        QWidget.setTabOrder(self.file_name_displayed_4d, self.go_left_data12)
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
        QWidget.setTabOrder(self.vtkWidget_legend2, self.pushButton_metadata)
        QWidget.setTabOrder(self.pushButton_metadata, self.tabWidget_time0)
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
        QWidget.setTabOrder(self.pushButton_reset_data02, self.pushButton_auto_data02)
        QWidget.setTabOrder(self.pushButton_auto_data02, self.vtkWidget_data03)
        QWidget.setTabOrder(self.vtkWidget_data03, self.fit_to_zoom_data00)
        QWidget.setTabOrder(self.fit_to_zoom_data00, self.vtkWidget_data00)
        QWidget.setTabOrder(self.vtkWidget_data00, self.go_down_data00)
        QWidget.setTabOrder(self.go_down_data00, self.go_up_data00)
        QWidget.setTabOrder(self.go_up_data00, self.go_left_data00)
        QWidget.setTabOrder(self.go_left_data00, self.go_right_data00)
        QWidget.setTabOrder(self.go_right_data00, self.zoom_in_data00)
        QWidget.setTabOrder(self.zoom_in_data00, self.zoom_out_data00)
        QWidget.setTabOrder(self.zoom_out_data00, self.zoom_in_data01)
        QWidget.setTabOrder(self.zoom_in_data01, self.zoom_out_data01)
        QWidget.setTabOrder(self.zoom_out_data01, self.fit_to_zoom_data01)
        QWidget.setTabOrder(self.fit_to_zoom_data01, self.go_down_data01)
        QWidget.setTabOrder(self.go_down_data01, self.go_up_data01)
        QWidget.setTabOrder(self.go_up_data01, self.go_left_data01)
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
        QWidget.setTabOrder(self.vtkWidget_legend0, self.lineEdit_31)
        QWidget.setTabOrder(self.lineEdit_31, self.lineEdit_43)
        QWidget.setTabOrder(self.lineEdit_43, self.lineEdit_33)
        QWidget.setTabOrder(self.lineEdit_33, self.doubleSpinBox_distanceAtlas)
        QWidget.setTabOrder(self.doubleSpinBox_distanceAtlas, self.doubleSpinBox_tp_ratio)
        QWidget.setTabOrder(self.doubleSpinBox_tp_ratio, self.doubleSpinBox_distance)
        QWidget.setTabOrder(self.doubleSpinBox_distance, self.pushButton_redAreas)
        QWidget.setTabOrder(self.pushButton_redAreas, self.textEdit_2)
        QWidget.setTabOrder(self.textEdit_2, self.doubleSpinBox_d_bregmaz)
        QWidget.setTabOrder(self.doubleSpinBox_d_bregmaz, self.pushButton_tp_bregma)
        QWidget.setTabOrder(self.pushButton_tp_bregma, self.zoom_in_data10)
        QWidget.setTabOrder(self.zoom_in_data10, self.lineEdit_24)
        QWidget.setTabOrder(self.lineEdit_24, self.lineEdit_19)
        QWidget.setTabOrder(self.lineEdit_19, self.zoom_out_data10)
        QWidget.setTabOrder(self.zoom_out_data10, self.lineEdit_29)
        QWidget.setTabOrder(self.lineEdit_29, self.doubleSpinBox_d_bregmax)
        QWidget.setTabOrder(self.doubleSpinBox_d_bregmax, self.doubleSpinBox_d_bregmay)
        QWidget.setTabOrder(self.doubleSpinBox_d_bregmay, self.go_down_data10)
        QWidget.setTabOrder(self.go_down_data10, self.tableWidget_barcode)
        QWidget.setTabOrder(self.tableWidget_barcode, self.vtkWidget_data10)
        QWidget.setTabOrder(self.vtkWidget_data10, self.fit_to_zoom_data10)
        QWidget.setTabOrder(self.fit_to_zoom_data10, self.pushButton_tp_next0)
        QWidget.setTabOrder(self.pushButton_tp_next0, self.lineEdit_20)
        QWidget.setTabOrder(self.lineEdit_20, self.pushButton_tp_lambda)
        QWidget.setTabOrder(self.pushButton_tp_lambda, self.go_left_data10)
        QWidget.setTabOrder(self.go_left_data10, self.lineEdit_58)
        QWidget.setTabOrder(self.lineEdit_58, self.vtkWidget_data11)
        QWidget.setTabOrder(self.vtkWidget_data11, self.go_right_data10)
        QWidget.setTabOrder(self.go_right_data10, self.doubleSpinBox_d_lambdaz)
        QWidget.setTabOrder(self.doubleSpinBox_d_lambdaz, self.go_up_data10)
        QWidget.setTabOrder(self.go_up_data10, self.doubleSpinBox_d_lambdax)
        QWidget.setTabOrder(self.doubleSpinBox_d_lambdax, self.lineEdit_30)
        QWidget.setTabOrder(self.lineEdit_30, self.doubleSpinBox_d_lambday)
        QWidget.setTabOrder(self.doubleSpinBox_d_lambday, self.go_down_data11)
        QWidget.setTabOrder(self.go_down_data11, self.fit_to_zoom_data11)
        QWidget.setTabOrder(self.fit_to_zoom_data11, self.textEdit_distance_shank)
        QWidget.setTabOrder(self.textEdit_distance_shank, self.go_up_data11)
        QWidget.setTabOrder(self.go_up_data11, self.go_left_data11)
        QWidget.setTabOrder(self.go_left_data11, self.go_right_data11)
        QWidget.setTabOrder(self.go_right_data11, self.pushButton_PyLdetection)
        QWidget.setTabOrder(self.pushButton_PyLdetection, self.zoom_in_data11)
        QWidget.setTabOrder(self.zoom_in_data11, self.zoom_out_data11)
        QWidget.setTabOrder(self.zoom_out_data11, self.fit_to_zoom_data12)
        QWidget.setTabOrder(self.fit_to_zoom_data12, self.doubleSpinBox_distance_shank)
        QWidget.setTabOrder(self.doubleSpinBox_distance_shank, self.checkBox_brain_region)
        QWidget.setTabOrder(self.checkBox_brain_region, self.pushButton_tp_deep)
        QWidget.setTabOrder(self.pushButton_tp_deep, self.lineEdit_21)
        QWidget.setTabOrder(self.lineEdit_21, self.lineEdit_22)
        QWidget.setTabOrder(self.lineEdit_22, self.spinBox_tp_channels)
        QWidget.setTabOrder(self.spinBox_tp_channels, self.spinBox_tp_separation)
        QWidget.setTabOrder(self.spinBox_tp_separation, self.tableWidget_shank_info)
        QWidget.setTabOrder(self.tableWidget_shank_info, self.pushButton_edgemask)
        QWidget.setTabOrder(self.pushButton_edgemask, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.pushButton_tp_insert)
        QWidget.setTabOrder(self.pushButton_tp_insert, self.pushButton_addShank)
        QWidget.setTabOrder(self.pushButton_addShank, self.lineEdit_vis3D)
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
        QWidget.setTabOrder(self.comboBox_Contrastimage, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.tabWidget_visualisation)
        QWidget.setTabOrder(self.tabWidget_visualisation, self.comboBox_mridBarcodes)
        QWidget.setTabOrder(self.comboBox_mridBarcodes, self.tableintensity_data3d)
        QWidget.setTabOrder(self.tableintensity_data3d, self.checkBox_measurement)
        QWidget.setTabOrder(self.checkBox_measurement, self.comboBox_measurementColors)
        QWidget.setTabOrder(self.comboBox_measurementColors, self.pushButton_deleteMeasurement)
        QWidget.setTabOrder(self.pushButton_deleteMeasurement, self.tableWidget_meaurement)
        QWidget.setTabOrder(self.tableWidget_meaurement, self.tabWidget_4)
        QWidget.setTabOrder(self.tabWidget_4, self.display_level_data3d0)
        QWidget.setTabOrder(self.display_level_data3d0, self.display_window_data3d0)
        QWidget.setTabOrder(self.display_window_data3d0, self.changeContrast_data3d0)
        QWidget.setTabOrder(self.changeContrast_data3d0, self.changeBrightness_data3d0)
        QWidget.setTabOrder(self.changeBrightness_data3d0, self.display_level_data3d1)
        QWidget.setTabOrder(self.display_level_data3d1, self.changeContrast_data3d1)
        QWidget.setTabOrder(self.changeContrast_data3d1, self.display_window_data3d1)
        QWidget.setTabOrder(self.display_window_data3d1, self.changeBrightness_data3d1)
        QWidget.setTabOrder(self.changeBrightness_data3d1, self.display_window_data3d2)
        QWidget.setTabOrder(self.display_window_data3d2, self.changeBrightness_data3d2)
        QWidget.setTabOrder(self.changeBrightness_data3d2, self.display_level_data3d2)
        QWidget.setTabOrder(self.display_level_data3d2, self.changeContrast_data3d2)
        QWidget.setTabOrder(self.changeContrast_data3d2, self.tabWidget_3)
        QWidget.setTabOrder(self.tabWidget_3, self.changeBrightness_data00)
        QWidget.setTabOrder(self.changeBrightness_data00, self.display_level_data00)
        QWidget.setTabOrder(self.display_level_data00, self.display_window_data00)
        QWidget.setTabOrder(self.display_window_data00, self.changeContrast_data00)
        QWidget.setTabOrder(self.changeContrast_data00, self.display_window_data01)
        QWidget.setTabOrder(self.display_window_data01, self.changeContrast_data01)
        QWidget.setTabOrder(self.changeContrast_data01, self.display_level_data01)
        QWidget.setTabOrder(self.display_level_data01, self.changeBrightness_data01)
        QWidget.setTabOrder(self.changeBrightness_data01, self.display_window_data02)
        QWidget.setTabOrder(self.display_window_data02, self.changeContrast_data02)
        QWidget.setTabOrder(self.changeContrast_data02, self.display_level_data02)
        QWidget.setTabOrder(self.display_level_data02, self.changeBrightness_data02)
        QWidget.setTabOrder(self.changeBrightness_data02, self.tabWidget_5)
        QWidget.setTabOrder(self.tabWidget_5, self.changeBrightness_data10)
        QWidget.setTabOrder(self.changeBrightness_data10, self.display_level_data10)
        QWidget.setTabOrder(self.display_level_data10, self.display_window_data10)
        QWidget.setTabOrder(self.display_window_data10, self.changeContrast_data10)
        QWidget.setTabOrder(self.changeContrast_data10, self.display_window_data11)
        QWidget.setTabOrder(self.display_window_data11, self.changeContrast_data11)
        QWidget.setTabOrder(self.changeContrast_data11, self.display_level_data11)
        QWidget.setTabOrder(self.display_level_data11, self.changeBrightness_data11)
        QWidget.setTabOrder(self.changeBrightness_data11, self.display_window_data12)
        QWidget.setTabOrder(self.display_window_data12, self.changeContrast_data12)
        QWidget.setTabOrder(self.changeContrast_data12, self.display_level_data12)
        QWidget.setTabOrder(self.display_level_data12, self.changeBrightness_data12)
        QWidget.setTabOrder(self.changeBrightness_data12, self.tabWidget_6)
        QWidget.setTabOrder(self.tabWidget_6, self.changeBrightness_data20)
        QWidget.setTabOrder(self.changeBrightness_data20, self.display_level_data20)
        QWidget.setTabOrder(self.display_level_data20, self.display_window_data20)
        QWidget.setTabOrder(self.display_window_data20, self.changeContrast_data20)
        QWidget.setTabOrder(self.changeContrast_data20, self.display_window_data21)
        QWidget.setTabOrder(self.display_window_data21, self.changeContrast_data21)
        QWidget.setTabOrder(self.changeContrast_data21, self.display_level_data21)
        QWidget.setTabOrder(self.display_level_data21, self.changeBrightness_data21)
        QWidget.setTabOrder(self.changeBrightness_data21, self.display_window_data22)
        QWidget.setTabOrder(self.display_window_data22, self.changeContrast_data22)
        QWidget.setTabOrder(self.changeContrast_data22, self.display_level_data22)
        QWidget.setTabOrder(self.display_level_data22, self.changeBrightness_data22)
        QWidget.setTabOrder(self.changeBrightness_data22, self.comboBox_finest)
        QWidget.setTabOrder(self.comboBox_finest, self.textEdit_6)
        QWidget.setTabOrder(self.textEdit_6, self.comboBox_movingimg)
        QWidget.setTabOrder(self.comboBox_movingimg, self.textEdit_pixels)
        QWidget.setTabOrder(self.textEdit_pixels, self.pushButton_registration)
        QWidget.setTabOrder(self.pushButton_registration, self.pushButton_regCancel)
        QWidget.setTabOrder(self.pushButton_regCancel, self.comboBox_coarest)
        QWidget.setTabOrder(self.comboBox_coarest, self.textBrowser_5)
        QWidget.setTabOrder(self.textBrowser_5, self.checkBox_threshold)
        QWidget.setTabOrder(self.checkBox_threshold, self.radioButton_bounded)
        QWidget.setTabOrder(self.radioButton_bounded, self.radioButton_lower)
        QWidget.setTabOrder(self.radioButton_lower, self.radioButton_upper)
        QWidget.setTabOrder(self.radioButton_upper, self.ScrollBar_lower)
        QWidget.setTabOrder(self.ScrollBar_lower, self.doubleSpinBox_lower)
        QWidget.setTabOrder(self.doubleSpinBox_lower, self.ScrollBar_upper)
        QWidget.setTabOrder(self.ScrollBar_upper, self.doubleSpinBox_upper)
        QWidget.setTabOrder(self.doubleSpinBox_upper, self.pushButton_Back1)
        QWidget.setTabOrder(self.pushButton_Back1, self.pushButton_Next1)
        QWidget.setTabOrder(self.pushButton_Next1, self.textBrowser_6)
        QWidget.setTabOrder(self.textBrowser_6, self.doubleSpinBox_Bubradius)
        QWidget.setTabOrder(self.doubleSpinBox_Bubradius, self.horizontalSlider_Bubradius)
        QWidget.setTabOrder(self.horizontalSlider_Bubradius, self.pushButton_Back2)
        QWidget.setTabOrder(self.pushButton_Back2, self.pushButton_Next2)
        QWidget.setTabOrder(self.pushButton_Next2, self.pushButton_addBubbles)
        QWidget.setTabOrder(self.pushButton_addBubbles, self.tableView_activeBub)
        QWidget.setTabOrder(self.tableView_activeBub, self.pushButton_delete)
        QWidget.setTabOrder(self.pushButton_delete, self.doubleSpinBox_SegStep)
        QWidget.setTabOrder(self.doubleSpinBox_SegStep, self.toolButton_forwardEvo)
        QWidget.setTabOrder(self.toolButton_forwardEvo, self.toolButton_runEvo)
        QWidget.setTabOrder(self.toolButton_runEvo, self.toolButton_backwardEvo)
        QWidget.setTabOrder(self.toolButton_backwardEvo, self.textBrowser_7)
        QWidget.setTabOrder(self.textBrowser_7, self.doubleSpinBox_Segiter)
        QWidget.setTabOrder(self.doubleSpinBox_Segiter, self.pushButton_Finish)
        QWidget.setTabOrder(self.pushButton_Finish, self.pushButton_Back3)
        QWidget.setTabOrder(self.pushButton_Back3, self.textEdit_SAMRI_reg)
        QWidget.setTabOrder(self.textEdit_SAMRI_reg, self.doubleSpinBox_labelOcc3d)
        QWidget.setTabOrder(self.doubleSpinBox_labelOcc3d, self.sizeSlider_labelOcc3d)
        QWidget.setTabOrder(self.sizeSlider_labelOcc3d, self.comboBox_paintOver)
        QWidget.setTabOrder(self.comboBox_paintOver, self.tableWidget_labels3D)
        QWidget.setTabOrder(self.tableWidget_labels3D, self.brush_size3d)
        QWidget.setTabOrder(self.brush_size3d, self.brush_sizeSlider3d)
        QWidget.setTabOrder(self.brush_sizeSlider3d, self.checkBox_Brush)
        QWidget.setTabOrder(self.checkBox_Brush, self.paint_square)
        QWidget.setTabOrder(self.paint_square, self.paint_round)
        QWidget.setTabOrder(self.paint_round, self.pushButton_paint_done)
        QWidget.setTabOrder(self.pushButton_paint_done, self.pushButton_resample100um)
        QWidget.setTabOrder(self.pushButton_resample100um, self.pushButton_openfile100um)
        QWidget.setTabOrder(self.pushButton_openfile100um, self.pushButton_done)
        QWidget.setTabOrder(self.pushButton_done, self.pushButton_resample25um)
        QWidget.setTabOrder(self.pushButton_resample25um, self.comboBox_resamplefiles)
        QWidget.setTabOrder(self.comboBox_resamplefiles, self.textBrowser_4)
        QWidget.setTabOrder(self.textBrowser_4, self.textEdit_resample25)
        QWidget.setTabOrder(self.textEdit_resample25, self.textEdit_resample100)
        QWidget.setTabOrder(self.textEdit_resample100, self.pushButton_anatOK)
        QWidget.setTabOrder(self.pushButton_anatOK, self.plainTextEdit_MRID_2)
        QWidget.setTabOrder(self.plainTextEdit_MRID_2, self.pushButton_segOK)
        QWidget.setTabOrder(self.pushButton_segOK, self.plainTextEdit_MRID_4)
        QWidget.setTabOrder(self.plainTextEdit_MRID_4, self.checkBox_Brush_MRID)
        QWidget.setTabOrder(self.checkBox_Brush_MRID, self.paint_square_Post)
        QWidget.setTabOrder(self.paint_square_Post, self.paint_round_Post)
        QWidget.setTabOrder(self.paint_round_Post, self.sizeSlider_labelOcc)
        QWidget.setTabOrder(self.sizeSlider_labelOcc, self.doubleSpinBox_labelOcc)
        QWidget.setTabOrder(self.doubleSpinBox_labelOcc, self.brush_size4d)
        QWidget.setTabOrder(self.brush_size4d, self.brush_sizeSlider4d)
        QWidget.setTabOrder(self.brush_sizeSlider4d, self.comboBox_paintOver_Post)
        QWidget.setTabOrder(self.comboBox_paintOver_Post, self.tableWidget_labels)
        QWidget.setTabOrder(self.tableWidget_labels, self.histogram_label)
        QWidget.setTabOrder(self.histogram_label, self.paintbrush_dataview)
        QWidget.setTabOrder(self.paintbrush_dataview, self.lineEdit_52)
        QWidget.setTabOrder(self.lineEdit_52, self.doubleSpinBox_fovy)
        QWidget.setTabOrder(self.doubleSpinBox_fovy, self.lineEdit_56)
        QWidget.setTabOrder(self.lineEdit_56, self.doubleSpinBox_spay)
        QWidget.setTabOrder(self.doubleSpinBox_spay, self.spinBox_dimey)
        QWidget.setTabOrder(self.spinBox_dimey, self.pushButton_SaveSpacing)
        QWidget.setTabOrder(self.pushButton_SaveSpacing, self.lineEdit_55)
        QWidget.setTabOrder(self.lineEdit_55, self.spinBox_dimez)
        QWidget.setTabOrder(self.spinBox_dimez, self.lineEdit_50)
        QWidget.setTabOrder(self.lineEdit_50, self.lineEdit_47)
        QWidget.setTabOrder(self.lineEdit_47, self.lineEdit_54)
        QWidget.setTabOrder(self.lineEdit_54, self.lineEdit_53)
        QWidget.setTabOrder(self.lineEdit_53, self.lineEdit_48)
        QWidget.setTabOrder(self.lineEdit_48, self.lineEdit_51)
        QWidget.setTabOrder(self.lineEdit_51, self.lineEdit_46)
        QWidget.setTabOrder(self.lineEdit_46, self.doubleSpinBox_fovz)
        QWidget.setTabOrder(self.doubleSpinBox_fovz, self.doubleSpinBox_spax)
        QWidget.setTabOrder(self.doubleSpinBox_spax, self.spinBox_dimex)
        QWidget.setTabOrder(self.spinBox_dimex, self.pushButton_cancel_spacing)
        QWidget.setTabOrder(self.pushButton_cancel_spacing, self.doubleSpinBox_fovx)
        QWidget.setTabOrder(self.doubleSpinBox_fovx, self.lineEdit_49)
        QWidget.setTabOrder(self.lineEdit_49, self.lineEdit_57)
        QWidget.setTabOrder(self.lineEdit_57, self.doubleSpinBox_spaz)
        QWidget.setTabOrder(self.doubleSpinBox_spaz, self.lineEdit_38)
        QWidget.setTabOrder(self.lineEdit_38, self.pushButton_cancel_metadata)
        QWidget.setTabOrder(self.pushButton_cancel_metadata, self.doubleSpinBox_originx)
        QWidget.setTabOrder(self.doubleSpinBox_originx, self.lineEdit_40)
        QWidget.setTabOrder(self.lineEdit_40, self.spinBox_dimy)
        QWidget.setTabOrder(self.spinBox_dimy, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.lineEdit_35)
        QWidget.setTabOrder(self.lineEdit_35, self.doubleSpinBox_originz)
        QWidget.setTabOrder(self.doubleSpinBox_originz, self.lineEdit_23)
        QWidget.setTabOrder(self.lineEdit_23, self.doubleSpinBox_spacingz)
        QWidget.setTabOrder(self.doubleSpinBox_spacingz, self.pushButton_SaveMetadata)
        QWidget.setTabOrder(self.pushButton_SaveMetadata, self.doubleSpinBox_spacingy)
        QWidget.setTabOrder(self.doubleSpinBox_spacingy, self.lineEdit_39)
        QWidget.setTabOrder(self.lineEdit_39, self.lineEdit_28)
        QWidget.setTabOrder(self.lineEdit_28, self.lineEdit_41)
        QWidget.setTabOrder(self.lineEdit_41, self.doubleSpinBox_originy)
        QWidget.setTabOrder(self.doubleSpinBox_originy, self.lineEdit_44)
        QWidget.setTabOrder(self.lineEdit_44, self.lineEdit_25)
        QWidget.setTabOrder(self.lineEdit_25, self.lineEdit_36)
        QWidget.setTabOrder(self.lineEdit_36, self.spinBox_dimx)
        QWidget.setTabOrder(self.spinBox_dimx, self.spinBox_dimz)
        QWidget.setTabOrder(self.spinBox_dimz, self.lineEdit_42)
        QWidget.setTabOrder(self.lineEdit_42, self.doubleSpinBox_maxIntensity)
        QWidget.setTabOrder(self.doubleSpinBox_maxIntensity, self.lineEdit_26)
        QWidget.setTabOrder(self.lineEdit_26, self.lineEdit_27)
        QWidget.setTabOrder(self.lineEdit_27, self.lineEdit_32)
        QWidget.setTabOrder(self.lineEdit_32, self.lineEdit_direction)
        QWidget.setTabOrder(self.lineEdit_direction, self.doubleSpinBox_spacingx)
        QWidget.setTabOrder(self.doubleSpinBox_spacingx, self.lineEdit_45)
        QWidget.setTabOrder(self.lineEdit_45, self.lineEdit_37)
        QWidget.setTabOrder(self.lineEdit_37, self.pushButton_changeSpacing)
        QWidget.setTabOrder(self.pushButton_changeSpacing, self.doubleSpinBox_minIntensity)
        QWidget.setTabOrder(self.doubleSpinBox_minIntensity, self.lineEdit_34)
        QWidget.setTabOrder(self.lineEdit_34, self.pushButton_reorient)
        QWidget.setTabOrder(self.pushButton_reorient, self.lineEdit_DicomOrient)
        QWidget.setTabOrder(self.lineEdit_DicomOrient, self.pushButton_anatRegion)
        QWidget.setTabOrder(self.pushButton_anatRegion, self.comboBox_mridTag)
        QWidget.setTabOrder(self.comboBox_mridTag, self.pushButton_selectAll)
        QWidget.setTabOrder(self.pushButton_selectAll, self.tableWidget_ephys)
        QWidget.setTabOrder(self.tableWidget_ephys, self.pushButton_deselectAll)
        QWidget.setTabOrder(self.pushButton_deselectAll, self.pushButton_showChannels)
        QWidget.setTabOrder(self.pushButton_showChannels, self.textEdit_ephys)
        QWidget.setTabOrder(self.textEdit_ephys, self.tabWidget_2)
        QWidget.setTabOrder(self.tabWidget_2, self.resetCamera_ephys)
        QWidget.setTabOrder(self.resetCamera_ephys, self.change_perspective_ephys)
        QWidget.setTabOrder(self.change_perspective_ephys, self.pushButton_slicey)
        QWidget.setTabOrder(self.pushButton_slicey, self.pushButton_Noslicing)
        QWidget.setTabOrder(self.pushButton_Noslicing, self.pushButton_slicex)
        QWidget.setTabOrder(self.pushButton_slicex, self.pushButton_slicez)
        QWidget.setTabOrder(self.pushButton_slicez, self.horizontalSlider_OtherRegions)
        QWidget.setTabOrder(self.horizontalSlider_OtherRegions, self.horizontalSlider_Background)
        QWidget.setTabOrder(self.horizontalSlider_Background, self.horizontalSlider_ElectrodeRegion)
        QWidget.setTabOrder(self.horizontalSlider_ElectrodeRegion, self.vtkWidget_ephys)
        QWidget.setTabOrder(self.vtkWidget_ephys, self.spinBox_y_ephys)
        QWidget.setTabOrder(self.spinBox_y_ephys, self.spinBox_z_ephys)
        QWidget.setTabOrder(self.spinBox_z_ephys, self.spinBox_x_ephys)
        QWidget.setTabOrder(self.spinBox_x_ephys, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.pushButton_videoPlay)
        QWidget.setTabOrder(self.pushButton_videoPlay, self.spinBox_frame)
        QWidget.setTabOrder(self.spinBox_frame, self.pushButton_AddVideo)
        QWidget.setTabOrder(self.pushButton_AddVideo, self.pushButton_filterpopup)
        QWidget.setTabOrder(self.pushButton_filterpopup, self.lineEdit_13)
        QWidget.setTabOrder(self.lineEdit_13, self.pushButton_FrequencyResponse)
        QWidget.setTabOrder(self.pushButton_FrequencyResponse, self.comboBox_FilterType)
        QWidget.setTabOrder(self.comboBox_FilterType, self.lineEdit_selectedChannels)
        QWidget.setTabOrder(self.lineEdit_selectedChannels, self.radioButton_bandPass)
        QWidget.setTabOrder(self.radioButton_bandPass, self.lineEdit_18)
        QWidget.setTabOrder(self.lineEdit_18, self.radioButton_lowPass)
        QWidget.setTabOrder(self.radioButton_lowPass, self.pushButton_Filter)
        QWidget.setTabOrder(self.pushButton_Filter, self.doubleSpinBox_upperFreq)
        QWidget.setTabOrder(self.doubleSpinBox_upperFreq, self.doubleSpinBox_lowerFreq)
        QWidget.setTabOrder(self.doubleSpinBox_lowerFreq, self.pushButton_detectFreq)
        QWidget.setTabOrder(self.pushButton_detectFreq, self.comboBox_ChangeanatRegion)
        QWidget.setTabOrder(self.comboBox_ChangeanatRegion, self.spinBox_ChangechannelID)
        QWidget.setTabOrder(self.spinBox_ChangechannelID, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.lineEdit_8)
        QWidget.setTabOrder(self.lineEdit_8, self.pushButton_fetch)
        QWidget.setTabOrder(self.pushButton_fetch, self.lineEdit_server)
        QWidget.setTabOrder(self.lineEdit_server, self.lineEdit_animalid)
        QWidget.setTabOrder(self.lineEdit_animalid, self.lineEdit_9)
        QWidget.setTabOrder(self.lineEdit_9, self.lineEdit_rawBase)
        QWidget.setTabOrder(self.lineEdit_rawBase, self.checkBox_bidsflag)
        QWidget.setTabOrder(self.checkBox_bidsflag, self.lineEdit_password)
        QWidget.setTabOrder(self.lineEdit_password, self.pushButton_browse)
        QWidget.setTabOrder(self.pushButton_browse, self.lineEdit_6)
        QWidget.setTabOrder(self.lineEdit_6, self.lineEdit_12)
        QWidget.setTabOrder(self.lineEdit_12, self.pushButton_re_fetch)
        QWidget.setTabOrder(self.pushButton_re_fetch, self.pushButton_continue)
        QWidget.setTabOrder(self.pushButton_continue, self.lineEdit_11)
        QWidget.setTabOrder(self.lineEdit_11, self.checkBox_atlasmask)
        QWidget.setTabOrder(self.checkBox_atlasmask, self.pushButton_browseAtlas)
        QWidget.setTabOrder(self.pushButton_browseAtlas, self.lineEdit_10)
        QWidget.setTabOrder(self.lineEdit_10, self.comboBox_register_key)
        QWidget.setTabOrder(self.comboBox_register_key, self.spinBox_num_threads)
        QWidget.setTabOrder(self.spinBox_num_threads, self.comboBox_tasks)
        QWidget.setTabOrder(self.comboBox_tasks, self.lineEdit_15)
        QWidget.setTabOrder(self.lineEdit_15, self.lineEdit_atlas_path)
        QWidget.setTabOrder(self.lineEdit_atlas_path, self.pushButton_browseBase)
        QWidget.setTabOrder(self.pushButton_browseBase, self.checkBox_elastic)
        QWidget.setTabOrder(self.checkBox_elastic, self.pushButton_createMovMask)
        QWidget.setTabOrder(self.pushButton_createMovMask, self.pushButton_browseMov)
        QWidget.setTabOrder(self.pushButton_browseMov, self.lineEdit_movMask)
        QWidget.setTabOrder(self.lineEdit_movMask, self.pushButton_browseBru2)
        QWidget.setTabOrder(self.pushButton_browseBru2, self.lineEdit_animalID)
        QWidget.setTabOrder(self.lineEdit_animalID, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.lineEdit_7)
        QWidget.setTabOrder(self.lineEdit_7, self.checkBox_mov_mask)
        QWidget.setTabOrder(self.checkBox_mov_mask, self.lineEdit_16)
        QWidget.setTabOrder(self.lineEdit_16, self.lineEdit_base_path)
        QWidget.setTabOrder(self.lineEdit_base_path, self.lineEdit_17)
        QWidget.setTabOrder(self.lineEdit_17, self.lineEdit_bru2_path)
        QWidget.setTabOrder(self.lineEdit_bru2_path, self.checkBox_presurgery)
        QWidget.setTabOrder(self.checkBox_presurgery, self.lineEdit_14)
        QWidget.setTabOrder(self.lineEdit_14, self.comboBox_working_session)
        QWidget.setTabOrder(self.comboBox_working_session, self.checkBox_registration)
        QWidget.setTabOrder(self.checkBox_registration, self.checkBox_biascorrection)
        QWidget.setTabOrder(self.checkBox_biascorrection, self.plainTextEdit_SAMRI)
        QWidget.setTabOrder(self.plainTextEdit_SAMRI, self.textEdit_vis3D)
        QWidget.setTabOrder(self.textEdit_vis3D, self.comboBox_mridTag_vis3D)
        QWidget.setTabOrder(self.comboBox_mridTag_vis3D, self.pushButton_slicey_vis3D)
        QWidget.setTabOrder(self.pushButton_slicey_vis3D, self.resetCamera_vis3D)
        QWidget.setTabOrder(self.resetCamera_vis3D, self.pushButton_slicex_vis3D)
        QWidget.setTabOrder(self.pushButton_slicex_vis3D, self.change_perspective_vis3D)
        QWidget.setTabOrder(self.change_perspective_vis3D, self.pushButton_slicez_vis3D)
        QWidget.setTabOrder(self.pushButton_slicez_vis3D, self.vtkWidget_vis3D)
        QWidget.setTabOrder(self.vtkWidget_vis3D, self.pushButton_Noslicing_vis3D)
        QWidget.setTabOrder(self.pushButton_Noslicing_vis3D, self.comboBox_anatRegion_vis3D)
        QWidget.setTabOrder(self.comboBox_anatRegion_vis3D, self.spinBox_channelID_vis3D)
        QWidget.setTabOrder(self.spinBox_channelID_vis3D, self.spinBox_y_vis3D)
        QWidget.setTabOrder(self.spinBox_y_vis3D, self.spinBox_z_vis3D)
        QWidget.setTabOrder(self.spinBox_z_vis3D, self.spinBox_x_vis3D)
        QWidget.setTabOrder(self.spinBox_x_vis3D, self.tableWidget_vis3D)
        QWidget.setTabOrder(self.tableWidget_vis3D, self.pushButton_zoomReset)
        QWidget.setTabOrder(self.pushButton_zoomReset, self.pushButtonAmp_plus)
        QWidget.setTabOrder(self.pushButtonAmp_plus, self.pushButton_timeline)
        QWidget.setTabOrder(self.pushButton_timeline, self.pushButtonAmp_minus)
        QWidget.setTabOrder(self.pushButtonAmp_minus, self.pushButton_zoomOut)
        QWidget.setTabOrder(self.pushButton_zoomOut, self.pushButton_selectTime)
        QWidget.setTabOrder(self.pushButton_selectTime, self.pushButton_measurement)
        QWidget.setTabOrder(self.pushButton_measurement, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.spinBox_startMs)
        QWidget.setTabOrder(self.spinBox_startMs, self.spinBox_startS)
        QWidget.setTabOrder(self.spinBox_startS, self.spinBox_startMin)
        QWidget.setTabOrder(self.spinBox_startMin, self.spinBox_duration)
        QWidget.setTabOrder(self.spinBox_duration, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.horizontalSlider_ephys)

        self.menubar.addAction(self.menuGUI.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu4D_Tools.menuAction())
        self.menuGUI.addAction(self.actionOpen)
        self.menuGUI.addAction(self.actionOpen_ephys_Data)
        self.menuGUI.addAction(self.actionStart_SAMRI_process)
        self.menuGUI.addAction(self.actionTrajectory_Planning)
        self.menuGUI.addSeparator()
        self.menuGUI.addAction(self.actionAddViewImage)
        self.menuGUI.addSeparator()
        self.menuGUI.addAction(self.actionQuit)
        self.menuTools.addAction(self.actionPaintbrush)
        self.menuTools.addAction(self.actionMeasurement)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionResample)
        self.menuTools.addAction(self.actionRegister)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionSegmentation)
        self.menu4D_Tools.addAction(self.actionStart_MRIDlabels)
        self.menu4D_Tools.addAction(self.menuElectrode_Localization.menuAction())
        self.menu4D_Tools.addSeparator()
        self.menu4D_Tools.addAction(self.actionContrast_Adjustments)
        self.menu4D_Tools.addSeparator()
        self.menuElectrode_Localization.addAction(self.actionGaussian_Centers)
        self.menuElectrode_Localization.addAction(self.actionGet_Coordinates)

        self.retranslateUi(MainWindow)

        self.tabWidget_visualisation.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.fit_to_zoom_data11.setDefault(False)
        self.fit_to_zoom_data13.setDefault(False)
        self.fit_to_zoom_data12.setDefault(False)
        self.tabWidget_time1.setCurrentIndex(0)
        self.fit_to_zoom_data10.setDefault(False)
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
        self.stackedWidget_3d.setCurrentIndex(0)
        self.stackedWidget_trajectoryplanning.setCurrentIndex(1)
        self.stackedWidget_sagittal.setCurrentIndex(0)
        self.fit_to_zoom_data3d1.setDefault(False)
        self.stackedWidget_coronal.setCurrentIndex(0)
        self.fit_to_zoom_data3d2.setDefault(False)
        self.stackedWidget_axial.setCurrentIndex(0)
        self.fit_to_zoom_data3d0.setDefault(False)
        self.stackedWidget_sagittal_2.setCurrentIndex(1)
        self.fit_to_zoom_data3d1_2.setDefault(False)
        self.tabWidget_4.setCurrentIndex(0)
        self.contrast_data.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_5.setCurrentIndex(2)
        self.tabWidget_6.setCurrentIndex(0)
        self.comboBox_finest.setCurrentIndex(0)
        self.comboBox_movingimg.setCurrentIndex(-1)
        self.comboBox_coarest.setCurrentIndex(0)
        self.stackedWidget_segmentation.setCurrentIndex(0)
        self.stackedWidget_4D.setCurrentIndex(0)
        self.histogram_label.setCurrentIndex(-1)
        self.tabWidget_2.setCurrentIndex(0)
        self.resetCamera_ephys.setDefault(False)
        self.stackedWidget_video.setCurrentIndex(0)
        self.resetCamera_vis3D.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(accessibility)
        MainWindow.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Load MRI Image", None))
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"Add Another Image (3D)", None))
        self.actionSave_Image.setText(QCoreApplication.translate("MainWindow", u"Save Image", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionPaintbrush.setText(QCoreApplication.translate("MainWindow", u"Paintbrush", None))
        self.actionmain_code_2.setText(QCoreApplication.translate("MainWindow", u"main code 2", None))
        self.actionGaussian_Centers.setText(QCoreApplication.translate("MainWindow", u"Warping and Gaussian Centres Extraction", None))
        self.actionGet_Coordinates.setText(QCoreApplication.translate("MainWindow", u"Final Localization", None))
        self.actionStart_with_Labels.setText(QCoreApplication.translate("MainWindow", u"Start with Labels", None))
        self.actionAddViewImage.setText(QCoreApplication.translate("MainWindow", u"Load Another MRI Image", None))
        self.actionContrast_Adjustments.setText(QCoreApplication.translate("MainWindow", u"Contrast Adjustments", None))
        self.actionResample.setText(QCoreApplication.translate("MainWindow", u"Resample", None))
        self.actionRegister.setText(QCoreApplication.translate("MainWindow", u"Registration", None))
        self.actionContrast_Adjustments_2.setText(QCoreApplication.translate("MainWindow", u"Measurement", None))
        self.actionStart_MRIDlabels.setText(QCoreApplication.translate("MainWindow", u"MRID-tag label creation", None))
        self.actionOpen_ephys_Data.setText(QCoreApplication.translate("MainWindow", u"Load ephys Data", None))
        self.actionSegmentation.setText(QCoreApplication.translate("MainWindow", u"Segmentation", None))
        self.actionGet_Position_in_HPC.setText(QCoreApplication.translate("MainWindow", u"Get Position in HPC", None))
        self.actionMeasurement.setText(QCoreApplication.translate("MainWindow", u"Measurement", None))
        self.actionVisualize_3D_data.setText(QCoreApplication.translate("MainWindow", u"Visualize 3D data", None))
        self.actionStart_SAMRI_process.setText(QCoreApplication.translate("MainWindow", u"Start SAMRI process", None))
        self.actionTd.setText(QCoreApplication.translate("MainWindow", u"Trajectory Planning", None))
        self.actionTrajectory_Planning.setText(QCoreApplication.translate("MainWindow", u"Trajectory Planning", None))
        self.groupBox_barcode.setTitle(QCoreApplication.translate("MainWindow", u"MRID Barcode", None))
        self.groupbox_barcode1.setTitle(QCoreApplication.translate("MainWindow", u"Barcode reconstructed", None))
        ___qtablewidgetitem = self.tableWidget_barcode.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Duo", None));
        ___qtablewidgetitem1 = self.tableWidget_barcode.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Trio", None));
        ___qtablewidgetitem2 = self.tableWidget_barcode.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Quad", None));
        ___qtablewidgetitem3 = self.tableWidget_barcode.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Penta", None));
        ___qtablewidgetitem4 = self.tableWidget_barcode.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Probabilities", None));
        ___qtablewidgetitem5 = self.tableWidget_barcode.verticalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Similarities", None));
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"CA1 Signal", None))
        self.groupbox_barcode0.setTitle(QCoreApplication.translate("MainWindow", u"Barcode detected", None))
        self.groupBox_data1.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.groupbox_legend1.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap Intensities", None))
        self.groupBox_time11.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=4", None))
        self.fit_to_zoom_data11.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data11.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data11.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data11.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data11.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data11.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data11.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_38.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem6 = self.tableintensity_data1.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem7 = self.tableintensity_data1.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem8 = self.tableintensity_data1.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
        self.heatmap_data1.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap", None))
        self.fit_to_zoom_data13.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data13.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data13.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data13.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data13.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data13.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data13.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Cursor position (x,y,z)", None))
        self.groupBox_time12.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=8", None))
        self.fit_to_zoom_data12.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data12.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data12.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data12.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data12.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data12.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data12.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_51.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_53.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_reset_data10.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.pushButton_auto_data10.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time1.setTabText(self.tabWidget_time1.indexOf(self.tabWidget_time12), QCoreApplication.translate("MainWindow", u"Timestamp 1", None))
        self.groupBox_45.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_54.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_auto_data11.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.pushButton_reset_data11.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.tabWidget_time1.setTabText(self.tabWidget_time1.indexOf(self.tabWidget_time10), QCoreApplication.translate("MainWindow", u"Timestamp 2", None))
        self.groupBox_55.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_56.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_reset_data12.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.pushButton_auto_data12.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time1.setTabText(self.tabWidget_time1.indexOf(self.tabWidget_time11), QCoreApplication.translate("MainWindow", u"Timestamp 3", None))
        self.groupBox_time10.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=0", None))
        self.zoom_in_data10.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data10.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.fit_to_zoom_data10.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data10.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data10.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data10.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data10.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.file_name_displayed_4d.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:12pt; font-weight:700; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:8pt; color:#ff0000;\">PLEASE LOAD FILE</span></p></body></html>", None))
        self.groupBox_data2.setTitle(QCoreApplication.translate("MainWindow", u"View AXIAL", None))
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"Curosr 2", None))
        self.groupBox_time20.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=0", None))
        self.fit_to_zoom_data20.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data20.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data20.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data20.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data20.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data20.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data20.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_57.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_58.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_reset_data20.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.pushButton_auto_data20.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time2.setTabText(self.tabWidget_time2.indexOf(self.tabWidget_time20), QCoreApplication.translate("MainWindow", u"Timestamp 1", None))
        self.groupBox_59.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_60.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_auto_data21.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.pushButton_reset_data21.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.tabWidget_time2.setTabText(self.tabWidget_time2.indexOf(self.tabWidget_time21), QCoreApplication.translate("MainWindow", u"Timestamp 2", None))
        self.groupBox_61.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_62.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_reset_data22.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.pushButton_auto_data22.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time2.setTabText(self.tabWidget_time2.indexOf(self.tabWidget_time22), QCoreApplication.translate("MainWindow", u"Timestamp 3", None))
        self.heatmap_data2.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap", None))
        self.go_down_data23.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data23.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data23.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data23.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.fit_to_zoom_data23.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.zoom_in_data23.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data23.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_39.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem9 = self.tableintensity_data2.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem10 = self.tableintensity_data2.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem11 = self.tableintensity_data2.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
        self.groupBox_time21.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=4", None))
        self.fit_to_zoom_data21.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data21.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data21.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data21.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data21.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data21.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data21.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_time22.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=8", None))
        self.fit_to_zoom_data22.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data22.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data22.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data22.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data22.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data22.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data22.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupbox_legend2.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap Intensities", None))
#if QT_CONFIG(tooltip)
        self.pushButton_metadata.setToolTip(QCoreApplication.translate("MainWindow", u"Metadata of Files", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_metadata.setText("")
        self.groupBox_data0.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.groupBox_46.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_49.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_reset_data00.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.pushButton_auto_data00.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time0.setTabText(self.tabWidget_time0.indexOf(self.tabWidget_time00), QCoreApplication.translate("MainWindow", u"Timestamp t=0", None))
        self.groupBox_41.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_42.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_auto_data01.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.pushButton_reset_data01.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.tabWidget_time0.setTabText(self.tabWidget_time0.indexOf(self.tabWidget_time01), QCoreApplication.translate("MainWindow", u"Timestamp t=4", None))
        self.groupBox_44.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp Slider", None))
        self.groupBox_43.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustment", None))
        self.pushButton_reset_data02.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.pushButton_auto_data02.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.tabWidget_time0.setTabText(self.tabWidget_time0.indexOf(self.tabWidget_time02), QCoreApplication.translate("MainWindow", u"Timestamp  t=8", None))
        self.heatmap_data0.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap", None))
        self.groupBox_time00.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=0", None))
        self.fit_to_zoom_data00.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data00.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data00.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data00.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data00.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data00.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data00.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_time01.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=4", None))
        self.zoom_in_data01.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data01.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.fit_to_zoom_data01.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data01.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data01.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data01.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data01.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"Cursor Position (x,y,z)", None))
        self.groupBox_time02.setTitle(QCoreApplication.translate("MainWindow", u"Timestamp t=8", None))
        self.go_down_data02.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data02.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data02.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data02.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data02.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data02.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.fit_to_zoom_data02.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem12 = self.tableintensity_data0.horizontalHeaderItem(1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem13 = self.tableintensity_data0.horizontalHeaderItem(2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem14 = self.tableintensity_data0.horizontalHeaderItem(3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
        self.groupbox_legend0.setTitle(QCoreApplication.translate("MainWindow", u"Heatmap Intensities", None))
        self.groupBox_40.setTitle(QCoreApplication.translate("MainWindow", u"Intensity under cursor", None))
        ___qtablewidgetitem15 = self.tableintensity_data3d.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Layer", None));
        ___qtablewidgetitem16 = self.tableintensity_data3d.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Intensity", None));
        ___qtablewidgetitem17 = self.tableintensity_data3d.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Opacity", None));
        self.groupBox_22.setTitle(QCoreApplication.translate("MainWindow", u"Distances  between Bregma and Lambda", None))
        self.lineEdit_31.setText(QCoreApplication.translate("MainWindow", u"Animal MRI", None))
        self.lineEdit_43.setText(QCoreApplication.translate("MainWindow", u"Ratio: Animal / Atlas", None))
        self.lineEdit_33.setText(QCoreApplication.translate("MainWindow", u"Atlas registered points", None))
        self.doubleSpinBox_distanceAtlas.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.doubleSpinBox_tp_ratio.setSuffix("")
        self.doubleSpinBox_distance.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.pushButton_redAreas.setText(QCoreApplication.translate("MainWindow", u"Paint Areas To Avoid", None))
        self.textEdit_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Please select Bregma and Lambda in the MRI Image</span></p></body></html>", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Bregma Coordinates xyz ", None))
        self.doubleSpinBox_d_bregmaz.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.pushButton_tp_bregma.setText(QCoreApplication.translate("MainWindow", u"Save Cursor Position \n"
" as Bregma", None))
        self.lineEdit_24.setText(QCoreApplication.translate("MainWindow", u"Animal Bregma Coordinates", None))
        self.lineEdit_19.setText(QCoreApplication.translate("MainWindow", u"Absolute Distance between Animal and Atlas Bregma", None))
        self.lineEdit_29.setText(QCoreApplication.translate("MainWindow", u"Atlas registered Bregma", None))
        self.doubleSpinBox_d_bregmax.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.doubleSpinBox_d_bregmay.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.pushButton_tp_next0.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("MainWindow", u"Lambda Coordinates xyz", None))
        self.lineEdit_20.setText(QCoreApplication.translate("MainWindow", u"Atlas registered Lambda", None))
        self.pushButton_tp_lambda.setText(QCoreApplication.translate("MainWindow", u"Save Cursor Position \n"
" as Lambda", None))
        self.lineEdit_58.setText(QCoreApplication.translate("MainWindow", u"Animal Lambda Coordinates", None))
        self.doubleSpinBox_d_lambdaz.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.doubleSpinBox_d_lambdax.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.lineEdit_30.setText(QCoreApplication.translate("MainWindow", u"Absolute Distance between Animal and Atlas Lambda", None))
        self.doubleSpinBox_d_lambday.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
#if QT_CONFIG(tooltip)
        self.pushButton_PyLdetection.setToolTip(QCoreApplication.translate("MainWindow", u"Channel in CA1 needed", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_PyLdetection.setText(QCoreApplication.translate("MainWindow", u"Detect PyL using DWI", None))
        self.pushButton_edgemask.setText(QCoreApplication.translate("MainWindow", u"Highlight Points \n"
" on Brain Edge", None))
        self.pushButton_addShank.setText(QCoreApplication.translate("MainWindow", u"Add Another \n"
" Shank", None))
        self.pushButton_SaveTraj.setText(QCoreApplication.translate("MainWindow", u"Save Trajectory", None))
        self.doubleSpinBox_distance_shank.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.groupBox_75.setTitle(QCoreApplication.translate("MainWindow", u"Coordinates xyz", None))
        self.groupBox_74.setTitle(QCoreApplication.translate("MainWindow", u"Coordinates xyz", None))
        self.pushButton_tp_deep.setText(QCoreApplication.translate("MainWindow", u"Save Cursor Position \n"
" as Deepest-Point", None))
        self.checkBox_brain_region.setText(QCoreApplication.translate("MainWindow", u"Show Brain Region \n"
" while Hovering", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Please select point of insertion along the edge of the brain </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">And the deepest point, where the shank should end up</span></p></body></html>", None))
        self.textEdit_distance_shank.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Distance between</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Insertion Point</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-ind"
                        "ent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">and Deepest Point </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">in MRI space</span></p></body></html>", None))
        self.pushButton_tp_insert.setText(QCoreApplication.translate("MainWindow", u"Save Edge Point vertically \n"
" above Cursor Position \n"
" as Insert-Point", None))
        self.pushButton_coronalView.setText(QCoreApplication.translate("MainWindow", u"Change \n"
" Coronal View", None))
        self.pushButton_axialView.setText(QCoreApplication.translate("MainWindow", u"Change \n"
" Axial View", None))
        self.pushButton_sagittalView.setText(QCoreApplication.translate("MainWindow", u"Change \n"
" Sagittal View", None))
        self.groupBox_shank.setTitle(QCoreApplication.translate("MainWindow", u"Shank Info", None))
        self.lineEdit_21.setText(QCoreApplication.translate("MainWindow", u"Total Channels", None))
        self.lineEdit_22.setText(QCoreApplication.translate("MainWindow", u"Channel Separation", None))
        self.spinBox_tp_separation.setSuffix(QCoreApplication.translate("MainWindow", u"um", None))
        ___qtablewidgetitem18 = self.tableWidget_shank_info.horizontalHeaderItem(0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"# Channels", None));
        ___qtablewidgetitem19 = self.tableWidget_shank_info.horizontalHeaderItem(1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Brain Region", None));
        self.pushButton_removeShank.setText(QCoreApplication.translate("MainWindow", u"Remove  \n"
" Shank", None))
        self.lineEdit_vis3D.setText(QCoreApplication.translate("MainWindow", u"3D Visualisation", None))
        self.pushButton_seg3D.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.groupBox_68.setTitle(QCoreApplication.translate("MainWindow", u"Cursor Position (x,y,z)", None))
        self.groupBox_contrast.setTitle(QCoreApplication.translate("MainWindow", u"Contrast Adjustments", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.pushButton_auto_data3d.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.pushButton_reset_data3d.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.textEdit_8.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">SAGITTAL</span></p></body></html>", None))
        self.go_down_data3d1.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data3d1.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data3d1.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data3d1.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data3d1.setText("")
        self.zoom_out_data3d1.setText("")
        self.fit_to_zoom_data3d1.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.textEdit_11.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">3D View (Sagittal)</span></p></body></html>", None))
        self.pushButton_resetSagittal.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.textEdit_9.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">CORONAL</span></p></body></html>", None))
        self.fit_to_zoom_data3d2.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.go_down_data3d2.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data3d2.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data3d2.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data3d2.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data3d2.setText("")
        self.zoom_out_data3d2.setText("")
        self.textEdit_10.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">3D View (Coronal)</span></p></body></html>", None))
        self.pushButton_resetCoronal.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.textEdit_7.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">AXIAL</span></p></body></html>", None))
        self.go_down_data3d0.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data3d0.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data3d0.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data3d0.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.fit_to_zoom_data3d0.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.zoom_in_data3d0.setText("")
        self.zoom_out_data3d0.setText("")
        self.textEdit_12.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">SAGITTAL</span></p></body></html>", None))
        self.go_down_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_up_data3d1_2.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.go_left_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.go_right_data3d1_2.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.zoom_in_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoom_out_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.fit_to_zoom_data3d1_2.setText(QCoreApplication.translate("MainWindow", u"Fit-to-Zoom", None))
        self.pushButton_resetAxial.setText(QCoreApplication.translate("MainWindow", u"Reset Camera", None))
        self.lineEdit_59.setText(QCoreApplication.translate("MainWindow", u"Change Depth of Slicing", None))
        self.textEdit_13.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:16pt;\">3D View (Axial)</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PostSurgery), QCoreApplication.translate("MainWindow", u"4D Data", None))
        self.groupBox_measurement.setTitle(QCoreApplication.translate("MainWindow", u"Measurement", None))
        self.checkBox_measurement.setText(QCoreApplication.translate("MainWindow", u" OFF", None))
        self.groupBox_.setTitle(QCoreApplication.translate("MainWindow", u"Measurement Table", None))
        self.comboBox_measurementColors.setItemText(0, QCoreApplication.translate("MainWindow", u"Red", None))
        self.comboBox_measurementColors.setItemText(1, QCoreApplication.translate("MainWindow", u"Green", None))
        self.comboBox_measurementColors.setItemText(2, QCoreApplication.translate("MainWindow", u"Blue", None))
        self.comboBox_measurementColors.setItemText(3, QCoreApplication.translate("MainWindow", u"Yellow", None))
        self.comboBox_measurementColors.setItemText(4, QCoreApplication.translate("MainWindow", u"Magenta", None))

        self.pushButton_deleteMeasurement.setText(QCoreApplication.translate("MainWindow", u"Delete Measurement", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("MainWindow", u"Manual Contrast Adjustments", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_28), QCoreApplication.translate("MainWindow", u"Coronal", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_29), QCoreApplication.translate("MainWindow", u"Sagittal", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_30), QCoreApplication.translate("MainWindow", u"Axial", None))
        self.ManualContrastAdjustments.setTitle(QCoreApplication.translate("MainWindow", u"Manual Contrast Adjustement", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"Timest 1", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"Timest 2", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"Timest 3", None))
        self.contrast_data.setItemText(self.contrast_data.indexOf(self.contrast_data0), QCoreApplication.translate("MainWindow", u"Data 0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_16), QCoreApplication.translate("MainWindow", u"Timest 1", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_17), QCoreApplication.translate("MainWindow", u"Timest 2", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_18), QCoreApplication.translate("MainWindow", u"Timest 3", None))
        self.contrast_data.setItemText(self.contrast_data.indexOf(self.contrast_data1), QCoreApplication.translate("MainWindow", u"Data 1", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_19), QCoreApplication.translate("MainWindow", u"Timest 1", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_20), QCoreApplication.translate("MainWindow", u"Timest 2", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Contrast / Window", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Brightness / Level", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_21), QCoreApplication.translate("MainWindow", u"Timest 3", None))
        self.contrast_data.setItemText(self.contrast_data.indexOf(self.contrast_data2), QCoreApplication.translate("MainWindow", u"Data 2", None))
        self.groupBox_register.setTitle(QCoreApplication.translate("MainWindow", u"Registration (Rigid Transformation)", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"Finest Level", None))
        self.comboBox_finest.setItemText(0, QCoreApplication.translate("MainWindow", u"1x", None))
        self.comboBox_finest.setItemText(1, QCoreApplication.translate("MainWindow", u"2x", None))
        self.comboBox_finest.setItemText(2, QCoreApplication.translate("MainWindow", u"4x", None))

        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"Moving Image", None))
        self.textEdit_6.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">If none is selectable, please load Another Image (3D)!</span></p></body></html>", None))
        self.textEdit_pixels.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:700;\">Please select other file. The MRI Scan needs at least 4pixels in each direction.</span></p></body></html>", None))
        self.pushButton_registration.setText(QCoreApplication.translate("MainWindow", u"Run Registration", None))
        self.pushButton_regCancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"Coarsest Level", None))
        self.comboBox_coarest.setItemText(0, QCoreApplication.translate("MainWindow", u"8x", None))
        self.comboBox_coarest.setItemText(1, QCoreApplication.translate("MainWindow", u"4x", None))
        self.comboBox_coarest.setItemText(2, QCoreApplication.translate("MainWindow", u"2x", None))
        self.comboBox_coarest.setItemText(3, QCoreApplication.translate("MainWindow", u"1x", None))

        self.groupBox_segmentation.setTitle(QCoreApplication.translate("MainWindow", u"Segmentation", None))
        self.textBrowser_5.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt;\">Step 1/3<br /></span><span style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:700;\">Presegmentation</span></p></body></html>", None))
        self.checkBox_threshold.setText(QCoreApplication.translate("MainWindow", u"Threshold ON", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"THRESHOLD", None))
        self.radioButton_bounded.setText(QCoreApplication.translate("MainWindow", u"Bounded", None))
        self.radioButton_lower.setText(QCoreApplication.translate("MainWindow", u"Lower-Only", None))
        self.radioButton_upper.setText(QCoreApplication.translate("MainWindow", u"Upper-Only", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Lower Threshold", None))
        self.groupBox_63.setTitle(QCoreApplication.translate("MainWindow", u"Upper Threshold", None))
        self.pushButton_Back1.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.pushButton_Next1.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.textBrowser_6.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt;\">Step 2/3<br /></span><span style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:700;\">Initialization</span></p></body></html>", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Bubble Radius", None))
        self.pushButton_Back2.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.pushButton_Next2.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.pushButton_addBubbles.setText(QCoreApplication.translate("MainWindow", u"Add Bubble at Cursor", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"Active Bubbles", None))
        self.pushButton_delete.setText(QCoreApplication.translate("MainWindow", u"Delete Active Bubble", None))
        self.groupBox_64.setTitle(QCoreApplication.translate("MainWindow", u"Step Size", None))
        self.groupBox_65.setTitle(QCoreApplication.translate("MainWindow", u"Start / Pause", None))
#if QT_CONFIG(tooltip)
        self.toolButton_forwardEvo.setToolTip(QCoreApplication.translate("MainWindow", u"One iteration of step size", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_forwardEvo.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_runEvo.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.toolButton_backwardEvo.setToolTip(QCoreApplication.translate("MainWindow", u"Reset to start", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_backwardEvo.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.textBrowser_7.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt;\">Step 3/3<br /></span><span style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:700;\">Evolution</span></p></body></html>", None))
        self.groupBox_66.setTitle(QCoreApplication.translate("MainWindow", u"Iteration", None))
        self.pushButton_Finish.setText(QCoreApplication.translate("MainWindow", u"Finish", None))
        self.pushButton_Back3.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.textEdit_SAMRI_reg.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Please create moving mask</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans'; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-in"
                        "dent:0px;\"><span style=\" font-family:'Sans'; font-size:10pt;\">Click on FINISH (at the end) to return to SAMRI registration.</span></p></body></html>", None))
        self.groupBox_paintbrush_3d.setTitle(QCoreApplication.translate("MainWindow", u"Paintbrush", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("MainWindow", u"Overall label opacity", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Segmentation Labels", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"Paint over", None))
        self.groupBox_50.setTitle(QCoreApplication.translate("MainWindow", u"Active Label", None))
        ___qtablewidgetitem20 = self.tableWidget_labels3D.horizontalHeaderItem(0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Idx", None));
        ___qtablewidgetitem21 = self.tableWidget_labels3D.horizontalHeaderItem(1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Color", None));
        ___qtablewidgetitem22 = self.tableWidget_labels3D.horizontalHeaderItem(2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Label", None));
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"Brush Size", None))
        self.checkBox_Brush.setText(QCoreApplication.translate("MainWindow", u"Brush ON", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Brush Style", None))
        self.paint_square.setText("")
        self.paint_round.setText("")
        self.pushButton_paint_done.setText(QCoreApplication.translate("MainWindow", u"Continue with Trajectory Planning", None))
        self.groupBox_resample.setTitle(QCoreApplication.translate("MainWindow", u"Resample", None))
        self.pushButton_resample100um.setText(QCoreApplication.translate("MainWindow", u"Resample 100um", None))
        self.pushButton_openfile100um.setText(QCoreApplication.translate("MainWindow", u"Done, open \n"
"resampled 100um file", None))
        self.pushButton_done.setText(QCoreApplication.translate("MainWindow", u"Done", None))
        self.pushButton_resample25um.setText(QCoreApplication.translate("MainWindow", u"Resample 25um", None))
        self.textBrowser_4.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Please select the file to resample!<br />Click on the buttons below to resample the data, after it is directly saved in the directory.</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_15), QCoreApplication.translate("MainWindow", u"Popups for 4D Data", None))
        self.groupBox_paintbrush.setTitle(QCoreApplication.translate("MainWindow", u"Paintbrush", None))
        self.pushButton_anatOK.setText(QCoreApplication.translate("MainWindow", u"NEXT", None))
        self.plainTextEdit_MRID_2.setPlainText(QCoreApplication.translate("MainWindow", u"Please paint all anatomical structures around the tags with the Paintbrush. Once this is done, please click NEXT", None))
        self.pushButton_segOK.setText(QCoreApplication.translate("MainWindow", u"DONE", None))
        self.plainTextEdit_MRID_4.setPlainText(QCoreApplication.translate("MainWindow", u"Please paint all MRID tags with the Paintbrush. Once this is done, please click DONE", None))
        self.checkBox_Brush_MRID.setText(QCoreApplication.translate("MainWindow", u"Brush ON", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"Paintbrush Inspector", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Brush Style", None))
        self.paint_square_Post.setText("")
        self.paint_round_Post.setText("")
        self.groupBox_31.setTitle(QCoreApplication.translate("MainWindow", u"Label Opacity", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"Brush Size", None))
        self.groupBox_33.setTitle(QCoreApplication.translate("MainWindow", u"Segmentation Labels", None))
        self.groupBox_35.setTitle(QCoreApplication.translate("MainWindow", u"Paint over", None))
        self.groupBox_47.setTitle(QCoreApplication.translate("MainWindow", u"Active Label", None))
        ___qtablewidgetitem23 = self.tableWidget_labels.horizontalHeaderItem(0)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Idx", None));
        ___qtablewidgetitem24 = self.tableWidget_labels.horizontalHeaderItem(1)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Color", None));
        ___qtablewidgetitem25 = self.tableWidget_labels.horizontalHeaderItem(2)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Label", None));
        self.groupBox_36.setTitle(QCoreApplication.translate("MainWindow", u"Histogram", None))
        self.groupBox_48.setTitle(QCoreApplication.translate("MainWindow", u"Label", None))
        self.lineEdit_52.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.doubleSpinBox_fovy.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.lineEdit_56.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.doubleSpinBox_spay.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.pushButton_SaveSpacing.setText(QCoreApplication.translate("MainWindow", u"Save new Metadata", None))
        self.lineEdit_55.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.lineEdit_50.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.lineEdit_47.setText(QCoreApplication.translate("MainWindow", u"Spacing", None))
        self.lineEdit_54.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.lineEdit_53.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.lineEdit_48.setText(QCoreApplication.translate("MainWindow", u"Field of View", None))
        self.lineEdit_51.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.lineEdit_46.setText(QCoreApplication.translate("MainWindow", u"Image Size", None))
        self.doubleSpinBox_fovz.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.doubleSpinBox_spax.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.pushButton_cancel_spacing.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.doubleSpinBox_fovx.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.lineEdit_49.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.lineEdit_57.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.doubleSpinBox_spaz.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.lineEdit_42.setText(QCoreApplication.translate("MainWindow", u"z:", None))
        self.lineEdit_28.setText(QCoreApplication.translate("MainWindow", u"Intensity Range", None))
        self.lineEdit_34.setText(QCoreApplication.translate("MainWindow", u"x:", None))
        self.pushButton_SaveMetadata.setText(QCoreApplication.translate("MainWindow", u"Save New Settings \n"
" and Reload Image", None))
        self.lineEdit_23.setText(QCoreApplication.translate("MainWindow", u"Dimensions", None))
        self.lineEdit_37.setText(QCoreApplication.translate("MainWindow", u"y:", None))
        self.pushButton_changeSpacing.setText(QCoreApplication.translate("MainWindow", u"Change Spacing", None))
        self.lineEdit_40.setText(QCoreApplication.translate("MainWindow", u"z:", None))
        self.lineEdit_39.setText(QCoreApplication.translate("MainWindow", u"y:", None))
        self.lineEdit_35.setText(QCoreApplication.translate("MainWindow", u"x:", None))
        self.pushButton_cancel_metadata.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.lineEdit_26.setText(QCoreApplication.translate("MainWindow", u"Origin", None))
        self.doubleSpinBox_spacingy.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.lineEdit_44.setText(QCoreApplication.translate("MainWindow", u"min", None))
        self.pushButton_reorient.setText(QCoreApplication.translate("MainWindow", u"Reorient to RAS", None))
        self.lineEdit_36.setText(QCoreApplication.translate("MainWindow", u"x:", None))
        self.lineEdit_41.setText(QCoreApplication.translate("MainWindow", u"z:", None))
        self.doubleSpinBox_spacingx.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.lineEdit_32.setText(QCoreApplication.translate("MainWindow", u"Direction", None))
        self.lineEdit_27.setText(QCoreApplication.translate("MainWindow", u"Orientation", None))
        self.lineEdit_25.setText(QCoreApplication.translate("MainWindow", u"Spacing", None))
        self.lineEdit_38.setText(QCoreApplication.translate("MainWindow", u"y:", None))
        self.lineEdit_45.setText(QCoreApplication.translate("MainWindow", u"max", None))
        self.doubleSpinBox_spacingz.setSuffix(QCoreApplication.translate("MainWindow", u"mm", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Popups for 4D Data II", None))
        self.pushButton_anatRegion.setText(QCoreApplication.translate("MainWindow", u"CHANGE ANAT REGION", None))
        self.groupBox_5.setTitle("")
        self.comboBox_mridTag.setCurrentText("")
        self.lineEdit_60.setText(QCoreApplication.translate("MainWindow", u"Selected Shank", None))
        self.pushButton_selectAll.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
        self.pushButton_deselectAll.setText(QCoreApplication.translate("MainWindow", u"Deselect All", None))
        self.pushButton_showChannels.setText(QCoreApplication.translate("MainWindow", u"Show only selected Channels", None))
        self.textEdit_ephys.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:20pt; color:#ffffff;\">Atlas 3D Visualisation</span></p></body></html>", None))
        self.groupBox_37.setTitle(QCoreApplication.translate("MainWindow", u"Coordinates of selected Channel", None))
#if QT_CONFIG(tooltip)
        self.resetCamera_ephys.setToolTip(QCoreApplication.translate("MainWindow", u"Reset Camera View", None))
#endif // QT_CONFIG(tooltip)
        self.resetCamera_ephys.setText("")
#if QT_CONFIG(tooltip)
        self.change_perspective_ephys.setToolTip(QCoreApplication.translate("MainWindow", u"Change Perspective", None))
#endif // QT_CONFIG(tooltip)
        self.change_perspective_ephys.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicey.setToolTip(QCoreApplication.translate("MainWindow", u"Coronal Slicing", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicey.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_Noslicing.setToolTip(QCoreApplication.translate("MainWindow", u"Exit Slicing Mode", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Noslicing.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicex.setToolTip(QCoreApplication.translate("MainWindow", u"Sagittal Slicing", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicex.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicez.setToolTip(QCoreApplication.translate("MainWindow", u"Axial Slicing", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicez.setText("")
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Change Opacity of Meshes", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Regions of Shank", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Background", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Region of Selected Electrode", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Anatomy", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"Jump to Frame", None))
        self.pushButton_videoPlay.setText("")
        self.pushButton_AddVideo.setText(QCoreApplication.translate("MainWindow", u"OPEN VIDEO", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Video", None))
        self.groupBox_anatRegion.setTitle(QCoreApplication.translate("MainWindow", u"Selected Channel ID and Anat Region Label", None))
        self.pushButton_changeTAG.setText(QCoreApplication.translate("MainWindow", u"CHANGE TAG", None))
        self.pushButton_filterpopup.setText(QCoreApplication.translate("MainWindow", u"Filter Channels", None))
        self.lineEdit_13.setText(QCoreApplication.translate("MainWindow", u"Please select something", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ephys), QCoreApplication.translate("MainWindow", u"ephys", None))
        self.pushButton_FrequencyResponse.setText(QCoreApplication.translate("MainWindow", u"Show Frequency Response", None))
        self.comboBox_FilterType.setItemText(0, QCoreApplication.translate("MainWindow", u"IIR - Butterworth", None))
        self.comboBox_FilterType.setItemText(1, QCoreApplication.translate("MainWindow", u"IIR - Chebyshev I", None))
        self.comboBox_FilterType.setItemText(2, QCoreApplication.translate("MainWindow", u"IIR - Chebyshev II", None))
        self.comboBox_FilterType.setItemText(3, QCoreApplication.translate("MainWindow", u"IIR - Elliptic", None))
        self.comboBox_FilterType.setItemText(4, QCoreApplication.translate("MainWindow", u"FIR - Hamming", None))
        self.comboBox_FilterType.setItemText(5, QCoreApplication.translate("MainWindow", u"FIR - Hann", None))
        self.comboBox_FilterType.setItemText(6, QCoreApplication.translate("MainWindow", u"FIR - Blackman", None))

        self.radioButton_bandPass.setText(QCoreApplication.translate("MainWindow", u"Band Pass Filter", None))
        self.lineEdit_18.setText(QCoreApplication.translate("MainWindow", u"Selected Channels IDs to be filtered (Please seperate with comma)", None))
        self.radioButton_lowPass.setText(QCoreApplication.translate("MainWindow", u"Low Pass Filter", None))
        self.pushButton_Filter.setText(QCoreApplication.translate("MainWindow", u"Filter Selected Channels", None))
        self.groupBox_upperFreq.setTitle(QCoreApplication.translate("MainWindow", u"Upper Frequency", None))
        self.groupBox_52.setTitle(QCoreApplication.translate("MainWindow", u"Lower Frequency", None))
        self.pushButton_detectFreq.setText(QCoreApplication.translate("MainWindow", u"Auto detect Frequency cut-off", None))
        self.groupBox_ChangeanatRegion.setTitle("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Anatomical Region", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Channel ID", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Popups for ephys", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"SAMRI - Logging Output", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"Server", None))
        self.pushButton_fetch.setText(QCoreApplication.translate("MainWindow", u"Fetch Data from Server", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.checkBox_bidsflag.setText(QCoreApplication.translate("MainWindow", u"Enable bids_flag", None))
        self.pushButton_browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"Raw Base", None))
        self.lineEdit_12.setText(QCoreApplication.translate("MainWindow", u"Animal ID", None))
        self.pushButton_re_fetch.setText(QCoreApplication.translate("MainWindow", u"Re-Fetch All Data", None))
        self.pushButton_continue.setText(QCoreApplication.translate("MainWindow", u"Continue without Data-Fetch", None))
        self.lineEdit_11.setText(QCoreApplication.translate("MainWindow", u"Moving Mask", None))
        self.checkBox_atlasmask.setText(QCoreApplication.translate("MainWindow", u"Use Atlas Mask", None))
        self.pushButton_browseAtlas.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.lineEdit_10.setText(QCoreApplication.translate("MainWindow", u"Atlas Files", None))
        self.lineEdit_15.setText(QCoreApplication.translate("MainWindow", u"Working Session", None))
        self.pushButton_browseBase.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.checkBox_elastic.setText(QCoreApplication.translate("MainWindow", u"Elastic", None))
        self.pushButton_createMovMask.setText(QCoreApplication.translate("MainWindow", u"Create \n"
" Moving  Mask", None))
        self.pushButton_browseMov.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.pushButton_browseBru2.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.lineEdit_animalID.setText(QCoreApplication.translate("MainWindow", u"Animal ID", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"Bru2 path", None))
        self.lineEdit_7.setText(QCoreApplication.translate("MainWindow", u"Base path", None))
        self.checkBox_mov_mask.setText(QCoreApplication.translate("MainWindow", u"Use moving mask", None))
        self.lineEdit_16.setText(QCoreApplication.translate("MainWindow", u"Register Key", None))
        self.lineEdit_17.setText(QCoreApplication.translate("MainWindow", u"Tasks", None))
        self.checkBox_presurgery.setText(QCoreApplication.translate("MainWindow", u"Presurgery", None))
        self.lineEdit_14.setText(QCoreApplication.translate("MainWindow", u"Num Threads", None))
        self.checkBox_registration.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.checkBox_biascorrection.setText(QCoreApplication.translate("MainWindow", u"Biascorrection ONLY", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_samri), QCoreApplication.translate("MainWindow", u"SAMRI", None))
        self.tabWidget_visualisation.setTabText(self.tabWidget_visualisation.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u" MRID Location", None))
        self.textEdit_vis3D.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:20pt; color:#ffffff;\">Atlas 3D Visualisation</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_slicey_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Slicing in Coronal Direction", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicey_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.resetCamera_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Reset Camera View", None))
#endif // QT_CONFIG(tooltip)
        self.resetCamera_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicex_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Slicing in Sagittal Direction", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicex_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.change_perspective_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Change Perspective", None))
#endif // QT_CONFIG(tooltip)
        self.change_perspective_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicez_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Slicing in Axial Direction", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicez_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_Noslicing_vis3D.setToolTip(QCoreApplication.translate("MainWindow", u"Exit Slicing Mode", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Noslicing_vis3D.setText("")
        self.groupBox_anatRegion_3.setTitle(QCoreApplication.translate("MainWindow", u"Selected Channel ID and Anat Region Label", None))
        self.groupBox_69.setTitle(QCoreApplication.translate("MainWindow", u"Coordinates of selected Channel", None))
        self.tabWidget_visualisation.setTabText(self.tabWidget_visualisation.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"3D Visualisation", None))
        self.menuGUI.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"3D Tools", None))
        self.menu4D_Tools.setTitle(QCoreApplication.translate("MainWindow", u"4D Tools", None))
        self.menuElectrode_Localization.setTitle(QCoreApplication.translate("MainWindow", u"Electrode Localization", None))
#if QT_CONFIG(tooltip)
        self.pushButton_zoomOut.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom Out", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_zoomOut.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_selectTime.setToolTip(QCoreApplication.translate("MainWindow", u"Select Time", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_selectTime.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_zoomReset.setToolTip(QCoreApplication.translate("MainWindow", u"Reset Zoom", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_zoomReset.setText("")
#if QT_CONFIG(tooltip)
        self.pushButtonAmp_minus.setToolTip(QCoreApplication.translate("MainWindow", u"Decrease Amplitude", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonAmp_minus.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_timeline.setToolTip(QCoreApplication.translate("MainWindow", u"Draw Timeline", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_timeline.setText("")
#if QT_CONFIG(tooltip)
        self.pushButtonAmp_plus.setToolTip(QCoreApplication.translate("MainWindow", u"Increase Amplitude", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonAmp_plus.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_measurement.setToolTip(QCoreApplication.translate("MainWindow", u"Measure", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_measurement.setText("")
        self.groupBox_3.setTitle("")
        self.spinBox_startMs.setSuffix(QCoreApplication.translate("MainWindow", u"ms", None))
        self.spinBox_startS.setSuffix(QCoreApplication.translate("MainWindow", u"s", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"Duration (ms)", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Start Time", None))
        self.spinBox_startMin.setSuffix(QCoreApplication.translate("MainWindow", u"min", None))
    # retranslateUi

