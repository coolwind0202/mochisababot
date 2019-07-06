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

client.run("NTk2ODkwMDgyNTkwNDU3ODU4.XSAHag.OqmhJ_QIqTIaWQ2R7uZwbHxRW0E")