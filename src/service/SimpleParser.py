import re
import uuid

import numpy as np

from src.service.ParseService import ParseService


class SimpleParser(ParseService):
    def __init__(self):
        self.title = ['진동속도(cm/s)', '진동레벨[dB(V)]', '소음[dB(A)]']
        self.other_simple_version = False

    def extract_columns(self, table_list):
        columns = ['구분', '진동속도(cm/s)', '진동레벨[dB(V)]', '소음[dB(A)]', '최저치', '최고치', '최저치', '최고치', '최저치', '최고치', '허용기준',
                   '비고']

        if '현장관리기준' in table_list:
            self.other_simple_version = True
            table_list = [i for i in table_list if '현장관리기준' not in i]

        return [i for i in table_list if i not in columns and not re.match(r'[^\w\s-]', i)]

    def conversion_error_value(self, non_columns_list):
        conversion_error_list = []

        for item in non_columns_list:
            if self.other_simple_version and re.match(r'n/*?t\(.*?\)', item, re.IGNORECASE):
                conversion_error_list.extend([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
            elif not self.other_simple_version and re.match(r'n/*?t', item, re.IGNORECASE) or item == '-':
                conversion_error_list.append(np.nan)
            else:
                conversion_error_list.append(item)

        return conversion_error_list

    def delete_other_value(self, conversion_error_list):
        filtered_list = []
        skip_count = 0

        for index, item in enumerate(conversion_error_list):
            try:
                if skip_count > 0:
                    skip_count -= 1
                    continue
                elif re.match(r'\d+\.\d+cm/s', item, re.IGNORECASE) and re.match(r'\d+\.\d+cm/s', conversion_error_list[index + 1], re.IGNORECASE):
                    skip_count += 2
                elif re.match(r'\d+\.\d+cm/s', item, re.IGNORECASE) and not re.match(r'\d+\.\d+cm/s', conversion_error_list[index + 1], re.IGNORECASE):
                    skip_count += 1
                else:
                    filtered_list.append(item)
            except TypeError as e:
                filtered_list.append(item)

        return filtered_list

    def classification_by_date(self, filtered_list):
        section_list = []
        current_date_section = []

        for item in filtered_list:
            try:
                if re.match(r'\d+월\d+일', item) and current_date_section:
                    section_list.append(current_date_section)
                    current_date_section = []
                current_date_section.append(item)
            except TypeError as e:
                current_date_section.append(item)

        if current_date_section:
            section_list.append(current_date_section)

        return section_list

    def extract_location(self, classification_list):
        location = []
        data_count = 6

        for items in classification_list:
            for item in items:
                try:
                    if len(location) == 0 and not re.match(r'\d+\.\d+', item) and item is not np.nan and not re.match(
                            r'\d+월\d+일', item):
                        location.append(item)
                    if re.match(r'\d+\.\d+', item) or item is np.nan:
                        data_count -= 1
                    elif data_count == 0 and not re.match(r'\d+월\d+일', item):
                        location.append(item)
                        data_count = 6
                except TypeError as e:
                    data_count -= 1

        return list(set(location))

    def get_dict(self, classification_list, location_list):
        result_dict = {}
        value_list = []

        date_key, location_key = None, None

        for items in classification_list:
            for index, item in enumerate(items):
                if isinstance(item, float):
                    item = str(item)

                if re.match(r'\d+월\d+일', item):
                    date_key = item
                elif item not in location_list:
                    value_list.append(item)
                elif item in location_list:
                    location_key = item
                    unique_key = str(uuid.uuid4())
                    result_dict[location_key] = {} if location_key not in result_dict else result_dict[location_key]

                    result_dict[location_key][unique_key] = {'일시': date_key}
                    idx1, idx2 = index + 1, index + 2
                    for j in range(len(self.title)):
                        result_dict[location_key][unique_key][f'{self.title[j]} 최저치'] = float(items[idx1])
                        result_dict[location_key][unique_key][f'{self.title[j]} 최고치'] = float(items[idx2])
                        idx1 += 2
                        idx2 += 2
                    idx1, idx2 = 0, 0

        return result_dict


