import subprocess
import time
import requests
from bs4 import BeautifulSoup
import pyodbc
import os
import logging

logging.basicConfig(level=logging.DEBUG,filename='AAAAAAA.log', filemode='a')
logging.info("程序启动开始连数据库")
logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
DBfile = r"D:\PY_Project\spider\DB.accdb"
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
cursor = conn.cursor()
logging.info("数据库连接成功")
logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

sql = "SELECT * FROM av_db WHERE isdown=False"


list_to_down=[]
## 存储列表

def getNewList():
    logging.info("清空下载文件列表")
    global list_to_down
    list_to_down=[]
    logging.info("获取下载文件列表")
    res = cursor.execute(sql)
    for row in res:
        item = {"f":row[1],'u':row[2]}
        list_to_down.append(item)

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
    logging.info("获取到m3u8为 "+res)
    return res


# 下载并合成
def dl(m3u,file):
    logging.info("开始下载文件"+file+".mp4")

    args = "./N_m3u8DL-CLI_v2.6.3.exe " + m3u +' --saveName ' +file+" --minThreads "+"32"+" --enableDelAfterDone"
    print(args)
    subprocess.call(args)

    logging.info("下载文件"+file+".mp4"+"完成")


def setHave(fanhao):
    sql = "UPDATE av_db SET isdown=True WHERE fanhao='{}'".format(fanhao)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("更新数据库中 "+fanhao+" 为已经下载")
    cursor.execute(sql)
    conn.commit()

# 更新数据库
def updateDB(filename_need_find):
    path=r"D:\NoInstallPrograme\N_m3u8DL-CLI\Downloads"
    g = os.walk(path)
    for path,dir_list,file_list in g:  
        for file_name in file_list:  
            (filename,extension) = os.path.splitext(file_name)
            if os.path.getsize(os.path.join(path,file_name)) > 100*1024*1024 and filename==filename_need_find:
                setHave(filename)

def main():
    getNewList()
    logging.info("主程序启动")
    for item in list_to_down:
        try:
            dl(get_hls(item),item.get('f'))
            # 检查下载的文件是否存在
            updateDB(item.get('f'))
        except Exception as e:
            print(e)

# 统计当前数据库中的下载情况
#返回当前下载量，总量和百分比
def get_db_info():
    sql_isdown = "SELECT * FROM av_db WHERE isdown=True"
    sql_all = "SELECT * FROM av_db"
    temp = cursor.execute(sql_isdown)
    count=0
    all_count=0
    for row in temp:
        count = count +1
    temp = cursor.execute(sql_all)
    for row in temp:
        all_count = all_count+1
    # print(count,all_count,str(count/all_count*100)+"%")
    logging.info("当前已经下载："+count+"还需要下载："+all_count)
    return count,  all_count,  str(count/all_count*100)+"%"

  
main()
