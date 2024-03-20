import numpy as np
import pandas as pd
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, \
    QWidget, QHeaderView
from PyQt5.QtCore import Qt


# 현재 ModalViewService에서 한번에 통합된 동작을 함
# 이 부분을 좀 더 디테일하게 나눠서 Controller에서 통합된 동작을 하게 하는게 좋을듯 함
class ModalViewService:

    def set_tabs_dialog(self, dialog: QDialog, data_dict: dict, parser_name: str):
        layout = QVBoxLayout()
        tabs = QTabWidget(dialog)

        for item in data_dict:
            df = pd.DataFrame(data_dict[item]).transpose()
            # df = df.reset_index()
            if parser_name == '복잡이':
                tabs.addTab(self.draw_dataframe(self.classification_time_data(df)), item)
            elif parser_name == '간단이':
                tabs.addTab(self.draw_dataframe(df), item)

        layout.addWidget(tabs)
        layout.addWidget(self.init_button('Done', dialog))

        # save_btn = QPushButton('Save', dialog)
        # save_btn.clicked.connect(lambda: self.save_table(data_dict))
        # font = QFont()
        # font.setFamily('Han Santteut Dotum')
        # save_btn.setFont(font)
        #
        # layout.addWidget(save_btn)

        dialog.setLayout(layout)
        dialog.setWindowTitle('분석 결과')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(150 * len(data_dict), 700)

        dialog.setModal(False)

    def set_alert_dialog(self, dialog: QDialog, alert_text: str, btn_text: str, title_text: str):
        layout = QVBoxLayout()
        layout.addWidget(self.init_label(alert_text))
        layout.addWidget(self.init_button(btn_text, dialog))

        dialog.setWindowTitle(title_text)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setLayout(layout)
        dialog.resize(100, 50)

        dialog.setModal(True)

    def classification_time_data(self, df: pd.DataFrame):
        new_columns = []
        for index, item in enumerate(list(df.index)):
            time = int(df.loc[item, '일시'].split(" ")[1].split(':')[0])
            if time >= 18:
                new_columns.append(df.loc[item, '소음레벨dB(A)'])
                df.loc[item, '소음레벨dB(A)'] = np.nan
            else:
                new_columns.append(np.nan)

        df['Atfter 18:00'] = new_columns
        df.loc['MIN'] = df.min()
        df.loc['MAX'] = df.max()

        return df

    def draw_dataframe(self, df):
        tableWidget = QTableWidget()

        tableWidget.setRowCount(len(df.index))
        tableWidget.setColumnCount(len(df.columns))
        tableWidget.setHorizontalHeaderLabels(df.columns)
        tableWidget.setVerticalHeaderLabels(df.index)
        # tableWidget.resizeColumnsToContents()
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for row_index, row in enumerate(df.index):
            alignment = Qt.AlignCenter

            tableWidget.horizontalHeader().setDefaultAlignment(alignment)
            tableWidget.verticalHeader().setDefaultAlignment(alignment)

            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(alignment)
                tableWidget.setItem(row_index, col_index, item)

        tableWidget.setStyleSheet("""
            QTableView {
                border: 1px solid black;
            }

            QTableView::item {
                padding-top: 5px;    /* top padding */
                padding-bottom: 5px; /* bottom padding */
            }
        """)

        vbox = QVBoxLayout()
        vbox.addWidget(tableWidget)

        tab = QWidget()
        tab.setLayout(vbox)

        return tab

    def init_label(self, alert_text):
        label = QLabel()
        label.setText(alert_text)

        font = label.font()
        font.setFamily("Han Santteut Dotum")
        font.setPointSize(9)

        label.setFont(font)

        return label

    def init_button(self, btn_text, attached_instance: QDialog):
        btn = QPushButton(btn_text, attached_instance)
        btn.clicked.connect(attached_instance.close)

        font = QFont()
        font.setFamily("Han Santteut Dotum")

        btn.setFont(font)

        return btn
