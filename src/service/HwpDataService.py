import time

import win32com.client, clipboard

from src.exception.CustomException import NotFoundKeyWordError


class HwpDataService:
    def __init__(self):
        pass

    def find_page(self, hwp: win32com.client.CDispatch, find_text: str) -> [int, int]:
        try:
            hwp.HAction.GetDefault("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)
            hwp.HParameterSet.HFindReplace.FindString = find_text
            hwp.HParameterSet.HFindReplace.WholeWordOnly = True
            hwp.HParameterSet.HFindReplace.IgnoreMessage = True
            hwp.HParameterSet.HFindReplace.FindType = True

            hwp.HAction.Execute("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)

            hwp.HAction.Run("Select")
            hwp.HAction.Run("Copy")

            target_page = int(''.join(clipboard.paste())[-4:])

            return target_page
        except Exception as e:
            raise NotFoundKeyWordError("Can't find the keyword")

    def delete_page(self, hwp: win32com.client.CDispatch) -> None:
        hwp.HAction.Run("Select")
        hwp.HAction.Run("MoveTopLevelBegin")
        hwp.HAction.Run("Delete")

    def move_page(self, hwp: win32com.client.CDispatch, target: int) -> None:
        hwp.HAction.GetDefault("Goto", hwp.HParameterSet.HGotoE.HSet)
        hwp.HParameterSet.HGotoE.SetSelectionIndex = 1
        hwp.HParameterSet.HGotoE.HSet.SetItem("DialogResult", target)
        hwp.HAction.Execute("Goto", hwp.HParameterSet.HGotoE.HSet)

    def delete_ctrl(self, hwp: win32com.client.CDispatch) -> None:
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

    def copy_table(self, hwp: win32com.client.CDispatch):
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

    def parse_table(self, hwp: win32com.client, title: str):
        target_page = self.find_page(hwp, title)
        self.move_page(hwp, target_page)

        self.delete_page(hwp)
        self.delete_ctrl(hwp)

        table_list = self.copy_table(hwp)

        return list(filter(lambda v: v, table_list.replace("\r\n", " ").split(" ")) )
