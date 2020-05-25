import subprocess

import requests        #导入requests包
from bs4 import BeautifulSoup
import pyodbc
import os


DBfile = r"D:\PY_Project\spider\DB.accdb"
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
cursor = conn.cursor()
sql = "SELECT * FROM av_db WHERE isdown=False"


list_to_down=[]
## 存储列表

def getNewList():
    res = cursor.execute(sql)
    for row in res:
        item = {"f":row[1],'u':row[2]}
        list_to_down.append(item)

getNewList()


proxies={
    "https":"socks5://127.0.0.1:20001"
}

#获取m3u8
def get_hls(item):
    url = item.get('u')
    strhtml = requests.get(url,proxies=proxies)        #Get方式获取网页数据
    soup=BeautifulSoup(strhtml.text,'lxml')
    data = soup.select('#site-content > div > div > div:nth-child(1) > section.pb-3.pb-e-lg-30 > link')
    res = ''
    for item in data:
        res = item.get('href')
    return res


# 下载并合成
def dl(m3u,file):
    args = "./N_m3u8DL-CLI_v2.6.3.exe " + m3u +' --saveName ' +file+" --minThreads "+"32"
    print(args)
    subprocess.call(args)


def setHave(fanhao):
    sql = "UPDATE av_db SET isdown=True WHERE fanhao='{}'".format(fanhao)
    print(sql)
    cursor.execute(sql)
    conn.commit()
# 更新数据库
def updateDB():
    path=r"D:\NoInstallPrograme\N_m3u8DL-CLI\Downloads"
    g = os.walk(path)
    for path,dir_list,file_list in g:  
        for file_name in file_list:  
            (filename,extension) = os.path.splitext(file_name)
            if os.path.getsize(os.path.join(path,file_name)) > 100*1024*1024:
                setHave(filename)
                print(filename+"  >>>>>  "+"True")

def main():
    for item in list_to_down:
        try:
            dl(get_hls(item),item.get('f'))
            # 检查下载的文件是否存在
            updateDB()
        except Exception as e:
            print(e)
            getNewList()


main()