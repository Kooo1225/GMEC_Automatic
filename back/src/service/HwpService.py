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
        root = tree.getroot()
        elements = list(root.iter())

        target_tag = []
        for item in elements:
            if item.text and search_text in item.text and item.text.startswith(search_text):
                target_tag.append(item)
        
        return target_tag
    
    def set_column_tag(self, target_tag):
        column_tag = None
        
        for item in target_tag.iterancestors():
            if item.tag == "ColumnSet":
                column_tag = item

        return column_tag
    
    def set_table_cell(self, column_tag, target_tag):
        table_tag = []
        current_table_tag = []
        start_collecting = False

        for item in column_tag.iter():
            if item == target_tag:
                start_collecting = True
            elif start_collecting and item.tag == "TableCell":
                data = {
                    'row': item.get('row'),
                    'col': item.get('col'),
                    'colspan': item.get('colspan'),
                    'rowspan': item.get('rowspan'),
                    'text': "".join(elem.text for elem in item.findall(".//Text") if elem.text).replace(" ", "")
                }

                if len(current_table_tag) != 0 and data['row'] == '0' and data['col'] == '0':
                    table_tag.append(current_table_tag)
                    current_table_tag = [data]
                else:
                    current_table_tag.append(data)

        if current_table_tag:
            table_tag.append(current_table_tag)

        return table_tag

