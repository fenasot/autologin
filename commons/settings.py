# import os
from pathlib import Path
from pathlib import PurePath
from configparser import ConfigParser
# from iniconfig import IniConfig as ini
# import selenium.webdriver
from selenium.webdriver.common.by import By


"""此文件用來存放全域變數與設定資料"""


'''設定共用路徑'''
p = Path()
p_cwd = p.cwd()

# PACKAGE_PATH = Path.PurePath()  # 當前檔案路徑
PACKAGE_PATH = str(p_cwd.parent)  # 專案頂層路徑

COMMONS_PATH = str(p.cwd())  # commons 路徑
CONFIGS_PATH = str(PurePath(PACKAGE_PATH, 'configs'))
DATAS_PATH = str(PurePath(PACKAGE_PATH, 'datas'))
LOGS_PATH = str(PurePath(PACKAGE_PATH, 'logs'))
SRC_PATH = str(PurePath(PACKAGE_PATH, 'src'))
# SRC_PATH = str(PurePath(PACKAGE_PATH, 'src'))
# PACKAGE_PATH = os.getcwd()


def aaaaa():
    print(PACKAGE_PATH)
    print('ssssss', p.cwd())
    print(CONFIGS_PATH)
    # raise PACKAGE_PATH


aaaaa()


# DOM 元素取得判斷
BY_TYPE = {
    "id": By.ID,
    "class": By.CLASS_NAME,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH
}

ini = ConfigParser()


class Readini:
    """ini文件讀取"""

    def __init__(self) -> None:
        self.ini = ini.read_file(PACKAGE_PATH)

    def get(self, section: str, name: str):
        """取得ini"""
        # ini.get(name, section, name)
        ini.get(section, name)

    def set_file(self, file_name: str):
        """設定讀取的ini文件"""
        ini.read_file(file_name)
