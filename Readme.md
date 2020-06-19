# 数据库爬取链接并且下载hls链接为mp4

通过数据库存储的数据爬取内容并按照相应的规律保存文件
数据库采用Access （方便）
并且会实时更新数据库内容

## 关于数据库的爬取

数据库的爬取使用的是另一个项目中的文件
本仓库是使用数据库中的基础数据进行hls抓取然后调用工具进行下载和保存操作
每个py文件内容尽量简短这样容易看懂

## 重要！！！ 项目依赖于`N_m3u8DL-CLI_v2.6.3.exe`和`ffmpeg.exe`

请到相应的项目下载可执行文件到该目录运行


## 最新更新，已经可以直接下载下来运行了，上面的依赖已经引入

使用方式

```
git clone git@github.com:whp98/hls_spider_downloader_with_rdb.git --depth 1
cd hls_spider_downloader_with_rdb
python ./main_proc.py
```