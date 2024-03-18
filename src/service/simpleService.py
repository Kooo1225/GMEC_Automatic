import pandas as pd
import numpy as np
import clipboard, re


class simple_service():
    def __init__(self):
        self.__columns = ['구분', '진동속도(cm/s)', '진동레벨[dB(V)]', '소음[dB(A)]', '허용기준', '비고']
        self.__columns2 = ['최저치', '최고치']

    def parsing_clipboard(self, clipboard_data):
        clipboard_list = [i for i in clipboard_data if i not in self.__columns and i not in self.__columns2]
        clipboard_list = list(map(lambda x: np.nan if x == '-' else x, clipboard_list))

        convert_list = []
        for i in clipboard_list:
            try:
                convert_list.append(float(i))
            except:
                convert_list.append(i)

        return convert_list

    def classfication_by_location(self, convert_list):
        classfication_dict = {}
        data_list = []
        current_data = []
        date_key, location_key = None, None

        for x, i in enumerate(convert_list):
            if re.match(r'\d+월\d+일', str(i)):
                date_key = i
            elif date_key and re.match(r'[\uAC00-\uD7A3]+', str(i)):
                location_key = i
            elif date_key and location_key:
                if len(data_list) >= 4:
                    for idx, sublist in enumerate(data_list):
                        if location_key not in classfication_dict:
                            classfication_dict[location_key] = {}
                        if f'{date_key} {x}' not in classfication_dict[location_key]:
                            classfication_dict[location_key][f'{date_key} {x}'] = {}
                        if idx == 0:
                            classfication_dict[location_key][f'{date_key} {x}']['일시'] = date_key
                        for sub_idx, data in enumerate(sublist):
                            if idx == 3:
                                classfication_dict[location_key][f'{date_key} {x}'][f'{self.__columns[idx + 1]}'] = data
                                classfication_dict[location_key][f'{date_key} {x}'][f'{self.__columns[idx + 2]}'] = sublist[
                                    sub_idx + 1]
                                break
                            else:
                                classfication_dict[location_key][f'{date_key} {x}'][
                                    f'{self.__columns[idx + 1]}{self.__columns2[sub_idx]}'] = data

                    data_list = []

                if not current_data or len(current_data) < 2:
                    current_data.append(i)
                else:
                    data_list.append(current_data)
                    current_data = [i]

        return classfication_dict