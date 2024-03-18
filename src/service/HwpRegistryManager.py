import winreg, os


class HwpRegistryManager:
    def __init__(self):
        pass

    def check_reg(self, HKEY, update_reg_path, value_name) -> bool:
        try:
            with winreg.OpenKey(HKEY, update_reg_path) as k:
                winreg.QueryValueEx(k, value_name)
                return False
        except FileNotFoundError:
            return True
        finally:
            winreg.CloseKey(k)

    def create_reg(self, HKEY, update_reg_path, value_name, value_data):
        key = winreg.OpenKey(HKEY, update_reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
        winreg.CloseKey(key)

    def update_module(self, HKEY, update_reg_path, value_name, value_data):
        if self.check_reg(HKEY, update_reg_path, value_name):
            self.create_reg(HKEY, update_reg_path, value_name, value_data)
        else:
            raise KeyError("Already Key Exists")
