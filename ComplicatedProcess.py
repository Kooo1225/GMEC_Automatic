import pandas as pd
import numpy as np

from PyQt5.QtCore import QThread, QEventLoop, QTimer
from PyQt5.QtWidgets import QTableWidgetItem

from controller.hwpController import hwpController
from controller.pandasController import pandasController

class ComplicateProcess(QThread):
    def __init__(self):
        super().__init__()

        self.h_controller = hwpController()
        self.p_controller = pandasController()
        self.pd_dict = {}

    # start로 시작할 부분
    def go(self, findStr):
        self.h_controller.openHwp()
        self.h_controller.getClipboard(findStr)
        items_list = self.h_controller.getList()

        self.p_controller.setList(items_list)
        self.p_controller.parseItems()
        self.p_controller.getLocation()
        self.p_controller.list2Dictionary()

        self.pd_dict = self.p_controller.getResult()

        return self.pd_dict

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
