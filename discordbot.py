import discord
from discord.ext import commands,tasks
import asyncio
import re
import aiohttp
import urllib
import os
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="!")

token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_ready():
    print("開始")
    bot.ch = bot.get_channel(603442982057934854)
    bot.session = aiohttp.ClientSession()
    q.start()

@tasks.loop(seconds=15)
async def q():
    
    def check(m):
        s = m.embeds[0].description
        return m.author.id==526620171658330112 and (not s.startswith("時間切れ") and not s.startswith("正解だ") and not s.startswith("残念"))

    await bot.ch.send("::t")
    msg = await bot.wait_for('message',check=check)

    if msg.embeds:

        s = msg.embeds[0].description
        s = re.search("「(.*)」の読み方をひらがなで答えなさい。",s)
        
        if not s:
            return
        s = s.group(1)

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
        
bot.run(token)
