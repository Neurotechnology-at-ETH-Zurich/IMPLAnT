# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tab_popups_time_series_ii.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox, QApplication,
    QCheckBox, QComboBox, QDoubleSpinBox, QFrame,
    QGridLayout, QGroupBox, QHeaderView, QLineEdit,
    QPlainTextEdit, QPushButton, QSizePolicy, QSlider,
    QSpinBox, QStackedWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QToolButton, QWidget)

from mplwidget import MplWidget
from pyqtgraph import PlotWidget

class Ui_tab_6(object):
    def setupUi(self, tab_6):
        if not tab_6.objectName():
            tab_6.setObjectName(u"tab_6")
        self.gridLayout_173 = QGridLayout(tab_6)
        self.gridLayout_173.setObjectName(u"gridLayout_173")
        self.tp_dwi1D_frame = QFrame(tab_6)
        self.tp_dwi1D_frame.setObjectName(u"tp_dwi1D_frame")
        self.tp_dwi1D_frame.setFrameShape(QFrame.StyledPanel)
        self.tp_dwi1D_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_183 = QGridLayout(self.tp_dwi1D_frame)
        self.gridLayout_183.setObjectName(u"gridLayout_183")
        self.tp_dwi1D_widget = MplWidget(self.tp_dwi1D_frame)
        self.tp_dwi1D_widget.setObjectName(u"tp_dwi1D_widget")

        self.gridLayout_183.addWidget(self.tp_dwi1D_widget, 0, 0, 1, 1)


        self.gridLayout_173.addWidget(self.tp_dwi1D_frame, 0, 1, 1, 1)

        self.groupBox_paintbrush = QGroupBox(tab_6)
        self.groupBox_paintbrush.setObjectName(u"groupBox_paintbrush")
        self.groupBox_paintbrush.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_paintbrush.sizePolicy().hasHeightForWidth())
        self.groupBox_paintbrush.setSizePolicy(sizePolicy)
        self.groupBox_paintbrush.setMinimumSize(QSize(300, 250))
        self.groupBox_paintbrush.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_43 = QGridLayout(self.groupBox_paintbrush)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.stackedWidget_4D = QStackedWidget(self.groupBox_paintbrush)
        self.stackedWidget_4D.setObjectName(u"stackedWidget_4D")
        self.stackedWidget_4D.setMinimumSize(QSize(250, 0))
        self.stackedWidget_4D.setMaximumSize(QSize(16777215, 16777215))
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout = QGridLayout(self.page_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_anatOK = QPushButton(self.page_8)
        self.pushButton_anatOK.setObjectName(u"pushButton_anatOK")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_anatOK.sizePolicy().hasHeightForWidth())
        self.pushButton_anatOK.setSizePolicy(sizePolicy1)
        self.pushButton_anatOK.setMinimumSize(QSize(100, 80))
        font = QFont()
        font.setBold(False)
        font.setStyleStrategy(QFont.PreferDefault)
        self.pushButton_anatOK.setFont(font)
        self.pushButton_anatOK.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout.addWidget(self.pushButton_anatOK, 1, 1, 1, 1)

        self.plainTextEdit_MRID_2 = QPlainTextEdit(self.page_8)
        self.plainTextEdit_MRID_2.setObjectName(u"plainTextEdit_MRID_2")
        self.plainTextEdit_MRID_2.setMinimumSize(QSize(80, 80))
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
        self.pushButton_segOK.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

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
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
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
        font2 = QFont()
        font2.setBold(False)
        self.paint_square_Post.setFont(font2)
        self.paint_square_Post.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u"Icons/mri/square.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paint_square_Post.setIcon(icon)
        self.paint_square_Post.setIconSize(QSize(20, 20))
        self.paint_square_Post.setCheckable(True)
        self.paint_square_Post.setChecked(True)
        self.paint_square_Post.setAutoExclusive(False)

        self.gridLayout_40.addWidget(self.paint_square_Post, 0, 0, 1, 1)

        self.paint_round_Post = QToolButton(self.groupBox_29)
        self.paint_round_Post.setObjectName(u"paint_round_Post")
        self.paint_round_Post.setEnabled(True)
        icon1 = QIcon()
        icon1.addFile(u"Icons/mri/circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paint_round_Post.setIcon(icon1)
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
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_labels.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_labels.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_labels.setHorizontalHeaderItem(2, __qtablewidgetitem2)
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


        self.gridLayout_38.addWidget(self.groupBox_47, 0, 1, 1, 1)


        self.gridLayout_43.addWidget(self.groupBox_33, 0, 4, 4, 1)

        self.groupBox_36 = QGroupBox(self.groupBox_paintbrush)
        self.groupBox_36.setObjectName(u"groupBox_36")
        self.groupBox_36.setEnabled(True)
        self.groupBox_36.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_44 = QGridLayout(self.groupBox_36)
        self.gridLayout_44.setObjectName(u"gridLayout_44")
        self.widget_histogram = PlotWidget(self.groupBox_36)
        self.widget_histogram.setObjectName(u"widget_histogram")
        self.widget_histogram.setMaximumSize(QSize(16777215, 1000))

        self.gridLayout_44.addWidget(self.widget_histogram, 0, 2, 1, 1)

        self.groupBox_48 = QGroupBox(self.groupBox_36)
        self.groupBox_48.setObjectName(u"groupBox_48")
        self.groupBox_48.setMinimumSize(QSize(0, 60))
        self.groupBox_48.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_45 = QGridLayout(self.groupBox_48)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.histogram_label = QComboBox(self.groupBox_48)
        self.histogram_label.setObjectName(u"histogram_label")
        self.histogram_label.setEnabled(True)

        self.gridLayout_45.addWidget(self.histogram_label, 0, 0, 1, 1)

        self.paintbrush_dataview = QComboBox(self.groupBox_48)
        self.paintbrush_dataview.setObjectName(u"paintbrush_dataview")

        self.gridLayout_45.addWidget(self.paintbrush_dataview, 1, 0, 1, 1)


        self.gridLayout_44.addWidget(self.groupBox_48, 0, 1, 1, 1)


        self.gridLayout_43.addWidget(self.groupBox_36, 0, 5, 4, 1)

        self.gridLayout_43.setColumnStretch(5, 1)

        self.gridLayout_173.addWidget(self.groupBox_paintbrush, 0, 0, 1, 1)

        self.frame_spacing = QFrame(tab_6)
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
        self.pushButton_SaveSpacing.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

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
        self.lineEdit_47.setMinimumSize(QSize(100, 0))
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
        self.lineEdit_48.setMinimumSize(QSize(100, 0))
        self.lineEdit_48.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_48, 2, 0, 1, 1)

        self.lineEdit_51 = QLineEdit(self.frame_spacing)
        self.lineEdit_51.setObjectName(u"lineEdit_51")
        self.lineEdit_51.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_51.setReadOnly(True)

        self.gridLayout_181.addWidget(self.lineEdit_51, 3, 2, 1, 1)

        self.lineEdit_46 = QLineEdit(self.frame_spacing)
        self.lineEdit_46.setObjectName(u"lineEdit_46")
        self.lineEdit_46.setMinimumSize(QSize(100, 0))
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
        self.pushButton_cancel_spacing.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

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

        self.frame_metadata = QFrame(tab_6)
        self.frame_metadata.setObjectName(u"frame_metadata")
        self.frame_metadata.setFrameShape(QFrame.StyledPanel)
        self.frame_metadata.setFrameShadow(QFrame.Raised)
        self.gridLayout_180 = QGridLayout(self.frame_metadata)
        self.gridLayout_180.setObjectName(u"gridLayout_180")
        self.spinBox_dimz = QSpinBox(self.frame_metadata)
        self.spinBox_dimz.setObjectName(u"spinBox_dimz")
        self.spinBox_dimz.setReadOnly(True)
        self.spinBox_dimz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimz.setMaximum(100000)

        self.gridLayout_180.addWidget(self.spinBox_dimz, 2, 7, 1, 1)

        self.lineEdit_direction = QTextEdit(self.frame_metadata)
        self.lineEdit_direction.setObjectName(u"lineEdit_direction")
        self.lineEdit_direction.setMaximumSize(QSize(500, 100))

        self.gridLayout_180.addWidget(self.lineEdit_direction, 8, 1, 1, 7)

        self.doubleSpinBox_originx = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_originx.setObjectName(u"doubleSpinBox_originx")
        self.doubleSpinBox_originx.setReadOnly(True)
        self.doubleSpinBox_originx.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_originx.setDecimals(5)
        self.doubleSpinBox_originx.setMinimum(-1000.000000000000000)

        self.gridLayout_180.addWidget(self.doubleSpinBox_originx, 5, 2, 1, 1)

        self.lineEdit_42 = QLineEdit(self.frame_metadata)
        self.lineEdit_42.setObjectName(u"lineEdit_42")
        self.lineEdit_42.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_42.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_42, 5, 6, 1, 1)

        self.doubleSpinBox_originy = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_originy.setObjectName(u"doubleSpinBox_originy")
        self.doubleSpinBox_originy.setReadOnly(True)
        self.doubleSpinBox_originy.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_originy.setDecimals(5)
        self.doubleSpinBox_originy.setMinimum(-1000.000000000000000)

        self.gridLayout_180.addWidget(self.doubleSpinBox_originy, 5, 5, 1, 1)

        self.lineEdit_25 = QLineEdit(self.frame_metadata)
        self.lineEdit_25.setObjectName(u"lineEdit_25")
        self.lineEdit_25.setMinimumSize(QSize(90, 0))
        self.lineEdit_25.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_25, 3, 0, 1, 1)

        self.pushButton_SaveMetadata = QPushButton(self.frame_metadata)
        self.pushButton_SaveMetadata.setObjectName(u"pushButton_SaveMetadata")
        self.pushButton_SaveMetadata.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_180.addWidget(self.pushButton_SaveMetadata, 10, 2, 1, 6)

        self.lineEdit_26 = QLineEdit(self.frame_metadata)
        self.lineEdit_26.setObjectName(u"lineEdit_26")
        self.lineEdit_26.setMinimumSize(QSize(90, 0))
        self.lineEdit_26.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_26, 5, 0, 1, 1)

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

        self.lineEdit_44 = QLineEdit(self.frame_metadata)
        self.lineEdit_44.setObjectName(u"lineEdit_44")
        self.lineEdit_44.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_44.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_44, 9, 4, 1, 1)

        self.lineEdit_27 = QLineEdit(self.frame_metadata)
        self.lineEdit_27.setObjectName(u"lineEdit_27")
        self.lineEdit_27.setMinimumSize(QSize(90, 0))
        self.lineEdit_27.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_27, 6, 0, 1, 1)

        self.lineEdit_34 = QLineEdit(self.frame_metadata)
        self.lineEdit_34.setObjectName(u"lineEdit_34")
        self.lineEdit_34.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_34.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_34, 2, 1, 1, 1)

        self.lineEdit_28 = QLineEdit(self.frame_metadata)
        self.lineEdit_28.setObjectName(u"lineEdit_28")
        self.lineEdit_28.setMinimumSize(QSize(90, 0))
        self.lineEdit_28.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_28, 9, 0, 1, 1)

        self.lineEdit_41 = QLineEdit(self.frame_metadata)
        self.lineEdit_41.setObjectName(u"lineEdit_41")
        self.lineEdit_41.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_41.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_41, 3, 6, 1, 1)

        self.doubleSpinBox_spacingy = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_spacingy.setObjectName(u"doubleSpinBox_spacingy")
        self.doubleSpinBox_spacingy.setReadOnly(True)
        self.doubleSpinBox_spacingy.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_spacingy.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_spacingy, 3, 5, 1, 1)

        self.pushButton_cancel_metadata = QPushButton(self.frame_metadata)
        self.pushButton_cancel_metadata.setObjectName(u"pushButton_cancel_metadata")
        self.pushButton_cancel_metadata.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_180.addWidget(self.pushButton_cancel_metadata, 10, 0, 1, 1)

        self.lineEdit_38 = QLineEdit(self.frame_metadata)
        self.lineEdit_38.setObjectName(u"lineEdit_38")
        self.lineEdit_38.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_38.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_38, 3, 4, 1, 1)

        self.doubleSpinBox_maxIntensity = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_maxIntensity.setObjectName(u"doubleSpinBox_maxIntensity")
        self.doubleSpinBox_maxIntensity.setReadOnly(True)
        self.doubleSpinBox_maxIntensity.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_maxIntensity.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_maxIntensity, 9, 7, 1, 1)

        self.lineEdit_23 = QLineEdit(self.frame_metadata)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        self.lineEdit_23.setMinimumSize(QSize(90, 0))
        self.lineEdit_23.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_23, 2, 0, 1, 1)

        self.lineEdit_37 = QLineEdit(self.frame_metadata)
        self.lineEdit_37.setObjectName(u"lineEdit_37")
        self.lineEdit_37.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_37.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_37, 2, 4, 1, 1)

        self.lineEdit_39 = QLineEdit(self.frame_metadata)
        self.lineEdit_39.setObjectName(u"lineEdit_39")
        self.lineEdit_39.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_39.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_39, 5, 4, 1, 1)

        self.spinBox_dimx = QSpinBox(self.frame_metadata)
        self.spinBox_dimx.setObjectName(u"spinBox_dimx")
        self.spinBox_dimx.setReadOnly(True)
        self.spinBox_dimx.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_dimx.setMaximum(100000)

        self.gridLayout_180.addWidget(self.spinBox_dimx, 2, 2, 1, 1)

        self.doubleSpinBox_originz = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_originz.setObjectName(u"doubleSpinBox_originz")
        self.doubleSpinBox_originz.setReadOnly(True)
        self.doubleSpinBox_originz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_originz.setDecimals(5)
        self.doubleSpinBox_originz.setMinimum(-1000.000000000000000)

        self.gridLayout_180.addWidget(self.doubleSpinBox_originz, 5, 7, 1, 1)

        self.doubleSpinBox_minIntensity = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_minIntensity.setObjectName(u"doubleSpinBox_minIntensity")
        self.doubleSpinBox_minIntensity.setReadOnly(True)
        self.doubleSpinBox_minIntensity.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_minIntensity.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_minIntensity, 9, 5, 1, 1)

        self.lineEdit_36 = QLineEdit(self.frame_metadata)
        self.lineEdit_36.setObjectName(u"lineEdit_36")
        self.lineEdit_36.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_36.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_36, 5, 1, 1, 1)

        self.lineEdit_45 = QLineEdit(self.frame_metadata)
        self.lineEdit_45.setObjectName(u"lineEdit_45")
        self.lineEdit_45.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_45.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_45, 9, 6, 1, 1)

        self.comboBox = QComboBox(self.frame_metadata)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_180.addWidget(self.comboBox, 0, 0, 1, 8)

        self.lineEdit_40 = QLineEdit(self.frame_metadata)
        self.lineEdit_40.setObjectName(u"lineEdit_40")
        self.lineEdit_40.setMaximumSize(QSize(30, 16777215))
        self.lineEdit_40.setReadOnly(False)

        self.gridLayout_180.addWidget(self.lineEdit_40, 2, 6, 1, 1)

        self.doubleSpinBox_spacingx = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_spacingx.setObjectName(u"doubleSpinBox_spacingx")
        self.doubleSpinBox_spacingx.setReadOnly(True)
        self.doubleSpinBox_spacingx.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_spacingx.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_spacingx, 3, 2, 1, 1)

        self.doubleSpinBox_spacingz = QDoubleSpinBox(self.frame_metadata)
        self.doubleSpinBox_spacingz.setObjectName(u"doubleSpinBox_spacingz")
        self.doubleSpinBox_spacingz.setReadOnly(True)
        self.doubleSpinBox_spacingz.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_spacingz.setDecimals(5)

        self.gridLayout_180.addWidget(self.doubleSpinBox_spacingz, 3, 7, 1, 1)

        self.lineEdit_32 = QLineEdit(self.frame_metadata)
        self.lineEdit_32.setObjectName(u"lineEdit_32")
        self.lineEdit_32.setMinimumSize(QSize(90, 0))
        self.lineEdit_32.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_32, 8, 0, 1, 1)

        self.pushButton_reorient = QPushButton(self.frame_metadata)
        self.pushButton_reorient.setObjectName(u"pushButton_reorient")
        self.pushButton_reorient.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")
        self.pushButton_reorient.setCheckable(True)
        self.pushButton_reorient.setChecked(False)

        self.gridLayout_180.addWidget(self.pushButton_reorient, 6, 7, 1, 1)

        self.pushButton_changeSpacing = QPushButton(self.frame_metadata)
        self.pushButton_changeSpacing.setObjectName(u"pushButton_changeSpacing")
        self.pushButton_changeSpacing.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_180.addWidget(self.pushButton_changeSpacing, 4, 0, 1, 8)

        self.lineEdit_DicomOrient = QLineEdit(self.frame_metadata)
        self.lineEdit_DicomOrient.setObjectName(u"lineEdit_DicomOrient")
        self.lineEdit_DicomOrient.setReadOnly(True)

        self.gridLayout_180.addWidget(self.lineEdit_DicomOrient, 6, 3, 1, 4)


        self.gridLayout_173.addWidget(self.frame_metadata, 1, 0, 1, 1)

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
        QWidget.setTabOrder(self.histogram_label, self.lineEdit_52)
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
        QWidget.setTabOrder(self.lineEdit_38, self.doubleSpinBox_originx)
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
        QWidget.setTabOrder(self.lineEdit_37, self.doubleSpinBox_minIntensity)
        QWidget.setTabOrder(self.doubleSpinBox_minIntensity, self.lineEdit_34)
        QWidget.setTabOrder(self.lineEdit_34, self.pushButton_reorient)
        QWidget.setTabOrder(self.pushButton_reorient, self.lineEdit_DicomOrient)

        self.retranslateUi(tab_6)

        self.stackedWidget_4D.setCurrentIndex(0)
        self.histogram_label.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(tab_6)
    # setupUi

    def retranslateUi(self, tab_6):
