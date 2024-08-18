from PIL import Image
import pytesseract as OCR
from translate import Translator
# import os


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
        except Exception as e:
            print(f'無法讀取圖片，{e}')

        img = Image.open(img_path)

        # 強迫只由左到右，不分上下
        text_config = (
            r'--oem 3 '
            r'--psm 6 '
            r'-c'
            r'tessedit_char_whitelist='
            r'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            r'abcdefghijklmnopqrstuvwxyz'
            r'0123456789'
        )

        text: str = OCR.image_to_string(img, lang='eng', config=text_config)

        # TEST
        # text = re.sub(r'[\s]+','',captcha_code)
        text = text.replace(' ', '').replace('\n', '')
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

