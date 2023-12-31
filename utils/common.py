
import os
import time
from selenium.webdriver.chrome.options import Options

#  整理 可通用的提示訊息
def message(type):
  if type == 0 : 
    print('請輸入網址。')
  elif type == 1 :
    print('尚未支援所輸入的網站。')
    
# 建立資料夾
def createdFolder(title):
  if not os.path.exists('video/' + title):
      os.makedirs('video/'+title)
  folderPath = os.path.join(os.getcwd(), 'video', title)
  
  print(folderPath)
  
  return folderPath

# 刪除 mp4 檔
def deleteMp4(folderPath):
    files = os.listdir(folderPath)
    originFile = folderPath.split(os.path.sep)[-1] + '.mp4'
    for file in files:
        if file != originFile:
            os.remove(os.path.join(folderPath, file))

# 刪除 m3u8 檔 
def deleteM3u8(folderPath):
    files = os.listdir(folderPath)
    for file in files:
        if file.endswith('.m3u8'):
            os.remove(os.path.join(folderPath, file))
            
# 合併檔案         
def mergeMp4(folderPath, tsList,video_name):
    # 開始時間
    start_time = time.time()
    print('開始合成影片..')

    for i in range(len(tsList)):
        file = tsList[i].split('/')[-1][0:-3] + '.mp4'
        full_path = os.path.join(folderPath, file)
        #video_name = folderPath.split(os.path.sep)[-1].split('/')[1]
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f1:
                with open(os.path.join(folderPath, video_name + '.mp4'), 'ab') as f2:
                    f2.write(f1.read())
        else:
            print(file + " 失敗 ")
    end_time = time.time()
    print('花費 {0:.2f} 秒合成影片'.format(end_time - start_time))
    print('下載完成!')
    
# 進行轉檔
def goConver(fileName):
    # 前往指定資料夾
    cd = 'cd ' + 'video/'+ fileName
    os.system(cd)

    # 做出路徑
    path = os.path.join('video',fileName,fileName)

    # 進行 轉換檔案
    shell_ffmpeg = 'ffmpeg -i ' + path + '.mp4 -c:v libx264 -b:v 2M -threads 10 -preset superfast ' + path + '_N.mp4'
        

    # print(shell_ffmpeg)
    os.system(shell_ffmpeg)

    print('轉換完成。')

# Selenium 設定檔
def SeleniumOption():
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    
    return options