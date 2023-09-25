
# 依賴
import re
import os
import ssl
import m3u8
import requests
import cloudscraper
import urllib.request
from Crypto.Cipher import AES
from utils.config import headers
from utils.crawler import prepareCrawl
from utils.common import deleteM3u8,deleteMp4,mergeMp4,goConver,createdFolder,SeleniumOption
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 透過 requests 去找尋 m3u8網址
def Download_m3u8_with_requests(url,title,folderPath) :
  htmlfile = cloudscraper.create_scraper(browser='chrome', delay=10).get(url)
  result = re.search("https://.+m3u8", htmlfile.text)
  m3u8url = result[0]
  # 拆成陣列
  m3u8urlList = m3u8url.split('/')
  m3u8urlList.pop(-1)
  # 建立下載網址
  downloadurl = '/'.join(m3u8urlList)
  # 儲存 m3u8 file 至資料夾
  m3u8file = os.path.join(folderPath, 'playlist.m3u8')
  ssl._create_default_https_context = ssl._create_unverified_context
  urllib.request.urlretrieve(m3u8url, m3u8file)
  
  # 得到 m3u8 file裡的 URI和 IV
  m3u8obj = m3u8.load('./video/'+ title +'/playlist.m3u8')
  m3u8uri = ''
  m3u8iv = ''
  
  for key in m3u8obj.keys:
    if key:
        m3u8uri = key.uri
        m3u8iv = key.iv
        
  # 儲存 ts網址 in tsList
  tsList = []
  for seg in m3u8obj.segments:
      tsUrl = downloadurl + '/' + seg.uri
      tsList.append(tsUrl)
      
  # 有加密
  if m3u8uri:
      m3u8keyurl = downloadurl + '/' + m3u8uri  # 得到 key 的網址

      # 得到 key的內容
      response = requests.get(m3u8keyurl, headers=headers, timeout=10)
      contentKey = response.content

      vt = m3u8iv.replace("0x", "")[:16].encode()  # IV取前16位

      ci = AES.new(contentKey, AES.MODE_CBC, vt)  # 建構解碼器
  else:
      ci = ''
      
  # 開始爬蟲並下載mp4片段至資料夾      
  prepareCrawl(ci, folderPath, tsList)
  # 刪除m3u8 file
  deleteM3u8(folderPath)
  # 合成mp4
  mergeMp4(folderPath, tsList,title)
  # 刪除子mp4
  deleteMp4(folderPath)
  # 進行轉檔
  goConver(title)
# 透過 Selenium 來建立下載項目
def Download_m3u8_with_selenium(url):
  print('正在下載影片: ' + url)
  # 建立番號資料夾
  urlSplit = url.split('/')
  dirName = urlSplit[-2]
  # 檢查有無video 資料夾
  createdFolder('video')
  
  if os.path.exists(f'video/{dirName}/{dirName}.mp4'):
    print('番號資料夾已存在, 跳過...')
    return
  if not os.path.exists('video/'+dirName):
      os.makedirs('video/'+dirName)
  folderPath = os.path.join(os.getcwd(), 'video', dirName)
  
  #配置Selenium參數
  options = SeleniumOption()
  dr = webdriver.Chrome(options=options)
  dr.get(url)
  title = dr.find_element(By.TAG_NAME,"h4").text
  
  result = re.search("https://.+m3u8", dr.page_source)
  print(f'result: {result}')
  m3u8url = result[0]
  print(f'm3u8url: {m3u8url}')

  # 得到 m3u8 網址
  m3u8urlList = m3u8url.split('/')
  m3u8urlList.pop(-1)
  downloadurl = '/'.join(m3u8urlList)
  
   # 儲存 m3u8 file 至資料夾
  m3u8file = os.path.join(folderPath, 'playlist.m3u8')
  urllib.request.urlretrieve(m3u8url, m3u8file)

  # 得到 m3u8 file裡的 URI和 IV
  m3u8obj = m3u8.load('./video/'+ dirName +'/playlist.m3u8')
  m3u8uri = ''
  m3u8iv = ''
  
  for key in m3u8obj.keys:
      if key:
          m3u8uri = key.uri
          m3u8iv = key.iv

  # 儲存 ts網址 in tsList
  tsList = []
  for seg in m3u8obj.segments:
      tsUrl = downloadurl + '/' + seg.uri
      tsList.append(tsUrl)

  # 有加密
  if m3u8uri:
      m3u8keyurl = downloadurl + '/' + m3u8uri  # 得到 key 的網址
      # 得到 key的內容
      response = requests.get(m3u8keyurl, headers=headers, timeout=10)
      contentKey = response.content

      vt = m3u8iv.replace("0x", "")[:16].encode()  # IV取前16位

      ci = AES.new(contentKey, AES.MODE_CBC, vt)  # 建構解碼器
  else:
      ci = ''

  # 刪除m3u8 file
  deleteM3u8(folderPath)

  # 開始爬蟲並下載mp4片段至資料夾
  prepareCrawl(ci, folderPath, tsList)

  # 合成mp4
  mergeMp4(folderPath, tsList,dirName)
  
  # 刪除子mp4
  deleteMp4(folderPath)
  
  # 進行轉檔
  goConver(dirName)
  
  # 補寫完整檔名
  os.path.join(folderPath, title+'.txt')
  with open(folderPath+'/'+title+'.txt','w',encoding="utf-8") as f:
    f.write(title)
    f.close()
    
    
    # 直接對輸入的m3u8網址進行下載
# 透過提供的 m3u8網址來進行下載
def Download_m3u8_with_url(url,title,folderPath):
    m3u8url = url
    m3u8urlList = m3u8url.split('/')
    m3u8urlList.pop(-1)
    # 先預設下載路徑皆為相同，建立一個下載路徑網址
    downloadurl = '/'.join(m3u8urlList)
    # 檢查 m3u8 playlist 有無提供 網址路徑， 如果有 則照著路徑下載，沒有的話則另外解析網址 
    m3u8file = os.path.join(folderPath, 'playlist.m3u8')
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(m3u8url, m3u8file)
    
    # 得到 m3u8 file裡的 URI和 IV
    m3u8obj = m3u8.load('./video/'+ title +'/playlist.m3u8')
    m3u8uri = ''
    m3u8iv = ''
    
    # 取出 key
    for key in m3u8obj.keys:
        if key:
            m3u8uri = key.uri
            m3u8iv = key.iv
            
    # 建立空陣列，紀錄檔案網址
    tsList = []
    for seg in m3u8obj.segments:
        # 判斷是不是本來就有完整網址路徑
        if('http' in seg.uri):
            tsUrl = seg.uri
        else:
            # 沒有的話才需要自行組合
            tsUrl = downloadurl + '/' + seg.uri
        # 加入陣列
        tsList.append(tsUrl)
        
     # 有加密
    if m3u8uri:
        m3u8keyurl = downloadurl + '/' + m3u8uri  # 得到 key 的網址
        # 得到 key的內容
        response = requests.get(m3u8keyurl, headers=headers, timeout=10)
        contentKey = response.content

        vt = m3u8iv.replace("0x", "")[:16].encode()  # IV取前16位

        ci = AES.new(contentKey, AES.MODE_CBC, vt)  # 建構解碼器
    else:
        ci = ''
        
    # 開始爬蟲並下載mp4片段至資料夾      
    prepareCrawl(ci, folderPath, tsList)
    # 刪除m3u8 file
    deleteM3u8(folderPath)
    # 合成mp4
    mergeMp4(folderPath, tsList,title)
    # 刪除子mp4
    deleteMp4(folderPath)
    # 進行轉檔
    goConver(title)
    