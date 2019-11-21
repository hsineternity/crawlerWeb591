from fake_useragent import UserAgent

def createHeaders( number ):
  headers = {}
  headers['Cookie'] = 'urlJumpIp=' + number # add County
  
  ua = UserAgent()
  headers['User-Agent'] = ua.random  # add header 偽裝請求
  return headers

def decidSex( sexLists ):
  statusSex = ''
  if '男' in sexLists and '女' in sexLists :
    statusSex = '男女生皆可'
  elif '女' in sexLists :
    statusSex = '女生'
  else :
    statusSex = '男生'
  return statusSex
