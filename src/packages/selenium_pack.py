from xml.dom.minidom import Element
from matplotlib.pyplot import locator_params
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# py原生
import io
import os
import time
# import certifi
# import re
# import requests

# 圖片處理
from PIL import Image

# 自定義
from src.packages.get_target_text import get_target_text
from src.packages.filter_img import filter_img
from src.defaults.log_setting import log
import src.defaults.defaults as DF  # default 共用變數


class selenium_pack:
    """
        selenium 封裝方法，將selenium的原生方法封裝，讓使用更便利。

        TODO: 待修改

        :param: test: test

        Attributes:
            datas (dict): 用於登入的資料。
            retry_interval (float, optional): 失敗後重試的間隔。
            max_retries (int, optional): 最大重試次數。
            verfi_text_chg (str or None, optional): 驗證碼是否需要全部大寫或小寫。
    """

    def __init__(
            self,
            # datas: dict,
            retry_interval: float = 0.5,
            max_retries: int = 10,
            verfi_text_chg: str | None = None,
            filter_type: str = "filter_gray"
    ) -> None:

        # 基本設定
        self.image_folder_path = f'{DF.PATH_DATAS}\\images'
        self.verfi_png_name = 'captcha_image.png'
        self.binary_png = 'binary_image.png'
        self.filter_type = filter_type

        # 重試次數
        self.max_retries = max_retries
        self.retry_interval = retry_interval

        # 驗證碼設定
        self.verfi_text_chg = verfi_text_chg

        # 拆解資料
        # self.datas = {}
        # for key in datas:
        #     self.datas[key] = datas.get(key)

    # 連結網頁
    def link(self, url: str) -> None:
        """開啟目標網頁

        使用前須將電腦畫面比例設為100%，以防止element座標與畫面不符。

        TODO: 設定自動偵測縮放比例並於自動執行視窗內調整回100%，以及各個瀏覽器的調整。
        """

        # 瀏覽器
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome()

        try:
            def page_has_loaded(driver):
                return driver.execute_script('return document.readyState')

            self.driver.get(url)
            wait(self.driver, 10).until(page_has_loaded)

            # self.driver.set_window_size(1920, 1080)
            # size = self.driver.get_window_size()
        except Exception as e:
            raise ConnectionError(f'開啟網頁失敗，{e}')

    # 嘗試尋找單一元素
    def try_find(self, element: str) -> WebElement:
        """
        TODO: 尋找
        """
        conditions = [
            (True, lambda: self.driver.find_element(By.ID, element)),
            (True, lambda: self.driver.find_element(By.NAME, element)),
            # (True, lambda: self.driver.find_element(By.CLASS_NAME, element)),
            (True, lambda: self.driver.find_element(By.CSS_SELECTOR, element)),
            (True, lambda: self.driver.find_element(By.XPATH, element)),
            ]

        by_type = [
            By.ID,
            By.CLASS_NAME,
            By.NAME,
            By.CSS_SELECTOR,
            By.XPATH
        ]

        a = (True, lambda: EC.element_located_to_be_selected(
            (by_type[3], element))),
        print(a)

        for i, (condition, func) in enumerate(conditions):
            try:
                conditions[i] = (condition, func())
            except Exception:
                conditions[i] = (False, None)

        for condition, value in conditions:
            if condition:
                return value

        print(f'無法找到元素 "{element}" 。')
        exit()

    # 取得欄位
    def find_element(self, locator_data: str) -> WebElement:

        type, locator = locator_data
        # 等待加載完成
        try:
            element = wait(self.driver, 10).until(
                EC.presence_of_element_located((DF.BY_TYPE[type], locator))
            )
        except TimeoutException:
            log.debug(f'找不到元素，{locator_data}')

        return element

    # 輸入驗證碼
    def try_verfi(self):
        # 路徑
        ori_path = f'{self.image_folder_path}\\{self.verfi_png_name}'
        binary_path = f'{self.image_folder_path}\\{self.binary_png}'

        # 修改圖片
        self.filter_img_type(ori_path, binary_path)

        # 取得圖片
        trans = get_target_text(binary_path)
        captcha_code = trans.get_text()

        match self.verfi_text_chg:
            case 'upper':
                captcha_code = captcha_code.upper()
            case 'lower':
                captcha_code = captcha_code.lower()

        print('驗證碼', '\n', captcha_code)

        if captcha_code == '':
            raise UnexpectedAlertPresentException('驗證碼辨識失敗')

        # 找到並填寫驗證碼
        captcha_field = self.try_find(self.datas['verfi_id'])
        captcha_field.send_keys(captcha_code)
        captcha_field.send_keys(Keys.RETURN)

    # filter_img_type 控制項
    def filter_img_type(self, ori_path, binary_path):
        processor = filter_img(ori_path)
        methods = self.filter_type.split(',')

        for method in methods:
            if not hasattr(processor, method):
                print(f'選擇的 {method} 不存在!')
                exit()

            call_method = getattr(processor, method)
            call_method()

        processor.save_img(binary_path)

    # 切換到frame內
    def to_iframe(self, iframe_name):
        wait = WebDriverWait(self.driver, 10)
        iframe = wait.until(
            EC.presence_of_element_located((By.ID, iframe_name)))
        self.driver.switch_to.frame(iframe)

    # 直接截圖
    def get_verfi_image(self, captcha_image: dict):
        location = captcha_image.location
        size = captcha_image.size
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']

        # 截圖整個網頁
        png = self.driver.get_screenshot_as_png()

        # 使用 PIL 將圖片裁剪出來
        im = Image.open(io.BytesIO(png))
        im = im.crop((left, top, right, bottom))

        if not os.path.exists(self.image_folder_path):
            os.makedirs(self.image_folder_path)

        filename = self.verfi_png_name
        save_path = os.path.join(self.image_folder_path, filename)
        im.save(save_path)

    # 關閉網頁
    def close_web(self):
        self.driver.quit()

    # 錯誤訊息
    def error_msg(self, error):
        match(error):
            case 'error_1':
                msg = f'無法找到元素 "{error}" 。'
        print(msg)
        exit()

    # 啟動
    def start(self):
        # 開啟網頁
        self.link()

        # 確認是否有iframe嵌套
        if (self.datas['iframe_id']):
            self.to_iframe(self.datas['iframe_id'])

        # 取得element
        self.find_element()
        self.try_verfi()

    # 未完成
    def chk_time(self):
        retries = 0
        while retries < self.max_retries:
            if self.start():
                print("Login successful!")
                break
            else:
                retries += 1
                print(
                    f"Login failed, retrying... ({retries}/{self.max_retries})")
                time.sleep(self.retry_interval)
        else:
            print("Maximum retries reached. Login failed.")

    # 重複登入
    def keeping_start(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.start()
                # time.sleep(1000)
                WebDriverWait(self.driver, 0.1).until(EC.alert_is_present())
                raise UnexpectedAlertPresentException('登入失敗')

            except (UnexpectedAlertPresentException,
                    NoSuchElementException) as e:
                print(f"{e.msg} Retrying...")
                self.driver.quit()
                retries += 1
                time.sleep(self.retry_interval)
                continue

            except SystemError as e:
                print(f"{e} Retrying...")
                self.driver.quit()
                retries += 1
                time.sleep(self.retry_interval)
                continue

            except (NoAlertPresentException, TimeoutException):
                print('Susccess login!')
                time.sleep(1000)
                break

            except Exception as e:
                print(f"An error occurred: {e}")
                self.driver.quit()
                break

        print('End')


# if __name__ == "__main__":
#     # auto_login = AutoLogin(max_retries=10, retry_interval=10)
#     auto_login = selenium_pack(max_retries=10, retry_interval=10)
#     auto_login.chk_time()
