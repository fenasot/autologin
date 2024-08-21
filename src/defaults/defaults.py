"""此文件用來存放全域變數、共用路徑與ini設定"""

# import os
from pathlib import Path
from pathlib import PurePath
from configparser import ConfigParser
# from iniconfig import IniConfig as ini
# import selenium.webdriver
from selenium.webdriver.common.by import By


'''全域變數'''
# DOM 元素取得判斷
BY_TYPE = {
    "id": By.ID,
    "class": By.CLASS_NAME,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH
}


'''設定共用路徑'''
p = Path()
p_cwd = p.cwd()

# PATH_PACKAGE = os.getcwd()
PATH_PACKAGE = str(p_cwd.parent)
"""專案頂層路徑"""
PATH_DEFAULT = str(p.cwd())
"""default 路徑"""
PATH_CONFIGS = str(PurePath(PATH_PACKAGE, 'configs'))
"""configs 路徑"""
PATH_DATAS = str(PurePath(PATH_PACKAGE, 'datas'))
"""datas 路徑"""
PATH_TESTS = str(PurePath(PATH_PACKAGE, 'tests'))
"""tests 路徑"""
PATH_SRC = str(PurePath(PATH_PACKAGE, 'src'))
"""src 路徑"""
PATH_LOGS = str(PurePath(PATH_DATAS, 'logs'))
"""logs 路徑"""


class Readini:
    """ini 文件讀取設定"""

    def __init__(self) -> None:
        self.ini = ConfigParser()
        self.ini.read_file(f'{PATH_CONFIGS}\\configs.ini')

    def get(self, section: str, option: str) -> None:
        """取得ini的option"""
        # self.__check_section(section)
        self.__check_option(section, option)
        self.ini.get(section, option)

    def set(self, section: str, option: str, value: str) -> None:
        """鍵入ini的option (若沒有section，將自動新增section)"""
        if self.ini.has_section(section) is False:
            self.ini.add_section(section)
        self.ini.set(section, option, value)

    def set_read_file(self, source: str) -> None:
        """改變讀取的ini文件"""
        self.ini.read_file(source)

    def __check_section(self, section: str) -> None:
        """確認section是否存在"""
        if self.ini.has_section(section) is False:
            raise AttributeError(f'ini section ({section}) not found.')

    def __check_option(self, section: str, option: str) -> None:
        """確認option是否存在"""
        if self.ini.has_option(section, option) is False:
            raise AttributeError(f'ini option ({option}) not found.')
