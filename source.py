import discord
from discord.ext import commands
import asyncio
import feedparser
import mw_api_client as mw
import urllib.request, urllib.error, sys
import json
import urllib

bot = commands.Bot(command_prefix='jsw:')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def Changes():
    feed = feedparser.parse('https://ja.scratch-wiki.info/w/api.php?hidebots=1&days=1&limit=5&hidecategorization=1&action=feedrecentchanges&feedformat=atom')
    for x in feed.entries:
        embed = discord.Embed(title="JPScratchWikiの最近の更新", description="Japanese Scratch Wikiでの最近の更新をお知らせします。", color=0x824880)
        embed.add_field(name="ページ:", value=(x.title), inline=False)
        embed.add_field(name="日時:", value=(x.updated), inline=False)
        embed.add_field(name="編集者:", value=(x.author), inline=False)
        embed.add_field(name="リンク:", value=(x.links[0].href), inline=False)
        await bot.say(embed=embed)

@bot.command()
async def statistics():
    try:
        r = requests.get("https://ja.scratch-wiki.info/w/images/2/2a/InterwikiBot_GA_Pageviews.png", stream=True)
        with open("pege.png", 'wb') as f:
            f.write(r.content)
            await bot.say("ページビュー:")
            await bot.send_file(msg.message.channel,"page.png")
        r = requests.get("https://ja.scratch-wiki.info/w/images/2/26/InterwikiBot_GA_Sessions.png", stream=True)
        with open("session.png", 'wb') as f:
            f.write(r.content)
            await bot.say("セッション:")
            await bot.send_file(msg.message.channel,"seession.png")
            await bot.say("詳しく:https://ja.scratch-wiki.info/wiki/Japanese Scratch-Wiki:統計情報")

@bot.command(pass_context = True)
async def category(msg):
    wp = mw.Wiki("https://ja.scratch-wiki.info/w/api.php")
    wp.login("T-taku@T-takumini", "pass")
    str1 = msg.message.content.replace("jsw:category ", "")
    for page in wp.category(str1).categorymembers():
        print(page.title)
        embed = discord.Embed(title="カテゴリ" + str1 + "に含まれる記事", description=" ", color=0xffa500)
        embed.add_field(name="ページ:", value=(page.title), inline=False)
        await bot.say(embed=embed)

@bot.command(pass_context = True)
async def Editcount(msg):
    str1 = msg.message.content.replace("jsw:Editcount ", "")
    username = str1
    print(username)
    resp = urllib.request.urlopen("https://ja.scratch-wiki.info/w/api.php?action=query&list=allusers&aufrom=" + username + "&auprop=editcount&format=json").read()
    resp = json.loads(resp)
    name = resp["query"]["allusers"][0]["name"]
    kaisuu = resp["query"]["allusers"][0]["editcount"]
    if name != username:
        await bot.say("取得できませんでした。以下を確認してください:ユーザー名 ユーザー名の頭文字(大文字、小文字など)")
    else:
        embed = discord.Embed(title="ユーザーの編集回数", description=" ", color=0x7fff00)
        embed.add_field(name="編集者:", value=(str(name)), inline=False)
        embed.add_field(name="編集回数(およそ):" , value=(str(kaisuu) + "回"), inline=False)
        embed.add_field(name="詳しく:", value=("https://ja.scratch-wiki.info/wiki/特別:編集回数/" + username), inline=False)
        await bot.say(embed=embed)

bot.run("token")
