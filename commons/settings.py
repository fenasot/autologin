import os
from pathlib import Path
from configparser import ConfigParser
# from iniconfig import IniConfig as ini
# import selenium.webdriver
from selenium.webdriver.common.by import By


"""此文件用來存放全域變數與設定資料"""

p = Path()
p.cwd()



# PACKAGE_PATH = Path.PurePath()
# PACKAGE_PATH = Path.cwd()
PACKAGE_PATH = os.getcwd('../')


def aaaaa():
    print(PACKAGE_PATH)
    print('ssssss', p)
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
