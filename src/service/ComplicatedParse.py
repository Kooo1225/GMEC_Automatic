import re

from src.service.ParseService import ParseService


class ComplicatedParse(ParseService):
    def __init__(self, table_list):
        self.table_list = table_list
        self.result_list = None

    def extract_columns(self):
        columns = []

        for i in self.table_list:
            if isinstance(i, str) and not bool(re.search(r'\d', i)):
                columns.append(i)
            else:
                break

        self.result_list = list(filter(lambda x: x not in columns, self.table_list))

    def conversion_error_value(self):
        for x, i in enumerate(self.result_list):
            if i == "계측기오류":
                for j in range(0, 3):
                    if j < 1:
                        self.result_list.pop(x + j)
                    self.result_list.insert(x + j, "계측기 오류")

    def classification_by_date(self):
        section = []
        current_section = []

        for i in self.result_list:
            if re.match(r'\d+월\d+일', i):
                if current_section:
                    section.append(current_section)
                    current_section = []
            current_section.append(i)

        if current_section:
            section.append(current_section)

        self.result_list = section

    def delete_other_value(self):
        section = []

        for j in self.result_list:
            temp_list = []
            first_key = None
            for x, i in enumerate(j):
                if first_key is None and re.match(r'\d.*?\.\d+[~-]\d+\.\d+', i):
                    first_key = i
                elif first_key is not None and re.match(r'\d.*?\.\d+[~-]\d+\.\d+', i):
                    first_key = None
                elif first_key is None and i != '계' and j[x - 1] != '계':
                    temp_list.append(i)
            section.append(temp_list)

        self.result_list = section

    def extract_location(self):
        pass

    def get_dict(self):
        pass