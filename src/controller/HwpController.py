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
        # target_tag는 별 문제 없음
        target_tag = self.service.set_target_tag(xml, title)

        # section_tag도 별 문제 없음
        column_tag = []
        for item in target_tag:
            column_tag.append(self.service.set_column_tag(item))
        
        if len(list(set(column_tag))) == 1:
            column_tag = [column_tag[0]]
            target_tag = [target_tag[0]]      

        table_cell = []
        for index in range(len(column_tag)):
            table_cell.extend(self.service.set_table_cell(column_tag[index], target_tag[index]))

        self.__table_list = table_cell
        
        os.remove(xml)

    def get_list(self):
        return self.__table_list


