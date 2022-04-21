'''create a bgm rss tracer'''
import asyncio
import aiohttp
import feedparser
from tools.log import logger


def create_bgm_rss(user_id,receive_queue,interval=10,loop=None):
    '''create a bgm rss tracer'''
    if not loop:
        loop = asyncio.get_event_loop()
    rss_url=f'https://bgm.tv/feed/user/{user_id}/timeline'

    async def update_rss():
        session = aiohttp.ClientSession()
        res = await session.get(rss_url)
        res = await res.text()
        res = feedparser.parse(res)
        content = res.entries
        while True:
            await asyncio.sleep(interval)
            res = await session.get(rss_url)
            res = await res.text()
            res = feedparser.parse(res)
            if content[0]==res.entries[0]:
                continue
            user_name = res['channel']['title'].strip('的时间胶囊')
            for item in res.entries:
                if item in content:
                    continue
                logger.info(user_name+' '+item['title'])
                await receive_queue.put(user_name+' '+item['title'])
            content = res.entries

    loop.create_task(update_rss())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    create_bgm_rss('428864',loop)
    loop.run_forever()
    