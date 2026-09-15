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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDialogButtonBox, QGridLayout, QGroupBox,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QWidget)

class Ui_tab(object):
    def setupUi(self, tab):
        if not tab.objectName():
            tab.setObjectName(u"tab")
        tab.resize(518, 584)
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


        self.gridLayout_21.addWidget(self.groupBox_ChangeanatRegion, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout = QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_saveTrace = QCheckBox(self.groupBox_3)
        self.checkBox_saveTrace.setObjectName(u"checkBox_saveTrace")
        self.checkBox_saveTrace.setMinimumSize(QSize(0, 0))
        self.checkBox_saveTrace.setSizeIncrement(QSize(0, 0))
        self.checkBox_saveTrace.setStyleSheet(u"QCheckBox::indicator {\n"
"     width: 20px;\n"
"     height: 20px;\n"
"}\n"
"")
        self.checkBox_saveTrace.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.checkBox_saveTrace, 3, 0, 1, 1)

        self.buttonBox_okcancel = QDialogButtonBox(self.groupBox_3)
        self.buttonBox_okcancel.setObjectName(u"buttonBox_okcancel")
        self.buttonBox_okcancel.setMinimumSize(QSize(0, 50))
        self.buttonBox_okcancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox_okcancel, 10, 1, 1, 2)

        self.checkBox_saveChannelSpectrogram = QCheckBox(self.groupBox_3)
        self.checkBox_saveChannelSpectrogram.setObjectName(u"checkBox_saveChannelSpectrogram")
        self.checkBox_saveChannelSpectrogram.setMinimumSize(QSize(0, 0))
        self.checkBox_saveChannelSpectrogram.setSizeIncrement(QSize(0, 0))
        self.checkBox_saveChannelSpectrogram.setStyleSheet(u"QCheckBox::indicator {\n"
"     width: 20px;\n"
"     height: 20px;\n"
"}\n"
"")
        self.checkBox_saveChannelSpectrogram.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.checkBox_saveChannelSpectrogram, 9, 0, 1, 1)

        self.checkBox_saveSpikeRuster = QCheckBox(self.groupBox_3)
        self.checkBox_saveSpikeRuster.setObjectName(u"checkBox_saveSpikeRuster")
        self.checkBox_saveSpikeRuster.setMinimumSize(QSize(0, 0))
        self.checkBox_saveSpikeRuster.setSizeIncrement(QSize(0, 0))
        self.checkBox_saveSpikeRuster.setStyleSheet(u"QCheckBox::indicator {\n"
"     width: 20px;\n"
"     height: 20px;\n"
"}\n"
"")
        self.checkBox_saveSpikeRuster.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.checkBox_saveSpikeRuster, 6, 0, 1, 1)

        self.checkBox_saveCSD = QCheckBox(self.groupBox_3)
        self.checkBox_saveCSD.setObjectName(u"checkBox_saveCSD")
        self.checkBox_saveCSD.setMinimumSize(QSize(0, 0))
        self.checkBox_saveCSD.setSizeIncrement(QSize(0, 0))
        self.checkBox_saveCSD.setStyleSheet(u"QCheckBox::indicator {\n"
"     width: 20px;\n"
"     height: 20px;\n"
"}\n"
"")
        self.checkBox_saveCSD.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.checkBox_saveCSD, 8, 0, 1, 1)

        self.checkBox_saveSpectrogram = QCheckBox(self.groupBox_3)
        self.checkBox_saveSpectrogram.setObjectName(u"checkBox_saveSpectrogram")
        self.checkBox_saveSpectrogram.setMinimumSize(QSize(0, 0))
        self.checkBox_saveSpectrogram.setSizeIncrement(QSize(0, 0))
        self.checkBox_saveSpectrogram.setStyleSheet(u"QCheckBox::indicator {\n"
"     width: 20px;\n"
"     height: 20px;\n"
"}\n"
"")
        self.checkBox_saveSpectrogram.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.checkBox_saveSpectrogram, 7, 0, 1, 1)

        self.pushButton_folder = QPushButton(self.groupBox_3)
        self.pushButton_folder.setObjectName(u"pushButton_folder")
        self.pushButton_folder.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.pushButton_folder, 1, 2, 1, 1)

        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 2)

        self.lineEdit_saveTrace = QLineEdit(self.groupBox_3)
        self.lineEdit_saveTrace.setObjectName(u"lineEdit_saveTrace")

        self.gridLayout.addWidget(self.lineEdit_saveTrace, 3, 1, 1, 2)

        self.lineEdit_saveSpikeRuster = QLineEdit(self.groupBox_3)
        self.lineEdit_saveSpikeRuster.setObjectName(u"lineEdit_saveSpikeRuster")

        self.gridLayout.addWidget(self.lineEdit_saveSpikeRuster, 6, 1, 1, 2)

        self.lineEdit_saveSpectrogram = QLineEdit(self.groupBox_3)
        self.lineEdit_saveSpectrogram.setObjectName(u"lineEdit_saveSpectrogram")

        self.gridLayout.addWidget(self.lineEdit_saveSpectrogram, 7, 1, 1, 2)

        self.lineEdit_saveCSD = QLineEdit(self.groupBox_3)
        self.lineEdit_saveCSD.setObjectName(u"lineEdit_saveCSD")

        self.gridLayout.addWidget(self.lineEdit_saveCSD, 8, 1, 1, 2)

        self.lineEdit_saveChannelSpectrogram = QLineEdit(self.groupBox_3)
        self.lineEdit_saveChannelSpectrogram.setObjectName(u"lineEdit_saveChannelSpectrogram")

        self.gridLayout.addWidget(self.lineEdit_saveChannelSpectrogram, 9, 1, 1, 2)

        self.lineEdit_title = QLineEdit(self.groupBox_3)
        self.lineEdit_title.setObjectName(u"lineEdit_title")
        self.lineEdit_title.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_title, 0, 0, 1, 3)


        self.gridLayout_21.addWidget(self.groupBox_3, 1, 0, 1, 1)

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
        self.groupBox_3.setTitle("")
        self.checkBox_saveTrace.setText(QCoreApplication.translate("tab", u"Raw / Lfp Data", None))
        self.checkBox_saveChannelSpectrogram.setText(QCoreApplication.translate("tab", u"ChannelSpectrogram", None))
        self.checkBox_saveSpikeRuster.setText(QCoreApplication.translate("tab", u"Spike Raster", None))
        self.checkBox_saveCSD.setText(QCoreApplication.translate("tab", u"Current Source Density", None))
        self.checkBox_saveSpectrogram.setText(QCoreApplication.translate("tab", u"Spectrogram", None))
        self.pushButton_folder.setText(QCoreApplication.translate("tab", u"Browse Folder To Save Files", None))
        self.lineEdit_title.setText(QCoreApplication.translate("tab", u"Please Select Which Plots you want to save", None))
        pass
    # retranslateUi

