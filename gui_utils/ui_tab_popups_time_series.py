# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tab_popups_time_series.ui'
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
    QGridLayout, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpinBox, QStackedWidget, QTabWidget,
    QTableView, QTableWidget, QTableWidgetItem, QTextBrowser,
    QTextEdit, QToolBox, QToolButton, QWidget)

class Ui_tab_15(object):
    def setupUi(self, tab_15):
        if not tab_15.objectName():
            tab_15.setObjectName(u"tab_15")
        self.gridLayout_104 = QGridLayout(tab_15)
        self.gridLayout_104.setObjectName(u"gridLayout_104")
        self.groupBox_register = QGroupBox(tab_15)
        self.groupBox_register.setObjectName(u"groupBox_register")
        self.gridLayout_14 = QGridLayout(self.groupBox_register)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
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


        self.gridLayout_14.addWidget(self.groupBox_17, 2, 0, 1, 1)

        self.groupBox_27 = QGroupBox(self.groupBox_register)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.groupBox_27.setEnabled(True)
        self.gridLayout_2 = QGridLayout(self.groupBox_27)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox_movingimg = QComboBox(self.groupBox_27)
        self.comboBox_movingimg.setObjectName(u"comboBox_movingimg")
        self.comboBox_movingimg.setEnabled(True)

        self.gridLayout_2.addWidget(self.comboBox_movingimg, 2, 1, 1, 1)

        self.textEdit_pixels = QTextEdit(self.groupBox_27)
        self.textEdit_pixels.setObjectName(u"textEdit_pixels")
        self.textEdit_pixels.setMaximumSize(QSize(16777215, 50))
        self.textEdit_pixels.setStyleSheet(u"color: rgb(170, 0, 0);")

        self.gridLayout_2.addWidget(self.textEdit_pixels, 3, 1, 1, 1)

        self.textEdit_6 = QTextEdit(self.groupBox_27)
        self.textEdit_6.setObjectName(u"textEdit_6")
        self.textEdit_6.setMaximumSize(QSize(16777215, 50))

        self.gridLayout_2.addWidget(self.textEdit_6, 0, 1, 1, 1)

        self.pushButton_loadOtherImage = QPushButton(self.groupBox_27)
        self.pushButton_loadOtherImage.setObjectName(u"pushButton_loadOtherImage")
        self.pushButton_loadOtherImage.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_2.addWidget(self.pushButton_loadOtherImage, 1, 1, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_27, 0, 0, 1, 2)

        self.pushButton_registration = QPushButton(self.groupBox_register)
        self.pushButton_registration.setObjectName(u"pushButton_registration")
        self.pushButton_registration.setEnabled(False)
        self.pushButton_registration.setAcceptDrops(False)
        self.pushButton_registration.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_14.addWidget(self.pushButton_registration, 3, 1, 1, 1)

        self.pushButton_regCancel = QPushButton(self.groupBox_register)
        self.pushButton_regCancel.setObjectName(u"pushButton_regCancel")

        self.gridLayout_14.addWidget(self.pushButton_regCancel, 3, 0, 1, 1)

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


        self.gridLayout_14.addWidget(self.groupBox_26, 2, 1, 1, 1)

        self.comboBox_regitstration_metric = QComboBox(self.groupBox_register)
        self.comboBox_regitstration_metric.addItem("")
        self.comboBox_regitstration_metric.addItem("")
        self.comboBox_regitstration_metric.addItem("")
        self.comboBox_regitstration_metric.setObjectName(u"comboBox_regitstration_metric")

        self.gridLayout_14.addWidget(self.comboBox_regitstration_metric, 1, 0, 1, 2)


        self.gridLayout_104.addWidget(self.groupBox_register, 1, 0, 1, 1)

        self.groupBox_resample = QGroupBox(tab_15)
        self.groupBox_resample.setObjectName(u"groupBox_resample")
        self.gridLayout_17 = QGridLayout(self.groupBox_resample)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.pushButton_resample100um = QPushButton(self.groupBox_resample)
        self.pushButton_resample100um.setObjectName(u"pushButton_resample100um")
        self.pushButton_resample100um.setAutoFillBackground(False)
        self.pushButton_resample100um.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_17.addWidget(self.pushButton_resample100um, 2, 0, 1, 3)

        self.pushButton_openfile100um = QPushButton(self.groupBox_resample)
        self.pushButton_openfile100um.setObjectName(u"pushButton_openfile100um")
        self.pushButton_openfile100um.setEnabled(False)
        self.pushButton_openfile100um.setAutoFillBackground(False)
        self.pushButton_openfile100um.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_17.addWidget(self.pushButton_openfile100um, 6, 2, 1, 1)

        self.pushButton_done = QPushButton(self.groupBox_resample)
        self.pushButton_done.setObjectName(u"pushButton_done")

        self.gridLayout_17.addWidget(self.pushButton_done, 6, 0, 1, 2)

        self.pushButton_resample25um = QPushButton(self.groupBox_resample)
        self.pushButton_resample25um.setObjectName(u"pushButton_resample25um")
        self.pushButton_resample25um.setAutoFillBackground(False)
        self.pushButton_resample25um.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

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

        self.groupBox_paintbrush_3d = QGroupBox(tab_15)
        self.groupBox_paintbrush_3d.setObjectName(u"groupBox_paintbrush_3d")
        self.gridLayout_18 = QGridLayout(self.groupBox_paintbrush_3d)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.groupBox_14 = QGroupBox(self.groupBox_paintbrush_3d)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.gridLayout_12 = QGridLayout(self.groupBox_14)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.paint_square = QToolButton(self.groupBox_14)
        self.paint_square.setObjectName(u"paint_square")
        icon = QIcon()
        icon.addFile(u"Icons/mri/square.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paint_square.setIcon(icon)
        self.paint_square.setIconSize(QSize(20, 20))
        self.paint_square.setCheckable(True)
        self.paint_square.setChecked(True)
        self.paint_square.setAutoExclusive(False)

        self.gridLayout_12.addWidget(self.paint_square, 0, 0, 1, 1)

        self.paint_round = QToolButton(self.groupBox_14)
        self.paint_round.setObjectName(u"paint_round")
        self.paint_round.setEnabled(True)
        icon1 = QIcon()
        icon1.addFile(u"Icons/mri/circle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paint_round.setIcon(icon1)
        self.paint_round.setIconSize(QSize(20, 20))
        self.paint_round.setCheckable(True)
        self.paint_round.setAutoExclusive(False)

        self.gridLayout_12.addWidget(self.paint_round, 0, 1, 1, 1)


        self.gridLayout_18.addWidget(self.groupBox_14, 1, 0, 1, 1)

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

        self.pushButton_paint_done = QPushButton(self.groupBox_paintbrush_3d)
        self.pushButton_paint_done.setObjectName(u"pushButton_paint_done")
        self.pushButton_paint_done.setMinimumSize(QSize(0, 50))
        self.pushButton_paint_done.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_18.addWidget(self.pushButton_paint_done, 4, 0, 1, 2)

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
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.checkBox_Brush.setFont(font)
        self.checkBox_Brush.setIconSize(QSize(16, 16))
        self.checkBox_Brush.setChecked(True)

        self.gridLayout_18.addWidget(self.checkBox_Brush, 0, 0, 1, 1)

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
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_labels3D.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_labels3D.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_labels3D.setHorizontalHeaderItem(2, __qtablewidgetitem2)
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

        self.gridLayout_18.setColumnStretch(0, 1)
        self.gridLayout_18.setColumnStretch(1, 1)

        self.gridLayout_104.addWidget(self.groupBox_paintbrush_3d, 1, 4, 1, 1)

        self.groupBox_measurement = QGroupBox(tab_15)
        self.groupBox_measurement.setObjectName(u"groupBox_measurement")
        self.gridLayout_9 = QGridLayout(self.groupBox_measurement)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.checkBox_measurement = QCheckBox(self.groupBox_measurement)
        self.checkBox_measurement.setObjectName(u"checkBox_measurement")
        self.checkBox_measurement.setEnabled(True)
        font1 = QFont()
        font1.setPointSize(25)
        font1.setBold(False)
        self.checkBox_measurement.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(u"Icons/mri/measure.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.checkBox_measurement.setIcon(icon2)
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
        self.pushButton_deleteMeasurement.setStyleSheet(u"")

        self.gridLayout_19.addWidget(self.pushButton_deleteMeasurement, 1, 1, 1, 1)

        self.tableWidget_meaurement = QTableWidget(self.groupBox_)
        self.tableWidget_meaurement.setObjectName(u"tableWidget_meaurement")
        self.tableWidget_meaurement.setMinimumSize(QSize(280, 0))
        self.tableWidget_meaurement.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_meaurement.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout_19.addWidget(self.tableWidget_meaurement, 0, 0, 1, 2)


        self.gridLayout_9.addWidget(self.groupBox_, 1, 0, 1, 1)


        self.gridLayout_104.addWidget(self.groupBox_measurement, 1, 3, 1, 1)

        self.groupBox_23 = QGroupBox(tab_15)
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
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_30.setFont(font2)

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
        self.label_29.setFont(font2)

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
        self.label_31.setFont(font2)

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
        self.label_32.setFont(font2)

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
        self.label_34.setFont(font2)

        self.gridLayout_154.addWidget(self.label_34, 2, 0, 1, 1)

        self.label_33 = QLabel(self.tab_30)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font2)

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

        self.ManualContrastAdjustments = QGroupBox(tab_15)
        self.ManualContrastAdjustments.setObjectName(u"ManualContrastAdjustments")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ManualContrastAdjustments.sizePolicy().hasHeightForWidth())
        self.ManualContrastAdjustments.setSizePolicy(sizePolicy)
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
        self.label_11.setFont(font2)

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
        self.label_12.setFont(font2)

        self.gridLayout_101.addWidget(self.label_12, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_10, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_102 = QGridLayout(self.tab_11)
        self.gridLayout_102.setObjectName(u"gridLayout_102")
        self.label_17 = QLabel(self.tab_11)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font2)

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
        self.label_18.setFont(font2)

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
        self.label_19.setFont(font2)

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
        self.label_20.setFont(font2)

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
        self.label_13.setFont(font2)

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
        self.label_14.setFont(font2)

        self.gridLayout_117.addWidget(self.label_14, 0, 0, 1, 1)

        self.tabWidget_5.addTab(self.tab_16, "")
        self.tab_17 = QWidget()
        self.tab_17.setObjectName(u"tab_17")
        self.gridLayout_118 = QGridLayout(self.tab_17)
        self.gridLayout_118.setObjectName(u"gridLayout_118")
        self.label_21 = QLabel(self.tab_17)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font2)

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
        self.label_22.setFont(font2)

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
        self.label_23.setFont(font2)

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
        self.label_24.setFont(font2)

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
        self.label_15.setFont(font2)

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
        self.label_16.setFont(font2)

        self.gridLayout_121.addWidget(self.label_16, 0, 0, 1, 1)

        self.tabWidget_6.addTab(self.tab_19, "")
        self.tab_20 = QWidget()
        self.tab_20.setObjectName(u"tab_20")
        self.gridLayout_122 = QGridLayout(self.tab_20)
        self.gridLayout_122.setObjectName(u"gridLayout_122")
        self.label_25 = QLabel(self.tab_20)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font2)

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
        self.label_26.setFont(font2)

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
        self.label_27.setFont(font2)

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
        self.label_28.setFont(font2)

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

        self.groupBox_segmentation = QGroupBox(tab_15)
        self.groupBox_segmentation.setObjectName(u"groupBox_segmentation")
        self.gridLayout_5 = QGridLayout(self.groupBox_segmentation)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.textEdit_SAMRI_reg = QTextEdit(self.groupBox_segmentation)
        self.textEdit_SAMRI_reg.setObjectName(u"textEdit_SAMRI_reg")
        self.textEdit_SAMRI_reg.setMaximumSize(QSize(300, 100))

        self.gridLayout_5.addWidget(self.textEdit_SAMRI_reg, 0, 0, 1, 1)

        self.stackedWidget_segmentation = QStackedWidget(self.groupBox_segmentation)
        self.stackedWidget_segmentation.setObjectName(u"stackedWidget_segmentation")
        self.stackedWidget_segmentation.setEnabled(True)
        self.stackedWidget_segmentation.setMaximumSize(QSize(300, 16777215))
        self.stackedWidget_segmentation.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")
        self.page_13 = QWidget()
        self.page_13.setObjectName(u"page_13")
        self.gridLayout_152 = QGridLayout(self.page_13)
        self.gridLayout_152.setObjectName(u"gridLayout_152")
        self.pushButton_Next1 = QPushButton(self.page_13)
        self.pushButton_Next1.setObjectName(u"pushButton_Next1")
        self.pushButton_Next1.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_152.addWidget(self.pushButton_Next1, 3, 1, 1, 1)

        self.pushButton_Back1 = QPushButton(self.page_13)
        self.pushButton_Back1.setObjectName(u"pushButton_Back1")
        self.pushButton_Back1.setEnabled(False)

        self.gridLayout_152.addWidget(self.pushButton_Back1, 3, 0, 1, 1)

        self.checkBox_threshold = QCheckBox(self.page_13)
        self.checkBox_threshold.setObjectName(u"checkBox_threshold")
        self.checkBox_threshold.setEnabled(True)
        font3 = QFont()
        font3.setPointSize(12)
        self.checkBox_threshold.setFont(font3)
        self.checkBox_threshold.setChecked(True)

        self.gridLayout_152.addWidget(self.checkBox_threshold, 1, 0, 1, 2)

        self.textBrowser_5 = QTextBrowser(self.page_13)
        self.textBrowser_5.setObjectName(u"textBrowser_5")
        self.textBrowser_5.setMaximumSize(QSize(16777215, 50))
        self.textBrowser_5.setStyleSheet(u"")
        self.textBrowser_5.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser_5.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gridLayout_152.addWidget(self.textBrowser_5, 0, 0, 1, 2)

        self.frame_15 = QFrame(self.page_13)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMaximumSize(QSize(16777215, 400))
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.gridLayout_28 = QGridLayout(self.frame_15)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.groupBox_7 = QGroupBox(self.frame_15)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMaximumSize(QSize(16777215, 150))
        self.groupBox_7.setFont(font3)
        self.gridLayout_29 = QGridLayout(self.groupBox_7)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.radioButton_bounded = QRadioButton(self.groupBox_7)
        self.radioButton_bounded.setObjectName(u"radioButton_bounded")
        self.radioButton_bounded.setFont(font3)
        self.radioButton_bounded.setChecked(True)

        self.gridLayout_29.addWidget(self.radioButton_bounded, 0, 0, 1, 1)

        self.radioButton_lower = QRadioButton(self.groupBox_7)
        self.radioButton_lower.setObjectName(u"radioButton_lower")
        self.radioButton_lower.setFont(font3)

        self.gridLayout_29.addWidget(self.radioButton_lower, 1, 0, 1, 1)

        self.radioButton_upper = QRadioButton(self.groupBox_7)
        self.radioButton_upper.setObjectName(u"radioButton_upper")
        self.radioButton_upper.setFont(font3)

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

        self.pushButton_Next2 = QPushButton(self.initialization)
        self.pushButton_Next2.setObjectName(u"pushButton_Next2")
        self.pushButton_Next2.setEnabled(False)
        self.pushButton_Next2.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_153.addWidget(self.pushButton_Next2, 5, 2, 1, 1)

        self.pushButton_Back2 = QPushButton(self.initialization)
        self.pushButton_Back2.setObjectName(u"pushButton_Back2")
        self.pushButton_Back2.setEnabled(True)

        self.gridLayout_153.addWidget(self.pushButton_Back2, 5, 0, 1, 2)

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

        self.pushButton_delete = QPushButton(self.groupBox_16)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_159.addWidget(self.pushButton_delete, 1, 0, 1, 1)


        self.gridLayout_153.addWidget(self.groupBox_16, 3, 0, 1, 3)

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

        self.pushButton_addBubbles = QPushButton(self.initialization)
        self.pushButton_addBubbles.setObjectName(u"pushButton_addBubbles")
        self.pushButton_addBubbles.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_153.addWidget(self.pushButton_addBubbles, 1, 0, 1, 3)

        self.stackedWidget_segmentation.addWidget(self.initialization)
        self.page_16 = QWidget()
        self.page_16.setObjectName(u"page_16")
        self.gridLayout_160 = QGridLayout(self.page_16)
        self.gridLayout_160.setObjectName(u"gridLayout_160")
        self.pushButton_Back3 = QPushButton(self.page_16)
        self.pushButton_Back3.setObjectName(u"pushButton_Back3")
        self.pushButton_Back3.setEnabled(True)

        self.gridLayout_160.addWidget(self.pushButton_Back3, 5, 0, 1, 1)

        self.pushButton_Finish = QPushButton(self.page_16)
        self.pushButton_Finish.setObjectName(u"pushButton_Finish")
        self.pushButton_Finish.setEnabled(True)
        self.pushButton_Finish.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_160.addWidget(self.pushButton_Finish, 5, 3, 1, 1)

        self.textBrowser_7 = QTextBrowser(self.page_16)
        self.textBrowser_7.setObjectName(u"textBrowser_7")
        self.textBrowser_7.setMinimumSize(QSize(185, 0))
        self.textBrowser_7.setMaximumSize(QSize(3007, 50))
        self.textBrowser_7.setStyleSheet(u"")
        self.textBrowser_7.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser_7.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gridLayout_160.addWidget(self.textBrowser_7, 0, 0, 1, 1)

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

        self.groupBox_65 = QGroupBox(self.page_16)
        self.groupBox_65.setObjectName(u"groupBox_65")
        self.groupBox_65.setMaximumSize(QSize(16777215, 100))
        self.gridLayout_163 = QGridLayout(self.groupBox_65)
        self.gridLayout_163.setObjectName(u"gridLayout_163")
        self.toolButton_backwardEvo = QToolButton(self.groupBox_65)
        self.toolButton_backwardEvo.setObjectName(u"toolButton_backwardEvo")
        self.toolButton_backwardEvo.setEnabled(True)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekBackward))
        self.toolButton_backwardEvo.setIcon(icon3)
        self.toolButton_backwardEvo.setIconSize(QSize(20, 20))

        self.gridLayout_163.addWidget(self.toolButton_backwardEvo, 0, 0, 1, 1)

        self.toolButton_forwardEvo = QToolButton(self.groupBox_65)
        self.toolButton_forwardEvo.setObjectName(u"toolButton_forwardEvo")
        self.toolButton_forwardEvo.setEnabled(True)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekForward))
        self.toolButton_forwardEvo.setIcon(icon4)
        self.toolButton_forwardEvo.setIconSize(QSize(20, 20))

        self.gridLayout_163.addWidget(self.toolButton_forwardEvo, 0, 2, 1, 1)

        self.toolButton_runEvo = QToolButton(self.groupBox_65)
        self.toolButton_runEvo.setObjectName(u"toolButton_runEvo")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
        self.toolButton_runEvo.setIcon(icon5)
        self.toolButton_runEvo.setIconSize(QSize(20, 20))
        self.toolButton_runEvo.setCheckable(True)
        self.toolButton_runEvo.setChecked(False)

        self.gridLayout_163.addWidget(self.toolButton_runEvo, 0, 1, 1, 1)

        self.lineEdit_evolution_status = QLineEdit(self.groupBox_65)
        self.lineEdit_evolution_status.setObjectName(u"lineEdit_evolution_status")
        self.lineEdit_evolution_status.setReadOnly(True)

        self.gridLayout_163.addWidget(self.lineEdit_evolution_status, 1, 0, 1, 3)


        self.gridLayout_160.addWidget(self.groupBox_65, 1, 0, 1, 4)

        self.stackedWidget_segmentation.addWidget(self.page_16)

        self.gridLayout_5.addWidget(self.stackedWidget_segmentation, 1, 0, 1, 1)


        self.gridLayout_104.addWidget(self.groupBox_segmentation, 0, 2, 1, 2)

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
        QWidget.setTabOrder(self.pushButton_Next2, self.tableView_activeBub)
        QWidget.setTabOrder(self.tableView_activeBub, self.doubleSpinBox_SegStep)
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

        self.retranslateUi(tab_15)

        self.comboBox_coarest.setCurrentIndex(0)
        self.comboBox_movingimg.setCurrentIndex(-1)
        self.comboBox_finest.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.contrast_data.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_5.setCurrentIndex(2)
        self.tabWidget_6.setCurrentIndex(0)
        self.stackedWidget_segmentation.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(tab_15)
    # setupUi

    def retranslateUi(self, tab_15):
