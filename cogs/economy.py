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


	async def editBal(self, ctx, amnt):

		log(ctx.author.id, amnt)

	@commands.command(pass_context=True)	
	async def start(self, ctx):
		if await self.accCheck(ctx.author.id) == False:
			with open(r"users.json", 'r') as f:
				users = json.load(f)


			users = {ctx.author.id : 100}

			with open(r"users.json", 'r+') as f:
				json.dump(users, f, indent=4)


			with open("user.json", "r+") as f:
			    data = json.load(f)

			    tmp = data["location"]
			    data["location"] = "NewPath"

			    f.seek(0)  # rewind
			    json.dump(data, f)
			    f.truncate()
		else:
			await ctx.send(f"{ctx.author.mention}, you already have an account registered!")


	async def accCheck(self, discordId):
		with open(r"users.json", 'r') as f:
			users = json.load(f)

		if discordId in users:
			return True
		else:
			return False




def setup(bot):
	bot.add_cog(Economy(bot))
