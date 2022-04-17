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