import asyncio
import aiohttp
import json


def create_qq_bridge(loop):
    qq_receive_queue = asyncio.Queue()    
    qq_send_queue = asyncio.Queue()

    async def get_msg():
        async with aiohttp.ClientSession() as session:
            
            last_msg_id = 0
            #get last message id
            async with session.get('http://127.0.0.1:5700/'
            + 'get_group_msg_history?group_id=747324697') as resp:
                last_msg_id = json.loads(await resp.text())['data']['messages'][-1]['message_id']

            #use sleep(0.3) to do the async
            while True:
                async with session.get('http://127.0.0.1:5700/'
                + 'get_group_msg_history?group_id=747324697') as response:
                    text = await response.text()
                    messages = json.loads(text)['data']['messages']
                    last_msg = messages[-1]
                    
                    if last_msg['message_id'] != last_msg_id:
                        msg = last_msg['message']
                        author = last_msg['sender']['nickname']
                        # print(msg) log
                        await qq_receive_queue.put(f"{author}: {msg}")
                        last_msg_id = last_msg['message_id']
                    
                    await asyncio.sleep(0.3)

    async def send_msg():
        async with aiohttp.ClientSession() as session:
            while True:
                    message = await qq_send_queue.get()
                    async with session.get('http://127.0.0.1:5700/'
                    + f'send_group_msg?group_id=747324697&message={message}') as response:
                        pass #log

    loop.create_task(get_msg())
    loop.create_task(send_msg())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    create_qq_bridge(loop)
    loop.run_forever()
