
from utils.common import message
from controller import avple,jable

# 開始
def start():
  url = input('請輸入網址 ：')
  # 傳入網址，進行路由判斷
  classification(url)
  
  

# 判斷輸入的網址
def classification(url): 
  
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