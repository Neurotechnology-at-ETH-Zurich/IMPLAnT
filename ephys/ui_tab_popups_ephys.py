# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tab_popups_ephys.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QTextEdit, QWidget)

class Ui_tab(object):
    def setupUi(self, tab):
        if not tab.objectName():
            tab.setObjectName(u"tab")
        self.gridLayout_21 = QGridLayout(tab)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.groupBox_ChangeanatRegion = QGroupBox(tab)
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

        self.frame_filterchannels = QFrame(tab)
        self.frame_filterchannels.setObjectName(u"frame_filterchannels")
        self.frame_filterchannels.setFrameShape(QFrame.StyledPanel)
        self.frame_filterchannels.setFrameShadow(QFrame.Raised)
        self.gridLayout_192 = QGridLayout(self.frame_filterchannels)
        self.gridLayout_192.setObjectName(u"gridLayout_192")
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


        self.gridLayout_192.addWidget(self.groupBox_52, 8, 0, 1, 1)

        self.radioButton_lowPass = QRadioButton(self.frame_filterchannels)
        self.radioButton_lowPass.setObjectName(u"radioButton_lowPass")

        self.gridLayout_192.addWidget(self.radioButton_lowPass, 6, 0, 1, 1)

        self.radioButton_bandPass = QRadioButton(self.frame_filterchannels)
        self.radioButton_bandPass.setObjectName(u"radioButton_bandPass")
        self.radioButton_bandPass.setChecked(True)

        self.gridLayout_192.addWidget(self.radioButton_bandPass, 4, 0, 1, 1)

        self.lineEdit_selectedChannels = QLineEdit(self.frame_filterchannels)
        self.lineEdit_selectedChannels.setObjectName(u"lineEdit_selectedChannels")

        self.gridLayout_192.addWidget(self.lineEdit_selectedChannels, 0, 1, 1, 1)

        self.comboBox_FilterType = QComboBox(self.frame_filterchannels)
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.addItem("")
        self.comboBox_FilterType.setObjectName(u"comboBox_FilterType")

        self.gridLayout_192.addWidget(self.comboBox_FilterType, 4, 1, 1, 1)

        self.pushButton_Filter = QPushButton(self.frame_filterchannels)
        self.pushButton_Filter.setObjectName(u"pushButton_Filter")

        self.gridLayout_192.addWidget(self.pushButton_Filter, 11, 1, 1, 1)

        self.pushButton_FrequencyResponse = QPushButton(self.frame_filterchannels)
        self.pushButton_FrequencyResponse.setObjectName(u"pushButton_FrequencyResponse")

        self.gridLayout_192.addWidget(self.pushButton_FrequencyResponse, 11, 0, 1, 1)

        self.pushButton_detectFreq = QPushButton(self.frame_filterchannels)
        self.pushButton_detectFreq.setObjectName(u"pushButton_detectFreq")

        self.gridLayout_192.addWidget(self.pushButton_detectFreq, 8, 1, 1, 1)

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


        self.gridLayout_192.addWidget(self.groupBox_upperFreq, 9, 0, 1, 1)

        self.textEdit_3 = QTextEdit(self.frame_filterchannels)
        self.textEdit_3.setObjectName(u"textEdit_3")

        self.gridLayout_192.addWidget(self.textEdit_3, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_filterchannels, 0, 0, 1, 1)

        QWidget.setTabOrder(self.pushButton_FrequencyResponse, self.comboBox_FilterType)
        QWidget.setTabOrder(self.comboBox_FilterType, self.lineEdit_selectedChannels)
        QWidget.setTabOrder(self.lineEdit_selectedChannels, self.radioButton_bandPass)
        QWidget.setTabOrder(self.radioButton_bandPass, self.radioButton_lowPass)
        QWidget.setTabOrder(self.radioButton_lowPass, self.pushButton_Filter)
        QWidget.setTabOrder(self.pushButton_Filter, self.doubleSpinBox_upperFreq)
        QWidget.setTabOrder(self.doubleSpinBox_upperFreq, self.doubleSpinBox_lowerFreq)
        QWidget.setTabOrder(self.doubleSpinBox_lowerFreq, self.pushButton_detectFreq)
        QWidget.setTabOrder(self.pushButton_detectFreq, self.comboBox_ChangeanatRegion)
        QWidget.setTabOrder(self.comboBox_ChangeanatRegion, self.spinBox_ChangechannelID)

        self.retranslateUi(tab)

        QMetaObject.connectSlotsByName(tab)
    # setupUi

    def retranslateUi(self, tab):
        self.groupBox_ChangeanatRegion.setTitle("")
