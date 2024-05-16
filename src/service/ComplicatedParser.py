import re, uuid
import numpy as np
from itertools import takewhile
from src.service.ParseService import ParseService


class ComplicatedParser:
    def delete_non_target_data(self, table_data):
        """
        한글 표에서 원하지 않은 부분까지 나온 데이터를 정리하여 리스트로 반환합니다.
        target_data_text에 표에 반복적으로 들어가는 텍스트를 입력하여 필요없는 데이터를 삭제합니다.
        """
        target_data_text = ['일시', '발파', '진동', '소음', 'STA', '시간']

        target_data = [
            sublist for sublist in table_data
            if any(
                entry['row'] in ['0', '1'] and any(keyword in entry['text'] for keyword in target_data_text)
                for entry in sublist
            )
        ]
        
        target_data = [[item for item in items if item['text'] != ''] for items in target_data]

        return target_data

    def extract_columns(self, table_list):
        """
        한글 표에서 공통적인 컬럼 부분을 추출합니다.
        컬럼은 대부분 표의 시작 부분에 작성되기 때문에 row 값은 0 혹은 1에 위치하게 됩니다.
        이후 컬럼 값들이 딕셔너리로 저장되어 있기 때문에 중복을 제거 후 리스트로 반환합니다.
        """
        columns = []
        for items in table_list:
            for item in items:
                if item not in [i for i in columns]:
                    if int(item['row']) == 0 or int(item['row']) == 1:
                        columns.append(item)

        return columns
    
    def extract_non_column_data(self, table_list, columns):
        """
        한글 표에서 컬럼 부분을 제거한 나머지 데이터들을 반환합니다.
        """
        return [[item for item in items[len(columns):] if not int(item['colspan']) > 1]for items in table_list]


    def group_by_date(self, dict_list):
        """
        한글 표 데이터를 날짜 별로 분류하여 리스트로 저장하여 반환합니다.
        날짜 별 분류는 하나의 TableCell에 포함된 동일한 row값들 끼리 묶는 것으로 수행합니다.
        """
        group_list = []

        for items in dict_list:
            rows = list(set([int(item['row']) for item in items]))
            for row in rows:
                temp = [item for item in items if int(item['row'])==row]
                group_list.append(temp)
        
        return [items for items in group_list if len(items) > 1] 
    
    def update_merge_data(self, group_list):
        """
        한글 표에 병합 처리된 셀에 대한 데이터 처리를 완료한 뒤 리스트로 반환합니다.
        병합 처리되어 있어 row에 포함되어 있지 않는 값은 이전의 셀을 참조하여 값을 추가합니다.
        반복 횟수는 하나의 row가 가지는 최대값 즉 하나의 row가 가져야하는 col의 길이를 나타내게 됩니다.
        이를 통해 row 내 부족한 col = index 를 확인하고 값을 추가합니다.
        """
        max_len = max(len(item) for item in group_list)

        for idx, items in enumerate(group_list):
            temp = []
            r = [i for i in range(max_len) if not any(int(item['col']) == i for item in items)]
            if len(r) > 0 and idx != 0:
                temp = [group_list[idx-1][row] for row in r ]
            
            new_item = temp + items
            group_list[idx] = new_item
        
        return group_list
    
    def serialize_to_dict(self, group_list, columns):
        """
        컬럼 리스트와 파싱이 끝난 그룹 리스트를 이용해서 데이터를 분류한 뒤 리스트로 반환합니다.
        컬럼 리스트에 대응하는 값들을 그룹 리스트에서 찾아서 추가해주는 작업을 수행합니다.
        """
        serialize_list = []
        find_word = ['일시', '시간', 'cm', 'dB', '측정위치']

        columns = [item for item in columns if int(item['colspan']) <= 1 and any(word in item['text'] for word in find_word)]
        for items in group_list:
            data = {}
            for item in items:
                for column in columns:
                    if item['col'] == column['col']:
                        data[column['text']] = item['text']
            serialize_list.append(data)

        return serialize_list
