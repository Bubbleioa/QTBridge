import logging
import os

tg_token = os.getenv('TG_BOT_TOKEN')
config = {
    'Telegram': {
        # tg使用的http代理（可选）
        'http_proxy': 'http://127.0.0.1:7890/',
        'forward_list': [
            {
                # tg bot的token
                'token': tg_token,
                # 需要转发的群id
                'chat_id': '-1001666288867',
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
                # 不转发的qq号
                'blacklist': [
                    '123456789'
                ],
            },
        ],
    },
    'bind':[
        {
            'tg_group':'-123456',
            'qq_group':'12345',
            'bgm_id':[
                '1234',
                'kriaeth'
            ],
        }
    ]
}

LOGGING_LEVEL=logging.INFO # logger