#if QT_CONFIG(tooltip)
        self.groupBox_2.setToolTip(QCoreApplication.translate("tab", u"Candidate atlas regions near this channel, ranked by distance \u2014 pick the correct one.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("tab", u"Anatomical Region", None))
#if QT_CONFIG(tooltip)
        self.comboBox_ChangeanatRegion.setToolTip(QCoreApplication.translate("tab", u"Candidate atlas regions near this channel's electrode, sorted by distance; select the correct one.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox.setToolTip(QCoreApplication.translate("tab", u"The ephys channel whose region assignment you're changing (read-only).", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("tab", u"Channel ID", None))
#if QT_CONFIG(tooltip)
        self.spinBox_ChangechannelID.setToolTip(QCoreApplication.translate("tab", u"The ephys channel whose region assignment you're changing (read-only).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.groupBox_52.setToolTip(QCoreApplication.translate("tab", u"Lower cutoff frequency (Hz) \u2014 the low-pass cutoff, or the band's lower edge in band-pass mode.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_52.setTitle(QCoreApplication.translate("tab", u"Lower Frequency", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_lowerFreq.setToolTip(QCoreApplication.translate("tab", u"Lower cutoff frequency (Hz) \u2014 the low-pass cutoff, or the band's lower edge in band-pass mode.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.radioButton_lowPass.setToolTip(QCoreApplication.translate("tab", u"Design a low-pass filter using only the lower cutoff frequency.", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_lowPass.setText(QCoreApplication.translate("tab", u"Low Pass Filter", None))
#if QT_CONFIG(tooltip)
        self.radioButton_bandPass.setToolTip(QCoreApplication.translate("tab", u"Design a band-pass filter using both the lower and upper cutoff frequencies.", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_bandPass.setText(QCoreApplication.translate("tab", u"Band Pass Filter", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_selectedChannels.setToolTip(QCoreApplication.translate("tab", u"Comma-separated channel numbers to filter \u2014 auto-filled when a CA1 channel is detected, but editable to target other channels.", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_FilterType.setItemText(0, QCoreApplication.translate("tab", u"IIR - Butterworth", None))
        self.comboBox_FilterType.setItemText(1, QCoreApplication.translate("tab", u"IIR - Chebyshev I", None))
        self.comboBox_FilterType.setItemText(2, QCoreApplication.translate("tab", u"IIR - Chebyshev II", None))
        self.comboBox_FilterType.setItemText(3, QCoreApplication.translate("tab", u"IIR - Elliptic", None))
        self.comboBox_FilterType.setItemText(4, QCoreApplication.translate("tab", u"FIR - Hamming", None))
        self.comboBox_FilterType.setItemText(5, QCoreApplication.translate("tab", u"FIR - Hann", None))
        self.comboBox_FilterType.setItemText(6, QCoreApplication.translate("tab", u"FIR - Blackman", None))

#if QT_CONFIG(tooltip)
        self.comboBox_FilterType.setToolTip(QCoreApplication.translate("tab", u"Filter implementation to use: IIR (Butterworth) or FIR.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_Filter.setToolTip(QCoreApplication.translate("tab", u"Apply the designed filter to the selected channels' data.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_Filter.setText(QCoreApplication.translate("tab", u"Filter Selected Channels", None))
#if QT_CONFIG(tooltip)
        self.pushButton_FrequencyResponse.setToolTip(QCoreApplication.translate("tab", u"Preview the designed filter's frequency response before applying it.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_FrequencyResponse.setText(QCoreApplication.translate("tab", u"Show Frequency Response", None))
#if QT_CONFIG(tooltip)
        self.pushButton_detectFreq.setToolTip(QCoreApplication.translate("tab", u"Estimate a cutoff frequency from the selected channels' power spectrum.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_detectFreq.setText(QCoreApplication.translate("tab", u"Auto detect Frequency cut-off", None))
#if QT_CONFIG(tooltip)
        self.groupBox_upperFreq.setToolTip(QCoreApplication.translate("tab", u"Only used for band-pass filtering \u2014 sets the upper cutoff frequency (Hz); disabled in low-pass mode.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_upperFreq.setTitle(QCoreApplication.translate("tab", u"Upper Frequency", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_upperFreq.setToolTip(QCoreApplication.translate("tab", u"Upper cutoff frequency (Hz) for band-pass filtering; disabled in low-pass mode.", None))
#endif // QT_CONFIG(tooltip)
        self.textEdit_3.setHtml(QCoreApplication.translate("tab", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Selected Channels IDs to be filtered (Please seperate with comma)</p></body></html>", None))
        pass
    # retranslateUi

