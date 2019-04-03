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

### 豆瓣图书按照标签爬取图书信息
- [代码链接](chapter6/douban.py)
- 使用 request 库请求页面
- 使用 pyquery 库解析 DOM 节点数据
- 写入 CSV 文件

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

### IP代理池 *
- [代码链接](https://github.com/gabearwin/ProxyPool)
- 使用 request、pyquery 库请求并解析免费 IP 代理
- 使用 Redis 有序集合保存 IP 信息，并给 IP 打分
- 使用 aiohttp 异步请求测试 IP 代理是否可用
- 使用 flask 提供轻量级 API 服务