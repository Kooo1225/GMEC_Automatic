import clipboard, winreg, os


from tkinter import filedialog


def checkReg() -> None:
    updateRegPath = r'Software\HNC\HwpAutomation\Modules'

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, updateRegPath, 0, winreg.KEY_WRITE)

    value_name = "SecurityModule"
    value_data = rf"{os.getcwd()}\FilePathCheckerModuleExample.dll"
    print(value_data)

    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)

    winreg.CloseKey(key)


class hwpService:
    def __init__(self):
        pass
    # HWP 레지스트리 보안 모듈 체크
    # 미등록 시 등록도 할 수 있게
    # 현재 디렉토리를 기준으로 data 값을 수정하기

    # 클래스 변환 작업하기
    def getHwpName(self) -> str:
        return filedialog.askopenfilename()

    # filedialog를 통해서 [ 파일 이름.확장자 ] 값 가져오기
    def openHwp(self, hwp, hwpName: str):
        hwp.Open(hwpName, "HWP", "forceopen:true")
        hwp.HAction.Run("MoveDocBegin")

    def findPage(self, hwp, findStr: str) -> [int, int]:
        hwp.HAction.GetDefault("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = findStr
        hwp.HParameterSet.HFindReplace.WholeWordOnly = True
        hwp.HParameterSet.HFindReplace.IgnoreMessage = True
        hwp.HParameterSet.HFindReplace.FindType = True

        hwp.HAction.Execute("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)

        hwp.HAction.Run("Select")
        hwp.HAction.Run("Copy")

        first_pageNum = int(hwp.XHwpDocuments.Item(0).XHwpDocumentInfo.CurrentPage)
        target_pageNum = int(''.join(clipboard.paste())[-4:])

        return target_pageNum, first_pageNum

    def delPage(self, hwp, target: int, first: int) -> None:
        hwp.HAction.Run("MoveDocBegin")

        for i in range(first):
            hwp.HAction.Run("DeletePage")

        for i in range(target):
            hwp.HAction.Run("DeletePage")

    def delCtrl(self, hwp) -> None:
        hwp.HAction.GetDefault("DeleteCtrls", hwp.HParameterSet.HDeleteCtrls.HSet)
        hwp.HParameterSet.HDeleteCtrls.CreateItemArray("DeleteCtrlType", 3)
        hwp.HParameterSet.HDeleteCtrls.DeleteCtrlType.SetItem(0, 31)
        hwp.HParameterSet.HDeleteCtrls.DeleteCtrlType.SetItem(1, 26)
        hwp.HParameterSet.HDeleteCtrls.DeleteCtrlType.SetItem(2, 14)
        hwp.HAction.Execute("DeleteCtrls", hwp.HParameterSet.HDeleteCtrls.HSet)

        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.AutoSpell = 1
        hwp.HParameterSet.HFindReplace.FindString = "^n"
        hwp.HParameterSet.HFindReplace.ReplaceString = ""
        hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)

        hwp.HAction.GetDefault("AllReplace", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.AutoSpell = 1
        hwp.HParameterSet.HFindReplace.FindString = " "
        hwp.HParameterSet.HFindReplace.ReplaceString = ""
        hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HAction.Execute("AllReplace", hwp.HParameterSet.HFindReplace.HSet)

    def copyGrapgh(self, hwp):
        result = ''
        ctrl = hwp.HeadCtrl

        while True:
            if not ctrl.CtrlID == "tbl":
                ctrl = ctrl.Next
            elif ctrl.CtrlID == "tbl":
                hwp.SetPosBySet(ctrl.GetAnchorPos(0))
                hwp.FindCtrl()
                hwp.Run("ShapeObjTableSelCell")
                hwp.Run("TableCellBlockExtend")
                hwp.Run("TableCellBlockExtend")

                hwp.Run("Copy")
                result += clipboard.paste()

                if not ctrl.Next.CtrlID == "tbl":
                    break
                else:
                    ctrl = ctrl.Next

        return result

    def closeHwp(self, hwp) -> None:
        hwp.HAction.Run("FileClose")
        hwp.XHwpDocuments.Close(False)
        hwp.Quit()