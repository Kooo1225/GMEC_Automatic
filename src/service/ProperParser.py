import re, uuid
import numpy as np

from src.service.ParseService import ParseService


class ProperParser(ParseService):
    def __init__(self):
        self.title = ['진동속도(cm/s)', '진동레벨(dB(V))', '소음레벨(dB(A))']

    def extract_columns(self, table_list):
        columns = ['일자', '발파횟수', '시간', '관리기준', '측정결과', '진동속도(cm/s)', '진동레벨(dB(V))', '소음레벨(dB(A))', '계측위치']
        return [ i for i in table_list if not i in columns ]

    def conversion_error_value(self, non_columns_list):
        conversion_error_list = []

        for item in non_columns_list:
            if re.match(r'n/*?t', item, re.IGNORECASE) or item == '-' or item == '감지안됨':
                conversion_error_list.append(np.nan)
            else:
                conversion_error_list.append(item)

        return conversion_error_list

    def delete_other_value(self, conversion_error_list):
        filtered_list = []
        skip_count = 0

        for index, item in enumerate(conversion_error_list):
            if skip_count > 0:
                skip_count -= 1
                continue
            elif re.match(r'\d+:\d+', str(item)) and re.match(r'\d+회', str(conversion_error_list[index - 1])):
                filtered_list.append(item)
                skip_count += 3
            else:
                filtered_list.append(item)

        return filtered_list

    def classification_by_date(self, filtered_list):
        section = []
        current_date_section = []

        for item in filtered_list:
            if re.match(r'\d+월\d+일', str(item)) and current_date_section:
                section.append(current_date_section)
                current_date_section = []

            current_date_section.append(item)

        if current_date_section:
            section.append(current_date_section)

        return section

    def extract_location(self, classification_list):
        location_list = []
        data_count = 0

        for items in classification_list:
            for item in items:
                if re.match(r'\d+\.\d+', str(item)) or item is np.nan:
                    data_count += 1
                elif data_count >= 3:
                    location_list.append(item)
                    data_count = 0

        return location_list

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
                    unique_key = uuid.uuid4()

                    result[location_key] = {} if location_key not in result else result[location_key]
                    result[location_key][unique_key] = {'일시': time_key}

                    for idx in range(len(self.title)):
                        try:
                            tmp = float(value[idx])
                        except ValueError:
                            tmp = np.nan

                        result[location_key][unique_key][self.title[idx]] = tmp

                    value = []

        return result