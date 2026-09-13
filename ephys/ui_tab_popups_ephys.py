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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGridLayout,
    QGroupBox, QSizePolicy, QSpinBox, QWidget)

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
        pass
    # retranslateUi

