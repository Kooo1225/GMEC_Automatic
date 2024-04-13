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
        target_tag = self.service.set_target_tag(xml, title)

        section_tag = []
        for item in target_tag:
            section_tag.extend(self.service.set_section_tag(item))
        
        table_cell = []
        for index, item in enumerate(list(set(section_tag))):
            table_cell.extend(self.service.set_table_cell(item, target_tag[index]))

        print(table_cell)
        self.__table_list = self.service.set_table_data(list(set(table_cell)))
    def get_list(self):
        return self.__table_list


