import os
import json
import asyncio
import base64
import aiohttp
import urllib
from tools.log import logger


def create_telegram_bridge(token,chat_id,blacklist=None,http_proxy=None,loop=None,is_test=False):
    if blacklist is None:
        blacklist = []
    if not loop:
        loop = asyncio.get_event_loop()
    receive_queue = asyncio.Queue()
    send_queue = asyncio.Queue()

    async def get_msg():
        session = aiohttp.ClientSession()
        logger.info("try to get %s",f'https://api.telegram.org/bot{token}/getUpdates?timeout=6')
        res = await session.get(f'https://api.telegram.org/bot{token}/getUpdates?timeout=6',proxy=http_proxy)
        res = await res.read()
        res = json.loads(res.decode())
        last_id = None
        while True:
            await asyncio.sleep(0.5)
            if len(res['result']) > 0:
                last_id = res['result'][-1]['update_id'] + 1
            api_url = f'https://api.telegram.org/bot{token}/getUpdates?timeout=6'
            if last_id:
                api_url+=f'&offset={last_id}'
            try:
                res = await session.get(api_url,proxy=http_proxy)
            except:
                logger.warn("Network has something wrong, retrying...")
                await asyncio.sleep(1)
                continue
            res = await res.read()
            res = json.loads(res.decode())
            for msg in res['result']:
                if 'message' not in msg:
                    continue
                msg = msg['message']
                if 'text' in msg and msg['text'][0]=='/':
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
                final_msg = f"{author}: "
                if 'text' not in msg:
                    if 'photo' in msg:
                        try:
                            if 'caption' in msg and (msg['caption'][0] == '!' or msg['caption'][0] == '！'):
                                continue
                            photo = msg['photo'][0]
                            rep = await session.get(f'https://api.telegram.org/bot{token}/getFile?file_id={photo["file_id"]}',proxy=http_proxy)
                            rep = await rep.read()
                            rep = json.loads(rep.decode())
                            rep = await session.get(f'https://api.telegram.org/file/bot{token}/{rep["result"]["file_path"]}',proxy=http_proxy)
                            img = await rep.content.read()
                            b64_str = base64.b64encode(img)
                            final_msg += f'[CQ:image,file={b64_str}]'
                            if 'caption' in msg:
                                final_msg += msg['caption']
                        except Exception as e:
                            logger.warn(e)
                            logger.warn("Get image failed")
                            continue
                    else :
                        continue
                if 'text' in msg:
                    final_msg += f"{msg['text']}"
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
        while True:
            try:
                res = await session.get(url + '/getMe', proxy=http_proxy)
            except:
                logger.warn("Network has something wrong, retrying...")
                await asyncio.sleep(1)
                continue
            break
        res = await res.read()
        res = res.decode()  # type: str
        res = res.strip()
        while True:
            message = await send_queue.get()
            message = urllib.parse.quote(message)
            while True:
                try:
                    res = await session.get(
                        url + '/sendMessage?chat_id=' + chat_id + "&text=" + message,
                        proxy=http_proxy
                    )
                except:
                    logger.warn("Network has something wrong, retrying...")
                    await asyncio.sleep(1)
                    continue
                break
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