import random
import numpy as np
from random import choice, randint
import os
import math
import requests
from bs4 import BeautifulSoup
import botFunctions
from botFunctions import getZmena, gymso, newOnGymso, getJokeTxt, getFact, wolframQuery, makeSuggestion, getLastInstaPost
import praw
import prawcore
import ksoftapi
import re
import bdbf
from bdbf import spamProtection, embed, hasLink
import asyncio
import discord
import pickle
import pkg_resources
from prettytable import PrettyTable
import commands
import botGames
import time

heroku = os.environ.get("isHeroku", False)
if not heroku:
	with open("C:\\Users\\alber\\OneDrive\\Plocha\\discordBotSecrets.txt", "r") as f:
		commands.kclient = eval(f.readline())
		token = eval(f.readline())
		commands.reddit = eval(f.readline())
		botFunctions.githubToken = eval(f.readline())
else:
	commands.kclient = ksoftapi.Client(os.environ.get("ksoft_token", None))

	commands.reddit = praw.Reddit(client_id = os.environ.get("reddit_client_id", None),
						client_secret = os.environ.get("reddit_client_secret", None),
						user_agent = os.environ.get("reddit_user_agent", None))

	token = os.environ.get('TOKEN', None)

botId = 540563812890443794
#84032 permissions int
#https://discordapp.com/oauth2/authorize?client_id=540563812890443794&scope=bot&permissions=8




client = discord.Client()

botGames.client = client

bdbf.commands.commandPrefix = "~"
bdbf.options.embedFooter= {
                "text": "Powered by Bertik23",
                "icon_url": "https://cdn.discordapp.com/avatars/452478521755828224/4cfdbde44582fe6ad05383171ac1b051.png"
                }
bdbf.options.embedColor = (37, 217, 55)

bdbf.options.botName = "TheBot"




klubik, obecne, choco_afroAnouncements = None,None, None

@client.event # event decorator/wrapper
async def on_ready():
	global klubik, obecne, choco_afroAnouncements
	print(f"We have logged in as {client.user}")
	klubik = await client.fetch_guild(697015129199607839)
	obecne = await client.fetch_channel(697015129199607843)
	choco_afroAnouncements = await client.fetch_channel(756497789424369737)
	print(klubik, obecne, choco_afroAnouncements)

	client.loop.create_task(checkWebsites())
	
	#newRolePerms = discord.Permissions(administrator=True)
	#newRole = await klubik.create_role(permissions=newRolePerms,color=discord.Color.from_rgb(0,255,0),name="Bůh 2.0")
	#bertiksMessage = await obecne.fetch_message(746658597655805954)
	#bertik = bertiksMessage.author
	#await bertik.add_roles(discord.Object(newRole.id))

@client.event
async def on_message(message):
	global klubik, obecne
	print(f"{message.channel} ({message.channel.id}): {message.author}: {message.author.name}: {message.content}")
		#print("on_msg", obecne, klubik)
	#await spamProtection(message, 5, f"{message.author.mention} nespamuj tady!", spamDelValue = 10)#, spamDelWarnMsg = f"{message.author.mention} další zprávy už ti smažu!")

	for i in ["hi","dobrý den","brý den","čau","ahoj", "zdravíčko", "tě péro", "těpéro", "zdárek párek","tě guli", "čus", "olá", "ola", "guten tag"]:
		if re.search(f"(\W|^){i}(\W|$)", message.content, re.I) and not message.author.bot:
			await message.channel.send(f"Hello {message.author.mention}")
			break

	if "kdy" in message.content.lower() and "aktualizace" in message.content.lower():
		await message.channel.send("Kdo ví")

	if (re.search("(\W|^)a+da+m(\W|$)", message.content, re.I)) and not message.author.bot:
		await message.channel.send(f"A{randint(0,20)*'a'}d{randint(1,20)*'a'}m {choice(['je gay','neumí olí','už nevytírá anály','is trajin to solf da rubix kjub','was trajin to olín',''])}")

	if (re.search("(\W|^)ji+ří+(\W|$)", message.content, re.I)) and not message.author.bot:
		await message.channel.send(f"Jiří {choice([' je buzík',' nic neumí','is FUCKING NORMIEEE REEEEEEEEEEEEEEEEEEEEEE'])}")

	if "fortnite" in message.content.lower():
		await message.delete()

	if (re.search("thebot", message.content, re.I) or client.user.mentioned_in(message)) and not message.author.bot:
		await message.channel.send(choice(["Slyšel jsem snad moje jméno?",f"{message.author.mention} ty ses opovážil vyslovit moje jméno?","Ještě jednou tu zazní moje jméno a uvidíte.",f"Chceš do držky {message.author.mention}?",f"Tak to je naposledy co jste {message.author.mention} viděli."]))

	if message.tts and not message.author.bot:
		await message.channel.send(f"Hej ty {message.author.mention}, žádný ttska tady.", tts = True)

	if message.channel.id == 715621624950292593:
		if not hasLink(message.content):
			await message.delete()

	if "No lyrics found for `" in message.content:
		try:
			results = await commands.kclient.music.lyrics(message.content.split("`")[1])
		except ksoftapi.NoResults:
			await message.channel.send(f"No lyrics found for `{message.content.split('`')[1]}`.")
		else:
			lyrics = results[0]
			for i in range(math.ceil(len(lyrics.lyrics)/2048)):
				e = embed(f"Lyrics for {lyrics.artist} - {lyrics.name}", description=lyrics.lyrics[(i*2048):((i+1)*2048)], thumbnail={"url": lyrics.album_art})
				await message.channel.send(embed=e)
		await message.delete()		

	if type(message.channel) != discord.DMChannel:
		await bdbf.commands.checkForCommands(message)
	if type(message.channel) == discord.DMChannel:
		if message.author.id == 452478521755828224:
			try:
				msgTextSplit = message.content.split(" ",1)
				channel = await client.fetch_channel(int(msgTextSplit[0]))
				await channel.send(msgTextSplit[1])
			except Exception as e:
				await message.channel.send(e)
				raise e

