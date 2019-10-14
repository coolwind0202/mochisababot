'''
このソースコードは、TAOの4択クイズをBOTで行うためのものです。

正解／不正解するたびに、問題とその答えの組み合わせを辞書に格納していきます。ファイルやデータベースへの書き込みは各自でプログラムしてください。
'''

import discord
import asyncio
import re

client = discord.Client()

@client.event
async def on_ready():
    client.ch = client.get_channel(チャンネルID)
    client.already_quiz = {}

    await client.ch.send("::q")

@client.event
async def on_message(message):
    me = message.guild.me
    tao = client.ch.guild.get_member(526620171658330112)

    if message.content == "::q" and message.author == me:
        def quiz_check(tao_msg):
            if tao_msg.author != tao:
                return 0
            elif not tao_msg.embeds and not tao_msg.embeds[0].description:
                return 0
            elif tao_msg.embeds[0].author.name != "Quiz":
                return 0
            return 1

        def ans_check(tao_msg):
            if tao_msg.author != tao:
                return 0
            elif not tao_msg.embeds and not tao_msg.embeds[0].description:
                return 0
            return 1
        
        try:
            quiz_msg = await client.wait_for("message",timeout=100,check=quiz_check)
        except asyncio.TimeoutError:
            await message.channel.send("::q")
            return

        quiz,*choice = quiz_msg.embeds[0].description.split("\n")
        true_choice = [word[4:] for word in choice]

        answer = client.already_quiz.get(quiz)
        await asyncio.sleep(7)

        react = 1
        if answer:
            react += true_choice.index(answer)        
        await quiz_msg.add_reaction(str(react).encode().decode('unicode-escape')+"\u20e3")

        try:
            ans_msg = await client.wait_for("message",check=ans_check)
        except asyncio.TimeoutError:
            await message.channel.send("::q")
            return

        tmp_embed = ans_msg.embeds[0].description
        if answer is None and not tmp_embed.startswith("時間切れ"):
            if tmp_embed.startswith("残念"):
                tmp = re.search("残念！正解は「(.*)」だ。",tmp_embed).group(1)
            elif tmp_embed.startswith("正解"):
                tmp = true_choice[0]
            client.already_quiz[quiz] = tmp

        await message.channel.send("::q")


client.run('your token here')
