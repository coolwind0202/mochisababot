'''
このソースコードは、TAOの ::atk を自動で行うBOTのためのサンプルコードです。

注意点として、
・レベル差が激しくリセットを行った場合
・チャンネルが使用不可だった場合
にはそれ以降 ::atk の処理を行わなくなります。はじめはレベルの低いチャンネルから使用するようにしてください。
'''

import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():

    client.send_flag = True #チャンネルに送信できない場合、それ以降処理しないフラグ。
    client.ch = client.get_channel(チャンネルID)
    await client.ch.send("::atk")

@client.event
async def on_message(message):

    if message.channel != client.ch:
        return

    tao = client.ch.guild.get_member(526620171658330112)

    if message.author == tao:

        if not client.send_flag:
            return

        def author_tao_check(msg):
            return msg.author == tao

        if not message.embeds:

            if "ダメージ" in message.content:
                #戦闘中の判定
                if "HP" in message.content:
                    #まだ倒し切れていない判定
                    if message.guild.me.display_name in message.content:
                        #そのメッセージ対象がPETでない判定
                        await asyncio.sleep(10)
                        await message.channel.send("::atk")

            elif "攻撃失敗" in message.content:
                print("攻撃に失敗しました。")
                await asyncio.sleep(10)
                await message.channel.send("::atk")
                #再度攻撃

            elif "ログイン失敗" in message.content:
                print("ログインに失敗しました。")
                await asyncio.sleep(10)
                await message.channel.send("::login")
                #再度ログイン

            elif "リセット失敗" in message.content:
                print("リセットに失敗しました。")
                await asyncio.sleep(10)
                await message.channel.send("::reset")
                #再度リセット

        else:
            embed = message.embeds[0]

            def battle_check(m):
                #そのメッセージが戦闘開始のメッセージであるかを判定する。
                if not m.embeds:
                    return 0
                if not m.embeds[0].title:
                    return 0

                return "待ち構えている" in m.embeds[0].title

            if battle_check(message):
                await message.channel.send("::atk")
                return

            if embed.description:
                if embed.description.startswith("このチャンネルは"):
                    print("このチャンネルは使用できません。")
                    client.send_flag = False
            
                elif "::reset" in embed.description:
                    print("リセットします。")
                    await message.channel.send("::reset")
                    client.send_flag = False

                elif "::login" in embed.description:
                    await message.channel.send("::login")
                    await client.wait_for("message",check=author_tao_check)
                    await message.channel.send("::atk")

client.run('your token here')
