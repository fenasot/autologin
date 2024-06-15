import cv2
from PIL import Image
import numpy as np

# 對圖片修改，未來可能放更多方法
class filter_img:
  """
  修改圖片用
  """
  def __init__(self,img_path):
    self.img_path = img_path
    self.image = cv2.imread(img_path)


  def resize_img(self, scale_factor=5):
    width = int(self.image.shape[1] * scale_factor)
    height = int(self.image.shape[0] * scale_factor)
    self.image = cv2.resize(self.image, (width, height), interpolation=cv2.INTER_LINEAR)
    return self


  # 灰階
  def gray_img(self):
    gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    _, self.image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return self


  # 灰階(嚴格模式)
  def gray_img_2(self):
    gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    _, self.image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return self


  #膨脹 or 蝦 or 搞不董
  def idk_img(self):  
    kernel = np.ones((5, 5), np.uint8) 
    self.image = cv2.erode(self.image, kernel, iterations=1)
    return self


  # 高斯
  def gaussian_blur(self, ksize=(1, 1), sigmaX=0):
    self.image = cv2.GaussianBlur(self.image, ksize, sigmaX)
    return self


  # 侵蝕
  def kernel_img(self):
    # ig = cv2.imread(self.img_path, 0)
    k = np.ones((5,5))
    self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, k)
    return self


  # 取得圖片
  def get_img(self):
    self.__chk_img()
    return self.image


  # 儲存圖片
  def save_img(self, output_path):
    self.__chk_img()
    cv2.imwrite(output_path, self.image)


  # 確認是否已處理過圖片
  def __chk_img(self):
    if self.image is None:
      print('圖片讀取失敗。')
      exit()

