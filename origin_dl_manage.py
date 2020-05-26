import subprocess

import requests        #导入requests包
from bs4 import BeautifulSoup

list_fanhao=["WANZ-957","WANZ-955"]
proxies={
    "https":"socks5://127.0.0.1:20001"
}
def getm3u8(key_id):
    url = 'https://jable.tv/videos/'+key_id+'/'
    strhtml = requests.get(url,proxies=proxies)        #Get方式获取网页数据
    soup=BeautifulSoup(strhtml.text,'lxml')
    data = soup.select('#site-content > div > div > div:nth-child(1) > section.pb-3.pb-e-lg-30 > link')
    res = ''
    for item in data:
        res = item.get('href')
    return res

def dl(m3u,file):
    args = "./N_m3u8DL-CLI_v2.6.3.exe " + m3u +' --saveName ' +file+" "+file+" --minThreads "+"32"
    subprocess.call(args)

def main():
    for fanhao in list_fanhao:
        m = getm3u8(fanhao)
        f = fanhao
        dl(m,f)
main()