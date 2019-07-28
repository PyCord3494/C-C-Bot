# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions

import datetime
import json


class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def log(discordID, credits): # Logs what credits have been spent where, by who, to who, why and the time which this has happened
		#localtime = time.asctime(time.localtime(time.time()))
		x = datetime.datetime.now()
							#  MON DAY HOUR:MIN:SEC
		localtime = x.strftime("%b %d %H:%M:%S")
		logs = open("logs.txt", "a")
		logs.write(f"{localtime} : {discordID} : {credits}\n")
		logs.flush()
		logs.close()


	@commands.command(pass_context=True)
	async def balance(self, ctx):
		with open('users.json') as f:
			data = json.load(f)
		await ctx.send(data[str(ctx.author.id)])


	async def editBal(self, discordId, amnt: int):
		with open('users.json') as f:
				data = json.load(f)

		data[str(discordId)] = data[str(discordId)] + amnt

		with open('users.json','w') as f:
			json.dump(data, f, indent=4)
		#log(ctx.author.id, amnt)

	async def checkBal(self, discordId, amnt: int):
		with open('users.json') as f:
				data = json.load(f)

		if data[str(discordId)] >= amnt:
			return True
		else:
			return False

	@commands.command(pass_context=True)
	async def addcoins(self, ctx, user: discord.Member, amnt: int):
		with open('users.json') as f:
				data = json.load(f)

		if str(user.id) in data:
			data[str(user.id)] = data[str(user.id)] + amnt

			with open('users.json','w') as f:
				json.dump(data, f, indent=4)
		else:
			await ctx.send("User not found. Please @mention him or provide me his ID.\nProper format: `+addcoins user amount`")
		#log(ctx.author.id, amnt)

	@commands.command(pass_context=True)
	async def start(self, ctx):
		if await self.accCheck(ctx.author.id) == False:
			newuser = {f"{ctx.author.id}" : 100}
			with open('users.json') as f:
				data = json.load(f)

			data.update(newuser)

			with open('users.json','w') as f:
				json.dump(data, f, indent=4)

		else:
			await ctx.send(f"{ctx.author.mention}, you already have an account registered!")


	async def accCheck(self, discordId):
		with open(r"users.json", 'r') as f:
			users = json.load(f)

		if str(discordId) in users:
			return True
		else:
			return False




def setup(bot):
	bot.add_cog(Economy(bot))
