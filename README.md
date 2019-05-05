Python3 网络爬虫实战
------
### 猫眼电影评分Top100爬取
- [代码链接](chapter3/maoyan.py)
- requests库，获取HTML
- re库，正则获取DOM节点数据
- 写入文件

### 美团外卖商家信息爬取(指定经纬度)
- [代码链接](chapter3/meituan_waimai.py)
- 拼装 Headers 头信息
- requests库，获取JSON数据
- 写入 CSV 文件

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

### 去哪儿攻略爬取
- [代码链接](chapter12/qunar.py)
- 使用 pyspider 爬虫框架可视化爬取
- 自动爬取下一页，内置 pyquery 等解析库
- 可视化开启任务以及查看任务状态，导出爬取结果
- 框架详细功能介绍请看[链接](https://github.com/binux/pyspider)

### Scrapy初始--爬取 quotes 网站
- [代码链接](chapter13/tutorial/tutorial/spiders/quotes.py)
- 使用 items 定义要提取的信息结构体
- 使用 spider 解析页面以及生成下一页请求
- 使用 pipelines 对结果过滤，以及存储到 MongoDB 中

### Scrapy初始--爬取 Image360 网站
- [代码链接](chapter13/pipeline/pipeline/spiders/images.py)
- 自定义初始请求动作
- 继承 ImagesPipeline，实现图片下载
- 使用 pipelines 将结果存储到 MongoDB 和 MySQL 中

### Scrapy进阶--结合 Selenium 爬取淘宝搜索页
- [代码链接](chapter13/scrapyselenium/scrapyselenium/spiders/taobao.py)
- 在 spider 中自定义初始请求动作，使用 xpath 解析页面
- 在 middlewares 中使用 selenium 完成请求
- 在 pipelines 中将结果存储到 MongoDB

### Scrapy进阶--抽象通用爬虫[以爬取中华网新闻为例]
- [代码链接](chapter13/universal/run.py)
- 定义爬虫站点配置 JSON 文件
    - `spider` 指定使用 spider 的名称
    - `settings` 为此 spider 自定义配置
    - `start_urls` 爬虫起始链接
    - `allowed_domains` 允许爬取的站点
    - `rules` 站点爬取规则
    - `item` 站点提取规则
- 在通用 spider 中对上面配置参数初始化，并提取 item
- 接入新的爬虫 china 的步骤
    - 配置 `universal.configs.china.json`，最基本且必须的配置
    - 配置 `universal.configs.rules.py`，定义规则
    - 配置 `universal.configs.urls.py`，定义爬虫起始链接，可选
    - 配置 `universal.loaders.py`，定义提取对象的处理
    - 配置 `universal.items.py`，定义提取对象
    - 配置 `universal.middlewares.py` 和 `universal.pipelines.py` 等中间件，可选
    - 执行 `python run.py china` 启动项目
