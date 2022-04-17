## 开发前准备

python 版本 3.8 以上

机器人入口
```
cd bot
python main.py
```
## 技术栈
采用 pip 作为包管理器（因为几乎用不到几个）

**不使用**类似 Nonebot 的机器人封装，本项目足够简单，无需封装。

使用 Docker 打包发行。

使用 Pylint 作为代码静态检查器。
```
pip install pylint
```

VS code: To enable linters, open the Command Palette (`Ctrl+Shift+P`) and select the Python: Select Linter command.

不使用单元/mock测试。

## 目录结构
```
├── LICENSE 
├── README.md
├── bot  
│   ├── Dockerfile
│   ├── main.py
│   ├── config.py // 机器人配置
│   ├── qq // qq 接口实现
│   │   └── __init__.py
│   ├── requirements.txt // 依赖包
│   ├── tg // tg 接口实现
│   │   └── __init__.py
│   └── tools // 共用工具 如日志
│       └── __init__.py
├── development-guide.md
├── docker-compose.yml // Docker 启动文件
└── go-cqhttp // qq api
    ├── Dockerfile
    ├── config.yml // 配置
    └── go-cqhttp
```
## 核心机制
Python 的 asyncio 和 aiohttp，参考 main.py 示例。
main.py 中我们有两个函数，分别获取天气和时间信息，从调用的顺序来看，我们先调用获取时间的函数，这个函数将在5秒后打印时间，从结果来看它确实做到了。
然后就是获取天气的函数，它是立刻获取的，从结果来看确实如此，但是这两个函数好像是同时运行互不干扰的，就像两个线程一样。实际上我们只用了一个线程！

欸等等，先别急，这段程序本来应该是每隔5秒循环一次的，但是它们在第一次打印结果之后就结束了，请试图修复它。

## 实现功能
暂时只有一个：实现 QQ 和 Telegram 的消息互相转发，只转发文本文字，不考虑其他类型的消息。但是链接在转发到 QQ 的时候可以试着和 Telegram 一样尝试获取摘要和缩略图。

也就是说，QQ Telegram 部分分别要提供一个函数，接收一个发送者昵称，字符串和群ID（也是字符串给出），然后在对应的群中发送消息。
而在内部对群消息轮询，将新消息识别，处理，并调用转发函数。

在开发时应在本地使用一个新分支而不是 main 进行工作。

## 配置参数
```python
# config.py
config = {
    'Telegram': {
        # tg使用的http代理（可选）
        'http_proxy': 'http://127.0.0.1:8008/',
        'forward_list': [
            {
                # tg bot的token
                'token': '123456:abcdefgABCDEFG',
                # 需要转发的群id
                'chat_id': '-1234567',
                # 不转发的id列表
                'blacklist': [
                    '123456'
                ],
            },
        ],
    },
    'QQ': {
        'base_uri': 'http://127.0.0.1:5700',
        'forward_list': [
            {
                # qq群id
                'group_id': 123456,
                # go-cqhttp中，http的地址
                # qq和irc互联时，irc的配置
                'irc': {
                    'nick': 'tencent_qq_bot',
                    'password': 'password_qq',
                },
                # 不转发的qq号
                'blacklist': [
                    '123456789'
                ],
            },
        ],
    },
    'pair':[
        ('-123456',123456), # tg 群和 QQ 群的配对
    ]
}
```