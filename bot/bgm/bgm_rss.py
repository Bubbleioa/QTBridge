import asyncio
import feedparser

res = feedparser.parse('https://bgm.tv/feed/user/428864/timeline')
user_name = res['channel']['title'].strip('的时间胶囊')
for item in res.entries:
    print(user_name+' '+item['title'])