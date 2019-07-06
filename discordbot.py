import discord

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    if client.user in message.mentions: # 話しかけられたかの判定
        reply =  message.guild.get_member(285999013310889995).mention # 返信メッセージの作成
        await message.channel.send("おしりの"+reply) # 返信メッセージを送信
    if message.content.startswith('プリコネ'):
        await message.channel.send('ブヒブヒ')
    if message.content.startswith('プリンセスコネクト'):
        await message.channel.send('Re:Dive！')
    if message.content.startswith('君の名は'):
        await message.channel.send('三葉の口噛み酒飲みたい')
    if message.content.startswith('ゆうと'):
        await message.channel.send('大好き♡')

client.run("NTk2ODkwMDgyNTkwNDU3ODU4.XSAHag.OqmhJ_QIqTIaWQ2R7uZwbHxRW0E")
