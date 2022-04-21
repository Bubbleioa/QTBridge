import logging
import os

tg_token = os.getenv('TG_BOT_TOKEN')
config = {
    'Telegram': {
        # tg使用的http代理（可选）
        'http_proxy': 'http://127.0.0.1:7890/',
        'token': tg_token,
    },
    'QQ': {
        'base_uri': 'http://127.0.0.1:5700',
    },
    'bind':[
        {
            'tg_group':'-123456',
            'qq_group':'747324697',
            'bgm_id':[
                '1234',
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
