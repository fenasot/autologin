from content.settings import settings
from content.auto_open import open_web
from content.filter_img import filter_img

# 自定義
from content.get_target_text import get_target_text

def start():
  a = settings().user_inputs()
  b = open_web(datas=a.get_datas(), verfi_text_chg="lower")
  b.keeping_start()


# 測試用
def test_1():
  filter_img(f'images\\captcha_image.png').gray_img().kernel_img().save_img(f'images\\a.png')
  filter_img(f'images\\captcha_image.png').kernel_img().save_img(f'images\\b.png')
  filter_img(f'images\\captcha_image.png').gray_img().save_img(f'images\\c.png')
  filter_img(f'images\\captcha_image.png').gray_img_2().save_img(f'images\\d.png')

# 執行
start()
# test_1()