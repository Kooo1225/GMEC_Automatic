import re, uuid
import numpy as np
from itertools import takewhile
from src.service.ParseService import ParseService


class ComplicatedParser(ParseService):
    def __init__(self):
        self.title = ['발파진동(cm/s)', '진동레벨dB(V)', '소음레벨dB(A)']
        self.blast_pattern = None

    def extract_columns(self, items_list):
        columns = list(takewhile(lambda x: not re.match(r'\d+월\d+일', x), items_list))
        if '발파패턴' in columns:
            self.blast_pattern = True
        else:
            self.blast_pattern = False

        return [i for i in items_list if i not in columns]

    def conversion_error_value(self, non_columns_list):
        conversion_error_list = []

        for item in non_columns_list:
            if item == "계측기오류" or item == "SD카드오류":
                conversion_error_list.extend([np.nan, np.nan, np.nan])
            elif re.match(r'n/*?t', item, re.IGNORECASE) or item == "-":
                conversion_error_list.append(np.nan)
            else:
                conversion_error_list.append(item)

        # print(conversion_error_list)
        return conversion_error_list

    def delete_other_value(self, conversion_error_list):
        filtered_list = []
        skip_count = 0

        for index in range(len(conversion_error_list)):
            try:
                if skip_count > 0:
                    skip_count -= 1
                    continue
                elif conversion_error_list[index] == '계' or conversion_error_list[index - 1] == '계':
                    continue
                elif re.match(r'\d+:\d+', conversion_error_list[index]) and re.match(r'\d+회', conversion_error_list[index - 1]):
                    filtered_list.append(conversion_error_list[index])
                    if self.blast_pattern == "발파패턴":
                        skip_count += 4
                    else:
                        skip_count += 3
                else:
                    filtered_list.append(conversion_error_list[index])
            except TypeError as e:
                filtered_list.append(conversion_error_list[index])

        # print(filtered_list)
        return filtered_list

    def classification_by_date(self, filtered_list):
        section = []
        current_date_section = []

        for i in filtered_list:
            try:
                if re.match(r'\d+월\d+일', i) and current_date_section:
                    section.append(current_date_section)
                    current_date_section = []
                current_date_section.append(i)
            except TypeError as t:
                current_date_section.append(i)

        if current_date_section:
            section.append(current_date_section)

        # print(section)
        return section

    def extract_location(self, classification_list):
        location_list = []
        data_count = 0

        for items in classification_list:
            for item in items:
                try:
                    if re.match(r'\d+\.\d+', item) or item is np.nan:
                        data_count += 1
                    elif data_count >= 3:
                        location_list.append(item)
                        data_count = 0
                except TypeError as t:
                    data_count += 1
        # print(sorted(list(set(location_list))))
        return sorted(list(set(location_list)))

    def get_dict(self, classification_list, location_list):
        result = {}
        value = []

        date_key, location_key = None, None

        for items in classification_list:
            for index, item in enumerate(items):
                if re.match(r'\d+월\d+일', str(item)):
                    date_key = item
                elif date_key and re.match(r'\d+:\d+', str(item)):
                    blast_time = item
                    time_key = f'{date_key} {blast_time}'
                elif re.match(r'\d+\.\d+', str(item)) or item is np.nan:
                    value.append(item)
                elif item in location_list:
                    location_key = item
                    unique_key = str(uuid.uuid4())

                    result[location_key] = {} if location_key not in result else result[location_key]
                    result[location_key][unique_key] = {'일시': time_key}

                    for idx in range(len(self.title)):
                        try:
                            tmp = float(value[idx])
                        except ValueError:
                            tmp = np.nan

                        result[location_key][unique_key][self.title[idx]] = tmp

                    value = []

        # print(result)
        return result
