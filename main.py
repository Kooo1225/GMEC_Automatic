import sys, os, xlsxwriter

import pandas as pd
import numpy as np

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QRect
from PyQt5.QtWidgets import QShortcut, QMainWindow, QApplication, QTableWidgetItem, QWidget, QTabWidget, QTableWidget, \
    QVBoxLayout, QDialog, QPushButton, QLabel, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, QKeySequence, QFont

from ComplicatedProcess import ComplicateProcess

UI = uic.loadUiType(r'.\ui\4th.ui')[0]


class MWindow(QMainWindow, UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.process = None

        self.setWindowTitle("GMEC")
        self.startBtn.clicked.connect(self.go)
        self.exitBtn.clicked.connect(self.exit)
        self.checkBtn.clicked.connect(self.checkReg)

        self.dialog = None
        self.layout = None

    def go(self):
        if self.dialog is not None and self.layout is not None:
            self.removeWidgets()
        else:
            try:
                result_dict = self.getHwpData()
                self.setDialog(result_dict)
            except ValueError:
                self.setAlertDialog('⛔An error occurred while parsing the file⛔')

    def setAlertDialog(self, alert_text: str):
        self.initDialog()

        self.layout.addWidget(self.initLabel(alert_text, self.dialog))
        self.layout.addWidget(self.initButton('Done', self.dialog, self.dialog_close))

        self.dialog.setWindowTitle("Detect Error")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(100, 50)

        self.dialog.setModal(True)
        self.dialog.show()

    # Dialog 가져오기 기능 변경하기
    # 어떻게 변경하려고 한거였을까?
    def setDialog(self, result_dict):
        self.initDialog()

        # 탭을 활용해서 데이터를 카테고리 별로 데이터를 분류
        tabs = QTabWidget(self.dialog)
        for i in result_dict:
            df = pd.DataFrame(result_dict[i]).transpose()
            tabs.addTab(self.drawPandas(self.classficationEveningData(df)), i)

        self.layout.addWidget(tabs)
        self.layout.addWidget(self.initButton('Done', self.dialog, self.dialog_close))

        btn = QPushButton('Save', self.dialog)
        btn.clicked.connect(lambda: self.save_table(result_dict))

        font = QFont()  # 현재 폰트 가져오기
        font.setFamily("Han Santteut Dotum")  # 글꼴 설정

        btn.setFont(font)  # 폰트 설정 적용

        self.layout.addWidget(btn)

        # QDialog 세팅
        self.dialog.setWindowTitle('Result')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(130 * len(result_dict), 600)

        self.dialog.setModal(False)
        self.dialog.show()

    def save_table(self, table):
        filename = 'Result'
        print(table)
        with pd.ExcelWriter(f'{filename}.xlsx') as writer:
            for i in table:
                data = self.classficationEveningData(pd.DataFrame(table[i]).transpose())
                data.to_excel(writer, sheet_name=i, index=False)

                wb = writer.book
                ws = writer.sheets[i]
                columns = data.columns

                center_alignment = wb.add_format({'align': 'center', 'valign': 'vcenter'})
                # for col_num in range(len(columns)):
                #     ws.set_column(col_num, col_num, None, center_alignment)

                for j, column in enumerate(columns):
                    width = 15
                    ws.set_column(j, j, width, center_alignment)

    # 자주 등장하는 초기화 과정을 함수로 묶어보면 어떨가 하는 내 생각
    def initDialog(self):
        self.dialog = QDialog()
        self.layout = QVBoxLayout(self.dialog)

    def initButton(self, button_msg: str, attached_instance, attached_action):
        button = QPushButton(button_msg, attached_instance)
        button.clicked.connect(attached_action)

        font = QFont()  # 현재 폰트 가져오기
        font.setFamily("Han Santteut Dotum")  # 글꼴 설정

        button.setFont(font)  # 폰트 설정 적용

        return button

    def initLabel(self, label_text: str, attached_instance):
        label = QLabel(attached_instance)
        label.setText(label_text)

        font = label.font()  # 현재 폰트 가져오기
        font.setFamily("Han Santteut Dotum")  # 글꼴 설정
        font.setPointSize(9)  # 글꼴 크기 설정
        label.setFont(font)  # 폰트 설정 적용

        return label

    def checkReg(self):
        ComplicateProcess().checkReg()

    def dialog_close(self):
        self.dialog.close()
        self.removeWidgets()

    # 위젯 지우기 >> 이거 없으면 이전 데이터랑 섞여버림
    def removeWidgets(self):
        self.dialog = None
        self.layout = None

    # 한글 데이터 가져오기
    def getHwpData(self):
        self.process = ComplicateProcess()
        return self.process.go(self.comboBox.currentText())

    # pandas 마지막에 저녁 데이터 분류
    # 해당 기능도 유지
    def classficationEveningData(self, df):
        new_columns = []

        for x, i in enumerate(list(df.index)):
            time = int(df.loc[i, '일시'].split(" ")[1].split(":")[0])
            if time >= 18:
                new_columns.append(df.loc[i, '소음레벨dB(A)'])
                df.loc[i, '소음레벨dB(A)'] = np.nan
            else:
                new_columns.append(np.nan)

        df['After 18:00'] = new_columns
        df.loc['MIN'] = df.min()
        df.loc['MAX'] = df.max()

        return df

    # 해당 기능은 유지
    def drawPandas(self, df):
        tableWidget = QTableWidget(self)

        tableWidget.setRowCount(len(df.index))
        tableWidget.setColumnCount(len(df.columns))
        tableWidget.setHorizontalHeaderLabels(df.columns)
        tableWidget.setVerticalHeaderLabels(df.index)

        for row_index, row in enumerate(df.index):
            alignment = Qt.AlignCenter

            tableWidget.horizontalHeader().setDefaultAlignment(alignment)
            tableWidget.verticalHeader().setDefaultAlignment(alignment)

            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(alignment)
                tableWidget.setItem(row_index, col_index, item)

        tableWidget.setStyleSheet("""
            QTableView {
                border: 1px solid black;
            }
        
            QTableView::item {
                padding-top: 5px;    /* top padding */
                padding-bottom: 5px; /* bottom padding */
            }
        """)

        vbox = QVBoxLayout()
        vbox.addWidget(tableWidget)

        tab = QWidget()
        tab.setLayout(vbox)

        return tab

    def exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sil = MWindow()
    sil.show()
    app.exec_()
