import re
import bs4
import requests
from utils.config import headers
from utils.common import createdFolder
from utils.downloadModule import Download_m3u8_with_requests

def start(url):
  #print(url)
  title = getTitle(url)
  folderPath = createdFolder(title)
  Download_m3u8_with_requests(url,title,folderPath)
  
def getTitle(url):
   # 請求網頁資料
    req = requests.get(url, headers=headers)
    # 調整網頁格式，防止亂碼
    req.encoding = 'utf-8'
    # 取得網頁節點
    html = bs4.BeautifulSoup(req.text, 'html.parser')
    # 取得網頁標籤 並做處理
    title = html.title.getText().split('|')[0].replace(' ', '').replace('）', ')').replace('（', '(').replace('&', '_').replace('/', '').replace('?', '_')
       
    
    
    return title