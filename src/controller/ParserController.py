import pandas as pd

from src.service.ComplicatedParser import ComplicatedParser
from src.service.ParseService import ParseService


class ParserController:
    def __init__(self, parser: ParseService, table_list):
        self.parser = parser
        self.table_list = table_list
        self.result_dict = None
        self.location_list = None

    def run_parse(self):
        non_columns_list = self.parser.extract_columns(self.table_list)
        conversion_error_list = self.parser.conversion_error_value(non_columns_list)
        filtered_list = self.parser.delete_other_value(conversion_error_list)
        classification_list = self.parser.classification_by_date(filtered_list)

        self.location_list = self.parser.extract_location(classification_list)
        self.result_dict = self.parser.get_dict(classification_list, self.location_list)

    def get_result_dict(self):
        return self.result_dict

    def get_location_list(self):
        return self.location_list
