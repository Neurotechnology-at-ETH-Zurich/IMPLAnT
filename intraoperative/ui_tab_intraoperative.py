# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tab_intraoperative.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, surgery):
        if not surgery.objectName():
            surgery.setObjectName(u"surgery")
        surgery.resize(1589, 843)
        self.gridLayout = QGridLayout(surgery)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(surgery)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(500, 0))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_109 = QLineEdit(surgery)
        self.lineEdit_109.setObjectName(u"lineEdit_109")
        self.lineEdit_109.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_109, 0, 1, 1, 1)

        self.pushButton_questionmark_2 = QPushButton(surgery)
        self.pushButton_questionmark_2.setObjectName(u"pushButton_questionmark_2")
        self.pushButton_questionmark_2.setMaximumSize(QSize(50, 16777215))
        self.pushButton_questionmark_2.setLayoutDirection(Qt.RightToLeft)
        self.pushButton_questionmark_2.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u"Icons/mri/question_mark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_questionmark_2.setIcon(icon)
        self.pushButton_questionmark_2.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.pushButton_questionmark_2, 0, 2, 1, 1)

        self.groupBox_76 = QGroupBox(surgery)
        self.groupBox_76.setObjectName(u"groupBox_76")
        self.groupBox_76.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_217 = QGridLayout(self.groupBox_76)
        self.gridLayout_217.setObjectName(u"gridLayout_217")
        self.lineEdit_82 = QLineEdit(self.groupBox_76)
        self.lineEdit_82.setObjectName(u"lineEdit_82")
        self.lineEdit_82.setReadOnly(True)

        self.gridLayout_217.addWidget(self.lineEdit_82, 0, 1, 1, 1)

        self.doubleSpinBox_sag_b = QDoubleSpinBox(self.groupBox_76)
        self.doubleSpinBox_sag_b.setObjectName(u"doubleSpinBox_sag_b")
        self.doubleSpinBox_sag_b.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(14)
        self.doubleSpinBox_sag_b.setFont(font)
        self.doubleSpinBox_sag_b.setDecimals(2)
        self.doubleSpinBox_sag_b.setMinimum(-200.000000000000000)
        self.doubleSpinBox_sag_b.setMaximum(200.000000000000000)

        self.gridLayout_217.addWidget(self.doubleSpinBox_sag_b, 1, 1, 1, 1)

        self.doubleSpinBox_cor_b = QDoubleSpinBox(self.groupBox_76)
        self.doubleSpinBox_cor_b.setObjectName(u"doubleSpinBox_cor_b")
        self.doubleSpinBox_cor_b.setMinimumSize(QSize(0, 50))
        self.doubleSpinBox_cor_b.setFont(font)
        self.doubleSpinBox_cor_b.setDecimals(2)
        self.doubleSpinBox_cor_b.setMinimum(-200.000000000000000)
        self.doubleSpinBox_cor_b.setMaximum(200.000000000000000)

        self.gridLayout_217.addWidget(self.doubleSpinBox_cor_b, 1, 2, 1, 1)

        self.lineEdit_81 = QLineEdit(self.groupBox_76)
        self.lineEdit_81.setObjectName(u"lineEdit_81")
        self.lineEdit_81.setReadOnly(True)

        self.gridLayout_217.addWidget(self.lineEdit_81, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.groupBox_76, 1, 0, 1, 1)

        self.tableWidget = QTableWidget(surgery)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(15)
        self.tableWidget.setFont(font1)

        self.gridLayout.addWidget(self.tableWidget, 1, 1, 2, 2)

        self.groupBox_77 = QGroupBox(surgery)
        self.groupBox_77.setObjectName(u"groupBox_77")
        self.groupBox_77.setMaximumSize(QSize(16777215, 200))
        self.gridLayout_218 = QGridLayout(self.groupBox_77)
        self.gridLayout_218.setObjectName(u"gridLayout_218")
        self.doubleSpinBox_sag_l = QDoubleSpinBox(self.groupBox_77)
        self.doubleSpinBox_sag_l.setObjectName(u"doubleSpinBox_sag_l")
        self.doubleSpinBox_sag_l.setMinimumSize(QSize(0, 50))
        self.doubleSpinBox_sag_l.setFont(font)
        self.doubleSpinBox_sag_l.setDecimals(2)
        self.doubleSpinBox_sag_l.setMinimum(-200.000000000000000)
        self.doubleSpinBox_sag_l.setMaximum(200.000000000000000)

        self.gridLayout_218.addWidget(self.doubleSpinBox_sag_l, 1, 1, 1, 1)

        self.doubleSpinBox_cor_l = QDoubleSpinBox(self.groupBox_77)
        self.doubleSpinBox_cor_l.setObjectName(u"doubleSpinBox_cor_l")
        self.doubleSpinBox_cor_l.setMinimumSize(QSize(0, 50))
        self.doubleSpinBox_cor_l.setFont(font)
        self.doubleSpinBox_cor_l.setDecimals(2)
        self.doubleSpinBox_cor_l.setMinimum(-200.000000000000000)
        self.doubleSpinBox_cor_l.setMaximum(200.000000000000000)

        self.gridLayout_218.addWidget(self.doubleSpinBox_cor_l, 1, 2, 1, 1)

        self.lineEdit_84 = QLineEdit(self.groupBox_77)
        self.lineEdit_84.setObjectName(u"lineEdit_84")
        self.lineEdit_84.setReadOnly(True)

        self.gridLayout_218.addWidget(self.lineEdit_84, 0, 2, 1, 1)

        self.lineEdit_85 = QLineEdit(self.groupBox_77)
        self.lineEdit_85.setObjectName(u"lineEdit_85")
        self.lineEdit_85.setReadOnly(True)

        self.gridLayout_218.addWidget(self.lineEdit_85, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_77, 2, 0, 1, 1)

        self.widget = QWidget(surgery)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(100, 100))

        self.gridLayout.addWidget(self.widget, 3, 0, 2, 1)

        self.label_2 = QLabel(surgery)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 50))
        font2 = QFont()
        font2.setPointSize(16)
        font2.setBold(False)
        self.label_2.setFont(font2)

        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 2)

        self.frame_13 = QFrame(surgery)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(500, 200))
        self.frame_13.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(255, 255, 255);\n"
