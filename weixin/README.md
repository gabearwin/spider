搜狗微信文章爬取
---
### 功能描述
- 自定义请求结构体，每一次请求都是一个单独的结构体，包含请求 URL、请求代理、超时时间
- 将所有请求结构体存储在 Redis 中，涉及到序列化和反序列化
- 每个代理都是从本地维护的 IP 代理池中随机获取的
- 解析微信文章，存储在 MySQL 中

### 使用说明
- 安装好必要的 Python 库
- 本地启动 Redis，MySQL，本地 IP 代理池的 REST 服务
- 创建 `spider` 数据库，执行 `weixin/weixin.sql` 建表语句
- 在 `weixin/config.py` 文件中配置相关信息
- 在 `https://weixin.sogou.com/` 页面登陆个人账号，将请求头复制下来，替换 `weixin/spider.py` 文件中的 headers 参数
- 执行 `weixin/spider.py` 文件