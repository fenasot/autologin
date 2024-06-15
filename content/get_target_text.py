from PIL import Image
import pytesseract
from translate import Translator
import os

class get_target_text:
  """
    輸入圖片路徑後，獲取圖片內文字
  """
  def __init__(self, img_path):
    self.img_path = img_path
    # self.text_all = self.__get_text()


  # 獲取圖片內文字
  def __get_text(self):
    img_path = self.img_path

    try:
      Image.open(img_path)
    except:
      print('無法讀取圖片')

    img = Image.open(img_path)
    # 強迫只由左到右，不分上下
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    # custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'

    text = pytesseract.image_to_string(img, lang='eng', config=custom_config)

    # TEST
    # text = re.sub(r'[\s]+','',captcha_code)
    text = text.replace(' ', '').replace('\n','')
    # text = text.replace(' ', '')

    return text


  # 英翻中(一次只能500)
  def __translate_text(self, text):
    translator = Translator(to_lang="zh")
    translation = translator.translate(text)
    return translation


  # 確認字數並批次翻譯
  def __count_text(self):
    text_all = self.text_all
    total = len(text_all)
    for n in range(0, total, 500):
      print(self.__translate_text(text_all[n:n+500]))


  # 執行 
  def get_text(self):
    return self.__get_text()

