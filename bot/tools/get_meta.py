import re
from bs4 import BeautifulSoup
from .log import logger
import asyncio,aiohttp
pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配url模式

async def get_meta(text :str) -> list|None:
    urls = re.findall(pattern,text)
    if len(urls):
        session=aiohttp.ClientSession()
        async with session.get(urls[0]) as response:
            try:
                html = await response.text()
                soup = BeautifulSoup(html,'html.parser')
                title = soup.title
                description = soup.find_all(property='og:description')
                if(len(description)==0):
                    description = soup.find_all(name="description")
                if(len(description)==0):
                    description = soup.find_all(itemprop="description")
                image = soup.find_all(property='og:image')
                if len(description)==0 or len(image)==0:
                    return None
                if image[0]['content'][0:4] != 'http':
                    base_url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
                    image[0]['content'] = base_url[0] + image[0]['content']
                return [title.text,description[0]['content'],image[0]['content']]
            except:
                logger.warn("faild resolve %s",text)
                return None     
    else:
        return None

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_meta('https://www.bilibili.com/video/BV1w34y1a71G'))
    loop.close()