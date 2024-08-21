"""範例測試案例1"""
import pytest

from src.packages.selenium_pack import selenium_pack
from defaults.defaults import Readini


ini = Readini()


class test_example1:
    def __init__(self) -> None:
        self.url = str(ini.get('test_example1', 'url'))

    @pytest.skip(reason="調整中，暫時跳過")
    def test_open_web(self):
        """開啟網頁"""
        s = selenium_pack()

        s.link(self.url)

        assert s.driver.current_url == self.url
