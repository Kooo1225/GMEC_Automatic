# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\4th.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(302, 144)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\ui\\../../../../Downloads/KakaoTalk_20240322_152353247-removebg-preview.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(24, 25))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 20, 90, 16))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(120, 50, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.comboBox.setFont(font)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(120, 90, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.startBtn.setFont(font)
        self.startBtn.setObjectName("startBtn")
        self.checkBtn = QtWidgets.QPushButton(self.centralwidget)
        self.checkBtn.setGeometry(QtCore.QRect(200, 10, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.checkBtn.setFont(font)
        self.checkBtn.setObjectName("checkBtn")
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitBtn.setGeometry(QtCore.QRect(200, 90, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.exitBtn.setFont(font)
        self.exitBtn.setObjectName("exitBtn")
        self.complicated_btn = QtWidgets.QRadioButton(self.centralwidget)
        self.complicated_btn.setGeometry(QtCore.QRect(20, 20, 90, 16))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.complicated_btn.setFont(font)
        self.complicated_btn.setObjectName("complicated_btn")
        self.simple_btn = QtWidgets.QRadioButton(self.centralwidget)
        self.simple_btn.setGeometry(QtCore.QRect(20, 60, 90, 16))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.simple_btn.setFont(font)
        self.simple_btn.setObjectName("simple_btn")
        self.proper_btn = QtWidgets.QRadioButton(self.centralwidget)
        self.proper_btn.setGeometry(QtCore.QRect(20, 98, 90, 16))
        font = QtGui.QFont()
        font.setFamily("Han Santteut Dotum")
        self.proper_btn.setFont(font)
        self.proper_btn.setObjectName("proper_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 302, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Guff"))
        self.label.setText(_translate("MainWindow", "표 페이지 제목"))
        self.comboBox.setItemText(0, _translate("MainWindow", "일자별 발파 및 계측 현황"))
        self.comboBox.setItemText(1, _translate("MainWindow", "일자별 계측 현황"))
        self.comboBox.setItemText(2, _translate("MainWindow", "직접 입력"))
        self.startBtn.setText(_translate("MainWindow", "Start"))
        self.checkBtn.setText(_translate("MainWindow", "Sys Check"))
        self.exitBtn.setText(_translate("MainWindow", "Exit"))
        self.complicated_btn.setText(_translate("MainWindow", "복잡이"))
        self.simple_btn.setText(_translate("MainWindow", "간단이"))
        self.proper_btn.setText(_translate("MainWindow", "어중이떠중이"))
