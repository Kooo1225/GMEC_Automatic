import win32com.client as win32
from src.exception.CustomException import *


class HwpFileManager:
    def __init__(self):
        self.__hwp = None

    def open_hwp(self, file_name):
        try:
            self.__hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
            self.__hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")
            self.__hwp.XHwpWindows.Item(0).Visible = False

            self.__hwp.Open(file_name, "HWP", "forceopen:true")
            self.__hwp.HAction.Run("MoveDocBegin")
        except Exception as e:
            raise HwpOpenError("Failed to open Hwp file.")

    def close_hwp(self):
        try:
            self.__hwp.HAction.Run("FileClose")
            self.__hwp.XHwpDocuments.Close(False)
            self.__hwp.Quit()
        except Exception as e:
            raise HwpObjectNotFoundError("Hwp Object is not initialized.")

    def get_hwp(self) -> win32.CDispatch:
        return self.__hwp
