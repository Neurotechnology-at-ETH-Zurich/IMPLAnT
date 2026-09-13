# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tab_samri.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpinBox, QTextEdit, QWidget)

class Ui_tab_samri(object):
    def setupUi(self, tab_samri):
        if not tab_samri.objectName():
            tab_samri.setObjectName(u"tab_samri")
        tab_samri.resize(1428, 990)
        self.gridLayout = QGridLayout(tab_samri)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_4 = QLineEdit(tab_samri)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_4, 0, 0, 1, 1)

        self.pushButton_questionmark_samri = QPushButton(tab_samri)
        self.pushButton_questionmark_samri.setObjectName(u"pushButton_questionmark_samri")
        icon = QIcon()
        icon.addFile(u"Icons/mri/question_mark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_questionmark_samri.setIcon(icon)
        self.pushButton_questionmark_samri.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.pushButton_questionmark_samri, 0, 1, 1, 1)

        self.frame_4 = QFrame(tab_samri)
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
        self.pushButton_fetch.setMinimumSize(QSize(0, 50))
        self.pushButton_fetch.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

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

        self.pushButton_continue = QPushButton(self.frame_4)
        self.pushButton_continue.setObjectName(u"pushButton_continue")
        self.pushButton_continue.setEnabled(False)
        self.pushButton_continue.setMinimumSize(QSize(0, 50))
        self.pushButton_continue.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_138.addWidget(self.pushButton_continue, 5, 1, 2, 2)

        self.pushButton_re_fetch = QPushButton(self.frame_4)
        self.pushButton_re_fetch.setObjectName(u"pushButton_re_fetch")
        self.pushButton_re_fetch.setEnabled(False)
        self.pushButton_re_fetch.setMinimumSize(QSize(0, 50))
        self.pushButton_re_fetch.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_138.addWidget(self.pushButton_re_fetch, 6, 0, 1, 1)

        self.checkBox_bidsflag = QCheckBox(self.frame_4)
        self.checkBox_bidsflag.setObjectName(u"checkBox_bidsflag")
        self.checkBox_bidsflag.setChecked(True)

        self.gridLayout_138.addWidget(self.checkBox_bidsflag, 4, 0, 1, 1)

        self.pushButton_credentials = QPushButton(self.frame_4)
        self.pushButton_credentials.setObjectName(u"pushButton_credentials")

        self.gridLayout_138.addWidget(self.pushButton_credentials, 4, 1, 1, 2)


        self.gridLayout.addWidget(self.frame_4, 0, 2, 2, 1)

        self.plainTextEdit_SAMRI = QPlainTextEdit(tab_samri)
        self.plainTextEdit_SAMRI.setObjectName(u"plainTextEdit_SAMRI")
        self.plainTextEdit_SAMRI.setReadOnly(True)

        self.gridLayout.addWidget(self.plainTextEdit_SAMRI, 1, 0, 2, 2)

        self.frame_samri = QFrame(tab_samri)
        self.frame_samri.setObjectName(u"frame_samri")
        self.frame_samri.setEnabled(False)
        self.frame_samri.setFrameShape(QFrame.StyledPanel)
        self.frame_samri.setFrameShadow(QFrame.Raised)
        self.gridLayout_139 = QGridLayout(self.frame_samri)
        self.gridLayout_139.setObjectName(u"gridLayout_139")
        self.pushButton_register = QPushButton(self.frame_samri)
        self.pushButton_register.setObjectName(u"pushButton_register")
        self.pushButton_register.setMinimumSize(QSize(0, 50))
        self.pushButton_register.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_139.addWidget(self.pushButton_register, 16, 2, 1, 2)

        self.pushButton_browseAtlas = QPushButton(self.frame_samri)
        self.pushButton_browseAtlas.setObjectName(u"pushButton_browseAtlas")

        self.gridLayout_139.addWidget(self.pushButton_browseAtlas, 3, 3, 1, 1)

        self.pushButton_browseBru2 = QPushButton(self.frame_samri)
        self.pushButton_browseBru2.setObjectName(u"pushButton_browseBru2")

        self.gridLayout_139.addWidget(self.pushButton_browseBru2, 1, 3, 1, 1)

        self.lineEdit_7 = QLineEdit(self.frame_samri)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_7, 2, 1, 1, 1)

        self.lineEdit_movMask = QTextEdit(self.frame_samri)
        self.lineEdit_movMask.setObjectName(u"lineEdit_movMask")
        self.lineEdit_movMask.setMaximumSize(QSize(16777215, 100))
        self.lineEdit_movMask.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_movMask, 12, 2, 1, 1)

        self.checkBox_presurgery = QCheckBox(self.frame_samri)
        self.checkBox_presurgery.setObjectName(u"checkBox_presurgery")

        self.gridLayout_139.addWidget(self.checkBox_presurgery, 14, 1, 1, 1)

        self.lineEdit_bru2_path = QTextEdit(self.frame_samri)
        self.lineEdit_bru2_path.setObjectName(u"lineEdit_bru2_path")
        self.lineEdit_bru2_path.setMaximumSize(QSize(16777215, 70))

        self.gridLayout_139.addWidget(self.lineEdit_bru2_path, 1, 2, 1, 1)

        self.comboBox_working_session = QComboBox(self.frame_samri)
        self.comboBox_working_session.setObjectName(u"comboBox_working_session")

        self.gridLayout_139.addWidget(self.comboBox_working_session, 5, 2, 1, 2)

        self.lineEdit_5 = QLineEdit(self.frame_samri)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_5, 1, 1, 1, 1)

        self.lineEdit_10 = QLineEdit(self.frame_samri)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_10, 3, 1, 1, 1)

        self.pushButton_browseBase = QPushButton(self.frame_samri)
        self.pushButton_browseBase.setObjectName(u"pushButton_browseBase")

        self.gridLayout_139.addWidget(self.pushButton_browseBase, 2, 3, 1, 1)

        self.checkBox_atlasmask = QCheckBox(self.frame_samri)
        self.checkBox_atlasmask.setObjectName(u"checkBox_atlasmask")
        self.checkBox_atlasmask.setChecked(True)

        self.gridLayout_139.addWidget(self.checkBox_atlasmask, 4, 1, 1, 1)

        self.lineEdit_14 = QLineEdit(self.frame_samri)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_14, 8, 1, 1, 1)

        self.frame_6 = QFrame(self.frame_samri)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_140 = QGridLayout(self.frame_6)
        self.gridLayout_140.setObjectName(u"gridLayout_140")
        self.pushButton_createMovMask = QPushButton(self.frame_6)
        self.pushButton_createMovMask.setObjectName(u"pushButton_createMovMask")
        self.pushButton_createMovMask.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_140.addWidget(self.pushButton_createMovMask, 1, 0, 1, 1)

        self.pushButton_browseMov = QPushButton(self.frame_6)
        self.pushButton_browseMov.setObjectName(u"pushButton_browseMov")

        self.gridLayout_140.addWidget(self.pushButton_browseMov, 0, 0, 1, 1)


        self.gridLayout_139.addWidget(self.frame_6, 12, 3, 1, 1)

        self.lineEdit_atlas_path = QTextEdit(self.frame_samri)
        self.lineEdit_atlas_path.setObjectName(u"lineEdit_atlas_path")
        self.lineEdit_atlas_path.setMaximumSize(QSize(16777215, 70))

        self.gridLayout_139.addWidget(self.lineEdit_atlas_path, 3, 2, 1, 1)

        self.pushButton_biascorrection = QPushButton(self.frame_samri)
        self.pushButton_biascorrection.setObjectName(u"pushButton_biascorrection")
        self.pushButton_biascorrection.setMinimumSize(QSize(0, 50))
        self.pushButton_biascorrection.setStyleSheet(u" QPushButton { background-color: #e67e22; color: white; } QPushButton:disabled { background-color: #a9713f; color: #cccccc; }")

        self.gridLayout_139.addWidget(self.pushButton_biascorrection, 16, 1, 1, 1)

        self.spinBox_num_threads = QSpinBox(self.frame_samri)
        self.spinBox_num_threads.setObjectName(u"spinBox_num_threads")

        self.gridLayout_139.addWidget(self.spinBox_num_threads, 8, 2, 1, 2)

        self.checkBox_mov_mask = QCheckBox(self.frame_samri)
        self.checkBox_mov_mask.setObjectName(u"checkBox_mov_mask")
        self.checkBox_mov_mask.setChecked(True)

        self.gridLayout_139.addWidget(self.checkBox_mov_mask, 9, 1, 1, 1)

        self.lineEdit_11 = QLineEdit(self.frame_samri)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_11, 12, 1, 1, 1)

        self.lineEdit_17 = QLineEdit(self.frame_samri)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_17, 6, 1, 1, 1)

        self.lineEdit_16 = QLineEdit(self.frame_samri)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_16, 7, 1, 1, 1)

        self.checkBox_elastic = QCheckBox(self.frame_samri)
        self.checkBox_elastic.setObjectName(u"checkBox_elastic")
        self.checkBox_elastic.setChecked(True)

        self.gridLayout_139.addWidget(self.checkBox_elastic, 15, 1, 1, 1)

        self.comboBox_register_key = QComboBox(self.frame_samri)
        self.comboBox_register_key.setObjectName(u"comboBox_register_key")

        self.gridLayout_139.addWidget(self.comboBox_register_key, 7, 2, 1, 2)

        self.lineEdit_base_path = QTextEdit(self.frame_samri)
        self.lineEdit_base_path.setObjectName(u"lineEdit_base_path")
        self.lineEdit_base_path.setMaximumSize(QSize(16777215, 70))

        self.gridLayout_139.addWidget(self.lineEdit_base_path, 2, 2, 1, 1)

        self.lineEdit_animalID = QLineEdit(self.frame_samri)
        self.lineEdit_animalID.setObjectName(u"lineEdit_animalID")
        self.lineEdit_animalID.setStyleSheet(u"color: rgb(224, 27, 36);")
        self.lineEdit_animalID.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_animalID, 0, 1, 1, 3)

        self.lineEdit_15 = QLineEdit(self.frame_samri)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setReadOnly(True)

        self.gridLayout_139.addWidget(self.lineEdit_15, 5, 1, 1, 1)

        self.comboBox_tasks = QComboBox(self.frame_samri)
        self.comboBox_tasks.setObjectName(u"comboBox_tasks")

        self.gridLayout_139.addWidget(self.comboBox_tasks, 6, 2, 1, 2)

        self.pushButton_paths = QPushButton(self.frame_samri)
        self.pushButton_paths.setObjectName(u"pushButton_paths")

        self.gridLayout_139.addWidget(self.pushButton_paths, 15, 2, 1, 2)


        self.gridLayout.addWidget(self.frame_samri, 2, 2, 1, 1)


        self.retranslateUi(tab_samri)

        QMetaObject.connectSlotsByName(tab_samri)
    # setupUi

    def retranslateUi(self, tab_samri):
        tab_samri.setWindowTitle(QCoreApplication.translate("tab_samri", u"Form", None))
        self.lineEdit_4.setText(QCoreApplication.translate("tab_samri", u"SAMRI - Logging Output", None))
