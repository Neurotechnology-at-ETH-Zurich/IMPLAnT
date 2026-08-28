# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_tp_3d.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(655, 736)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_deselectAll = QPushButton(Form)
        self.pushButton_deselectAll.setObjectName(u"pushButton_deselectAll")
        self.pushButton_deselectAll.setMinimumSize(QSize(0, 50))
        self.pushButton_deselectAll.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout.addWidget(self.pushButton_deselectAll, 6, 1, 1, 1)

        self.comboBox_Shanks_tp3d = QComboBox(Form)
        self.comboBox_Shanks_tp3d.setObjectName(u"comboBox_Shanks_tp3d")
        self.comboBox_Shanks_tp3d.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.comboBox_Shanks_tp3d, 0, 0, 1, 4)

        self.frame_axisNav_vis3D = QFrame(Form)
        self.frame_axisNav_vis3D.setObjectName(u"frame_axisNav_vis3D")
        self.horizontalLayout_axisNav_vis3D = QHBoxLayout(self.frame_axisNav_vis3D)
        self.horizontalLayout_axisNav_vis3D.setObjectName(u"horizontalLayout_axisNav_vis3D")
        self.pushButton_stepBack10_vis3D = QPushButton(self.frame_axisNav_vis3D)
        self.pushButton_stepBack10_vis3D.setObjectName(u"pushButton_stepBack10_vis3D")

        self.horizontalLayout_axisNav_vis3D.addWidget(self.pushButton_stepBack10_vis3D)

        self.pushButton_stepBack1_vis3D = QPushButton(self.frame_axisNav_vis3D)
        self.pushButton_stepBack1_vis3D.setObjectName(u"pushButton_stepBack1_vis3D")

        self.horizontalLayout_axisNav_vis3D.addWidget(self.pushButton_stepBack1_vis3D)

        self.label_selectedAxis_vis3D = QLabel(self.frame_axisNav_vis3D)
        self.label_selectedAxis_vis3D.setObjectName(u"label_selectedAxis_vis3D")
        self.label_selectedAxis_vis3D.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_axisNav_vis3D.addWidget(self.label_selectedAxis_vis3D)

        self.pushButton_stepFwd1_vis3D = QPushButton(self.frame_axisNav_vis3D)
        self.pushButton_stepFwd1_vis3D.setObjectName(u"pushButton_stepFwd1_vis3D")

        self.horizontalLayout_axisNav_vis3D.addWidget(self.pushButton_stepFwd1_vis3D)

        self.pushButton_stepFwd10_vis3D = QPushButton(self.frame_axisNav_vis3D)
        self.pushButton_stepFwd10_vis3D.setObjectName(u"pushButton_stepFwd10_vis3D")

        self.horizontalLayout_axisNav_vis3D.addWidget(self.pushButton_stepFwd10_vis3D)


        self.gridLayout.addWidget(self.frame_axisNav_vis3D, 2, 0, 1, 4)

        self.pushButton_selectAll = QPushButton(Form)
        self.pushButton_selectAll.setObjectName(u"pushButton_selectAll")
        self.pushButton_selectAll.setMinimumSize(QSize(0, 50))
        self.pushButton_selectAll.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout.addWidget(self.pushButton_selectAll, 6, 0, 1, 1)

        self.pushButton_add_region = QPushButton(Form)
        self.pushButton_add_region.setObjectName(u"pushButton_add_region")
        self.pushButton_add_region.setMinimumSize(QSize(0, 50))
        self.pushButton_add_region.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout.addWidget(self.pushButton_add_region, 6, 2, 1, 2)

        self.tableWidgetshank_legend = QTableWidget(Form)
        self.tableWidgetshank_legend.setObjectName(u"tableWidgetshank_legend")
        self.tableWidgetshank_legend.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout.addWidget(self.tableWidgetshank_legend, 3, 0, 1, 2)

        self.frame_33 = QFrame(Form)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setEnabled(True)
        self.frame_33.setMinimumSize(QSize(0, 200))
        self.frame_33.setStyleSheet(u"border-color: rgb(170, 170, 170);\n"
"background-color: rgb(131, 131, 131);\n"
"")
        self.frame_33.setFrameShape(QFrame.NoFrame)
        self.gridLayout_2 = QGridLayout(self.frame_33)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_slicex_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicex_vis3D.setObjectName(u"pushButton_slicex_vis3D")
        icon = QIcon()
        icon.addFile(u"Icons/mri/axis_x.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicex_vis3D.setIcon(icon)
        self.pushButton_slicex_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_2.addWidget(self.pushButton_slicex_vis3D, 2, 3, 1, 1)

        self.pushButton_slicez_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicez_vis3D.setObjectName(u"pushButton_slicez_vis3D")
        icon1 = QIcon()
        icon1.addFile(u"Icons/mri/axis_z.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicez_vis3D.setIcon(icon1)
        self.pushButton_slicez_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_2.addWidget(self.pushButton_slicez_vis3D, 2, 5, 1, 1)

        self.pushButton_slicey_vis3D = QPushButton(self.frame_33)
        self.pushButton_slicey_vis3D.setObjectName(u"pushButton_slicey_vis3D")
        icon2 = QIcon()
        icon2.addFile(u"Icons/mri/axis_y.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_slicey_vis3D.setIcon(icon2)
        self.pushButton_slicey_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_2.addWidget(self.pushButton_slicey_vis3D, 2, 4, 1, 1)

        self.resetCamera_vis3D = QPushButton(self.frame_33)
        self.resetCamera_vis3D.setObjectName(u"resetCamera_vis3D")
        self.resetCamera_vis3D.setEnabled(True)
        self.resetCamera_vis3D.setStyleSheet(u"")
        icon3 = QIcon(QIcon.fromTheme(u"go-home"))
        self.resetCamera_vis3D.setIcon(icon3)
        self.resetCamera_vis3D.setIconSize(QSize(40, 40))
        self.resetCamera_vis3D.setAutoDefault(False)
        self.resetCamera_vis3D.setFlat(False)

        self.gridLayout_2.addWidget(self.resetCamera_vis3D, 2, 0, 1, 1)

        self.change_perspective_vis3D = QPushButton(self.frame_33)
        self.change_perspective_vis3D.setObjectName(u"change_perspective_vis3D")
        self.change_perspective_vis3D.setStyleSheet(u"")
        icon4 = QIcon()
        icon4.addFile(u"Icons/ephys/projection_parallel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.change_perspective_vis3D.setIcon(icon4)
        self.change_perspective_vis3D.setIconSize(QSize(40, 40))

        self.gridLayout_2.addWidget(self.change_perspective_vis3D, 2, 1, 1, 1)

        self.pushButton_alongTraj = QPushButton(self.frame_33)
        self.pushButton_alongTraj.setObjectName(u"pushButton_alongTraj")

        self.gridLayout_2.addWidget(self.pushButton_alongTraj, 2, 6, 1, 1)

        self.pushButton_pitch = QPushButton(self.frame_33)
        self.pushButton_pitch.setObjectName(u"pushButton_pitch")

        self.gridLayout_2.addWidget(self.pushButton_pitch, 2, 8, 1, 1)

        self.pushButton_roll = QPushButton(self.frame_33)
        self.pushButton_roll.setObjectName(u"pushButton_roll")

        self.gridLayout_2.addWidget(self.pushButton_roll, 2, 7, 1, 1)

        self.vtkWidget_vis3D = QVTKRenderWindowInteractor(self.frame_33)
        self.vtkWidget_vis3D.setObjectName(u"vtkWidget_vis3D")
        self.vtkWidget_vis3D.setEnabled(True)
        self.vtkWidget_vis3D.setMinimumSize(QSize(500, 0))
        self.vtkWidget_vis3D.setStyleSheet(u"background-color: rgb(200, 177, 176);")

        self.gridLayout_2.addWidget(self.vtkWidget_vis3D, 0, 0, 1, 9)

        self.gridLayout_2.setColumnMinimumWidth(0, 1)
        self.gridLayout_2.setColumnMinimumWidth(1, 1)
        self.gridLayout_2.setColumnMinimumWidth(2, 1)
        self.gridLayout_2.setColumnMinimumWidth(3, 1)
        self.gridLayout_2.setColumnMinimumWidth(4, 1)
        self.gridLayout_2.setColumnMinimumWidth(5, 1)
        self.gridLayout_2.setRowMinimumHeight(0, 1)

        self.gridLayout.addWidget(self.frame_33, 1, 0, 1, 4)

        self.listWidget_visible_regions = QListWidget(Form)
        self.listWidget_visible_regions.setObjectName(u"listWidget_visible_regions")

        self.gridLayout.addWidget(self.listWidget_visible_regions, 3, 2, 2, 2)

        self.checkBox_forbiddenareas = QCheckBox(Form)
        self.checkBox_forbiddenareas.setObjectName(u"checkBox_forbiddenareas")

        self.gridLayout.addWidget(self.checkBox_forbiddenareas, 4, 0, 1, 1)

        self.checkBox_hideplanes = QCheckBox(Form)
        self.checkBox_hideplanes.setObjectName(u"checkBox_hideplanes")

        self.gridLayout.addWidget(self.checkBox_hideplanes, 4, 1, 1, 1)

        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(Form)

        self.resetCamera_vis3D.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.pushButton_deselectAll.setToolTip(QCoreApplication.translate("Form", u"Uncheck every shank, hiding the regions they traverse (unless another checked shank still needs one)", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_deselectAll.setText(QCoreApplication.translate("Form", u"Deselect All Shanks", None))
#if QT_CONFIG(tooltip)
        self.comboBox_Shanks_tp3d.setToolTip(QCoreApplication.translate("Form", u"Select which shank is highlighted (bolder) in the 3D view", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_stepBack10_vis3D.setToolTip(QCoreApplication.translate("Form", u"Move 10 voxels back along the selected axis", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_stepBack10_vis3D.setText(QCoreApplication.translate("Form", u"<<", None))
#if QT_CONFIG(tooltip)
        self.pushButton_stepBack1_vis3D.setToolTip(QCoreApplication.translate("Form", u"Move 1 voxel back along the selected axis", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_stepBack1_vis3D.setText(QCoreApplication.translate("Form", u"<", None))
        self.label_selectedAxis_vis3D.setText(QCoreApplication.translate("Form", u"no axis selected", None))
#if QT_CONFIG(tooltip)
        self.pushButton_stepFwd1_vis3D.setToolTip(QCoreApplication.translate("Form", u"Move 1 voxel forward along the selected axis", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_stepFwd1_vis3D.setText(QCoreApplication.translate("Form", u">", None))
#if QT_CONFIG(tooltip)
        self.pushButton_stepFwd10_vis3D.setToolTip(QCoreApplication.translate("Form", u"Move 10 voxels forward along the selected axis", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_stepFwd10_vis3D.setText(QCoreApplication.translate("Form", u">>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_selectAll.setToolTip(QCoreApplication.translate("Form", u"Check every shank, showing all the regions each one traverses", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_selectAll.setText(QCoreApplication.translate("Form", u"Select All Shanks", None))
#if QT_CONFIG(tooltip)
        self.pushButton_add_region.setToolTip(QCoreApplication.translate("Form", u"Manually add a specific atlas region to the 3D view, by name", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add_region.setText(QCoreApplication.translate("Form", u"Show Another Region", None))
#if QT_CONFIG(tooltip)
        self.tableWidgetshank_legend.setToolTip(QCoreApplication.translate("Form", u"Each shank's color and visibility -- click a row to select that shank (bolder in 3D); check its box to show the regions it passes through", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_slicex_vis3D.setToolTip(QCoreApplication.translate("Form", u"Select the sagittal (x) axis -- the step buttons below then move the selected shank along it", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicex_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicez_vis3D.setToolTip(QCoreApplication.translate("Form", u"Select the axial (z) axis -- the step buttons below then move the selected shank along it", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicez_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_slicey_vis3D.setToolTip(QCoreApplication.translate("Form", u"Select the coronal (y) axis -- the step buttons below then move the selected shank along it", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_slicey_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.resetCamera_vis3D.setToolTip(QCoreApplication.translate("Form", u"Reset Camera View", None))
#endif // QT_CONFIG(tooltip)
        self.resetCamera_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.change_perspective_vis3D.setToolTip(QCoreApplication.translate("Form", u"Change Perspective", None))
#endif // QT_CONFIG(tooltip)
        self.change_perspective_vis3D.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_alongTraj.setToolTip(QCoreApplication.translate("Form", u"Select the shank's own insert-to-deep axis -- the step buttons below then move it deeper/shallower along its own trajectory", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_alongTraj.setText(QCoreApplication.translate("Form", u"Along\n"
" Trajectory", None))
        self.pushButton_pitch.setText(QCoreApplication.translate("Form", u"pitch", None))
        self.pushButton_roll.setText(QCoreApplication.translate("Form", u"roll", None))
#if QT_CONFIG(tooltip)
        self.listWidget_visible_regions.setToolTip(QCoreApplication.translate("Form", u"Atlas regions currently shown in the 3D view -- check or uncheck to toggle", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_forbiddenareas.setText(QCoreApplication.translate("Form", u"Hide Forbidden Areas", None))
        self.checkBox_hideplanes.setText(QCoreApplication.translate("Form", u"Hide planes", None))
    # retranslateUi

