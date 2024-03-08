import pandas as pd
import numpy as np

from PyQt5.QtCore import QThread, QEventLoop, QTimer
from PyQt5.QtWidgets import QTableWidgetItem

from controller.hwpController import hwpController
from service.simpleService import simple_service

class SimpleProcess(QThread):
    def __init__(self):
        super().__init__()

        self.h_controller = hwpController()
        self.s_controller = simple_service()

    # start로 시작할 부분
    def go(self, findStr='일자별 계측 현황'):
        self.h_controller.openHwp()
        self.h_controller.getClipboard(findStr)
        items_list = self.h_controller.getList()

        convert_list = self.s_controller.parsing_clipboard(items_list)
        print(convert_list)
        result = self.s_controller.classfication_by_location(convert_list)
        print(result)


        return result

    def get_file_name(self):
        return self.h_controller.get_file_name()

    def stop(self):
        self.h_controller.closeHwp()

    def checkReg(self):
        self.h_controller.updateReg()

    # time.sleep 효과를 스레드에서 실행하는 방법
    @staticmethod
    def timeSleep(wait_time):
        loop = QEventLoop()
        QTimer.singleShop(wait_time, loop.quit)
        loop.exec_()

