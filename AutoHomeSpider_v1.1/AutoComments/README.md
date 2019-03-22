## 程序的启动
- 运行main.py，这里使用多进程来执行
    - 启动异步代理客户端程序
    - 启动异步代理的flask 服务器
    - 运行 scrapy 爬虫


## 程序的配置
- AutoComments/async_proxy_pool/config.py
    - 该文件主要是涉及到代理池的一些配置信息
    - 重要的配置：server host 和 server port
- AutoComments/settings.py
    - spider 的相关配置
    - 写文件的配置
    -

