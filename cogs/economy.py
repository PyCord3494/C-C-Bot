	# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions

import datetime
import json

def log(discordID, credits): # Logs what credits have been spent where, by who, to who, why and the time which this has happened
	#localtime = time.asctime(time.localtime(time.time()))
	x = datetime.datetime.now()
						#  MON DAY HOUR:MIN:SEC
	localtime = x.strftime("%b %d %H:%M:%S")
	logs = open("logs.txt", "a")
	logs.write(f"{localtime} : {discordID} : {credits}\n")
	logs.flush()
	logs.close()

class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	def getCurrency(self):
		with open(r"config.json", 'r') as f:
			config = json.load(f)

		currency = config["currency"]
		return currency

	@commands.command(aliases=["bal", "money"],pass_context=True)
	async def balance(self, ctx):
		if await self.bot.get_cog("Economy").accCheck(ctx.author.id) == False:
			await ctx.send("You must $start your account before you can buy stuff.")
			
		currency = self.getCurrency()
		bal = self.getBal(ctx.author.id)
		await ctx.send(f"You have {bal} {currency}")


	def getBal(self, discordId):
		with open('users.json', 'r') as f:
			data = json.load(f)
		bal = data[str(discordId)]
		return bal

	async def editBal(self, discordId, amnt: int):
		with open('users.json') as f:
				data = json.load(f)

		data[str(discordId)] = data[str(discordId)] + amnt

		with open('users.json','w') as f:
			json.dump(data, f, indent=4)
		log(discordId, amnt)

	async def checkBal(self, discordId, amnt: int):
		with open('users.json') as f:
				data = json.load(f)

		if data[str(discordId)] >= amnt:
			return True
		else:
			return False


	@commands.command(pass_context=True)
	async def start(self, ctx):
		if await self.accCheck(ctx.author.id) == False:
			newuser = {str(ctx.author.id) : 100}
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
