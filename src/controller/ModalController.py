from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication

from src.service.ModalViewService import ModalViewService


class ModalViewController:
    def __init__(self):
        self.service = ModalViewService()
        self.dialog = None

    def get_dialog(self):
        return self.dialog

    def set_error_view(self, alert_text: str, btn_text: str, title_text: str):
        self.dialog = QDialog()
        self.service.set_alert_dialog(self.dialog, alert_text, btn_text, title_text)

    def set_tabs_view(self, data_dict: dict, parser_name: str):
        self.dialog = QDialog()
        self.service.set_tabs_dialog(self.dialog, data_dict, parser_name)