"")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.gridLayout_224 = QGridLayout(self.frame_13)
        self.gridLayout_224.setSpacing(0)
        self.gridLayout_224.setObjectName(u"gridLayout_224")
        self.gridLayout_224.setContentsMargins(4, 4, 4, 4)
        self.widget_axialView = QWidget(self.frame_13)
        self.widget_axialView.setObjectName(u"widget_axialView")

        self.gridLayout_224.addWidget(self.widget_axialView, 2, 1, 1, 2)


        self.gridLayout.addWidget(self.frame_13, 4, 1, 2, 2)

        self.groupBox_78 = QGroupBox(surgery)
        self.groupBox_78.setObjectName(u"groupBox_78")
        self.groupBox_78.setMaximumSize(QSize(16777215, 75))
        self.gridLayout_220 = QGridLayout(self.groupBox_78)
        self.gridLayout_220.setObjectName(u"gridLayout_220")
        self.resetCamera_vis3D_2 = QPushButton(self.groupBox_78)
        self.resetCamera_vis3D_2.setObjectName(u"resetCamera_vis3D_2")
        self.resetCamera_vis3D_2.setEnabled(True)
        self.resetCamera_vis3D_2.setStyleSheet(u"")
        icon1 = QIcon(QIcon.fromTheme(u"go-home"))
        self.resetCamera_vis3D_2.setIcon(icon1)
        self.resetCamera_vis3D_2.setIconSize(QSize(40, 40))
        self.resetCamera_vis3D_2.setAutoDefault(False)
        self.resetCamera_vis3D_2.setFlat(False)

        self.gridLayout_220.addWidget(self.resetCamera_vis3D_2, 0, 0, 1, 1)

        self.change_perspective_vis3D_2 = QPushButton(self.groupBox_78)
        self.change_perspective_vis3D_2.setObjectName(u"change_perspective_vis3D_2")
        self.change_perspective_vis3D_2.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u"Icons/ephys/projection_parallel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.change_perspective_vis3D_2.setIcon(icon2)
        self.change_perspective_vis3D_2.setIconSize(QSize(40, 40))

        self.gridLayout_220.addWidget(self.change_perspective_vis3D_2, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_78, 5, 0, 1, 1)


        self.retranslateUi(surgery)

        self.resetCamera_vis3D_2.setDefault(False)


        QMetaObject.connectSlotsByName(surgery)
    # setupUi

    def retranslateUi(self, surgery):
        surgery.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lineEdit_109.setText(QCoreApplication.translate("Form", u"All Distances measured from Bregma Point!", None))
        self.pushButton_questionmark_2.setText("")
        self.groupBox_76.setTitle(QCoreApplication.translate("Form", u"Bregma Position (x,y,z)", None))
        self.lineEdit_82.setText(QCoreApplication.translate("Form", u"RL [mm]", None))
        self.lineEdit_81.setText(QCoreApplication.translate("Form", u"AP [mm] - P is negative", None))
        self.groupBox_77.setTitle(QCoreApplication.translate("Form", u"Lambda Position (x,y,z)", None))
        self.lineEdit_84.setText(QCoreApplication.translate("Form", u"AP [mm] - P is negative", None))
        self.lineEdit_85.setText(QCoreApplication.translate("Form", u"RL [mm]", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Skull Reference", None))
        self.groupBox_78.setTitle("")
#if QT_CONFIG(tooltip)
        self.resetCamera_vis3D_2.setToolTip(QCoreApplication.translate("Form", u"Reset Camera View", None))
#endif // QT_CONFIG(tooltip)
        self.resetCamera_vis3D_2.setText("")
#if QT_CONFIG(tooltip)
        self.change_perspective_vis3D_2.setToolTip(QCoreApplication.translate("Form", u"Change Perspective", None))
#endif // QT_CONFIG(tooltip)
        self.change_perspective_vis3D_2.setText("")
    # retranslateUi

