import numpy as np
import re

title = ['발파진동(cm/s)', '진동레벨dB(V)', '소음레벨dB(A)']

class pandasService:
    def __init__(self):
        pass

    def extractColumns(self, item_list):
        columns = []

        for i in item_list:
            if isinstance(i, str) and not bool(re.search(r'\d', i)):
                columns.append(i)
            else:
                break

        items_list = list(filter(lambda x: x not in columns, item_list))

        return items_list

    def conversionErrorValue(self, item_list):
        for x, i in enumerate(item_list):
            if i == "계측기오류":
                for j in range(0, 3):
                    if j < 1:
                        item_list.pop(x + j)
                    item_list.insert(x + j, "계측기 오류")

        return item_list

    def classificationByDate(self, item_list):
        section = []
        current_section = []

        for i in item_list:
            if re.match(r'\d+월\d+일', i):
                if current_section:
                    section.append(current_section)
                    current_section = []
            current_section.append(i)

        if current_section:
            section.append(current_section)

        return section

    def delOtherValue(self, section_list):
        section2 = []

        for j in section_list:
            temp_list = []
            first_key = None
            for x, i in enumerate(j):
                if first_key is None and re.match(r'\d.*?\.\d+[~-]\d+\.\d+', i):
                    first_key = i
                elif first_key is not None and re.match(r'\d.*?\.\d+[~-]\d+\.\d+', i):
                    first_key = None
                elif first_key is None and i != '계' and j[x - 1] != '계':
                    temp_list.append(i)
            section2.append(temp_list)

        return section2

    def extractLocation(self, section_list):
        location = []
        date_count, count_count, time_count, pass_count = None, None, None, 0

        for i in section_list:
            for j in i:
                # if j.replace("(", "").replace(")", "").isalnum() and not j.isdigit() and not re.match(r'\d+월\d+일', j) and not re.match(r'\d+회', j):
                if re.match(r'\d+월\d+일', j):
                    date_count = True
                elif re.match(r'\d+회', j):
                    count_count = True
                elif re.match(r'\d+:\d+', j):
                    time_count = True
                elif date_count and count_count and time_count and pass_count == 3:
                    location.append(j)
                    pass_count = 0
                elif date_count and count_count and time_count:
                    pass_count += 1

        return list(set(location))

    def getDict(self, section_list, location_list):
        result = {}
        value = []

        date_key, time_key, count_key, location_key = None, None, None, None

        for item in section_list:
            for x, i in enumerate(item):
                if re.match(r"\d+월\d+일", i):
                    date_key = i
                elif re.match(r"\d+회", i):
                    count_key = i
                elif re.match(r'\d+:\d+', i):
                    time_key = i
                elif i not in location_list:
                    value.append(i)
                elif i in location_list:
                    location_key = i
                    result[location_key] = {} if location_key not in result else result[location_key]
                    result[location_key][f'{time_key} | {count_key}'] = {'일시': f'{date_key} {time_key}'}

                    for j in range(len(title)):
                        tmp = None
                        try:
                            tmp = float(value[j])
                        except ValueError:
                            tmp = np.nan
                        finally:
                            result[location_key][f'{time_key} | {count_key}'][title[j]] = tmp
                    value = []

        return result

