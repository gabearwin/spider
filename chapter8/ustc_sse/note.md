软院信息化平台通知爬取
---
### 功能描述
- 自动登录信息化平台，爬取最新通知
- 将通知信息存储到 MongoDB 中
- 对于新通知(其ID不在MongoDB中)，会发送邮件提醒

### 使用说明
- 提前安装好 MongoDB、ChromeDriver，以及相关 Python 库（requests、pymongo、pyquery、selenium）
- 将 `ustc_sse/config.py` 配置文件中相关账号改成自己的，注意邮箱密码是客户端授权码
- 执行 `ustc_sse.py` 文件
