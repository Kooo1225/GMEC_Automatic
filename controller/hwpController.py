import pandas as pd
import win32com.client as win32
import clipboard, re

from service.hwpService import hwpService
from service.hwpService import checkReg

find_title = ['일자별 발파 및 계측 현황', '일자별 계측 현황']


class hwpController:
    def __init__(self):
        self.__hwp_file_name = None
        self.__items_list = []
        self.__service = hwpService()

        self.__hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
        self.__hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")  # 보안 모듈 등록 > 첫 화면에 대화 상자 스킵
        self.__hwp.XHwpWindows.Item(0).Visible = True  # 화면에 화면이 보일지 말지 결정하는 값

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

    def get__hwp(self):
        return self.__hwp

    def updateReg(self):
        try:
            checkReg()
        except:
            pass
        finally:
            self.closeHwp()

    def openHwp(self):
        self.__hwp_file_name = self.__service.getHwpName()
        self.__service.openHwp(self.__hwp, self.__hwp_file_name)

    def getClipboard(self, title: str):
        first_page, target_page = self.__service.findPage(self.__hwp, title)
        self.__service.delPage(self.__hwp, first_page, target_page)
        self.__service.delCtrl(self.__hwp)

        result_clipboard = self.__service.copyGrapgh(self.__hwp)
        self.__service.closeHwp(self.__hwp)

        self.__items_list = list(filter(lambda v: v, result_clipboard.replace("\r\n", " ").split(" ")))

    def getList(self):
        return self.__items_list

    def get_file_name(self):
        return self.__hwp_file_name

    def closeHwp(self):
        self.__service.closeHwp(self.__hwp)
