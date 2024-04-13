import sys
from tkinter import filedialog

import pandas as pd

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QIcon

from src.controller.HwpController import HwpController
from src.controller.ModalController import ModalViewController
from src.controller.PandasController import PandasController
from src.controller.ParserController import ParserController
from src.exception.CustomException import *
from src.service.ComplicatedParser import ComplicatedParser
from src.service.ProperParser import ProperParser
from src.service.SimpleParser import SimpleParser
from ui.main_ui import Ui_MainWindow
from ui.res import *


class MWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':icon/main_icon.ico'))

        self.startBtn.clicked.connect(self.go)
        self.exitBtn.clicked.connect(self.exit)
        self.checkBtn.clicked.connect(self.check_regedit)
        self.complicated_btn.toggled.connect(self.on_radio_btn_toggle)
        self.simple_btn.toggled.connect(self.on_radio_btn_toggle)
        self.proper_btn.toggled.connect(self.on_radio_btn_toggle)
        self.radio_btn = None

        self.hwp_controller = HwpController()
        self.modal_controller = ModalViewController()
        self.pandas_controller = PandasController()
        self.parser_controller = None

    def check_btn(self):
        return self.complicated_btn.isChecked() or self.simple_btn.isChecked() or self.proper_btn.isChecked()

    def on_radio_btn_toggle(self):
        self.radio_btn = self.sender()

    def select_parser(self, parser_name):
        if parser_name == "복잡이":
            return ComplicatedParser()
        elif parser_name == "간단이":
            return SimpleParser()
        elif parser_name == "어중이떠중이":
            return ProperParser()

    def go(self):
        if self.radio_btn is None:
            self.modal_controller.set_error_view('⚠️표 종류를 선택해주세요⚠️', 'Exit', 'Select Parser')
            self.modal_controller.get_dialog().show()
            return

        try:
            # 1. 한글에서 표 데이터 가져오기 ( 파일명이랑 표 제목 매개로 보내기 )
            filepath, _ = QFileDialog.getOpenFileName(self, "Open File", "")
            self.hwp_controller.get_table_list(filepath, self.comboBox.currentText())
            # table_list = self.hwp_controller.get_list()
            # print(len(table_list))

            # # 2. 사용자가 선택한 Parser로 데이터 분석하기
            # self.parser_controller = ParserController(self.select_parser(self.radio_btn.text()), table_list)
            # self.parser_controller.run_parse()
            # result_dict = self.parser_controller.get_result_dict()

            # # 3. Dict -> DataFrame으로 변경하고 리스트로 관리하기
            # dataframe_list = []
            # for item in result_dict:
            #     dataframe = pd.DataFrame(result_dict[item]).transpose().reset_index(drop=True)
            #     dataframe.index = dataframe.index.astype(str)

            #     self.pandas_controller.classification_evening_data_from_dataframe(dataframe, self.radio_btn.text())
            #     dataframe = self.pandas_controller.get_dataframe()

            #     dataframe_list.append([item, dataframe])

            # self.modal_controller.set_tabs_view(dataframe_list)
            # self.modal_controller.get_dialog().show()
        except HwpOpenError as open_error:
            self.modal_controller.set_error_view('⚠️HWP 열기에 실패하였습니다⚠️', 'Exit', 'HWP Error')
            self.modal_controller.get_dialog().show()
        except HwpObjectNotFoundError as not_found_error:
            self.modal_controller.set_error_view('⚠️HWP 객체를 탐색하지 못했습니다⚠️', 'Exit', 'HWP Error')
            self.modal_controller.get_dialog().show()
        except NotFoundKeyWordError as not_found_key_word:
            self.modal_controller.set_error_view('⚠️HWP 키워드를 탐색하지 못했습니다⚠️', 'Exit', 'HWP Error')
            self.modal_controller.get_dialog().show()
        except ParseException as parse_exception:
            self.modal_controller.set_error_view("⚠️HWP 표 분석 중 에러가 발생했습니다⚠️", 'Exit', 'Parse Error')
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

    def exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sil = MWindow()
    sil.show()
    app.exec_()
