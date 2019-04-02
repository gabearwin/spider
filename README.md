Python3 网络爬虫实战
------
### 猫眼电影评分Top100爬取
- [代码链接](chapter3/maoyan.py)
- requests库，获取HTML
- re库，正则获取DOM节点数据
- 写入文件

### 新浪微博爬取
- [代码链接](chapter6/weibo.py)
- 直接分析使用 Ajax 返回的 JSON 数据
- 使用 pyquery 库解析 DOM 节点数据
- 使用 pymongo 库存储数据到 MongoDB

### 今日头条「街拍」关键词图片爬取
- [代码链接](chapter6/jiepai.py)
- 直接分析使用 Ajax 返回的 JSON 数据
- 使用 os.path 创建文件夹
- 使用 hashlib.md5 将图片内容值信息作为文件名
- 写入文件
- 使用 multiprocessing.pool 多线程下载

### 淘宝搜索页商品爬取
- [代码链接](chapter7/taobao.py)
- 使用 selenium 自动搜索和翻页
- 使用 pyquery 库解析 DOM 节点数据
- 使用 pymongo 库存储数据到 MongoDB

### 软院信息化平台信息爬取
- [代码链接](chapter8/ustc_sse/ustc_sse.py)
- 使用 selenium 自动登录，切换 frame
- 使用 pyquery 库解析 DOM 节点数据
- ~~使用 tesserocr 库识别验证码~~ 从 Cookie 中获取验证码
- 使用 pymongo 库存储数据到 MongoDB
- 使用 smtplib 发送邮件