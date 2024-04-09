from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication, QPushButton

from src.service.ModalViewService import ModalViewService


class ModalViewController:
    def __init__(self):
        self.service = ModalViewService()
        self.dialog = None
        self.layout = None

    def get_dialog(self):
        return self.dialog

    def set_error_view(self, alert_text: str, btn_text: str, title_text: str):
        self.dialog = QDialog()
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.service.init_label(alert_text))
        self.layout.addWidget(self.service.init_button(btn_text, self.dialog))
        self.dialog = self.service.set_dialog(self.dialog, self.layout, title_text, True)

    def set_tabs_view(self, data):
        self.dialog = QDialog()
        self.layout = QVBoxLayout()

        tabs = self.service.set_table_tabs(data)
        self.layout.addWidget(tabs)

        # 함수 처리가 미비해서 임시로 생성한 버튼
        save_btn = QPushButton('Save', self.dialog)
        save_btn.clicked.connect(lambda: self.service.save_table(data))
        save_btn.setFont(self.service.init_font("Arial"))
        self.layout.addWidget(save_btn)
        self.layout.addWidget(self.service.init_button('Done', self.dialog))

        self.dialog = self.service.set_dialog(self.dialog, self.layout, '분석 결과', False)

        QTimer.singleShot(0, lambda: self.dialog.resize(tabs.currentWidget().sizeHint() * 2.5))
