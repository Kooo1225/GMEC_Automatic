from tkinter import filedialog

from src.controller.HwpController import HwpController


# def open_hwp(self, file_name):
#     try:
#         self.__hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
#         self.__hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")
#         self.__hwp.XHwpWindows.Item(0).Visible = True
#
#         self.__hwp.Open(file_name, "HWP", "forceopen:true")
#         self.__hwp.HAction.Run("MoveDocBegin")
#     except Exception as e:
#         raise HwpOpenError("Failed to open Hwp file.")


test_case = HwpController()
print(test_case.get_table_list(filedialog.askopenfilename(), '일자별 발파 및 계측 현황'))