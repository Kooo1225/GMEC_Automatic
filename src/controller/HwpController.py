import winreg, os
from tkinter import filedialog

from src.exception.CustomException import HwpOpenError, HwpObjectNotFoundError, NotFoundKeyWordError
from src.service.HwpDataService import HwpDataService
from src.service.HwpRegistryManager import HwpRegistryManager
from src.service.HwpFileManager import HwpFileManager


class HwpController:
    # 의존성 주입을 통한 클래스 생성자 정의
    def __init__(self):
        self.registry_manager = HwpRegistryManager()
        self.file_manager = HwpFileManager()
        self.data_service = HwpDataService()

        self.__table_list = None

    def check_and_create_reg(self):
        HKEY = winreg.HKEY_CURRENT_USER
        update_reg_path = r'Software\HNC\HwpAutomation\Modules'
        value_name = 'SecurityModule'
        value_data = rf'{os.getcwd()}\FilePathCheckerModuleExample.dll'

        try:
            self.registry_manager.update_module(HKEY, update_reg_path, value_name, value_data)
        except KeyError:
            raise KeyError('Already Key Exists')

    def get_table_list(self, file_name: str, title: str):
        try:
            self.file_manager.open_hwp(file_name)
            self.__table_list = self.data_service.parse_table(self.file_manager.get_hwp(), title)
        except HwpOpenError as e:
            raise HwpOpenError("Failed to open Hwp file.")
        except HwpObjectNotFoundError as e:
            raise HwpObjectNotFoundError("Hwp Object is not initialized.")
        except NotFoundKeyWordError as e:
            raise NotFoundKeyWordError("Can't find the keyword")
        finally:
            self.file_manager.close_hwp()

    def get_list(self):
        return self.__table_list
