#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
 
from PyQt5 import QtCore, QtGui, QtWidgets
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 416)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(70, 60, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(70, 110, 54, 12))
        self.label_2.setObjectName("label_2")
        self.name_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.name_lineEdit.setGeometry(QtCore.QRect(150, 60, 113, 20))
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.password_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.password_lineEdit.setGeometry(QtCore.QRect(150, 110, 113, 20))
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.login_btn = QtWidgets.QPushButton(self.centralWidget)
        self.login_btn.setGeometry(QtCore.QRect(150, 230, 75, 23))
        self.login_btn.setObjectName("login_btn")
        self.msg_plainTextEdit = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.msg_plainTextEdit.setGeometry(QtCore.QRect(380, 60, 211, 171))
        self.msg_plainTextEdit.setObjectName("msg_plainTextEdit")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 630, 23))
        self.menuBar.setObjectName("menuBar")
        self.menuPyQt5 = QtWidgets.QMenu(self.menuBar)
        self.menuPyQt5.setObjectName("menuPyQt5")
        self.menupython3 = QtWidgets.QMenu(self.menuBar)
        self.menupython3.setObjectName("menupython3")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionlist = QtWidgets.QAction(MainWindow)
        self.actionlist.setObjectName("actionlist")
        self.actionlis2 = QtWidgets.QAction(MainWindow)
        self.actionlis2.setObjectName("actionlis2")
        self.actionlist3 = QtWidgets.QAction(MainWindow)
        self.actionlist3.setObjectName("actionlist3")
        self.menupython3.addSeparator()
        self.menupython3.addAction(self.actionlist)
        self.menupython3.addAction(self.actionlis2)
        self.menupython3.addAction(self.actionlist3)
        self.menuBar.addAction(self.menuPyQt5.menuAction())
        self.menuBar.addAction(self.menupython3.menuAction())
 
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyQt5_Test"))
        self.label.setText(_translate("MainWindow", "用户名"))
        self.label_2.setText(_translate("MainWindow", "密码"))
        self.login_btn.setText(_translate("MainWindow", "登陆"))
        self.menuPyQt5.setTitle(_translate("MainWindow", "PyQt5"))
        self.menupython3.setTitle(_translate("MainWindow", "python3"))
        self.actionlist.setText(_translate("MainWindow", "list"))
        self.actionlis2.setText(_translate("MainWindow", "lis2"))
        self.actionlist3.setText(_translate("MainWindow", "list3"))
