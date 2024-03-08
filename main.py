import sys, os, xlsxwriter

import pandas as pd
import numpy as np

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QRect
from PyQt5.QtWidgets import QShortcut, QMainWindow, QApplication, QTableWidgetItem, QWidget, QTabWidget, QTableWidget, \
    QVBoxLayout, QDialog, QPushButton, QLabel, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, QKeySequence, QFont

from ComplicatedProcess import ComplicateProcess
from SimpleProcess import SimpleProcess

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

        self.radio_btn_group = [self.complicated_btn, self.simple_btn]

        self.dialog = None
        self.layout = None

    def check_btn(self):
        return self.complicated_btn.isChecked() or self.simple_btn.isChecked()

    def go(self):
        if not self.check_btn():
            self.setAlertDialog('Check Radio Button')
            return
        if self.dialog is not None and self.layout is not None:
            self.removeWidgets()
        else:
            try:
                pros = None
                if self.complicated_btn.isChecked():
                    pros = ComplicateProcess()
                elif self.simple_btn.isChecked():
                    pros = SimpleProcess()

                result_dict = self.getHwpData(pros)
                print(f'go {result_dict}')
                self.setDialog(result_dict)
            except ValueError:
                self.setAlertDialog('⛔An error occurred while parsing the file⛔')
            except Exception as e:
                print(e)

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
            try:
                tabs.addTab(self.drawPandas(self.classficationEveningData(df)), i)
            except IndexError:
                tabs.addTab(self.drawPandas(df), i)

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
        self.dialog.resize(400 * len(result_dict), 600)

        self.dialog.setModal(False)
        self.dialog.show()

    def save_table(self, table):
        filename = 'Result'
        with pd.ExcelWriter(f'{filename}.xlsx') as writer:
            for i in table:
                try:
                    data = self.classficationEveningData(pd.DataFrame(table[i]).transpose())
                except:
                    data = pd.DataFrame(table[i]).transpose()
                data.to_excel(writer, sheet_name=i, index=False)

                wb = writer.book
                ws = writer.sheets[i]
                columns = data.columns

                center_alignment = wb.add_format({'align': 'center', 'valign': 'vcenter'})
                # for col_num in range(len(columns)):
                #     ws.set_column(col_num, col_num, None, center_alignment)

                for j, column in enumerate(columns):
                    width = 30
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
    def getHwpData(self, pros):
        self.process = pros
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