#if QT_CONFIG(tooltip)
        self.pushButton_questionmark_samri.setToolTip(QCoreApplication.translate("tab_samri", u"Re-show the current step's instructions (fetch, then select session).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_questionmark_samri.setText("")
        self.lineEdit_8.setText(QCoreApplication.translate("tab_samri", u"Server", None))
#if QT_CONFIG(tooltip)
        self.pushButton_fetch.setToolTip(QCoreApplication.translate("tab_samri", u"Download this animal's data from the Bruker server before continuing.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_fetch.setText(QCoreApplication.translate("tab_samri", u"Fetch Data from Server", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_server.setToolTip(QCoreApplication.translate("tab_samri", u"Hostname/address of the Bruker MRI server to fetch data from.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_animalid.setToolTip(QCoreApplication.translate("tab_samri", u"Animal ID used to locate this subject's data on the server and in the local raw-data folder.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_9.setText(QCoreApplication.translate("tab_samri", u"Password", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_rawBase.setToolTip(QCoreApplication.translate("tab_samri", u"Local base folder for raw/fetched data; combined with the Animal ID to detect whether this session was already fetched.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_password.setToolTip(QCoreApplication.translate("tab_samri", u"Password for the Bruker server. Entering it here only affects this run \u2014 it is not currently saved back to disk.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_browse.setToolTip(QCoreApplication.translate("tab_samri", u"Browse for the local raw-data base folder.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_browse.setText(QCoreApplication.translate("tab_samri", u"Browse", None))
        self.lineEdit_6.setText(QCoreApplication.translate("tab_samri", u"Raw Base", None))
        self.lineEdit_12.setText(QCoreApplication.translate("tab_samri", u"Animal ID", None))
#if QT_CONFIG(tooltip)
        self.pushButton_continue.setToolTip(QCoreApplication.translate("tab_samri", u"Skip fetching and continue directly with data already present at the raw-data path (enabled once that path exists).", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_continue.setText(QCoreApplication.translate("tab_samri", u"Continue without Data-Fetch", None))
#if QT_CONFIG(tooltip)
        self.pushButton_re_fetch.setToolTip(QCoreApplication.translate("tab_samri", u"Re-download all sessions for this animal, including ones already fetched.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_re_fetch.setText(QCoreApplication.translate("tab_samri", u"Re-Fetch All Sessions", None))
#if QT_CONFIG(tooltip)
        self.checkBox_bidsflag.setToolTip(QCoreApplication.translate("tab_samri", u"Convert the fetched data into BIDS format.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_bidsflag.setText(QCoreApplication.translate("tab_samri", u"Enable bids_flag", None))
        self.pushButton_credentials.setText(QCoreApplication.translate("tab_samri", u"Save Credentials", None))
#if QT_CONFIG(tooltip)
        self.pushButton_register.setToolTip(QCoreApplication.translate("tab_samri", u"Run registration using the settings configured on this tab.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_register.setText(QCoreApplication.translate("tab_samri", u"Register", None))
#if QT_CONFIG(tooltip)
        self.pushButton_browseAtlas.setToolTip(QCoreApplication.translate("tab_samri", u"Browse for the atlas folder to register against.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_browseAtlas.setText(QCoreApplication.translate("tab_samri", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.pushButton_browseBru2.setToolTip(QCoreApplication.translate("tab_samri", u"Browse for the raw Bruker2Bids data folder.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_browseBru2.setText(QCoreApplication.translate("tab_samri", u"Browse", None))
        self.lineEdit_7.setText(QCoreApplication.translate("tab_samri", u"Base path", None))
#if QT_CONFIG(tooltip)
        self.checkBox_presurgery.setToolTip(QCoreApplication.translate("tab_samri", u"Mark this session as the pre-surgery scan (affects how it's registered).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_presurgery.setText(QCoreApplication.translate("tab_samri", u"Presurgery", None))
#if QT_CONFIG(tooltip)
        self.comboBox_working_session.setToolTip(QCoreApplication.translate("tab_samri", u"Which session (ses-*) of this animal to register.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_5.setText(QCoreApplication.translate("tab_samri", u"Bru2 path", None))
        self.lineEdit_10.setText(QCoreApplication.translate("tab_samri", u"Atlas Files", None))
#if QT_CONFIG(tooltip)
        self.pushButton_browseBase.setToolTip(QCoreApplication.translate("tab_samri", u"Browse for the base (reference) data folder.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_browseBase.setText(QCoreApplication.translate("tab_samri", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.checkBox_atlasmask.setToolTip(QCoreApplication.translate("tab_samri", u"Restrict the registration metric to the atlas mask region instead of the whole brain volume.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_atlasmask.setText(QCoreApplication.translate("tab_samri", u"Use Atlas Mask", None))
        self.lineEdit_14.setText(QCoreApplication.translate("tab_samri", u"Num Threads", None))
#if QT_CONFIG(tooltip)
        self.pushButton_createMovMask.setToolTip(QCoreApplication.translate("tab_samri", u"Create a moving mask for registration by segmenting the working-session anatomical scan.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_createMovMask.setText(QCoreApplication.translate("tab_samri", u"Create \n"
" Moving  Mask", None))
#if QT_CONFIG(tooltip)
        self.pushButton_browseMov.setToolTip(QCoreApplication.translate("tab_samri", u"Browse for an existing moving-mask NIfTI file.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_browseMov.setText(QCoreApplication.translate("tab_samri", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.pushButton_biascorrection.setToolTip(QCoreApplication.translate("tab_samri", u"Run bias-field correction only, without registration.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_biascorrection.setText(QCoreApplication.translate("tab_samri", u"Biascorrection ONLY", None))
#if QT_CONFIG(tooltip)
        self.spinBox_num_threads.setToolTip(QCoreApplication.translate("tab_samri", u"Number of CPU threads to use for registration (1\u20138).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkBox_mov_mask.setToolTip(QCoreApplication.translate("tab_samri", u"Use a moving-image mask during registration; enables the mask path field and the button to create one.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_mov_mask.setText(QCoreApplication.translate("tab_samri", u"Use moving mask", None))
        self.lineEdit_11.setText(QCoreApplication.translate("tab_samri", u"Moving Mask", None))
        self.lineEdit_17.setText(QCoreApplication.translate("tab_samri", u"Tasks", None))
        self.lineEdit_16.setText(QCoreApplication.translate("tab_samri", u"Register Key", None))
#if QT_CONFIG(tooltip)
        self.checkBox_elastic.setToolTip(QCoreApplication.translate("tab_samri", u"Use elastic (deformable) registration instead of rigid/affine.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_elastic.setText(QCoreApplication.translate("tab_samri", u"Elastic", None))
#if QT_CONFIG(tooltip)
        self.comboBox_register_key.setToolTip(QCoreApplication.translate("tab_samri", u"Which scan sequence (protocol name) to use for registration.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_animalID.setText(QCoreApplication.translate("tab_samri", u"Animal ID", None))
        self.lineEdit_15.setText(QCoreApplication.translate("tab_samri", u"Working Session", None))
#if QT_CONFIG(tooltip)
        self.comboBox_tasks.setToolTip(QCoreApplication.translate("tab_samri", u"Anatomical view/orientation (coronal, sagittal, or axial) of the acquired scan to register.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_paths.setText(QCoreApplication.translate("tab_samri", u"Save  all paths", None))
    # retranslateUi

