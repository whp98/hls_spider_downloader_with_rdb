import subprocess
import time
import requests
from bs4 import BeautifulSoup
import pyodbc
import os
import logging
import pymysql

logging.basicConfig(level=logging.DEBUG,filename='AAAAAAA.log', filemode='a')
logging.info("程序启动开始连数据库")
logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# DBfile = r"D:\PY_Project\spider\DB.accdb"
# conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
# cursor = conn.cursor()
db = pymysql.connect(host='redis.intellij.xyz',user='root',passwd='mysql_password',db='av_db',port=3307,charset='utf8')
cursor = db.cursor()
logging.info("数据库连接成功")
logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

sql_one = "SELECT * FROM avtable1 WHERE isdown=False and doing=False LIMIT 1"


# list_to_down=[]
## 存储列表

# def getNewList():
#     logging.info("清空下载文件列表")
#     global list_to_down
#     list_to_down=[]
#     logging.info("获取下载文件列表")
#     cursor.execute(sql)
#     res = cursor.fetchall()
#     for row in res:
#         item = {"f":row[0],'u':row[1]}
#         list_to_down.append(item)

def getOne():
    logging.info("开始获取一条数据")
    cursor.execute(sql_one)
    row = cursor.fetchone()
    item = {"f":row[0],'u':row[1]}
    logging.info("获取完成")
    return item


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

def setdoing(fanhao):
    sql = "UPDATE avtable1 SET doing=True WHERE fanhao='{}'".format(fanhao)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡")
    logging.info("更新数据库中 "+fanhao+" 为开始下载")
    cursor.execute(sql)
    db.commit()

def setnotdoing(fanhao):
    sql = "UPDATE avtable1 SET doing=False WHERE fanhao='{}'".format(fanhao)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍")
    logging.info("更新数据库中 "+fanhao+" 为下载完成")
    cursor.execute(sql)
    db.commit()

# 下载并合成
def dl(m3u,file):
    logging.info("开始下载文件"+file+".mp4")

    args = "./N_m3u8DL-CLI_v2.6.3.exe " + m3u +' --saveName ' +file+" --minThreads "+"32"+" --enableDelAfterDone"
    print(args)
    subprocess.call(args)

    logging.info("下载文件"+file+".mp4"+"完成")


def setHave(fanhao):
    sql = "UPDATE avtable1 SET isdown=True WHERE fanhao='{}'".format(fanhao)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁")
    logging.info("更新数据库中 "+fanhao+" 为已经下载")
    cursor.execute(sql)
    db.commit()

# 更新数据库
def updateDB(filename_need_find):
    path=r"D:\NoInstallPrograme\N_m3u8DL-CLI\Downloads"
    g = os.walk(path)
    for path,dir_list,file_list in g:  
        for file_name in file_list:  
            (filename,extension) = os.path.splitext(file_name)
            if os.path.getsize(os.path.join(path,file_name)) > 100*1024*1024 and filename==filename_need_find:
                setHave(filename)

# 统计当前数据库中的下载情况
#返回当前下载量，剩余量和百分比
def get_db_info():
    sql_isdown = "SELECT * FROM avtable1 WHERE isdown=True"
    sql_all = "SELECT * FROM avtable1"
    count=cursor.execute(sql_isdown)
    need_count=0
    all_count = cursor.execute(sql_all)
    need_count=all_count-count
    
    # print(count,all_count,str(count/all_count*100)+"%")
    logging.info("当前已经下载："+str(count)+"还需要下载："+str(need_count)+"下载进度： "+str(count/all_count*100)+"%")
    return count,  all_count,  str(count/all_count*100)+"%"

def main():
    logging.info("主程序启动")
    while True:
        try:
            item = getOne()
            if(item!=None):
                get_db_info()
                setdoing(item.get('f'))
                dl(get_hls(item),item.get('f'))
                setnotdoing(item.get('f'))
                # 检查下载的文件是否存在
                updateDB(item.get('f'))
            else:
                print("异常")
        except Exception as e:
            print(e)



  
main()
