import os
from tkinter import filedialog

from src.service.HwpService import HwpService
from src.exception.CustomException import HwpOpenError, HwpObjectNotFoundError, NotFoundKeyWordError


class HwpController:
    # 의존성 주입을 통한 클래스 생성자 정의
    def __init__(self):
        self.service = HwpService()
        self.__table_list = None

    def get_table_list(self, file_name: str, title: str):
        xml = self.service.hwp2xml(file_name)
        xml_tag = self.service.find_tag(xml, title)
        table_data = self.service.find_table(xml_tag[1])

        self.__table_list = self.service.delete_non_target_data(table_data)

    def get_list(self):
        return self.__table_list
