import discord
from discord.ext import commands,tasks
import asyncio
import re
import aiohttp
import urllib
import os
import math
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="!")

token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print("開始")
    bot.ch = bot.get_channel(603442982057934854)
    bot.tao = bot.ch.guild.get_member(526620171658330112)

    bot.session = aiohttp.ClientSession()
    bot.task = bot.loop.create_task(quiz())

    bot.q_count = 0
    bot.s_count = 0
    
    change.start()

async def quiz():
    msg = ""
    
    def check(m):
        return m.author == bot.tao and m.embeds[0].description

    def end_check(m):
        l = ["残念","正解","時間切れ"]
        return m.author == bot.tao and any(i in m.embeds[0].description for i in l)

    while not bot.is_closed():
        await bot.ch.send("::t")
        msg = await bot.wait_for('message',check=check)

        while not msg.embeds[0].description.startswith("「"):
            msg = await bot.wait_for('message',check=check)

        s = msg.embeds[0].description
        s = re.search("「(.*)」の読み方をひらがなで答えなさい。",s)

        if s is None:
            continue

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

        ans_m = await bot.wait_for('message',check=end_check)
        bot.q_count += 1

        if ans_m.embeds[0].description.startswith("正解"):
            bot.s_count += 1

@tasks.loop(seconds=30)
async def change():
    n = math.floor((bot.s_count/bot.q_count)*100)
    print(n)
    await bot.change_presence(activity=discord.Game(name='{bot.q_count}問／{bot.s_count} 正解({n}%)'))
            
bot.run(token)
