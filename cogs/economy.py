	# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions

import math
import datetime
import json
import operator

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

	@commands.command(pass_context=True)
	async def test(self, ctx):
		embed = discord.Embed(title="Epic Account Verification", color=0xdfe324)
		embed.add_field(name="_ _", value=f"Member: {ctx.author.mention}")
		await ctx.send(embed=embed)
		#user = await self.bot.fetch_user(552292743762673675)
		#await ctx.send(user.mention)



	def getCurrency(self):
		with open(r"config.json", 'r') as f:
			config = json.load(f)

		currency = config["currency"]
		return currency

	@commands.command(aliases=["bal", "money"],pass_context=True)
	async def balance(self, ctx):
		if await self.bot.get_cog("Economy").accCheck(ctx.author.id) == False:
			embed = discord.Embed(title="C&C Bot: Balance", color=0xfd0006, description="You must $start your account before you can use my commands.")
			await ctx.send(embed=embed)
			return

		currency = self.getCurrency()
		bal = self.getBal(ctx.author.id)
		embed = discord.Embed(title="C&C Bot: Balance", color=0xdfe324, description=f"You currently have {bal} {currency}")
		await ctx.send(embed=embed)


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

			embed = discord.Embed(title="C&C Bot: New Account", color=0xdfe324, description=f"{ctx.author.mention}, successfully registered!")
			await ctx.send(embed=embed)

		else:
			embed = discord.Embed(title="C&C Bot: New Account", color=0xfd0006, description=f"{ctx.author.mention}, you already have an account registered!")
			await ctx.send(embed=embed)


	async def accCheck(self, discordId):
		with open(r"users.json", 'r') as f:
			users = json.load(f)

		if str(discordId) in users:
			return True
		else:
			return False

	@commands.command(pass_context=True)
	async def lb(self, ctx):
		currency = self.getCurrency()
		with open('users.json') as f:
			data = json.load(f)
		lines = sorted(data.items(), key=operator.itemgetter(1), reverse=True) # sorts lines by balance

		lb = [] # leaderboard
		for line in lines: # each line in file
			user = self.bot.get_user(line[0]) # grab user object from ID 
			if not user:
				user = await self.bot.fetch_user(line[0])
			else:
				print("SUCCESSFULLY GET_USER")
			lb.append(f"{user.name} | {line[1]} {currency}\n") # add username and balance to leaderboard

		lb = 5*lb
		limitedMsgs = [] # array for each page
		pageCount = math.ceil(len(lb) / 10) # pageCount = number of users / 10 users per page
		for x in range(0, pageCount): # for every page
			limitedMsgs.append("".join(lb[x*10:x*10+10])) # add those 10 users to 1 page

		currPage = 0
		embed = discord.Embed(color=0xdfe324, description=limitedMsgs[0])
		embed.set_footer(text=f"Page: {currPage + 1} of {pageCount}")

		msg = await ctx.send(embed=embed)


		def check(reaction, user):
			return (user == ctx.message.author) and (str(reaction.emoji) == '⬅' or str(reaction.emoji) == '➡')

		while(True):
			if currPage == 0: # if first page
				await msg.add_reaction("➡")

			elif (currPage + 1) == pageCount: # if last page
				await msg.add_reaction("⬅")

			else: # if not first nor last
				await msg.add_reaction("➡")
				await msg.add_reaction("⬅")
			
			try:
				reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check) # wait for user reaction
			except asyncio.TimeoutError:
				break # end while loop if no user reaction

			if str(reaction.emoji) == '⬅': # if go to previous page
				currPage = currPage - 1
			if str(reaction.emoji) == '➡': # if go to next page
				currPage = currPage + 1
			embed = discord.Embed(color=0xdfe324, description=limitedMsgs[currPage])
			embed.set_footer(text=f"Page: {currPage + 1} of {pageCount}")
			await msg.clear_reactions()
			await msg.edit(embed=embed)

		await msg.clear_reactions() # clear reactions after while loop



	



def setup(bot):
	bot.add_cog(Economy(bot))
