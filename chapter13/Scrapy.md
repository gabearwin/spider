Scrapy 知识点总结
---
### 起步
- `scrapy startproject downloader` 创建一个项目
- 进入项目文件夹，`scrapy genspider httpbin httpbin.org`，创建一个 spider，并指定网站域名
- `scrapy crawl httpbin`，启动 httpbin 这个 spider
- `scrapy crawl httpbin -o result.csv`，启动 httpbin 这个 spider，将结果保存在 result.csv 文件中
- `scrapy shell http://www.baidu.com/` 发送请求并进入内置 shell

![Scrapy架构图](scrapy.png)


### Spider 的用法
- 定义爬取网站的动作
- 分析爬取下来的网页
    - 解析出有效结果(字典或者 Item 对象)，当做 response 处理
    - 解析出下一页链接，利用此链接构造新的 Request 并设置回调函数，等待调度
    
### Downloader Middleware 的用法
- 此组件非常重要，是做异常处理和应对反爬虫处理的核心
- 修改请求头，如 User-Agent
- 设置代理
- 处理重定向
- 失败重试
- 设置 Cookies

### Spider Middleware 的用法
- 使用频率不如 Downloader Middleware 的高
- 在必要的时候可以用来数据处理

### Item Pipeline 的用法
- 清理 HTML 数据
- 验证爬取数据，检查爬取字段
- 查重并丢弃重复内容
- 将爬取结果保存至数据库