#if QT_CONFIG(tooltip)
        self.groupBox_paintbrush.setToolTip(QCoreApplication.translate("tab_6", u"Manually paint or erase segmentation labels on the current slice.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_paintbrush.setTitle(QCoreApplication.translate("tab_6", u"Paintbrush", None))
#if QT_CONFIG(tooltip)
        self.pushButton_anatOK.setToolTip(QCoreApplication.translate("tab_6", u"Disabled until every anatomical region has been painted in all views", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_anatOK.setText(QCoreApplication.translate("tab_6", u"NEXT", None))
        self.plainTextEdit_MRID_2.setPlainText(QCoreApplication.translate("tab_6", u"Please paint all anatomical structures around the tags with the Paintbrush. Once this is done, please click NEXT", None))
#if QT_CONFIG(tooltip)
        self.pushButton_segOK.setToolTip(QCoreApplication.translate("tab_6", u"Finalizes MRID-tag/segmentation painting and generates the contrast heatmap. Unpainted tags are skipped rather than causing an error.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_segOK.setText(QCoreApplication.translate("tab_6", u"DONE", None))
        self.plainTextEdit_MRID_4.setPlainText(QCoreApplication.translate("tab_6", u"Please paint all MRID tags with the Paintbrush. Once this is done, please click DONE", None))
#if QT_CONFIG(tooltip)
        self.checkBox_Brush_MRID.setToolTip(QCoreApplication.translate("tab_6", u"Toggle the paintbrush tool for manually painting regions on the current view (e.g. forbidden areas).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_Brush_MRID.setText(QCoreApplication.translate("tab_6", u"Brush ON", None))
#if QT_CONFIG(tooltip)
        self.groupBox_28.setToolTip(QCoreApplication.translate("tab_6", u"Fine-tune the paintbrush: stroke shape, label opacity, and brush size.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_28.setTitle(QCoreApplication.translate("tab_6", u"Paintbrush Inspector", None))
#if QT_CONFIG(tooltip)
        self.groupBox_29.setToolTip(QCoreApplication.translate("tab_6", u"Choose whether the paintbrush stroke is square or round.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_29.setTitle(QCoreApplication.translate("tab_6", u"Brush Style", None))
#if QT_CONFIG(tooltip)
        self.paint_square_Post.setToolTip(QCoreApplication.translate("tab_6", u"Use a square paintbrush stroke.", None))
#endif // QT_CONFIG(tooltip)
        self.paint_square_Post.setText("")
#if QT_CONFIG(tooltip)
        self.paint_round_Post.setToolTip(QCoreApplication.translate("tab_6", u"Use a round paintbrush stroke.", None))
#endif // QT_CONFIG(tooltip)
        self.paint_round_Post.setText("")
#if QT_CONFIG(tooltip)
        self.groupBox_31.setToolTip(QCoreApplication.translate("tab_6", u"Sets how opaque the painted label overlay appears on top of the MRI.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_31.setTitle(QCoreApplication.translate("tab_6", u"Label Opacity", None))
#if QT_CONFIG(tooltip)
        self.sizeSlider_labelOcc.setToolTip(QCoreApplication.translate("tab_6", u"Adjusts the painted label overlay's opacity; mirrors the spin box next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_labelOcc.setToolTip(QCoreApplication.translate("tab_6", u"Type the label overlay opacity directly (0 = invisible, 1 = fully opaque).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_30.setToolTip(QCoreApplication.translate("tab_6", u"Sets the paintbrush stroke size, in voxels (1-20).", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_30.setTitle(QCoreApplication.translate("tab_6", u"Brush Size", None))
#if QT_CONFIG(tooltip)
        self.brush_size4d.setToolTip(QCoreApplication.translate("tab_6", u"Type the paintbrush size directly, in voxels (1-20); mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.brush_sizeSlider4d.setToolTip(QCoreApplication.translate("tab_6", u"Adjusts the paintbrush size, in voxels (1-20); mirrors the spin box next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_33.setToolTip(QCoreApplication.translate("tab_6", u"Choose which label the paintbrush paints, and which existing label it's allowed to paint over.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_33.setTitle(QCoreApplication.translate("tab_6", u"Segmentation Labels", None))
#if QT_CONFIG(tooltip)
        self.groupBox_35.setToolTip(QCoreApplication.translate("tab_6", u"Restrict painting to only overwrite this existing label (protects other labels from being painted over).", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_35.setTitle(QCoreApplication.translate("tab_6", u"Paint over", None))
#if QT_CONFIG(tooltip)
        self.comboBox_paintOver_Post.setToolTip(QCoreApplication.translate("tab_6", u"Restrict painting to only overwrite this existing label, or choose all labels to overwrite anything the brush passes over.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_47.setToolTip(QCoreApplication.translate("tab_6", u"Click a row to choose which label the paintbrush currently paints with.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_47.setTitle(QCoreApplication.translate("tab_6", u"Active Label", None))
        ___qtablewidgetitem = self.tableWidget_labels.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("tab_6", u"Idx", None));
        ___qtablewidgetitem1 = self.tableWidget_labels.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("tab_6", u"Color", None));
        ___qtablewidgetitem2 = self.tableWidget_labels.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("tab_6", u"Label", None));
#if QT_CONFIG(tooltip)
        self.groupBox_36.setToolTip(QCoreApplication.translate("tab_6", u"Shows the intensity histogram for the selected label's voxels.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_36.setTitle(QCoreApplication.translate("tab_6", u"Histogram", None))
#if QT_CONFIG(tooltip)
        self.groupBox_48.setToolTip(QCoreApplication.translate("tab_6", u"Choose which label (and which loaded data layer) the histogram above is computed from.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_48.setTitle(QCoreApplication.translate("tab_6", u"Label", None))
#if QT_CONFIG(tooltip)
        self.histogram_label.setToolTip(QCoreApplication.translate("tab_6", u"Choose which label's voxel intensities the histogram above shows (or 'All anat Regions').", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.paintbrush_dataview.setToolTip(QCoreApplication.translate("tab_6", u"Choose which loaded data layer the histogram above is computed from.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_52.setText(QCoreApplication.translate("tab_6", u"y", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_fovy.setToolTip(QCoreApplication.translate("tab_6", u"Field of view along Y, in mm \u2014 editing this rescales the Y voxel spacing to match (voxel count stays fixed).", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_fovy.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
        self.lineEdit_56.setText(QCoreApplication.translate("tab_6", u"z", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_spay.setToolTip(QCoreApplication.translate("tab_6", u"Voxel spacing along Y, in mm \u2014 editing this rescales the Y field of view to match (voxel count stays fixed).", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_spay.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
#if QT_CONFIG(tooltip)
        self.spinBox_dimey.setToolTip(QCoreApplication.translate("tab_6", u"Number of voxels along Y in the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_SaveSpacing.setToolTip(QCoreApplication.translate("tab_6", u"Apply the edited spacing/field-of-view values to the volume's metadata.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_SaveSpacing.setText(QCoreApplication.translate("tab_6", u"Save new Metadata", None))
        self.lineEdit_55.setText(QCoreApplication.translate("tab_6", u"z", None))
#if QT_CONFIG(tooltip)
        self.spinBox_dimez.setToolTip(QCoreApplication.translate("tab_6", u"Number of voxels along Z in the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_50.setText(QCoreApplication.translate("tab_6", u"x", None))
        self.lineEdit_47.setText(QCoreApplication.translate("tab_6", u"Spacing", None))
        self.lineEdit_54.setText(QCoreApplication.translate("tab_6", u"y", None))
        self.lineEdit_53.setText(QCoreApplication.translate("tab_6", u"y", None))
        self.lineEdit_48.setText(QCoreApplication.translate("tab_6", u"Field of View", None))
        self.lineEdit_51.setText(QCoreApplication.translate("tab_6", u"x", None))
        self.lineEdit_46.setText(QCoreApplication.translate("tab_6", u"Image Size", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_fovz.setToolTip(QCoreApplication.translate("tab_6", u"Field of view along Z, in mm \u2014 editing this rescales the Z voxel spacing to match (voxel count stays fixed).", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_fovz.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_spax.setToolTip(QCoreApplication.translate("tab_6", u"Voxel spacing along X, in mm \u2014 editing this rescales the X field of view to match (voxel count stays fixed).", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_spax.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
#if QT_CONFIG(tooltip)
        self.spinBox_dimex.setToolTip(QCoreApplication.translate("tab_6", u"Number of voxels along X in the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_cancel_spacing.setToolTip(QCoreApplication.translate("tab_6", u"Close this dialog without applying the spacing/field-of-view changes.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_cancel_spacing.setText(QCoreApplication.translate("tab_6", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_fovx.setToolTip(QCoreApplication.translate("tab_6", u"Field of view (mm) along this axis in the Change Spacing popup \u2014 editing it recalculates the matching spacing value.", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_fovx.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
        self.lineEdit_49.setText(QCoreApplication.translate("tab_6", u"x", None))
        self.lineEdit_57.setText(QCoreApplication.translate("tab_6", u"z", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_spaz.setToolTip(QCoreApplication.translate("tab_6", u"New voxel spacing (mm) along the z axis to stage before saving \u2014 editing it recalculates the matching field of view.", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_spaz.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
#if QT_CONFIG(tooltip)
        self.spinBox_dimz.setToolTip(QCoreApplication.translate("tab_6", u"Number of voxels along the z axis of the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_originx.setToolTip(QCoreApplication.translate("tab_6", u"Volume origin coordinate (mm) along the x axis, read from the file header (read-only).", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_42.setText(QCoreApplication.translate("tab_6", u"z:", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_originy.setToolTip(QCoreApplication.translate("tab_6", u"Volume origin coordinate (mm) along the y axis, read from the file header (read-only).", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_25.setText(QCoreApplication.translate("tab_6", u"Spacing", None))
#if QT_CONFIG(tooltip)
        self.pushButton_SaveMetadata.setToolTip(QCoreApplication.translate("tab_6", u"Writes the edited voxel spacing to the NIfTI file on disk and reloads the volume; shows 'OK' instead when nothing has changed.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_SaveMetadata.setText(QCoreApplication.translate("tab_6", u"Save New Settings \n"
" and Reload Image", None))
        self.lineEdit_26.setText(QCoreApplication.translate("tab_6", u"Origin", None))
        self.lineEdit_35.setText(QCoreApplication.translate("tab_6", u"x:", None))
#if QT_CONFIG(tooltip)
        self.spinBox_dimy.setToolTip(QCoreApplication.translate("tab_6", u"Number of voxels along the y axis of the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_44.setText(QCoreApplication.translate("tab_6", u"min", None))
        self.lineEdit_27.setText(QCoreApplication.translate("tab_6", u"Orientation", None))
        self.lineEdit_34.setText(QCoreApplication.translate("tab_6", u"x:", None))
        self.lineEdit_28.setText(QCoreApplication.translate("tab_6", u"Intensity Range", None))
        self.lineEdit_41.setText(QCoreApplication.translate("tab_6", u"z:", None))
        self.doubleSpinBox_spacingy.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
#if QT_CONFIG(tooltip)
        self.pushButton_cancel_metadata.setToolTip(QCoreApplication.translate("tab_6", u"Close this metadata panel without changing anything.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_cancel_metadata.setText(QCoreApplication.translate("tab_6", u"Cancel", None))
        self.lineEdit_38.setText(QCoreApplication.translate("tab_6", u"y:", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_maxIntensity.setToolTip(QCoreApplication.translate("tab_6", u"Highest voxel intensity value in the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_23.setText(QCoreApplication.translate("tab_6", u"Dimensions", None))
        self.lineEdit_37.setText(QCoreApplication.translate("tab_6", u"y:", None))
        self.lineEdit_39.setText(QCoreApplication.translate("tab_6", u"y:", None))
#if QT_CONFIG(tooltip)
        self.spinBox_dimx.setToolTip(QCoreApplication.translate("tab_6", u"Number of voxels along the x axis of the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_originz.setToolTip(QCoreApplication.translate("tab_6", u"Volume origin coordinate (mm) along the z axis, read from the file header (read-only).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_minIntensity.setToolTip(QCoreApplication.translate("tab_6", u"Lowest voxel intensity value in the loaded volume (read-only).", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_36.setText(QCoreApplication.translate("tab_6", u"x:", None))
        self.lineEdit_45.setText(QCoreApplication.translate("tab_6", u"max", None))
        self.lineEdit_40.setText(QCoreApplication.translate("tab_6", u"z:", None))
        self.doubleSpinBox_spacingx.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
        self.doubleSpinBox_spacingz.setSuffix(QCoreApplication.translate("tab_6", u"mm", None))
        self.lineEdit_32.setText(QCoreApplication.translate("tab_6", u"Direction", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reorient.setToolTip(QCoreApplication.translate("tab_6", u"Reloads the volume mirrored between RAS and LAS convention (flips left/right). Does not affect the underlying registration or trajectory-planning data, which always stay in RAS.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reorient.setText(QCoreApplication.translate("tab_6", u"Reorient to RAS", None))
#if QT_CONFIG(tooltip)
        self.pushButton_changeSpacing.setToolTip(QCoreApplication.translate("tab_6", u"Open a popup to stage a new voxel spacing before saving it to the file.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_changeSpacing.setText(QCoreApplication.translate("tab_6", u"Change Spacing", None))
        pass
    # retranslateUi

