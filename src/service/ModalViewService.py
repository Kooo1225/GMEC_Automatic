import numpy as np
import pandas as pd
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, \
    QWidget, QHeaderView, QLayout, QFileDialog
from PyQt5.QtCore import Qt


# 현재 ModalViewService에서 한번에 통합된 동작을 함
# 이 부분을 좀 더 디테일하게 나눠서 Controller에서 통합된 동작을 하게 하는게 좋을듯 함
class ModalViewService:
    def set_table_tabs(self, evening_data):
        tabs = QTabWidget()
        max_width = 0
        max_height = 0

        for item in evening_data:
            # 여기서 item은 하나의 pd.DataFrame
            tab = self.draw_dataframe(item[1])
            tabs.addTab(tab, item[0])

            size_hint = tab.sizeHint()
            max_width = max(max_width, size_hint.width())
            max_height = max(max_height, size_hint.height())

        return tabs

    def draw_dataframe(self, df):
        tableWidget = QTableWidget()

        tableWidget.setRowCount(len(df.index))
        tableWidget.setColumnCount(len(df.columns))
        tableWidget.setHorizontalHeaderLabels(df.columns)
        tableWidget.setVerticalHeaderLabels(df.index)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for row_index, row in enumerate(df.index):
            alignment = Qt.AlignCenter

            tableWidget.horizontalHeader().setDefaultAlignment(alignment)
            tableWidget.verticalHeader().setDefaultAlignment(alignment)

            for col_index, column in enumerate(df.columns):
                # df.at[row, column] 이 속도가 빠르다고 함.
                value = df.at[row, column]
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

    def save_table(self, save_data):
        filename = QFileDialog.getSaveFileName(None, "Save Excel File", "", "Excel Files (*.xlsx)")[0]
        if not filename:
            return False

        with pd.ExcelWriter(filename) as writer:
            for data_key, df in save_data:
                df.to_excel(writer, sheet_name=data_key, index=False)
                worksheet = writer.sheets[data_key]
                center_format = writer.book.add_format({'align': 'center', 'valign': 'center'})

                for idx, col in enumerate(df.columns):
                    max_len = df[col].astype(str).map(len).max()
                    max_len = max(max_len, len(str(col))) + 5
                    worksheet.set_column(idx, idx, max_len, center_format)

        return True

    def set_dialog(self, dialog, layout, window_title, set_modal):
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint)

        dialog.setWindowIcon(QIcon(':icon/main_icon.ico'))
        dialog.setWindowTitle(window_title)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setLayout(layout)
        dialog.setModal(set_modal)

        return dialog

    def init_label(self, alert_text):
        label = QLabel()
        label.setText(alert_text)

        label.setFont(self.init_font("Han Santteut Dotum", 9))

        return label

    def init_button(self, btn_text, attached_instance: QDialog):
        btn = QPushButton(btn_text, attached_instance)
        btn.clicked.connect(attached_instance.close)

        btn.setFont(self.init_font("Han Santteut Dotum"))

        return btn

    def init_font(self, font_name: str, optional_font_size: int = None):
        font = QFont()
        font.setFamily(font_name)

        if optional_font_size is not None:
            font.setPointSize(optional_font_size)

        return font
