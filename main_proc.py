import subprocess
import time
import requests
from bs4 import BeautifulSoup
import os
import logging
import pymysql

logging.basicConfig(level=logging.DEBUG, filename='AAAAAAA.log', filemode='a')
# logging.info("程序启动开始连数据库")
# logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# DBfile = r"D:\PY_Project\spider\DB.accdb"
# conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
# cursor = conn.cursor()
# db = pymysql.connect(host='redis.intellij.xyz', user='root',
#                      passwd='mysql_password', db='av_db', port=3307, charset='utf8')
# cursor = db.cursor()
# logging.info("数据库连接成功")
# logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

sql_one = "SELECT * FROM avtable1 WHERE isdown=FALSE and doing=FALSE LIMIT 1"

def safeexecuteforcommit(sql):
    logging.info("开始执行插入sql")
    logging.info(sql)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db = pymysql.connect(host='redis.intellij.xyz', user='root',passwd='mysql_password', db='av_db', port=3307, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    logging.info("sql执行成功")

def safeexecuteforqueryCount(sql):
    logging.info("开始执行查询sql")
    logging.info(sql)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db = pymysql.connect(host='redis.intellij.xyz', user='root',passwd='mysql_password', db='av_db', port=3307, charset='utf8')
    cursor = db.cursor()
    count=cursor.execute(sql)
    db.close()
    logging.info("sql执行完成")
    return count

def safeexecuteforOne(sql):
    logging.info("开始执行查询sql")
    logging.info(sql)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db = pymysql.connect(host='redis.intellij.xyz', user='root',passwd='mysql_password', db='av_db', port=3307, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    one = cursor.fetchone()
    db.close()
    logging.info("sql执行完成")
    return one


def getOne():
    logging.info("开始获取一条数据")
    row = safeexecuteforOne(sql_one)
    item = {"f": row[0], 'u': row[1]}
    logging.info("获取完成")
    return item


proxies = {
    "https": "socks5://127.0.0.1:20001"
}


def get_hls(item):
    url = item.get('u')
    strhtml = requests.get(url, proxies=proxies)  # Get方式获取网页数据
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data = soup.select('#site-content > div > div > div:nth-child(1) > section.pb-3.pb-e-lg-30 > link')
    res = ''
    for item in data:
        res = item.get('href')
    logging.info("获取到m3u8为 "+res)
    return res


def setdoing(fanhao):
    sql = "UPDATE avtable1 SET doing=TRUE WHERE fanhao='{}'".format(fanhao)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡")
    logging.info("更新数据库中 "+fanhao+" 为开始下载")
    safeexecuteforcommit(sql)


def setnotdoing(fanhao):
    sql_haha = "UPDATE avtable1 SET doing=FALSE WHERE fanhao='{}'".format(
        fanhao)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍👍")
    logging.info("更新数据库中 "+fanhao+" 为停止下载")
    logging.info(sql_haha)
    safeexecuteforcommit(sql_haha)

# 下载并合成


def dl(m3u, file):
    logging.info("开始下载文件"+file+".mp4")
    args = "./N_m3u8DL-CLI_v2.6.3.exe " + m3u + ' --saveName ' + \
        file+" --minThreads "+"32"+" --enableDelAfterDone"
    logging.info(args)
    subprocess.call(args)
    logging.info("下载文件"+file+".mp4"+"完成")


def setHave(fanhao):
    sql_update = "UPDATE avtable1 SET isdown=TRUE WHERE fanhao='{}'".format(
        fanhao)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁")
    logging.info("更新数据库中 "+fanhao+" 为已经下载")
    safeexecuteforcommit(sql_update)

# 更新数据库


def updateDB(filename_need_find):
    logging.info("开始查找视频文件")
    path = "./Downloads"
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            (filename, extension) = os.path.splitext(file_name)
            if os.path.getsize(os.path.join(path, file_name)) > 100*1024*1024 and filename == filename_need_find:
                logging.info("文件找到，开始更改数据库中文件存储状态")
                setHave(filename)
                logging.info("数据库中的数据字段更新完成")
    logging.info("查找更新文件完成")

# 统计当前数据库中的下载情况
# 返回当前下载量，剩余量和百分比


def get_db_info():
    logging.info("获取当前下载进度👀👀👀👀👀👀👀👀👀👀👀👀")
    sql_isdown = "SELECT * FROM avtable1 WHERE isdown=TRUE"
    sql_all = "SELECT * FROM avtable1"
    count = safeexecuteforqueryCount(sql_isdown)
    need_count = 0
    all_count = safeexecuteforqueryCount(sql_all)
    need_count = all_count-count
    # print(count,all_count,str(count/all_count*100)+"%")
    logging.info("当前已经下载："+str(count)+"还需要下载："+str(need_count) +
                 "下载进度： "+str(count/all_count*100)+"%")
    return count,  all_count,  str(count/all_count*100)+"%"


def main():
    logging.info("主程序启动")
    while True:
        item = getOne()
        if(item != None):
            get_db_info()
            setdoing(item.get('f'))
            dl(get_hls(item), item.get('f'))
            setnotdoing(item.get('f'))
            # 检查下载的文件是否存在
            updateDB(item.get('f'))
        else:
            print("异常")
        


main()