#if QT_CONFIG(tooltip)
        self.groupBox_register.setToolTip(QCoreApplication.translate("tab_15", u"Rigidly register another image onto the currently loaded MRI so both share the same space.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_register.setTitle(QCoreApplication.translate("tab_15", u"Registration (Rigid Transformation)", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("tab_15", u"Coarsest Level", None))
        self.comboBox_coarest.setItemText(0, QCoreApplication.translate("tab_15", u"8x", None))
        self.comboBox_coarest.setItemText(1, QCoreApplication.translate("tab_15", u"4x", None))
        self.comboBox_coarest.setItemText(2, QCoreApplication.translate("tab_15", u"2x", None))
        self.comboBox_coarest.setItemText(3, QCoreApplication.translate("tab_15", u"1x", None))

#if QT_CONFIG(tooltip)
        self.comboBox_coarest.setToolTip(QCoreApplication.translate("tab_15", u"Coarsest pyramid level to start registration from. For already well-aligned images, coarse levels can converge to a wrong result -- try a lower coarsest/finest setting (closer to 1x) if registration looks wrong.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_27.setTitle(QCoreApplication.translate("tab_15", u"Moving Image", None))
#if QT_CONFIG(tooltip)
        self.comboBox_movingimg.setToolTip(QCoreApplication.translate("tab_15", u"Select which loaded image to register onto the main file as the moving image.", None))
#endif // QT_CONFIG(tooltip)
        self.textEdit_pixels.setHtml(QCoreApplication.translate("tab_15", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:700;\">Please select other file. The MRI Scan needs at least 4pixels in each direction.</span></p></body></html>", None))
        self.textEdit_6.setHtml(QCoreApplication.translate("tab_15", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">If none is selectable, please load Another Image!</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_loadOtherImage.setToolTip(QCoreApplication.translate("tab_15", u"Add another image file to register against the main file.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_loadOtherImage.setText(QCoreApplication.translate("tab_15", u"Load Another Image", None))
#if QT_CONFIG(tooltip)
        self.pushButton_registration.setToolTip(QCoreApplication.translate("tab_15", u"Runs rigid registration of the selected moving image onto the main image. If the result looks wrong, retry with a coarser finest level when prompted.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_registration.setText(QCoreApplication.translate("tab_15", u"Run Registration", None))
#if QT_CONFIG(tooltip)
        self.pushButton_regCancel.setToolTip(QCoreApplication.translate("tab_15", u"Close the registration dialog without registering.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_regCancel.setText(QCoreApplication.translate("tab_15", u"Cancel", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("tab_15", u"Finest Level", None))
        self.comboBox_finest.setItemText(0, QCoreApplication.translate("tab_15", u"1x", None))
        self.comboBox_finest.setItemText(1, QCoreApplication.translate("tab_15", u"2x", None))
        self.comboBox_finest.setItemText(2, QCoreApplication.translate("tab_15", u"4x", None))

#if QT_CONFIG(tooltip)
        self.comboBox_finest.setToolTip(QCoreApplication.translate("tab_15", u"Finest pyramid level to end registration at. Must not be coarser than the coarsest-level setting. Stopping before 1x (full resolution) can help if registration converges to a wrong result on already well-aligned images.", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_regitstration_metric.setItemText(0, QCoreApplication.translate("tab_15", u"NMI", None))
        self.comboBox_regitstration_metric.setItemText(1, QCoreApplication.translate("tab_15", u"NCC", None))
        self.comboBox_regitstration_metric.setItemText(2, QCoreApplication.translate("tab_15", u"SSD", None))

#if QT_CONFIG(tooltip)
        self.comboBox_regitstration_metric.setToolTip(QCoreApplication.translate("tab_15", u"Image similarity metric: NMI (Normalised Mutual Information, works across different contrasts/modalities), NCC (Normalised Cross-Correlation, radius 4x4x4), or SSD (Sum of Squared Differences, same-contrast images only).", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_resample.setTitle(QCoreApplication.translate("tab_15", u"Resample", None))
#if QT_CONFIG(tooltip)
        self.pushButton_resample100um.setToolTip(QCoreApplication.translate("tab_15", u"Resample the selected file to 100\u00b5m isotropic spacing.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resample100um.setText(QCoreApplication.translate("tab_15", u"Resample 100um", None))
#if QT_CONFIG(tooltip)
        self.pushButton_openfile100um.setToolTip(QCoreApplication.translate("tab_15", u"Open the resampled 100\u00b5m file as the new main image.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_openfile100um.setText(QCoreApplication.translate("tab_15", u"Done, open \n"
"resampled 100um file", None))
#if QT_CONFIG(tooltip)
        self.pushButton_done.setToolTip(QCoreApplication.translate("tab_15", u"Close this dialog.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_done.setText(QCoreApplication.translate("tab_15", u"Done", None))
#if QT_CONFIG(tooltip)
        self.pushButton_resample25um.setToolTip(QCoreApplication.translate("tab_15", u"Resample the selected file to 25\u00b5m isotropic spacing.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resample25um.setText(QCoreApplication.translate("tab_15", u"Resample 25um", None))
#if QT_CONFIG(tooltip)
        self.comboBox_resamplefiles.setToolTip(QCoreApplication.translate("tab_15", u"Choose which loaded file to resample.", None))
#endif // QT_CONFIG(tooltip)
        self.textBrowser_4.setHtml(QCoreApplication.translate("tab_15", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Please select the file to resample!<br />Click on the buttons below to resample the data, after it is directly saved in the directory.</span></p></body></html>", None))
        self.groupBox_paintbrush_3d.setTitle(QCoreApplication.translate("tab_15", u"Paintbrush", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("tab_15", u"Brush Style", None))
#if QT_CONFIG(tooltip)
        self.paint_square.setToolTip(QCoreApplication.translate("tab_15", u"Use a square brush.", None))
#endif // QT_CONFIG(tooltip)
        self.paint_square.setText("")
#if QT_CONFIG(tooltip)
        self.paint_round.setToolTip(QCoreApplication.translate("tab_15", u"Use a round brush.", None))
#endif // QT_CONFIG(tooltip)
        self.paint_round.setText("")
        self.groupBox_20.setTitle(QCoreApplication.translate("tab_15", u"Overall label opacity", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_labelOcc3d.setToolTip(QCoreApplication.translate("tab_15", u"Opacity of the segmentation label overlay (0 = invisible, 1 = fully opaque); linked to the slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sizeSlider_labelOcc3d.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust the segmentation label overlay's opacity; linked to the spin box above.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_paint_done.setToolTip(QCoreApplication.translate("tab_15", u"Finish painting and continue on to trajectory planning.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_paint_done.setText(QCoreApplication.translate("tab_15", u"Continue with Trajectory Planning", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("tab_15", u"Brush Size", None))
#if QT_CONFIG(tooltip)
        self.brush_size3d.setToolTip(QCoreApplication.translate("tab_15", u"Diameter of the paintbrush, in pixels; linked to the slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.brush_sizeSlider3d.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust the paintbrush diameter; linked to the spin box above.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_Brush.setText(QCoreApplication.translate("tab_15", u"Brush ON", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("tab_15", u"Segmentation Labels", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("tab_15", u"Paint over", None))
#if QT_CONFIG(tooltip)
        self.comboBox_paintOver.setToolTip(QCoreApplication.translate("tab_15", u"Restrict new brush strokes to only overwrite pixels currently assigned to this label (or paint over all/none).", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_50.setTitle(QCoreApplication.translate("tab_15", u"Active Label", None))
        ___qtablewidgetitem = self.tableWidget_labels3D.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("tab_15", u"Idx", None));
        ___qtablewidgetitem1 = self.tableWidget_labels3D.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("tab_15", u"Color", None));
        ___qtablewidgetitem2 = self.tableWidget_labels3D.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("tab_15", u"Label", None));
        self.groupBox_measurement.setTitle(QCoreApplication.translate("tab_15", u"Measurement", None))
#if QT_CONFIG(tooltip)
        self.checkBox_measurement.setToolTip(QCoreApplication.translate("tab_15", u"Toggle the distance-measurement tool for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_measurement.setText(QCoreApplication.translate("tab_15", u" OFF", None))
        self.groupBox_.setTitle(QCoreApplication.translate("tab_15", u"Measurement Table", None))
        self.comboBox_measurementColors.setItemText(0, QCoreApplication.translate("tab_15", u"Red", None))
        self.comboBox_measurementColors.setItemText(1, QCoreApplication.translate("tab_15", u"Green", None))
        self.comboBox_measurementColors.setItemText(2, QCoreApplication.translate("tab_15", u"Blue", None))
        self.comboBox_measurementColors.setItemText(3, QCoreApplication.translate("tab_15", u"Yellow", None))
        self.comboBox_measurementColors.setItemText(4, QCoreApplication.translate("tab_15", u"Magenta", None))

#if QT_CONFIG(tooltip)
        self.comboBox_measurementColors.setToolTip(QCoreApplication.translate("tab_15", u"Color to use for the next measurement line you draw.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_deleteMeasurement.setToolTip(QCoreApplication.translate("tab_15", u"Delete the selected measurement.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_deleteMeasurement.setText(QCoreApplication.translate("tab_15", u"Delete Measurement", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("tab_15", u"Manual Contrast Adjustments", None))
#if QT_CONFIG(tooltip)
        self.display_level_data3d0.setToolTip(QCoreApplication.translate("tab_15", u"Current brightness (level) value for this view; synced with the brightness slider below.", None))
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data3d0.setToolTip(QCoreApplication.translate("tab_15", u"Current contrast (window) value for this view; synced with the contrast slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data3d0.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's contrast (display window) \u2014 the intensity range mapped across the grayscale.", None))
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.changeBrightness_data3d0.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's brightness (display level) \u2014 the intensity value centered in the grayscale range.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_28), QCoreApplication.translate("tab_15", u"Coronal", None))
#if QT_CONFIG(tooltip)
        self.display_level_data3d1.setToolTip(QCoreApplication.translate("tab_15", u"Current brightness (level) value for this view; synced with the brightness slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data3d1.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's contrast (display window) \u2014 the intensity range mapped across the grayscale.", None))
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data3d1.setToolTip(QCoreApplication.translate("tab_15", u"Current contrast (window) value for this view; synced with the contrast slider below.", None))
#endif // QT_CONFIG(tooltip)
        self.label_32.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.changeBrightness_data3d1.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's brightness (display level) \u2014 the intensity value centered in the grayscale range.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_29), QCoreApplication.translate("tab_15", u"Sagittal", None))
#if QT_CONFIG(tooltip)
        self.display_window_data3d2.setToolTip(QCoreApplication.translate("tab_15", u"Current contrast (window) value for this view; synced with the contrast slider below.", None))
#endif // QT_CONFIG(tooltip)
        self.label_34.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
        self.label_33.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.changeBrightness_data3d2.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's brightness (display level) \u2014 the intensity value centered in the grayscale range.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.display_level_data3d2.setToolTip(QCoreApplication.translate("tab_15", u"Current brightness (level) value for this view; synced with the brightness slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data3d2.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's contrast (display window) \u2014 the intensity range mapped across the grayscale.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_30), QCoreApplication.translate("tab_15", u"Axial", None))
        self.ManualContrastAdjustments.setTitle(QCoreApplication.translate("tab_15", u"Manual Contrast Adjustement", None))
#if QT_CONFIG(tooltip)
        self.changeBrightness_data00.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's brightness (display level) \u2014 the intensity value centered in the grayscale range.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.display_level_data00.setToolTip(QCoreApplication.translate("tab_15", u"Current brightness (level) value for this view; synced with the brightness slider below.", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_window_data00.setToolTip(QCoreApplication.translate("tab_15", u"Current contrast (window) value for this view; synced with the contrast slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data00.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's contrast (display window) \u2014 the intensity range mapped across the grayscale.", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), QCoreApplication.translate("tab_15", u"Timest 1", None))
        self.label_17.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data01.setToolTip(QCoreApplication.translate("tab_15", u"Current contrast (window) value for this view; synced with the contrast slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data01.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's contrast (display window) \u2014 the intensity range mapped across the grayscale.", None))
#endif // QT_CONFIG(tooltip)
        self.label_18.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_level_data01.setToolTip(QCoreApplication.translate("tab_15", u"Current brightness (level) value for this view; synced with the brightness slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeBrightness_data01.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's brightness (display level) \u2014 the intensity value centered in the grayscale range.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_11), QCoreApplication.translate("tab_15", u"Timest 2", None))
        self.label_19.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data02.setToolTip(QCoreApplication.translate("tab_15", u"Current contrast (window) value for this view; synced with the contrast slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data02.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's contrast (display window) \u2014 the intensity range mapped across the grayscale.", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_level_data02.setToolTip(QCoreApplication.translate("tab_15", u"Current brightness (level) value for this view; synced with the brightness slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeBrightness_data02.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's brightness (display level) \u2014 the intensity value centered in the grayscale range.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_12), QCoreApplication.translate("tab_15", u"Timest 3", None))
        self.contrast_data.setItemText(self.contrast_data.indexOf(self.contrast_data0), QCoreApplication.translate("tab_15", u"Data 0", None))
#if QT_CONFIG(tooltip)
        self.changeBrightness_data10.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's brightness (display level) \u2014 the intensity value centered in the grayscale range.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.display_level_data10.setToolTip(QCoreApplication.translate("tab_15", u"Current brightness (level) value for this view; synced with the brightness slider below.", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_window_data10.setToolTip(QCoreApplication.translate("tab_15", u"Current contrast (window) value for this view; synced with the contrast slider below.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data10.setToolTip(QCoreApplication.translate("tab_15", u"Drag to adjust this view's contrast (display window) \u2014 the intensity range mapped across the grayscale.", None))
#endif // QT_CONFIG(tooltip)
        self.label_14.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_16), QCoreApplication.translate("tab_15", u"Timest 1", None))
        self.label_21.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data11.setToolTip(QCoreApplication.translate("tab_15", u"Type the contrast (window width) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data11.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the contrast (intensity window width) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.label_22.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_level_data11.setToolTip(QCoreApplication.translate("tab_15", u"Type the brightness (window level) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeBrightness_data11.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the brightness (intensity window level) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_17), QCoreApplication.translate("tab_15", u"Timest 2", None))
        self.label_23.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data12.setToolTip(QCoreApplication.translate("tab_15", u"Type the contrast (window width) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data12.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the contrast (intensity window width) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.label_24.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_level_data12.setToolTip(QCoreApplication.translate("tab_15", u"Type the brightness (window level) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeBrightness_data12.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the brightness (intensity window level) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_18), QCoreApplication.translate("tab_15", u"Timest 3", None))
        self.contrast_data.setItemText(self.contrast_data.indexOf(self.contrast_data1), QCoreApplication.translate("tab_15", u"Data 1", None))
#if QT_CONFIG(tooltip)
        self.changeBrightness_data20.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the brightness (intensity window level) for this view.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.display_level_data20.setToolTip(QCoreApplication.translate("tab_15", u"Type the brightness (window level) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_window_data20.setToolTip(QCoreApplication.translate("tab_15", u"Type the contrast (window width) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data20.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the contrast (intensity window width) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.label_16.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_19), QCoreApplication.translate("tab_15", u"Timest 1", None))
        self.label_25.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data21.setToolTip(QCoreApplication.translate("tab_15", u"Type the contrast (window width) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data21.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the contrast (intensity window width) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.label_26.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_level_data21.setToolTip(QCoreApplication.translate("tab_15", u"Type the brightness (window level) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeBrightness_data21.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the brightness (intensity window level) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_20), QCoreApplication.translate("tab_15", u"Timest 2", None))
        self.label_27.setText(QCoreApplication.translate("tab_15", u"Contrast / Window", None))
#if QT_CONFIG(tooltip)
        self.display_window_data22.setToolTip(QCoreApplication.translate("tab_15", u"Type the contrast (window width) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeContrast_data22.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the contrast (intensity window width) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.label_28.setText(QCoreApplication.translate("tab_15", u"Brightness / Level", None))
#if QT_CONFIG(tooltip)
        self.display_level_data22.setToolTip(QCoreApplication.translate("tab_15", u"Type the brightness (window level) value directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.changeBrightness_data22.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the brightness (intensity window level) for this view.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_21), QCoreApplication.translate("tab_15", u"Timest 3", None))
        self.contrast_data.setItemText(self.contrast_data.indexOf(self.contrast_data2), QCoreApplication.translate("tab_15", u"Data 2", None))
#if QT_CONFIG(tooltip)
        self.groupBox_segmentation.setToolTip(QCoreApplication.translate("tab_15", u"Threshold, seed, and grow a 3D segmentation mask (threshold \u2192 bubble seeding \u2192 level-set evolution).", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_segmentation.setTitle(QCoreApplication.translate("tab_15", u"Segmentation", None))
        self.textEdit_SAMRI_reg.setHtml(QCoreApplication.translate("tab_15", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
#if QT_CONFIG(tooltip)
        self.pushButton_Next1.setToolTip(QCoreApplication.translate("tab_15", u"Confirm the current threshold and continue to placing seed bubbles.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Next1.setText(QCoreApplication.translate("tab_15", u"Next", None))
#if QT_CONFIG(tooltip)
        self.pushButton_Back1.setToolTip(QCoreApplication.translate("tab_15", u"Close the segmentation panel and exit the workflow (this is the first page, so there is no earlier step to return to).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Back1.setText(QCoreApplication.translate("tab_15", u"Back", None))
#if QT_CONFIG(tooltip)
        self.checkBox_threshold.setToolTip(QCoreApplication.translate("tab_15", u"Toggle whether the threshold mask is shown as a live preview on the current view.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_threshold.setText(QCoreApplication.translate("tab_15", u"Threshold ON", None))
        self.textBrowser_5.setHtml(QCoreApplication.translate("tab_15", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt;\">Step 1/3<br /></span><span style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:700;\">Presegmentation</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.groupBox_7.setToolTip(QCoreApplication.translate("tab_15", u"Choose which side of the intensity range counts as inside the segmented region.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_7.setTitle(QCoreApplication.translate("tab_15", u"THRESHOLD", None))
#if QT_CONFIG(tooltip)
        self.radioButton_bounded.setToolTip(QCoreApplication.translate("tab_15", u"Keep only voxels between the lower and upper threshold.", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_bounded.setText(QCoreApplication.translate("tab_15", u"Bandpass", None))
#if QT_CONFIG(tooltip)
        self.radioButton_lower.setToolTip(QCoreApplication.translate("tab_15", u"Keep only voxels above the lower threshold.", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_lower.setText(QCoreApplication.translate("tab_15", u"Highpass", None))
#if QT_CONFIG(tooltip)
        self.radioButton_upper.setToolTip(QCoreApplication.translate("tab_15", u"Keep only voxels below the upper threshold.", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_upper.setText(QCoreApplication.translate("tab_15", u"Lowpass", None))
#if QT_CONFIG(tooltip)
        self.groupBox_13.setToolTip(QCoreApplication.translate("tab_15", u"Sets the lower intensity bound used to build the segmentation mask.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_13.setTitle(QCoreApplication.translate("tab_15", u"Lower Threshold", None))
#if QT_CONFIG(tooltip)
        self.ScrollBar_lower.setToolTip(QCoreApplication.translate("tab_15", u"Sets the lower intensity threshold; drag while thresholding is enabled to preview the mask live.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_lower.setToolTip(QCoreApplication.translate("tab_15", u"Type the lower intensity threshold directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_63.setToolTip(QCoreApplication.translate("tab_15", u"Sets the upper intensity bound used to build the segmentation mask.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_63.setTitle(QCoreApplication.translate("tab_15", u"Upper Threshold", None))
#if QT_CONFIG(tooltip)
        self.ScrollBar_upper.setToolTip(QCoreApplication.translate("tab_15", u"Sets the upper intensity threshold; drag while thresholding is enabled to preview the mask live.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_upper.setToolTip(QCoreApplication.translate("tab_15", u"Type the upper intensity threshold directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
        self.textBrowser_6.setHtml(QCoreApplication.translate("tab_15", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt;\">Step 2/3<br /></span><span style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:700;\">Initialization</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_Next2.setToolTip(QCoreApplication.translate("tab_15", u"Confirm the seed bubbles and start the level-set evolution step.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Next2.setText(QCoreApplication.translate("tab_15", u"Next", None))
#if QT_CONFIG(tooltip)
        self.pushButton_Back2.setToolTip(QCoreApplication.translate("tab_15", u"Return to the threshold page to adjust the intensity bounds.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Back2.setText(QCoreApplication.translate("tab_15", u"Back", None))
#if QT_CONFIG(tooltip)
        self.groupBox_16.setToolTip(QCoreApplication.translate("tab_15", u"Lists the seed bubbles placed so far; select one to delete it.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_16.setTitle(QCoreApplication.translate("tab_15", u"Active Bubbles", None))
#if QT_CONFIG(tooltip)
        self.pushButton_delete.setToolTip(QCoreApplication.translate("tab_15", u"Delete the currently selected seed bubble.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_delete.setText(QCoreApplication.translate("tab_15", u"Delete Active Bubble", None))
#if QT_CONFIG(tooltip)
        self.groupBox_10.setToolTip(QCoreApplication.translate("tab_15", u"Sets the radius of the next seed bubble to be placed.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_10.setTitle(QCoreApplication.translate("tab_15", u"Bubble Radius", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_Bubradius.setToolTip(QCoreApplication.translate("tab_15", u"Type the seed bubble radius directly; mirrors the slider next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.horizontalSlider_Bubradius.setToolTip(QCoreApplication.translate("tab_15", u"Adjusts the seed bubble radius; mirrors the spin box next to it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_addBubbles.setToolTip(QCoreApplication.translate("tab_15", u"Place a new seed bubble at the current cursor position.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_addBubbles.setText(QCoreApplication.translate("tab_15", u"Add Bubble at Cursor", None))
#if QT_CONFIG(tooltip)
        self.pushButton_Back3.setToolTip(QCoreApplication.translate("tab_15", u"Return to the bubble-seeding page.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Back3.setText(QCoreApplication.translate("tab_15", u"Back", None))
#if QT_CONFIG(tooltip)
        self.pushButton_Finish.setToolTip(QCoreApplication.translate("tab_15", u"Finish segmentation and close this panel, keeping the current mask.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Finish.setText(QCoreApplication.translate("tab_15", u"Finish", None))
        self.textBrowser_7.setHtml(QCoreApplication.translate("tab_15", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:10pt;\">Step 3/3<br /></span><span style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:700;\">Evolution</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.groupBox_64.setToolTip(QCoreApplication.translate("tab_15", u"Number of level-set iterations to run per step (used by both continuous play and single-stepping).", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_64.setTitle(QCoreApplication.translate("tab_15", u"Step Size", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_SegStep.setToolTip(QCoreApplication.translate("tab_15", u"Number of level-set iterations to run per step (used by both continuous play and single-stepping).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_66.setToolTip(QCoreApplication.translate("tab_15", u"Shows how many level-set iterations have run so far.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_66.setTitle(QCoreApplication.translate("tab_15", u"Iteration", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_Segiter.setToolTip(QCoreApplication.translate("tab_15", u"Running count of level-set iterations completed so far; updates automatically as the evolution plays.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_65.setToolTip(QCoreApplication.translate("tab_15", u"Controls for running, single-stepping, and resetting the level-set evolution.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_65.setTitle(QCoreApplication.translate("tab_15", u"Start / Pause", None))
#if QT_CONFIG(tooltip)
        self.toolButton_backwardEvo.setToolTip(QCoreApplication.translate("tab_15", u"Reset to start", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_backwardEvo.setText(QCoreApplication.translate("tab_15", u"...", None))
#if QT_CONFIG(tooltip)
        self.toolButton_forwardEvo.setToolTip(QCoreApplication.translate("tab_15", u"One iteration of step size", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_forwardEvo.setText(QCoreApplication.translate("tab_15", u"...", None))
#if QT_CONFIG(tooltip)
        self.toolButton_runEvo.setToolTip(QCoreApplication.translate("tab_15", u"Play or pause the level-set evolution; it runs in chunks of the configured step size.", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_runEvo.setText(QCoreApplication.translate("tab_15", u"...", None))
        self.lineEdit_evolution_status.setText(QCoreApplication.translate("tab_15", u"Currently: Pause", None))
        pass
    # retranslateUi

