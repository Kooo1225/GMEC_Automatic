import pandas as pd
import re

from controller.hwpController import hwpController
from service.pandasService import pandasService

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class pandasController:
    def __init__(self):
        self.service = pandasService()
        self.__clipboard_list = []
        self.location_list = []
        self.section_list = []
        self.result = {}

    def parseItems(self):
        self.__clipboard_list = self.service.extractColumns(self.__clipboard_list)
        # print(f'ExtractColumns\n{self.__clipboard_list}')
        self.__clipboard_list = self.service.conversionErrorValue(self.__clipboard_list)
        # print(f'ConversionErrorValue\n{self.__clipboard_list}')
        self.section_list = self.service.classificationByDate(self.__clipboard_list)
        # print(f'ClassficationByDate\n{self.section_list}')
        self.section_list = self.service.delOtherValue(self.section_list)
        # print(f'DelOtherValue\n{self.section_list}')

    def getLocation(self):
        self.location_list = self.service.extractLocation(self.section_list)

    def list2Dictionary(self):
        self.result = self.service.getDict(self.section_list, self.location_list)

    def getResult(self):
        return self.result

    def setList(self, items_list):
        self.__clipboard_list = items_list

    def getLocationList(self):
        return self.location_list

    def getItemList(self):
        return self.__clipboard_list

    def getSectionList(self):
        return self.section_list