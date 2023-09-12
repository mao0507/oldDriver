import bs4
import requests
from utils.config import headers
from utils.common import createdFolder
from utils.downloadModule import Download_m3u8


# 開始執行 Avple 網站影片抓取
def start(url):
    title =  getTitle(url)
    print('片名 : ' + title)
    
    # 建立資料夾
    folderPath = createdFolder(title)
    Download_m3u8(url,title,folderPath)
    
# 取得title    
def getTitle(url):
  
  # 取得網頁資料
  req = requests.get(url, headers=headers)
  # 調整網頁格式，防止亂碼
  req.encoding = 'utf-8'
  # 取得網頁節點
  html = bs4.BeautifulSoup(req.text, 'html.parser')
  # 取得網頁標籤 並做處理
  title = html.title.getText().split('|')[0].replace('）', ')').replace('（', '(').replace('&', '_').replace('/', '').replace('?', '_').replace(' ', '')
 
  return title
  


  