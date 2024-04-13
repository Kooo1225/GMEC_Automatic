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

    def set_target_tag(self, xml, search_text: str):
        tree = ET.parse(xml)
        root = list(tree.getroot().iter())

        target_tag = []
        for item in root:
            if item.text and search_text in item.text and item.text.startswith(search_text):
                target_tag.append(item)
        
        return target_tag
    
    def set_section_tag(self, target_tag):
        section_tag = []
        
        for item in target_tag.iterancestors():
            if item.tag == "SectionDef":
                section_tag.append(item)

        return section_tag
    
    def set_table_cell(self, section_tag, target_tag):
        table_tag = []
        start_collecting = False

        for item in section_tag.iter():
            if item == target_tag:
                start_collecting = True
            elif start_collecting and item.tag == "TableCell":
                table_tag.append(item)

        return table_tag

    def set_table_data(self, table_tag):
        table_data = []

        for cell in table_tag:
            cell_data = "".join(elem.text for elem in cell.findall(".//Text") if elem.text)
            table_data.append(cell_data)
        return table_data
    
    # def delete_non_target_data(self, table_data):
    #     target_data_text = ['일자', '계측위치', '진동레벨', '소음레벨']

    #     target_data = [
    #         sublist for sublist in table_data
    #         if any(
    #             entry['row'] in ['0', '1'] and any(keyword in entry['text'] for keyword in target_data_text)
    #             for entry in sublist
    #         )
    #     ]

    #     text_data = []
    #     for items in target_data:
    #         for item in items:
    #             text_data.append(item['text'].replace(" ", ""))
        
    #     text_data = list(filter(lambda x: x, text_data))
    #     return text_data
    