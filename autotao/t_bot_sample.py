'''
このソースコードはTAOの四字熟語クイズBOTのサンプルコードです。
はじめは一切の回答がNoneになりますが、もし既に知っている単語があればそれを送信します。

なお、登録した単語は全て辞書に保存する仕組みです。ファイルおよびデータベースへの書き込みは各自でプログラムしてください。
'''

import discord
import asyncio
import re

client = discord.Client()

@client.event
async def on_ready():
    client.ch = client.get_channel(610766813533306880)
    client.words_dict = {}

    await client.ch.send("::t")

@client.event
async def on_message(message):
    me = message.guild.me
    tao = client.ch.guild.get_member(526620171658330112)

    if message.content == "::t" and message.author == me:
        def quiz_check(tao_msg):
            if not tao_msg.embeds and not tao_msg.embeds[0].author:
                return 0
            elif tao_msg.author != tao:
                return 0

            e_title = tao_msg.embeds[0].author.name
            return e_title == "Training"

        def ans_check(tao_msg):
            if not tao_msg.embeds and not tao_msg.embeds[0].description:
                return 0
            elif tao_msg.author != tao:
                return 0

            e_content = tao_msg.embeds[0].description
            result_text_list = ["正解","残念","時間切れ"]

            return any(e_content.startswith(result) for result in result_text_list)

        quiz_msg = await client.wait_for("message",check=quiz_check)

        s_1 = quiz_msg.embeds[0].description
        quiz_content = re.search("「(.*)」の読み方をひらがなで答えなさい。",s_1).group(1)
        get_word = client.words_dict.get(quiz_content)

        await asyncio.sleep(5)
        await message.channel.send(str(get_word))

        ans_msg = await client.wait_for('message',check=ans_check)

        s_2 = ans_msg.embeds[0].description

        if s_2.startswith("残念"):
            ans_content = re.search("残念！正解は「(.*)」だ。",s_2).group(1)
            client.words_dict[quiz_content] = ans_content
        
        await asyncio.sleep(5)
        await message.channel.send("::t")

client.run('your token here')
