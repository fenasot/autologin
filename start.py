# 自定義
from content.settings import settings
from content.open_web import open_web
from content.filter_img import filter_img
# from content.get_target_text import get_target_text

def start():
  a = settings("datas/settings.json").user_inputs()
  # b = open_web(datas=a.get_datas(), verfi_text_chg="lower", filter_type="filter_gray")
  b = open_web(datas=a.get_datas(), verfi_text_chg="lower", filter_type="kernel_img_2,gray_img_2,resize_img")
  b.keeping_start()


# 測試用(生成多種處理後的圖片)
def test_1():
  filter_img(f'images\\captcha_image.png').gray_img().kernel_img().save_img(f'images\\test_a.png')
  filter_img(f'images\\captcha_image.png').kernel_img().save_img(f'images\\test_b.png')
  filter_img(f'images\\captcha_image.png').gray_img().save_img(f'images\\test_c.png')
  filter_img(f'images\\captcha_image.png').gray_img_2().save_img(f'images\\test_d.png')
  filter_img(f'images\\captcha_image.png').gray_img_2().kernel_img_2().save_img(f'images\\test_e.png')

# 執行
start()
# test_1()