import os
import lxml.etree as ET
import re

class HwpService:
    def hwp2xml(self, file_path: str):
        exefile="hwp5proc"

        mXml = f'{file_path[:-4]}.xml'
        mHwp = file_path
        command = f'{exefile} xml "{mHwp}" > "{mXml}"'

        try:
            os.system(command)
        except:
            pass

        return mXml

    def find_tag(self, xml, search_text: str):
        tree = ET.parse(xml)
        root = tree.getroot()

        result_tag = []
        for elem in root.iter():
            if elem.text and search_text in elem.text:
                for find_tag in elem.iterancestors():
                    if find_tag.tag == "ColumnSet":
                        result_tag.append(find_tag)

        return result_tag
    
    def find_table(self, xml_tag):
        table_data = []
        current_table_data = []

        for cell in xml_tag.findall(".//TableCell"):
            cell_data = {
                "row": cell.get("row"),
                "col": cell.get("col"),
                "text": "".join(elem.text for elem in cell.findall(".//Text") if elem.text)
            }

            if len(current_table_data) != 0 and cell_data['row'] == '0' and cell_data['col'] == '0':
                table_data.append(current_table_data)
                current_table_data = [cell_data]
            else:
                current_table_data.append(cell_data)
        
        if current_table_data:
            table_data.append(current_table_data)

        return table_data
    
    def delete_non_target_data(self, table_data):
        target_data_text = ['일자', '계측위치', '진동레벨', '소음레벨']

        target_data = [
            sublist for sublist in table_data
            if any(
                entry['row'] in ['0', '1'] and any(keyword in entry['text'] for keyword in target_data_text)
                for entry in sublist
            )
        ]

        text_data = []
        for items in target_data:
            for item in items:
                text_data.append(item['text'].replace(" ", ""))
        
        text_data = list(filter(lambda x: x, text_data))
        return text_data
    