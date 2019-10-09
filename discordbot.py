import discord
from discord.ext import commands,tasks
import asyncio
import re
import aiohttp
import urllib
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="!")

TOKEN = "NTk2ODkwMDgyNTkwNDU3ODU4.XZ2m5g.6sCjBfihE0W8W5qiEq6Q7u26YKk"
#TOKEN = "NTkwMTM4NTE5NjUwMDQxODc2.XZybdw.Usd-s0sSYefjkH24yy077Xbk22Y"

@bot.event
async def on_ready():
    print("開始")
    bot.ch = bot.get_channel(603442982057934854)
    bot.session = aiohttp.ClientSession()
    q.start()

@tasks.loop(seconds=15)
async def q():

    await bot.ch.send("::t")
    msg = await bot.wait_for('message',check=lambda m:m.author.id==526620171658330112)

    if msg.embeds:

        s = msg.embeds[0].description
        s = re.search("「(.*)」の読み方をひらがなで答えなさい。",s).group(1)

        url = f"https://dictionary.goo.ne.jp/word/{urllib.parse.quote(s)}/"
        
        async with bot.session.get(url) as resp:
            text = await resp.text()
            parsed = BeautifulSoup(text, "html.parser")

        result = re.search(".*\((.*)\)の意味・使い方 - 四字熟語一覧 - goo辞書",str(parsed.title))
        
        await asyncio.sleep(5)

        if result:
            await bot.ch.send(result.group(1))
        else:
            await bot.ch.send("わからない")
        

bot.run(TOKEN)
