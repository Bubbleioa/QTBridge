import logging
import os

tg_token = os.getenv('TG_BOT_TOKEN')
config = {
    'Telegram': {
        # tg使用的http代理（可选）
        'http_proxy': 'http://host.docker.internal:7890',
        'token': tg_token,
    },
    'QQ': {
        'base_uri': 'http://gocqhttp:5700/',
    },
    'bind':[
        {
            'tg_group':'-1001731004217',
            'qq_group':'780703469',
            'bgm_id':[
                '428864',
                'kriaeth',
                '488709',
                'fffeiya',
                '341379',
                '483226',
                'ttsuxx',
                'vishford',
                'gfzum',
                'limu_lingmeng'
            ],
            'tg_blacklist': [
                '123456789'
            ],
            'qq_blacklist': [
                2320711942
            ],
        }
    ]
}

LOGGING_LEVEL=logging.INFO # logger
