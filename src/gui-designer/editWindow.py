# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editWindow.ui'
#
# Created: Thu Jan 13 02:47:58 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 176)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 130, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.fontComboBox = QtGui.QFontComboBox(Dialog)
        self.fontComboBox.setGeometry(QtCore.QRect(0, 10, 231, 22))
        self.fontComboBox.setObjectName("fontComboBox")
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(0, 40, 231, 81))
        self.textEdit.setObjectName("textEdit")
        self.kcolorbutton = KColorButton(Dialog)
        self.kcolorbutton.setGeometry(QtCore.QRect(10, 140, 48, 24))
        self.kcolorbutton.setObjectName("kcolorbutton")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kdeui import KColorButton
