import discord
from discord.ext import commands,tasks
import asyncio
import re
import aiohttp
import urllib
import os
import math
import datetime
import json
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="!")

token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print("開始")
    bot.ch = bot.get_channel(610766813533306880)
    bot.tao = bot.ch.guild.get_member(526620171658330112)
    bot.flag = True
    bot.true_flag = True
    bot.bad_word = {}
    bot.stop = False
    
    with open('word_list.json','r') as f:
        bot.already_word = json.load(f)

    bot.session = aiohttp.ClientSession()

    bot.q_count = 0
    bot.s_count = 0
    await bot.ch.send("::t")
    check_last.start()

@bot.event
async def on_message(message):
    if message.content == "::t":
        timediff =  datetime.datetime.now() - message.created_at
        
        if timediff.total_seconds() > 300:
            return
        
        if bot.true_flag == True:
            # もしbotのクイズ機能が拒否されていなければ
            if bot.flag == True and message.author == message.guild.me:
                # botの再開が拒否されていなければ（再開すべきなら）
                await quiz(True)
            else:
                # botを再開すべきでないなら
                await quiz(false)
            
    if message.content == "!flg": #flgはbotの再開を阻止する
        bot.flag = not bot.flag
        await bot.ch.send(f"{not bot.flag} to {bot.flag}")
    if message.content == "!sw": # swはbotの回答そのものを阻止する
        bot.true_flag = not bot.true_flag
        await bot.ch.send(f"{not bot.true_flag} to {bot.true_flag}")
    if message.content == "!log": # 全回答ログを表示
        print(bot.already_word)
    if message.content == "!bad_word": # 全不正解ログを表示
        print(bot.bad_word)
        
@tasks.loop(minutes=3)
async def check_last():
    
    tmp_timediff = datetime.datetime.now() - bot.ch.last_message.created_at
    last_message_time = tmp_timediff.total_seconds()
    
    if last_message_time > 300:
        # もし最後のメッセージから5分以上経過していたら復帰する
        if bot.ch.last_message.content != "::t":
            await bot.ch.send("::t") 
            print("復帰")


async def quiz(send_flag):
    msg = ""
    
    def check(m):
        return m.author == bot.tao and m.embeds
        # TAOによる埋め込みありの投稿か確認する

    def end_check(m):
        l = ["残念","正解","時間切れ"]
        return m.author == bot.tao and m.embeds and any(i in m.embeds[0].description for i in l) 
        # 1問の終了の確認

    msg = await bot.wait_for('message',check=check)

    while not msg.embeds[0].description.startswith("「"):
        msg = await bot.wait_for('message',check=check)

    s = msg.embeds[0].description
    s = re.search("「(.*)」の読み方をひらがなで答えなさい。",s)

    if s is None: # 内容が異なった場合は無視
        return

    s = s.group(1)

    if s not in bot.already_word.keys():
        # まだその単語を回答していなければ接続する
        url = f"https://yoji.jitenon.jp/cat/search.php?getdata={urllib.parse.quote(s)}&search=part&page=1"
        
        async with bot.session.get(url) as resp:
            text = await resp.text()
            parsed = BeautifulSoup(text, "html.parser")
            
        result = re.search("「.*」（(.*)）の意味",str(parsed.title)) #タイトルから読みを抽出
 
        if result:
            reply = result.group(1).replace("（","").replace("）","")
        else:
            reply = "わからない"
            
    else:
        reply = bot.already_word[s] # 既に回答していたら答えにはそれを使う
        
    await asyncio.sleep(10)    
    await bot.ch.send(reply) # 答えを送信

    ans_m = await bot.wait_for('message',check=end_check)
    bot.q_count += 1 # 総問題数カウント

    if ans_m.embeds[0].description.startswith("正解"):
        bot.s_count += 1 # 正解カウント
        if s not in bot.already_word.keys():
            bot.already_word[s] = reply
            # 辞書追記
            
    elif ans_m.embeds[0].description.startswith("残念"):  
        bot.bad_word[s] = bot.already_word[s] = re.search("残念！正解は「(.*)」だ。",ans_m.embeds[0].description).group(1)
        # 不正解辞書追記
            
    n = math.floor((bot.s_count/bot.q_count)*100)
    await bot.change_presence(activity=discord.Game(name=f'{bot.q_count}問／{bot.s_count} 正解({n}%)'))
    # 正解率反映

    if send_flag == True:
        # 再開すべきなら
        await bot.ch.send("::t")
        # 再開処理
    
bot.run(token)
