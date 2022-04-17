"""main.py"""
# pylint: disable=invalid-name 
import asyncio
import aiohttp

def qq(config, loop):
    """A dummy docstring."""
    async def get_time():
        async with aiohttp.ClientSession() as session:
            async with session.get("http://worldtimeapi.org/api/timezone/Asia/Hong_Kong") as res:
                await asyncio.sleep(5)
                r = await res.text()
                print(r)
    
    loop.create_task(get_time())

def tg(config, loop):
    """A dummy docstring."""
    async def get_wt():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://wttr.in/") as res:
                r = await res.text()
                print(r)
                await asyncio.sleep(5)
    loop.create_task(get_wt())

def main():
    """A dummy docstring."""
    loop = asyncio.get_event_loop()
    config=''
    qq(config, loop)
    tg(config, loop)
    loop.run_forever()

if __name__ == '__main__':
    main()
