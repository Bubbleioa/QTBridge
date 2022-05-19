import asyncio
import aiohttp
import json

from tools.log import logger
from tools.get_meta import get_meta

def create_qq_bridge(base_uri, group_id, loop, blacklist=[]):
    qq_receive_queue = asyncio.Queue()    
    qq_send_queue = asyncio.Queue()
    print(blacklist)
    async def get_msg():
        async with aiohttp.ClientSession() as session:
            
            last_msg_id = 0
            #get last message id
            async with session.get(f'{base_uri}'
            + f'get_group_msg_history?group_id={group_id}') as resp:
                last_msg_id = json.loads(await resp.text())['data']['messages'][-1]['message_id']

            #use sleep(0.3) to do the async
            while True:
                async with session.get(f'{base_uri}'
                + f'get_group_msg_history?group_id={group_id}') as response:
                    text = await response.text()
                    messages = {}
                    try:
                        messages = json.loads(text)['data']['messages']
                    except:
                        logger.warn("NoneType! Retrying... text is %s",text)
                        await asyncio.sleep(1)
                        continue
                    last_msg = messages[-1]

                    # if receive new meesage               
                    if last_msg['message_id'] != last_msg_id:
                        last_msg_id = last_msg['message_id']
                        qqid = last_msg['sender']['user_id']
                        # blacklist
                        if qqid in blacklist:
                            continue

                        # get name in group
                        async with session.get(f'{base_uri}'
                        + f'get_group_member_info?group_id={group_id}&user_id={qqid}') as res:
                            data = json.loads(await res.text())['data']
                            card_name = data['card']

                            msg = last_msg['message']
                            await qq_receive_queue.put(f"{card_name}: {msg}")

                        # print(msg) log
                    
                    await asyncio.sleep(0.3)

    async def send_msg():
        async with aiohttp.ClientSession() as session:
            while True:
                    message = await qq_send_queue.get()
                    res = await get_meta(message)
                    if res != None:
                        message += '\n' + res[0] + '\n' + res[1] + '\n' + f'[CQ:image,file={res[2]}]'
                    async with session.get(f'{base_uri}'
                    + f'send_group_msg?group_id={group_id}&message={message}') as response:
                        pass #log

    loop.create_task(get_msg())
    loop.create_task(send_msg())

    return qq_receive_queue, qq_send_queue

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    create_qq_bridge('http://127.0.0.1:5700/','747324697',loop)
    loop.run_forever()
