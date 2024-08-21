<h1>Selenium、pytest自動化測試整合包</h1>

<h2>整合包用途</h2>

一、將Selenium方法封裝，提供更簡易、快速的測試案例使用方法與log輸出。

二、提供自動登入網站、驗證碼辨識功能。


測試網址:
https://webap.nkust.edu.tw/nkust/


<h2>當前目標</h2>
是讓使用者只需複製網頁頁面的元素css_selector、xpath等資料，並直接帶入已撰寫好的function就可直接執行測試

![alt text](/doc/copy_dom_path.png)
![alt text](/doc/yaml_example.png)
![alt text](/doc/testcase_exampe.png)


<h2>版本需求</h2>

python 3.11.2

pytest 8.2.1

selenium 4.21.0

<h2>使用方式</h2>

開始: 直接執行main.py即可開始測試

修改設定: 直接修改configs/configs.ini的[commons]內容，細節如下圖
![alt text](/doc/ini_settings.png)

後續待更新
