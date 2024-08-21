<h1>Selenium、pytest自動化測試整合包</h1>

<h2>整合包用途</h2>

一、將Selenium方法封裝，提供更簡易、快速的測試案例使用方法與log輸出。

二、提供自動登入網站、驗證碼辨識功能。

測試網址:
https://webap.nkust.edu.tw/nkust/

<h2>版本需求</h2>

python 3.11.2

pytest 8.2.1

selenium 4.21.0

<h2>使用方式</h2>

一、
<!-- 一、先將settings_sample.json改名為settings.json，並分別輸入
  1. 網址
  2. 帳號
  3. 密碼
  4. 帳號輸入欄位的id或name
  5. 密碼輸入欄位的id或name
  6. 驗證碼圖片的id或name
  7. 驗證碼輸入欄位的id或name
  8. 帳密欄位若被包裝在iframe內，則輸入iframe的id或name

![alt text](/doc/image-2.png)

二、直接使用 cmd 執行 start.py，程式將會開始自動執行，直到成功登入或達到嘗試次數上限為止。

![alt text](/doc/image-1.png)



三、細節改動
暫無 -->
