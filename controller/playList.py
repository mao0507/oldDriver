

from utils.common import createdFolder
from utils.downloadModule import Download_m3u8_with_url

# 直接下載 m3u8 list
def  start(url ,title) :
  
  if(title == ''):
    return
  else:
    folderPath = createdFolder(title)
    Download_m3u8_with_url(url,title,folderPath)
    
     