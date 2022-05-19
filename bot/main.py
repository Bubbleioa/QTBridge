"""main.py"""
import os,time
import asyncio
from config import config
from qq.bot import create_qq_bridge
from tg.tg_bot import create_telegram_bridge
from bgm.bgm_rss import create_bgm_rss


def create_bridge(group,loop):
    tg_rev_queue, tg_send_queue = \
    create_telegram_bridge(config['Telegram']['token'],group['tg_group'],group['tg_blacklist'],config['Telegram']['http_proxy'],loop)
    qq_rev_queue, qq_send_queue = \
    create_qq_bridge(config['QQ']['base_uri'],group['qq_group'],loop,group['qq_blacklist'])
    bgm_rev_queue = asyncio.Queue()
    for bgm_id in group['bgm_id']:
        create_bgm_rss(bgm_id,bgm_rev_queue,10,loop)
    
    async def qq_tg():
        while True:
            msg = await qq_rev_queue.get()
            await tg_send_queue.put(msg)
    async def tg_qq():
        while True:
            msg = await tg_rev_queue.get()
            await qq_send_queue.put(msg)
    async def bgm_qq_tg():
        while True:
            msg = await bgm_rev_queue.get()
            await qq_send_queue.put(msg)
            await tg_send_queue.put(msg)
    loop.create_task(qq_tg())
    loop.create_task(tg_qq())
    loop.create_task(bgm_qq_tg())

def main():
    """A dummy docstring."""

    # start after go-cqhttp, may use better method.
    if os.getenv('isdocker'):
        time.sleep(22)

    loop = asyncio.get_event_loop()
    for group in config['bind']:
        create_bridge(group,loop)
    loop.run_forever()

if __name__ == '__main__':
    main()
