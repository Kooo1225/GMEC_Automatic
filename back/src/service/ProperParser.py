from src.service.ParseService import ParseService

class ProperParser:
    def delete_non_target_data(self, table_data):
        """
        한글 표에서 원하지 않은 부분까지 나온 데이터를 정리하여 리스트로 반환합니다.
        target_data_text에 표에 반복적으로 들어가는 텍스트를 입력하여 필요없는 데이터를 삭제합니다.
        """
        target_data_text = ['일자', '계측위치', '진동레벨', '진동속도', '소음레벨']

        target_data = [
            sublist for sublist in table_data
            if any(
                entry['row'] in ['0', '1'] and any(keyword in entry['text'] for keyword in target_data_text)
                for entry in sublist
            )
        ]

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
        """
        group_list = []

        for items in dict_list:
            rows = list(set([int(item['row']) for item in items]))
            for row in rows:
                temp = [item for item in items if int(item['row'])==row]
                group_list.append(temp)
        
        return group_list
    
    def update_merge_data(self, group_list):
        """
        한글 표에 병합 처리된 셀에 대한 데이터 처리를 완료한 뒤 리스트로 반환합니다.
        병합 처리된 셀은 rowspan 값을 이용하여 탐지한 뒤 해당 row값이 없는 리스트에 추가해 줍니다.
        """
        cached_merge_data = []
        cached_head_data = []
        
        for idx, items in enumerate(group_list):
            head_data = [data for data in items if int(data['col']) == 0 and int(data['rowspan']) > 1]
            merge_data = [data for data in items if int(data['col']) != 0 and int(data['rowspan']) > 1]
            
            if head_data:
                cached_head_data = head_data
            if merge_data:
                cached_merge_data = merge_data

            new_items = []
            if any(data not in items for data in cached_head_data):
                new_items.extend(cached_head_data)
            if any(data not in items for data in cached_merge_data):
                new_items.extend(cached_merge_data)

            group_list[idx] = new_items + items
        
        return group_list
    
    def serialize_to_dict(self, group_list, columns):
        """
        컬럼 리스트와 파싱이 끝난 그룹 리스트를 이용해서 데이터를 분류한 뒤 리스트로 반환합니다.
        컬럼 리스트에 대응하는 값들을 그룹 리스트에서 찾아서 추가해주는 작업을 수행합니다.
        """
        serialize_list = []

        columns = [item for item in columns if int(item['colspan']) <= 1]
        for items in group_list:
            data = {column['text']: item['text'] for column, item in zip(columns, items) if column != '발파횟수'}
            serialize_list.append(data)

        return serialize_list