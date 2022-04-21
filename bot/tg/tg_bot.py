import os
import json
import asyncio
import aiohttp
import urllib
# from tools.log import logger


def create_telegram_bridge(token,chat_id,blacklist=None,http_proxy=None,loop=None,is_test=False):
    if blacklist is None:
        blacklist = []
    if not loop:
        loop = asyncio.get_event_loop()
    receive_queue = asyncio.Queue()
    send_queue = asyncio.Queue()

    async def get_msg():
        session = aiohttp.ClientSession()
        res = await session.get(f'https://api.telegram.org/bot{token}/getUpdates?timeout=6',proxy=http_proxy)
        res = await res.read()
        res = json.loads(res.decode())
        print(res)
        last_id = None
        while True:
            await asyncio.sleep(0.3)
            if len(res['result']) > 0:
                last_id = res['result'][-1]['update_id'] + 1
            api_url = f'https://api.telegram.org/bot{token}/getUpdates?timeout=6'
            if last_id:
                api_url+=f'&offset={last_id}'
            res = await session.get(api_url,proxy=http_proxy)
            res = await res.read()
            print(res)
            res = json.loads(res.decode())
            for msg in res['result']:
                if 'message' not in msg:
                    continue
                msg = msg['message']
                if msg['text'][0]=='/':
                    continue
                if str(msg['from']['id']) in blacklist:
                    continue
                if msg.get('chat') and msg['chat'].get('id') \
                    and msg['chat']['id'] != int(chat_id):
                    continue
                if 'last_name' in msg['from']:
                    author = f"{msg['from']['first_name']} {msg['from']['last_name']}"
                else:
                    author = msg['from']['first_name']
                # logger.info(f"receive message from telegram group:{chat_id}")
                # logger.info(json.dumps(msg, indent='  '))
                if 'text' not in msg:
                    continue
                final_msg = f"{author}: {msg['text']}"
                await receive_queue.put(final_msg)
                if len(res['result']) > 0:
                    last_id = res['result'][-1]['update_id'] + 1
                if is_test:
                    await send_test_mock(final_msg)
    async def send_test_mock(msg):
        msg = urllib.parse.quote(msg)
        session = aiohttp.ClientSession()
        url = f'https://api.telegram.org/bot{token}'
        res = await session.get(url + '/getMe', proxy=http_proxy)
        res = await res.read()
        res = res.decode()  # type: str
        res = res.strip()
        print("getMe:",res)
        res = await session.get(
            url + '/sendMessage?chat_id=' + chat_id + "&text=" + msg,
            proxy=http_proxy
        )
        res = await res.read()
        res = json.loads(res.decode())
        print(res)
        await session.close()
    async def send_msg():
        session = aiohttp.ClientSession()
        url = f'https://api.telegram.org/bot{token}'
        res = await session.get(url + '/getMe', proxy=http_proxy)
        res = await res.read()
        res = res.decode()  # type: str
        res = res.strip()
        while True:
            message = await send_queue.get()
            message = urllib.parse.quote(message)
            res = await session.get(
                url + '/sendMessage?chat_id=' + chat_id + "&text=" + message,
                proxy=http_proxy
            )
            res = await res.read()
            res = json.loads(res.decode())
            await asyncio.sleep(0.3)
            # logger.info(res)

    loop.create_task(get_msg())
    loop.create_task(send_msg())

    return receive_queue, send_queue



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    config=''
    create_telegram_bridge(os.getenv('TG_BOT_TOKEN'),'-1001666288867','','http://172.31.64.1:7890/',loop,is_test=True)
    loop.run_forever()