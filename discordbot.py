import discord
from discord.ext import commands,tasks
import asyncio
import re
import aiohttp
import urllib
import os
import math
import datetime
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="!")

token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print("開始")
    bot.ch = bot.get_channel(610766813533306880)
    bot.tao = bot.ch.guild.get_member(526620171658330112)
    bot.flag = False

    bot.session = aiohttp.ClientSession()

    bot.q_count = 0
    bot.s_count = 0
    await bot.ch.send("::t")
    check_last.start()

@bot.event
async def on_message(message):
    if message.content == "::t":
        if bot.flag == True:
            await quiz()
    if message.content == "!flg":
        bot.flag = not bot.flag
        
@tasks.loop(minutes=3)
async def check_last():
    tmp_timediff = datetime.datetime.now() - bot.ch.last_message.created_at
    last_message_time = tmp_timediff.total_seconds()
    
    if last_message_time > 300:
        await bot.ch.send("::t")

async def quiz():
    msg = ""
    
    def check(m):
        return m.author == bot.tao and m.embeds[0].description

    def end_check(m):
        l = ["残念","正解","時間切れ"]
        return m.author == bot.tao and any(i in m.embeds[0].description for i in l)

    msg = await bot.wait_for('message',check=check)

    while not msg.embeds[0].description.startswith("「"):
        msg = await bot.wait_for('message',check=check)

    s = msg.embeds[0].description
    s = re.search("「(.*)」の読み方をひらがなで答えなさい。",s)

    if s is None:
        return

    s = s.group(1)
    url = f"https://yoji.jitenon.jp/cat/search.php?getdata={urllib.parse.quote(s)}&search=part&page=1"
        
    async with bot.session.get(url) as resp:
        text = await resp.text()
        parsed = BeautifulSoup(text, "html.parser")
            
    result = re.search("「.*」（(.*)）の意味",str(parsed.title))
    await asyncio.sleep(5)

    if result:
        await bot.ch.send(result.group(1).replace("（","").replace("）",""))
    else:
        await bot.ch.send("わからない")

    ans_m = await bot.wait_for('message',check=end_check)
    bot.q_count += 1

    if ans_m.embeds[0].description.startswith("正解"):
        bot.s_count += 1
            
    n = math.floor((bot.s_count/bot.q_count)*100)
    await bot.change_presence(activity=discord.Game(name=f'{bot.q_count}問／{bot.s_count} 正解({n}%)'))
    await bot.ch.send("::t")
    
bot.run(token)
