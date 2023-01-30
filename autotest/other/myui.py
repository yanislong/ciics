#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import mainwindow
 
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
 
 
def button_clicked_event():
    global mainwindow_ui
    name = mainwindow_ui.name_lineEdit.text()
    pwd = mainwindow_ui.password_lineEdit.text()
    msg_value = name + " " + pwd
    print(msg_value)
    mainwindow_ui.msg_plainTextEdit.setPlainText(str(msg_value))
 
 
#################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow_ui = mainwindow.Ui_MainWindow()
    qMainWindow = QMainWindow()
    mainwindow_ui.setupUi(qMainWindow)
    mainwindow_ui.login_btn.clicked.connect(button_clicked_event)
    qMainWindow.show()
 
    sys.exit(app.exec_())
