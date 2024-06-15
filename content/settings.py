import json



# 預載資料設定檔
# 引導輸入資料並調整為正確資料(整合版本)
class settings:
  def __init__(self):
    
    with open('datas/settings.json','r',encoding="utf-8") as f:
      f_data = json.load(f)
      self.default_data = f_data


  # 輸入資料
  def user_inputs(self):
    settings = {
      'url'          : "Input url(Like https://example.com): ",
      'acc'          : "Input user's account: ",
      'pwd'          : "Input user's password: ",
      'acc_id'       : "Input web account element's id: ",
      'pwd_id'       : "Input web password element's id: ",
      'verfi_id'     : "Input web verfi element's id: ",
      'verfi_img_id' : "Input web verfi_img_id element's id: ",
      'iframe_id'    : "Input web iframe element's id: ",
    }
    datas = {}
    data_keys = []

    for key, msg in settings.items():
      # datas[key] = input(f"{msg}")
      datas[key] = ''
      data_keys.append(key)
      
    self.datas = datas
    self.data_keys = data_keys
    return self


  # 取得資料(dict)
  def get_datas(self):
    datas = {}

    for key in self.data_keys :
      datas[key] = self.datas.get(key) if self.datas.get(key) != '' else self.default_data[key]

    return datas


  # 用於確認資料
  def get_inputs(self):
    return self.datas


# 引導輸入資料
class user_inputs:
  def __init__(self):
    settings = {
      'url'          : "Input url(Like https://example.com, Enter with none will use default data) : ",
      'acc'          : "Input user's account (Enter with none will use default data) : ",
      'pwd'          : "Input user's password (Enter with none will use default data) : ",
      'acc_id'       : "Input web account element's id(Enter with none will use default data) : ",
      'pwd_id'       : "Input web password element's id(Enter with none will use default data) : ",
      'verfi_id'     : "Input web verfi element's id(Enter with none will use default data) : ",
      'verfi_img_id' : "Input web verfi_img_id element's id(Enter with none will use default data) : ",
      'iframe_id'    : "Input web iframe element's id(Enter with none will use default data) : ",
    }
    datas = {}

    for key, msg in settings.items():
      datas[key] = input(f"{msg}")
      
    self.datas = datas

  # 取得資料
  def get_inputs(self):
    return self.datas
  
