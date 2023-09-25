
from utils.common import message
from controller import avple,jable,playList

# 開始
def start():
  url = input('請輸入網址 ：')
  # 傳入網址，進行路由判斷
  classification(url)
  
  

# 判斷輸入的網址
def classification(url): 
  # 檢查是不是m3u8檔，如果是，直接下載
  if('m3u8' in url) :
    print('m3u8')   
    # 輸入 檔案名稱
    title = input('請輸入檔案名稱 : ')
    print('依照所提供的 m3u8 網址，來進行下載')
    # 執行功能
    playList.start(url,title)
    
  else: 
    if url == '' :
      message(0)
    
    elif 'avple' in url : 
      print('來源網站 : avple')
      avple.start(url)
      
    elif 'jable' in url : 
      print('來源網站 : jable')
      jable.start(url)
    
    elif 'cableav' in url:
      print('來源網站 : cableav')
      
    else :
      message(1)
    

if __name__ == '__main__':
  start()