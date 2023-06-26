# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/FileExplorer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileExplorer(object):
    def setupUi(self, FileExplorer):
        FileExplorer.setObjectName("FileExplorer")
        FileExplorer.resize(400, 165)
        FileExplorer.setMinimumSize(QtCore.QSize(400, 165))
        FileExplorer.setMaximumSize(QtCore.QSize(400, 165))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\resources/open_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FileExplorer.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(FileExplorer)
        self.buttonBox.setGeometry(QtCore.QRect(230, 120, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(FileExplorer)
        self.widget.setGeometry(QtCore.QRect(10, 21, 381, 81))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(19, 19))
        self.pushButton.setMaximumSize(QtCore.QSize(19, 19))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)

        self.retranslateUi(FileExplorer)
        self.buttonBox.accepted.connect(FileExplorer.accept)
        self.buttonBox.rejected.connect(FileExplorer.reject)
        QtCore.QMetaObject.connectSlotsByName(FileExplorer)

    def retranslateUi(self, FileExplorer):
        _translate = QtCore.QCoreApplication.translate
        FileExplorer.setWindowTitle(_translate("FileExplorer", " File Explorer"))
        self.label.setText(_translate("FileExplorer", "Path to directory"))
        self.pushButton.setText(_translate("FileExplorer", "..."))
