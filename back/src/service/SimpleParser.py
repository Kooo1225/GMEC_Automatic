import numpy as np
from src.service.ParseService import ParseService

class SimpleParser:
    def delete_non_target_data(self, table_data):
        """
        한글 표에서 원하지 않은 부분까지 나온 데이터를 정리하여 리스트로 반환합니다.
        target_data_text에 표에 반복적으로 들어가는 텍스트를 입력하여 필요없는 데이터를 삭제합니다.
        """
        target_data_text = ['구분', '진동속도', '진동레벨', '소음', '허용기준', '비고']

        target_data = [
            sublist for sublist in table_data
            if any(
                entry['row'] in ['1', '2'] and any(keyword in entry['text'] for keyword in target_data_text)
                for entry in sublist
            )
        ]

        target_data = [[item for item in items if item['text'] != ''] for items in target_data]

        return target_data

    def extract_columns(self, table_list):
        """
        한글 표에서 공통적인 컬럼 부분을 추출합니다.
        컬럼은 대부분 표의 시작 부분에 작성되기 때문에 row 값은 0 혹은 1에 위치하게 됩니다.
        또한 한글 표를 row순서대로 읽기 때문에 특정 병합이 되어 있을 경우
        한글에선 뒤에 있는 컬럼이 앞에 있을 수 있기 때문에 해당 부분도 max함수와 row값을 이용해서 조정합니다.
        이후 컬럼 값들이 딕셔너리로 저장되어 있기 때문에 중복을 제거 후 리스트로 반환합니다.
        """
        columns = []
        for items in table_list:
            for item in items:
                if item not in [i for i in columns]:
                    row = int(item['row'])

                    if row == 0 and row == 0:
                        continue
                    elif row == 1 or row == 2:
                        columns.append(item)
        
        data = {
            'row': 0,
            'col': 0,
            'colspan': 1,
            'rowspan': 1,
            'text': '일시'
        }
        columns.insert(0, data)

        return columns
    
    def extract_non_column_data(self, table_list, columns):
        """
        한글 표에서 컬럼 부분을 제거한 나머지 데이터들을 반환합니다.
        """
        dict_list = []
        for items in table_list:
            data = []
            for item in items:
                if not int(item['colspan']) > 1 and item['text'] not in [column['text'] for column in columns]:
                    data.append(item)
            dict_list.append(data)

        return dict_list

    def group_by_date(self, dict_list):
        """
        한글 표 데이터를 날짜 별로 분류하여 리스트로 저장하여 반환합니다.
        날짜 별 분류는 하나의 TableCell에 포함된 동일한 row값들 끼리 묶는 것으로 수행합니다.
        """
        group_list = []

        for items in dict_list:
            rows = list(set([int(item['row']) for item in items]))
            for row in rows:
                temp = [item for item in items if int(item['row']) == row]
                group_list.append(temp)
        
        return group_list
    
    def update_merge_data(self, group_list):
        """
        한글 표에 병합 처리된 셀에 대한 데이터 처리를 완료한 뒤 리스트로 반환합니다.
        SimpleParser에서는 병합 셀이 아닌 셀의 최초 값이 공통 값으로 결정되기 때문에 이를 통해 값을 추가합니다.
        """
        cached_head_data = []

        for idx, items in enumerate(group_list):
            if len(items) == 1:
                cached_head_data = items

            new_items = []
            if any(data not in items for data in cached_head_data):
                new_items.extend(cached_head_data)

            group_list[idx] = new_items + items

        return [items for items in group_list if len(items) != 1]

    
    def serialize_to_dict(self, group_list, columns):
        """
        컬럼 리스트와 파싱이 끝난 그룹 리스트를 이용해서 데이터를 분류한 뒤 리스트로 반환합니다.
        컬럼 리스트에 대응하는 값들을 그룹 리스트에서 찾아서 추가해주는 작업을 수행합니다.
        """
        serialize_list = []
        cached_columns = []
        
        for item in columns:
            if int(item['colspan']) > 1:
                for t in ['최저치', '최고치']:
                    data = {
                        'row': item['row'],
                        'col': item['col'],
                        'colspan': item['colspan'],
                        'rowspan': item['rowspan'],
                        'text': f'{item['text']} {t}'
                    }
                    cached_columns.append(data)
            else:
                cached_columns.append(item)

        for items in group_list:
            data = {column['text']: item['text'] for column, item in zip(cached_columns, items) if column != '발파횟수'}
            serialize_list.append(data)

        return serialize_list
