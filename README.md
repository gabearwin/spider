Python3 网络爬虫实战
------
### 猫眼电影评分Top100爬取
- [代码链接](chapter3/maoyan.py)
- requests库，获取HTML
- re库，正则获取DOM节点数据
- 写入文件

### 新浪个人微博爬取
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

### 软院信息化平台通知爬取
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

### 搜狗微信文章爬取
- [代码链接](weixin/spider.py)
- 使用 request、pyquery 库请求并解析网页
- 使用 IP 代理池提供的代理进行网络请求
- 自定义请求结构体，拓展代理、回调函数等功能
- 使用 Redis 存储请求结构体队列，使用 pickle 将对象序列化/反序列化
- 使用 MySQL 存储微信文章

### GitHub 模拟登陆及动态爬取
- [代码链接](chapter10/github.py)
- 使用 request 库请求页面，使用 session 保持登陆状态
- 使用 xpath 解析网页
- 分析登录接口参数，模拟登录

### 搭建Cookies池[以登录新浪微博为例] *
- [代码链接](https://github.com/gabearwin/CookiesPool)
- 使用 selenium 自动登录新浪微博，以及使用动作链破解四宫格验证码
- 使用 Redis 的 Hash 存储(用户名，密码)和(用户名，Cookie)
- 使用 flask 提供 API 服务，获取随机 Cookie 值
- 使用三个线程分别用来获取 Cookie、验证 Cookie、提供 API 服务
