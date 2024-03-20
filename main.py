import sys, os, xlsxwriter
from tkinter import filedialog

import pandas as pd
import numpy as np

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QRect
from PyQt5.QtWidgets import QShortcut, QMainWindow, QApplication, QTableWidgetItem, QWidget, QTabWidget, QTableWidget, \
    QVBoxLayout, QDialog, QPushButton, QLabel, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, QKeySequence, QFont

from src.controller.HwpController import HwpController
from src.controller.ModalController import ModalViewController
from src.controller.ParserController import ParserController
from src.exception.CustomException import HwpObjectNotFoundError, HwpOpenError
from src.service.ComplicatedParser import ComplicatedParser
from src.service.SimpleParser import SimpleParser
from ui.temp_ui import Ui_MainWindow


class MWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.startBtn.clicked.connect(self.go)
        self.exitBtn.clicked.connect(self.exit)
        self.checkBtn.clicked.connect(self.check_regedit)
        self.complicated_btn.toggled.connect(self.on_radio_btn_toggle)
        self.simple_btn.toggled.connect(self.on_radio_btn_toggle)
        self.radio_btn = None

        self.hwp_controller = HwpController()
        self.modal_controller = ModalViewController()
        self.parser_controller = None

    def check_btn(self):
        return self.complicated_btn.isChecked() or self.simple_btn.isChecked()

    def on_radio_btn_toggle(self):
        self.radio_btn = self.sender()

    def select_parser(self, parser_name):
        if parser_name == "복잡이":
            return ComplicatedParser()
        elif parser_name == "간단이":
            return SimpleParser()

    def go(self):
        if self.radio_btn is None:
            self.modal_controller.set_error_view('⚠️표 종류를 선택해주세요⚠️', 'Exit', 'Select Parser')
            self.modal_controller.get_dialog().show()
            return

        try:
            # 1. 한글에서 표 데이터 가져오기 ( 파일명이랑 표 제목 매개로 보내기 )
            self.hwp_controller.get_table_list(filedialog.askopenfilename(), self.comboBox.currentText())
            table_list = self.hwp_controller.get_list()
            print(table_list)

            # # 2. 사용자가 선택한 Parser로 데이터 분석하기
            self.parser_controller = ParserController(self.select_parser(self.radio_btn.text()), table_list)
            self.parser_controller.run_parse()
            result_dict = self.parser_controller.get_result_dict()

            self.modal_controller.set_tabs_view(result_dict, self.radio_btn.text())
            self.modal_controller.get_dialog().show()
        except HwpOpenError as open_error:
            self.modal_controller.set_error_view('⚠️HWP 열기에 실패하였습니다⚠️', 'Exit', 'HWP Error')
            self.modal_controller.get_dialog().show()
        except HwpObjectNotFoundError as not_found_error:
            self.modal_controller.set_error_view('⚠️HWP 객체를 탐색하지 못했습니다⚠️', 'Exit', 'HWP Error')
            self.modal_controller.get_dialog().show()
        except Exception as error:
            print(error)

    def check_regedit(self):
        try:
            self.hwp_controller.check_and_create_reg()
            self.modal_controller.set_error_view('Success👌', 'Exit', 'Regedit Manager')
            self.modal_controller.get_dialog().show()
        except KeyError as e:
            self.modal_controller.set_error_view(f'{e}', 'Exit', 'Regedit Manager')
            self.modal_controller.get_dialog().show()

    # def save_table(self, table):
    #     filename = 'Result'
    #     with pd.ExcelWriter(f'{filename}.xlsx') as writer:
    #         for i in table:
    #             try:
    #                 data = self.classficationEveningData(pd.DataFrame(table[i]).transpose())
    #             except:
    #                 data = pd.DataFrame(table[i]).transpose()
    #             data.to_excel(writer, sheet_name=i, index=False)
    #
    #             wb = writer.book
    #             ws = writer.sheets[i]
    #             columns = data.columns
    #
    #             center_alignment = wb.add_format({'align': 'center', 'valign': 'vcenter'})
    #             # for col_num in range(len(columns)):
    #             #     ws.set_column(col_num, col_num, None, center_alignment)
    #
    #             for j, column in enumerate(columns):
    #                 width = 30
    #                 ws.set_column(j, j, width, center_alignment)



    def exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sil = MWindow()
    sil.show()
    app.exec_()