@client.event
async def on_raw_reaction_add(payload):
	guild = await client.fetch_guild(payload.guild_id)
	channel = await client.fetch_channel(payload.channel_id)
	message = await channel.fetch_message(payload.message_id)
	emoji = payload.emoji
	member = payload.member

	#print(emoji)
	
	if message.id == 746719599982280754:
		#1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣
		if emoji.name == "1️⃣":
			await member.add_roles(discord.Object(746396397280034946)) #Minecraft
			print(f"{member.name} in {guild} got role Minecraft for pressing {emoji}")
		if emoji.name == "2️⃣":
			await member.add_roles(discord.Object(746396668198649856)) #CS:GO
			print(f"{member.name} in {guild} got role CS:GO for pressing {emoji}")
		if emoji.name == "3️⃣":
			await member.add_roles(discord.Object(746712499705086013)) #Rocket League
			print(f"{member.name} in {guild} got role Rocket League for pressing {emoji}")
		if emoji.name == "4️⃣":
			await member.add_roles(discord.Object(746396772179378197)) #Fortnite
			print(f"{member.name} in {guild} got role Fortnite for pressing {emoji}")
		if emoji.name == "5️⃣":
			await member.add_roles(discord.Object(746704088070357012)) #Mobile Gaming
			print(f"{member.name} in {guild} got role Mobile Gaming for pressing {emoji}")
		if emoji.name == "6️⃣":
			await member.add_roles(discord.Object(746709189040275456)) #PS4 Gamers
			print(f"{member.name} in {guild} got role PS4 Gamers for pressing {emoji}")


# @client.event
# async def on_raw_reaction_remove(payload):
# 	guild = await client.fetch_guild(payload.guild_id)
# 	channel = await client.fetch_channel(payload.channel_id)
# 	message = await channel.fetch_message(payload.message_id)
# 	emoji = payload.emoji
# 	for m in guild.members:
# 		if m.id == payload.user_id:
# 			member = m

# 	if message.id == 746674728076312627:
		
# 		if emoji.name == "👶":
# 			await member.remove_roles(discord.Object(513730880464748557))
# 			print(guild, channel, message, member, emoji)
# 		if emoji.name == "🧒":
# 			await member.remove_roles(discord.Object(513730883824386049))
# 			print(guild, channel, message, member, emoji)
# 		if emoji.name == "👦":
# 			await member.remove_roles(discord.Object(513730888069152788))
# 			print(guild, channel, message, member, emoji)
# 		if emoji.name == "👶":
# 			await member.remove_roles(discord.Object(513730889222455309))
# 			print(guild, channel, message, member, emoji)
	

async def checkWebsites():
	while True:
		#Gymso
		try:
			print("Checking for new posts on Gymso")
			clanky = newOnGymso()
			if clanky:
				for clanek in clanky:
					for i in range(math.ceil(len(clanek["text"])/2048)):
						e = embed(clanek["title"], url = clanek["url"], description=clanek["text"][(i*2048):((i+1)*2048)])
						await obecne.send(f"{klubik.default_role} nový příspěvek na Gymso", embed=e)
		except Exception as e:
			print(e)

		#choco_afro
		try:
			print("Checking for new post on choco_afro")
			lastChocoPost = getLastInstaPost("choco_afro")
			if time.time() - lastChocoPost["taken_at_timestamp"] <= 7000:
				await choco_afroAnouncements.send(lastChocoPost["display_url"])
		except Exception as e:
			print(e)

		await asyncio.sleep(600)





client.run(token)
