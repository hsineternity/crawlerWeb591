import requests
import re

from elasticsearch import  Elasticsearch
from bs4 import BeautifulSoup
from smallTools import createHeaders, decidSex

def getBriefContent( number ):
  lists = []

  url = "https://rent.591.com.tw" 
  headers = createHeaders( number )

  # get page
  response = requests.get( url, headers=headers)
  soup = BeautifulSoup( response.content, 'lxml' ) 
  page = soup.find_all("a", class_="pageNum-form")[-1].get_text()
  
  for i in range(int(page)) :
    response = requests.get( url, headers=headers, params={ 'firstRow' : i*30} )
    soup = BeautifulSoup( response.content, 'lxml' ) 

    homes = soup.find_all( "li", class_="pull-left infoContent" )
    for h in homes:
      lists.append( "http:" + h.a.get('href') )
    return lists

def getDetailContent( url ):
  houseDetail = {}

  response = requests.get( url )
  soup = BeautifulSoup( response.content, 'lxml' )
  landlord = soup.find('div', { 'class' : 'avatarRight'}).i.string

  tempIdentity = soup.find('div', { 'class' : 'avatarRight'}).text
  parserIdentity = re.findall(r'\u5c4b\u4e3b', tempIdentity)
  identity = '屋主' if len(parserIdentity) == 1 else '代理人'
  
  housePhone = soup.find("div", { 'class' : 'hidtel' }).string
  cellphone = soup.find("span", { 'class' : 'dialPhoneNum' }).get('data-value')

  tempHouse = soup.find('ul', { 'class' : 'attr' }).text
  parserHouse = re.sub(r':|\s','' , tempHouse)
  house = re.sub(r'.*(\u578b\u614b)|(\u73fe\u6cc1).*','' , parserHouse)
  
  tempStatus = soup.find('ul', { 'class' : 'attr' }).text
  parserStatus = re.sub(r':|\s','' , tempStatus)
  status = re.sub(r'.*(\u73fe\u6cc1)|(\u793e\u5340).*','' , parserStatus)
  
  tempSex = soup.find_all('div', { 'class' : 'two' })
  parserSex = re.findall(r'(\u7537)|(\u5973)', str(tempSex))
  sex = decidSex(parserSex)
  
  houseDetail['landlord'] = landlord
  houseDetail['identity'] = identity
  houseDetail['housePhone'] = housePhone
  houseDetail['cellphone'] = cellphone
  houseDetail['status'] = status
  houseDetail['sex'] = sex

  return houseDetail

def main():
  es = Elasticsearch()
  countyHouseUrls = {}
  
  # 縣市
  countyNumber = { 'taipei' : '1', 'newtaipei' : '3' }
  
  for k, v in countyNumber.items() :
    countyHouseUrls[k] = getBriefContent( v )

  for k, v in countyHouseUrls.items():
    for url in v :
      houseId = re.findall(r'\d+', url)[-1]
      houseDetail = getDetailContent(url)
      es.index( index=k, doc_type='house' , id=houseId, body=houseDetail )


if __name__ == "__main__":
  main()  
