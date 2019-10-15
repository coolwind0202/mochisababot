'''
このコードは、TAOの::tを四字熟語のデータ込みで行うサンプルコードです。
データは同ディレクトリの trainig.json にあります。

Copyright (c) 2018 dischanet
Released under the MIT license
https://github.com/dischanet/mmo-discord-bot/blob/master/LICENSE
'''

import discord
import asyncio
import re
import json

client = discord.Client()

@client.event
async def on_ready():
    with open("training.json","r",encoding="utf-8") as raw_data:
        client.t_data = json.load(raw_data)
    client.t_ch = client.get_channel(597269336981504022) 
    await client.t_ch.send("::t")
    
def t_check(tao_msg):
    if not tao_msg.embeds or tao_msg.author.id != 526620171658330112:
        return 0 #埋め込みが無いか、TAOが送信していない
    if not tao_msg.embeds[0].description:
        return 0 #埋め込みに説明がない
    embed_content = tao_msg.embeds[0].description
    if embed_content.endswith("読み方をひらがなで答えなさい。"):
        return 2 #クイズそのもの
    else:
        tmp_words = ['正解','残念','時間切れ']
        return any(embed_content.startswith(word) for word in tmp_words) #結果

def get_key(key):
    tmp = [elem[1] for elem in client.t_data if elem[0] == key]
    if not tmp: return
    return tmp[0]

@client.event
async def on_message(message):
    if t_check(message) == 2: #TAOから問題が出題されたとき
        embed = message.embeds[0]
        quiz = re.search("「(.*)」の読み方をひらがなで答えなさい。",embed.description).group(1)
        
        await asyncio.sleep(5)
        await message.channel.send(str(get_key(quiz))) #漢字から読みのリストを検索する
        await client.wait_for("message",check=t_check)
        await message.channel.send("::t")

client.run('your token here')
