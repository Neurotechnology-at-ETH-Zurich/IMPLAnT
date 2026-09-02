# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dock_ephys.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QLineEdit, QPushButton, QSizePolicy, QSlider,
    QSpinBox, QStackedWidget, QWidget)

from pgwidget import PgWidget

class Ui_Dock_ephys(object):
    def setupUi(self, Dock_ephys):
        if not Dock_ephys.objectName():
            Dock_ephys.setObjectName(u"Dock_ephys")
        Dock_ephys.resize(650, 867)
        Dock_ephys.setMinimumSize(QSize(650, 0))
        self.gridLayout_69 = QGridLayout(Dock_ephys)
        self.gridLayout_69.setObjectName(u"gridLayout_69")
        self.pushButton_lfp = QPushButton(Dock_ephys)
        self.pushButton_lfp.setObjectName(u"pushButton_lfp")
        self.pushButton_lfp.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        self.pushButton_lfp.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_lfp, 1, 4, 1, 4)

        self.groupBox_3 = QGroupBox(Dock_ephys)
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


        self.gridLayout_69.addWidget(self.groupBox_3, 5, 0, 1, 8)

        self.pushButton_selectTime = QPushButton(Dock_ephys)
        self.pushButton_selectTime.setObjectName(u"pushButton_selectTime")
        self.pushButton_selectTime.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon = QIcon()
        icon.addFile(u"Icons/ephys/select_time.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_selectTime.setIcon(icon)
        self.pushButton_selectTime.setIconSize(QSize(40, 40))
        self.pushButton_selectTime.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_selectTime, 3, 6, 1, 1)

        self.pushButton_zoomReset = QPushButton(Dock_ephys)
        self.pushButton_zoomReset.setObjectName(u"pushButton_zoomReset")
        self.pushButton_zoomReset.setEnabled(True)
        self.pushButton_zoomReset.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon1 = QIcon()
        icon1.addFile(u"Icons/ephys/zoom-in (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_zoomReset.setIcon(icon1)
        self.pushButton_zoomReset.setIconSize(QSize(40, 40))
        self.pushButton_zoomReset.setCheckable(False)

        self.gridLayout_69.addWidget(self.pushButton_zoomReset, 3, 1, 1, 1)

        self.widget_pgEphys = PgWidget(Dock_ephys)
        self.widget_pgEphys.setObjectName(u"widget_pgEphys")
        palette = QPalette()
        brush = QBrush(QColor(237, 51, 59, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush)
        self.widget_pgEphys.setPalette(palette)

        self.gridLayout_69.addWidget(self.widget_pgEphys, 2, 0, 1, 8)

        self.pushButton_timeline = QPushButton(Dock_ephys)
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
        icon2 = QIcon()
        icon2.addFile(u"Icons/ephys/select_timeline.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_timeline.setIcon(icon2)
        self.pushButton_timeline.setIconSize(QSize(40, 40))
        self.pushButton_timeline.setCheckable(True)
        self.pushButton_timeline.setChecked(True)

        self.gridLayout_69.addWidget(self.pushButton_timeline, 3, 4, 1, 1)

        self.pushButton_measurement = QPushButton(Dock_ephys)
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
        icon3 = QIcon()
        icon3.addFile(u"Icons/mri/measure.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_measurement.setIcon(icon3)
        self.pushButton_measurement.setIconSize(QSize(40, 40))
        self.pushButton_measurement.setCheckable(True)

        self.gridLayout_69.addWidget(self.pushButton_measurement, 3, 7, 1, 1)

        self.groupBox_1 = QGroupBox(Dock_ephys)
        self.groupBox_1.setObjectName(u"groupBox_1")
        self.gridLayout_205 = QGridLayout(self.groupBox_1)
        self.gridLayout_205.setObjectName(u"gridLayout_205")
        self.stackedWidget_theta = QStackedWidget(self.groupBox_1)
        self.stackedWidget_theta.setObjectName(u"stackedWidget_theta")
        self.page_27 = QWidget()
        self.page_27.setObjectName(u"page_27")
        self.gridLayout_200 = QGridLayout(self.page_27)
        self.gridLayout_200.setObjectName(u"gridLayout_200")
        self.pushButton_next_theta = QPushButton(self.page_27)
        self.pushButton_next_theta.setObjectName(u"pushButton_next_theta")

        self.gridLayout_200.addWidget(self.pushButton_next_theta, 2, 2, 1, 1)

        self.checkBox_thetaCycles = QCheckBox(self.page_27)
        self.checkBox_thetaCycles.setObjectName(u"checkBox_thetaCycles")
        self.checkBox_thetaCycles.setChecked(True)

        self.gridLayout_200.addWidget(self.checkBox_thetaCycles, 3, 0, 1, 1)

        self.pushButton_add_theta = QPushButton(self.page_27)
        self.pushButton_add_theta.setObjectName(u"pushButton_add_theta")

        self.gridLayout_200.addWidget(self.pushButton_add_theta, 0, 2, 1, 1)

        self.checkBox_theta = QCheckBox(self.page_27)
        self.checkBox_theta.setObjectName(u"checkBox_theta")
        self.checkBox_theta.setChecked(True)

        self.gridLayout_200.addWidget(self.checkBox_theta, 0, 0, 1, 1)

        self.pushButton_prev_theta = QPushButton(self.page_27)
        self.pushButton_prev_theta.setObjectName(u"pushButton_prev_theta")

        self.gridLayout_200.addWidget(self.pushButton_prev_theta, 2, 0, 1, 1)

        self.stackedWidget_theta.addWidget(self.page_27)
        self.page_28 = QWidget()
        self.page_28.setObjectName(u"page_28")
        self.gridLayout_204 = QGridLayout(self.page_28)
        self.gridLayout_204.setObjectName(u"gridLayout_204")
        self.lineEdit_63 = QLineEdit(self.page_28)
        self.lineEdit_63.setObjectName(u"lineEdit_63")

        self.gridLayout_204.addWidget(self.lineEdit_63, 0, 0, 1, 1)

        self.stackedWidget_theta.addWidget(self.page_28)

        self.gridLayout_205.addWidget(self.stackedWidget_theta, 0, 0, 1, 1)


        self.gridLayout_69.addWidget(self.groupBox_1, 0, 4, 1, 4)

        self.groupBox_67 = QGroupBox(Dock_ephys)
        self.groupBox_67.setObjectName(u"groupBox_67")
        self.gridLayout_206 = QGridLayout(self.groupBox_67)
        self.gridLayout_206.setObjectName(u"gridLayout_206")
        self.stackedWidget_ripplAI = QStackedWidget(self.groupBox_67)
        self.stackedWidget_ripplAI.setObjectName(u"stackedWidget_ripplAI")
        self.page_21 = QWidget()
        self.page_21.setObjectName(u"page_21")
        self.gridLayout_197 = QGridLayout(self.page_21)
        self.gridLayout_197.setObjectName(u"gridLayout_197")
        self.pushButton_addRipple = QPushButton(self.page_21)
        self.pushButton_addRipple.setObjectName(u"pushButton_addRipple")

        self.gridLayout_197.addWidget(self.pushButton_addRipple, 0, 1, 1, 1)

        self.pushButton_next_rippl = QPushButton(self.page_21)
        self.pushButton_next_rippl.setObjectName(u"pushButton_next_rippl")

        self.gridLayout_197.addWidget(self.pushButton_next_rippl, 1, 1, 1, 1)

        self.checkBox_ripplAI = QCheckBox(self.page_21)
        self.checkBox_ripplAI.setObjectName(u"checkBox_ripplAI")
        self.checkBox_ripplAI.setChecked(True)

        self.gridLayout_197.addWidget(self.checkBox_ripplAI, 0, 0, 1, 1)

        self.pushButton_prev_rippl = QPushButton(self.page_21)
        self.pushButton_prev_rippl.setObjectName(u"pushButton_prev_rippl")

        self.gridLayout_197.addWidget(self.pushButton_prev_rippl, 1, 0, 1, 1)

        self.stackedWidget_ripplAI.addWidget(self.page_21)
        self.page_22 = QWidget()
        self.page_22.setObjectName(u"page_22")
        self.gridLayout_198 = QGridLayout(self.page_22)
        self.gridLayout_198.setObjectName(u"gridLayout_198")
        self.lineEdit_18 = QLineEdit(self.page_22)
        self.lineEdit_18.setObjectName(u"lineEdit_18")

        self.gridLayout_198.addWidget(self.lineEdit_18, 0, 0, 1, 1)

        self.stackedWidget_ripplAI.addWidget(self.page_22)

        self.gridLayout_206.addWidget(self.stackedWidget_ripplAI, 0, 0, 1, 1)


        self.gridLayout_69.addWidget(self.groupBox_67, 0, 0, 1, 4)

        self.pushButtonAmp_plus = QPushButton(Dock_ephys)
        self.pushButtonAmp_plus.setObjectName(u"pushButtonAmp_plus")
        self.pushButtonAmp_plus.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon4 = QIcon()
        icon4.addFile(u"Icons/ephys/amplitude_plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonAmp_plus.setIcon(icon4)
        self.pushButtonAmp_plus.setIconSize(QSize(40, 40))
        self.pushButtonAmp_plus.setCheckable(False)

        self.gridLayout_69.addWidget(self.pushButtonAmp_plus, 3, 2, 1, 1)

        self.pushButtonAmp_minus = QPushButton(Dock_ephys)
        self.pushButtonAmp_minus.setObjectName(u"pushButtonAmp_minus")
        self.pushButtonAmp_minus.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon5 = QIcon()
        icon5.addFile(u"Icons/ephys/amplitude_minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonAmp_minus.setIcon(icon5)
        self.pushButtonAmp_minus.setIconSize(QSize(40, 40))
        self.pushButtonAmp_minus.setCheckable(False)

        self.gridLayout_69.addWidget(self.pushButtonAmp_minus, 3, 3, 1, 1)

        self.pushButton_zoomIn = QPushButton(Dock_ephys)
        self.pushButton_zoomIn.setObjectName(u"pushButton_zoomIn")
        self.pushButton_zoomIn.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon6 = QIcon()
        icon6.addFile(u"Icons/ephys/zoom_in.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_zoomIn.setIcon(icon6)
        self.pushButton_zoomIn.setIconSize(QSize(40, 40))
        self.pushButton_zoomIn.setCheckable(True)
        self.pushButton_zoomIn.setChecked(False)

        self.gridLayout_69.addWidget(self.pushButton_zoomIn, 3, 0, 1, 1)

        self.pushButton_zoomOut = QPushButton(Dock_ephys)
        self.pushButton_zoomOut.setObjectName(u"pushButton_zoomOut")
        self.pushButton_zoomOut.setEnabled(True)
        self.pushButton_zoomOut.setStyleSheet(u"\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        icon7 = QIcon()
        icon7.addFile(u"Icons/ephys/zoom-out.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_zoomOut.setIcon(icon7)
        self.pushButton_zoomOut.setIconSize(QSize(40, 40))
        self.pushButton_zoomOut.setCheckable(False)

        self.gridLayout_69.addWidget(self.pushButton_zoomOut, 3, 5, 1, 1)

        self.pushButton_broadband = QPushButton(Dock_ephys)
        self.pushButton_broadband.setObjectName(u"pushButton_broadband")
        self.pushButton_broadband.setStyleSheet(u"QPushButton:checked {\n"
"                background-color: palette(highlight);\n"
"                color: palette(highlighted-text);\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 30);\n"
"                border-radius: 4px;\n"
"            }")
        self.pushButton_broadband.setCheckable(True)
        self.pushButton_broadband.setChecked(True)

        self.gridLayout_69.addWidget(self.pushButton_broadband, 1, 0, 1, 4)

        self.horizontalSlider_ephys = QSlider(Dock_ephys)
        self.horizontalSlider_ephys.setObjectName(u"horizontalSlider_ephys")
        self.horizontalSlider_ephys.setSingleStep(100)
        self.horizontalSlider_ephys.setPageStep(1000)
        self.horizontalSlider_ephys.setOrientation(Qt.Horizontal)

        self.gridLayout_69.addWidget(self.horizontalSlider_ephys, 4, 1, 1, 6)

        self.pushButton_Timeprev = QPushButton(Dock_ephys)
        self.pushButton_Timeprev.setObjectName(u"pushButton_Timeprev")
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekBackward))
        self.pushButton_Timeprev.setIcon(icon8)

        self.gridLayout_69.addWidget(self.pushButton_Timeprev, 4, 0, 1, 1)

        self.pushButton_Timenext = QPushButton(Dock_ephys)
        self.pushButton_Timenext.setObjectName(u"pushButton_Timenext")
        icon9 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekForward))
        self.pushButton_Timenext.setIcon(icon9)

        self.gridLayout_69.addWidget(self.pushButton_Timenext, 4, 7, 1, 1)

        self.gridLayout_69.setRowStretch(2, 1)
        QWidget.setTabOrder(self.pushButton_zoomOut, self.pushButton_selectTime)
        QWidget.setTabOrder(self.pushButton_selectTime, self.pushButton_measurement)
        QWidget.setTabOrder(self.pushButton_measurement, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.spinBox_startMs)
        QWidget.setTabOrder(self.spinBox_startMs, self.spinBox_startS)
        QWidget.setTabOrder(self.spinBox_startS, self.spinBox_startMin)
        QWidget.setTabOrder(self.spinBox_startMin, self.spinBox_duration)
        QWidget.setTabOrder(self.spinBox_duration, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.horizontalSlider_ephys)

        self.retranslateUi(Dock_ephys)

        self.stackedWidget_theta.setCurrentIndex(0)
        self.stackedWidget_ripplAI.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dock_ephys)
    # setupUi

    def retranslateUi(self, Dock_ephys):
#if QT_CONFIG(tooltip)
        self.pushButton_lfp.setToolTip(QCoreApplication.translate("Dock_ephys", u"Jump half duration forward", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_lfp.setText(QCoreApplication.translate("Dock_ephys", u"Display LFP-filtered Data", None))
        self.groupBox_3.setTitle("")
#if QT_CONFIG(tooltip)
        self.spinBox_startMs.setToolTip(QCoreApplication.translate("Dock_ephys", u"Milliseconds component of the visible window's start time.", None))
#endif // QT_CONFIG(tooltip)
        self.spinBox_startMs.setSuffix(QCoreApplication.translate("Dock_ephys", u"ms", None))
#if QT_CONFIG(tooltip)
        self.spinBox_startS.setToolTip(QCoreApplication.translate("Dock_ephys", u"Seconds component of the visible window's start time.", None))
#endif // QT_CONFIG(tooltip)
        self.spinBox_startS.setSuffix(QCoreApplication.translate("Dock_ephys", u"s", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Dock_ephys", u"Duration (ms)", None))
        self.lineEdit.setText(QCoreApplication.translate("Dock_ephys", u"Start Time", None))
#if QT_CONFIG(tooltip)
        self.spinBox_startMin.setToolTip(QCoreApplication.translate("Dock_ephys", u"Minutes component of the visible window's start time.", None))
#endif // QT_CONFIG(tooltip)
        self.spinBox_startMin.setSuffix(QCoreApplication.translate("Dock_ephys", u"min", None))
#if QT_CONFIG(tooltip)
        self.spinBox_duration.setToolTip(QCoreApplication.translate("Dock_ephys", u"Length of the visible time window, in milliseconds.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_selectTime.setToolTip(QCoreApplication.translate("Dock_ephys", u"Select Time", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_selectTime.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_zoomReset.setToolTip(QCoreApplication.translate("Dock_ephys", u"Reset Zoom", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_zoomReset.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_timeline.setToolTip(QCoreApplication.translate("Dock_ephys", u"Draw Timeline", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_timeline.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_measurement.setToolTip(QCoreApplication.translate("Dock_ephys", u"Measure", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_measurement.setText("")
#if QT_CONFIG(tooltip)
        self.groupBox_1.setToolTip(QCoreApplication.translate("Dock_ephys", u"Step through detected theta events, add one manually, and toggle event/cycle-boundary visibility.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_1.setTitle(QCoreApplication.translate("Dock_ephys", u"Theta Detection", None))
#if QT_CONFIG(tooltip)
        self.pushButton_next_theta.setToolTip(QCoreApplication.translate("Dock_ephys", u"Jump the view to the next detected theta event.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_next_theta.setText(QCoreApplication.translate("Dock_ephys", u"Next Theta", None))
#if QT_CONFIG(tooltip)
        self.checkBox_thetaCycles.setToolTip(QCoreApplication.translate("Dock_ephys", u"Show or hide the dotted theta-cycle boundary lines.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_thetaCycles.setText(QCoreApplication.translate("Dock_ephys", u"Visible Phase Cycles", None))
#if QT_CONFIG(tooltip)
        self.pushButton_add_theta.setToolTip(QCoreApplication.translate("Dock_ephys", u"Add a theta event centered on the current view, then drag its edges into place.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add_theta.setText(QCoreApplication.translate("Dock_ephys", u"Add", None))
#if QT_CONFIG(tooltip)
        self.checkBox_theta.setToolTip(QCoreApplication.translate("Dock_ephys", u"Show or hide theta event markers on the trace.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_theta.setText(QCoreApplication.translate("Dock_ephys", u"Visible", None))
#if QT_CONFIG(tooltip)
        self.pushButton_prev_theta.setToolTip(QCoreApplication.translate("Dock_ephys", u"Jump the view to the previous detected theta event.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_prev_theta.setText(QCoreApplication.translate("Dock_ephys", u"Previous Theta", None))
        self.lineEdit_63.setText(QCoreApplication.translate("Dock_ephys", u"No File found. Please first do Ephys Analysis -> Theta Detection", None))
#if QT_CONFIG(tooltip)
        self.groupBox_67.setToolTip(QCoreApplication.translate("Dock_ephys", u"Step through detected ripple (SWR) events, add one manually, and toggle their visibility.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_67.setTitle(QCoreApplication.translate("Dock_ephys", u"Rippl-AI", None))
#if QT_CONFIG(tooltip)
        self.pushButton_addRipple.setToolTip(QCoreApplication.translate("Dock_ephys", u"Add a ripple (SWR) event centered on the current view, then drag its edges into place.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_addRipple.setText(QCoreApplication.translate("Dock_ephys", u"Add", None))
#if QT_CONFIG(tooltip)
        self.pushButton_next_rippl.setToolTip(QCoreApplication.translate("Dock_ephys", u"Jump the view to the next detected ripple (SWR).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_next_rippl.setText(QCoreApplication.translate("Dock_ephys", u"Next SWR", None))
#if QT_CONFIG(tooltip)
        self.checkBox_ripplAI.setToolTip(QCoreApplication.translate("Dock_ephys", u"Show or hide ripple (SWR) event markers on the trace.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_ripplAI.setText(QCoreApplication.translate("Dock_ephys", u"Visible", None))
#if QT_CONFIG(tooltip)
        self.pushButton_prev_rippl.setToolTip(QCoreApplication.translate("Dock_ephys", u"Jump the view to the previous detected ripple (SWR).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_prev_rippl.setText(QCoreApplication.translate("Dock_ephys", u"Previous SWR", None))
        self.lineEdit_18.setText(QCoreApplication.translate("Dock_ephys", u"No File found. Please first do Ephys Analysis -> Rippl AI", None))
#if QT_CONFIG(tooltip)
        self.pushButtonAmp_plus.setToolTip(QCoreApplication.translate("Dock_ephys", u"Increase Amplitude", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonAmp_plus.setText("")
#if QT_CONFIG(tooltip)
        self.pushButtonAmp_minus.setToolTip(QCoreApplication.translate("Dock_ephys", u"Decrease Amplitude", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonAmp_minus.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_zoomIn.setToolTip(QCoreApplication.translate("Dock_ephys", u"Left-drag mode: draw a rubber-band box to zoom into that time/channel range.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_zoomIn.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_zoomOut.setToolTip(QCoreApplication.translate("Dock_ephys", u"Zoom Out", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_zoomOut.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_broadband.setToolTip(QCoreApplication.translate("Dock_ephys", u"Show the raw broadband trace instead of the filtered LFP.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_broadband.setText(QCoreApplication.translate("Dock_ephys", u"Display raw Data", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider_ephys.setToolTip(QCoreApplication.translate("Dock_ephys", u"Scrub through the recording; position corresponds to the start of the visible time window.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_Timeprev.setToolTip(QCoreApplication.translate("Dock_ephys", u"Jump half duration backwards", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Timeprev.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_Timenext.setToolTip(QCoreApplication.translate("Dock_ephys", u"Jump half duration forward", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Timenext.setText("")
        pass
    # retranslateUi

