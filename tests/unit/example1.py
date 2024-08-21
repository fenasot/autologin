"""範例測試案例1"""
import pytest

from src.packages.selenium_pack import selenium_pack
from defaults.defaults import Readini
from defaults.defaults import Readyaml


ini = Readini()
yaml = Readyaml().load_yaml('example.yaml')


class test_example1:
    def __init__(self) -> None:
        self.url = str(ini.get('test_example1', 'url'))

    def test_open_web(self):
        """開啟網頁"""
        s = selenium_pack()

        s.link(self.url)

        assert s.driver.current_url == self.url

    @pytest.skip(reason="調整中，暫時跳過")
    def test_click_web(self):
        """點擊google搜尋欄，並輸入文字"""
        s = selenium_pack()
        s.find_element(yaml['google搜尋欄'])
