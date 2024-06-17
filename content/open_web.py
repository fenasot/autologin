# 自動登入
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, NoSuchElementException, TimeoutException

# 圖片處理
from PIL import Image
import io
import os

# certifi 用於SSL驗證
import certifi  

# others
import requests
import time
import re

# 自定義
from content.get_target_text import get_target_text 
# from content.settings import user_inputs, settings
from content.filter_img import filter_img

class open_web():
  """
    自動登入網頁
      Attributes:
          datas (dict): 用於登入的資料。
          retry_interval (float, optional): 失敗後重試的間隔。
          max_retries (int, optional): 最大重試次數。
          verfi_text_chg (str or None, optional): 驗證碼是否需要全部大寫或小寫。
  """
  def __init__(self, datas:dict, retry_interval:float = 0.5, max_retries:int = 10, verfi_text_chg:str|None = None) -> None:
    # 基本設定
    self.image_folder_path = 'images'
    self.verfi_png_name = 'captcha_image.png'
    self.binary_png = 'binary_image.png'

    # 重試次數
    self.max_retries = max_retries
    self.retry_interval = retry_interval

    # 驗證碼設定
    self.verfi_text_chg = verfi_text_chg

    # 拆解資料
    self.datas = {}
    for key in datas:
      self.datas[key] = datas.get(key)


  # 連結網頁
  def link(self):
    # 初始化 WebDriver
    # 確保系統上安裝了 Chrome 瀏覽器和相應的 WebDriver
    # driver = webdriver.Chrome()  
    # driver.get('http://example.com/login')  

    # 瀏覽器
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    self.driver = webdriver.Chrome()  

    try:
      self.driver.get(self.datas['url'])  
    except Exception as e:
      print('開啟網頁失敗')


  # 嘗試尋找單一元素(可保有註釋)
  def try_find_2(self, element):
    a_bl = b_bl = c_bl = True

    try:
      a = self.driver.find_element(By.ID, element)
    except Exception as e:
      a_bl = False

    try:
      b = self.driver.find_element(By.NAME, element)
    except Exception as e:
      b_bl = False

    # TEST need try, and check answer is single or mutiple
    # try:
    #   c = self.driver.find_element(By.CLASS_NAME, element)
    # except Exception as e:
    #   c_bl = False

    # 確定是否有找到
    if(a_bl):
      return a
    
    if(b_bl):
      return b
    
    # if(c_bl):
    #   return c

    print(f'無法找到元素 "{element}" 。')
    exit()


  # 嘗試尋找單一元素
  def try_find(self, element):
    conditions = [
        (True, lambda: self.driver.find_element(By.ID, element)),
        (True, lambda: self.driver.find_element(By.NAME, element)),
        # (True, lambda: self.driver.find_element(By.CLASS_NAME, element)),
    ]

    for i, (condition, func) in enumerate(conditions):
        try:
            conditions[i] = (condition, func())
        except Exception as e:
            conditions[i] = (False, None)

    for condition, value in conditions:
        if condition:
            return value

    print(f'無法找到元素 "{element}" 。')
    exit()


  # 取得欄位
  def find_element(self):
    # 等待加載完成
    WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, self.datas['acc_id']))
    )
    print("網頁加載完成")

    # 抓element
    username_field = self.try_find(self.datas['acc_id'])
    password_field = self.try_find(self.datas['pwd_id'])
    captcha_image = self.try_find(self.datas['verfi_img_id'])  # 替換為驗證碼圖片元素的 ID

    # 鍵入值
    username_field.send_keys(self.datas['acc']) 
    password_field.send_keys(self.datas['pwd'])

    # 驗證
    self.get_verfi_image(captcha_image)


  # 輸入驗證碼
  def try_verfi(self):
    # 路徑
    ori_path = f'{self.image_folder_path}\{self.verfi_png_name}'
    binary_path = f'{self.image_folder_path}\{self.binary_png}'
    
    # TEST
    # 修改圖片
    # filter_img(ori_path).gray_img().kernel_img().save_img(binary_path)
    filter_img(ori_path).gray_img_2().save_img(binary_path)
    # filter_img(ori_path).gray_img_2().resize_img().save_img(binary_path)
    # filter_img(ori_path).gray_img_2().gaussian_blur().resize_img().save_img(binary_path)

    # 取得圖片
    trans = get_target_text(binary_path)    
    captcha_code = trans.get_text()

    match self.verfi_text_chg:
      case 'upper':
        captcha_code = captcha_code.upder()
      case 'lower':
        captcha_code = captcha_code.lower()

    print('驗證碼','\n',captcha_code)
    
    if captcha_code == '': 
      raise UnexpectedAlertPresentException('驗證碼辨識失敗')
    
    # 找到並填寫驗證碼
    captcha_field = self.try_find(self.datas['verfi_id'])
    captcha_field.send_keys(captcha_code)
    captcha_field.send_keys(Keys.RETURN)


  # 切換到frame內
  def to_iframe(self, iframe_name):
    wait = WebDriverWait(self.driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.ID, iframe_name)))
    self.driver.switch_to.frame(iframe) 


  # 直接截圖 
  def get_verfi_image(self, captcha_image:dict):
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


  # 用url獲取圖片(失敗)
  def get_verfi_image_2(self, captcha_image):
    captcha_image_url = captcha_image.get_attribute('src')
    self.driver.execute_script("window.open('{}');".format(captcha_image_url))
    
    # 获取所有窗口句柄
    all_handles = self.driver.window_handles

    # 切换到新打开的标签页
    new_window_handle = [handle for handle in all_handles if handle != self.driver.current_window_handle][0]
    self.driver.switch_to.window(new_window_handle)

    self.driver.close()
    self.driver.switch_to.window(self.driver.window_handles[0])

    # 下載驗證碼圖片
    response = requests.get(captcha_image_url, verify=False)
    
    self.captcha_image = Image.open(io(response.content))
    # captcha_image.show() 

    if response.status_code == 200:
        # 保存图片到本地或者处理图片内容
        with open("captcha_image.jpg", "wb") as f:
            f.write(response.content)
        print("獲取應證圖片成功")

    else:
        print("獲取驗證圖片失敗:", response.status_code)


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
    if(self.datas['iframe_id']):
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
            print(f"Login failed, retrying... ({retries}/{self.max_retries})")
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
        break

      except (UnexpectedAlertPresentException, NoSuchElementException) as e:
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

      except (NoAlertPresentException, TimeoutException) as e :
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
#     auto_login = open_web(max_retries=10, retry_interval=10)  
#     auto_login.chk_time()