import logging
import os

tg_token = os.getenv('TG_BOT_TOKEN')
config = {
    'Telegram': {
        # tg使用的http代理（可选）
        'http_proxy': 'http://172.21.128.1:7890/',
        'token': tg_token,
    },
    'QQ': {
        'base_uri': 'http://127.0.0.1:5700/',
    },
    'bind':[
        {
            'tg_group':'-1001666288867',
            'qq_group':'780703469',
            'bgm_id':[
                '428864',
                'kriaeth'
            ],
            'tg_blacklist': [
                '123456789'
            ],
            'qq_blacklist': [
                '123456789'
            ],
        }
    ]
}

LOGGING_LEVEL=logging.INFO # logger
