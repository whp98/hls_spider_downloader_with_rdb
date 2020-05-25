import requests        #导入requests包
from bs4 import BeautifulSoup


def getm3u8(key_id):
    url = 'https://jable.tv/videos/'+key_id+'/'
    strhtml = requests.get(url)        #Get方式获取网页数据
    soup=BeautifulSoup(strhtml.text,'lxml')
    data = soup.select('#site-content > div > div > div:nth-child(1) > section.pb-3.pb-e-lg-30 > link')
    res = ''
    for item in data:
        res = item.get('href')
    return res
print(getm3u8("IPX-491"))