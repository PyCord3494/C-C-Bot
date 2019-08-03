	# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
import asyncio

import math
import datetime
import json
import operator

def log(discordID, credits): # Logs the time, the user's id, and the amount in which a balance gets edited
	x = datetime.datetime.now()
						#  MON DAY HOUR:MIN:SEC
	localtime = x.strftime("%b %d %H:%M:%S")
	logs = open("logs.txt", "a")
	logs.write(f"{localtime} : {discordID} : {credits}\n")
	logs.flush()
	logs.close()


async def get_prefix(bot, message):
	with open(r"config.json", 'r') as f:
			config = json.load(f)

	prefix = config["prefix"]
	return prefix


class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def getCurrency(self): # grabs currency from config file
		with open(r"config.json", 'r') as f:
			config = json.load(f)

		currency = config["currency"]
		return currency


	@commands.command(aliases=["bal", "money"], pass_context=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def balance(self, ctx, *, member: discord.Member=None):
		if not member:
			if await self.bot.get_cog("Economy").accCheck(ctx, ctx.author.id) == False:
				return

			currency = self.getCurrency()
			bal = self.getBal(ctx.author.id)
			embed = discord.Embed(title="C&C Bot: Balance", color=0xdfe324, description=f"You currently have {format(bal, ',d')} {currency}")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
		else:
			if await self.bot.get_cog("Economy").accCheck(ctx, member.id) == False:
				return

			currency = self.getCurrency()
			bal = self.getBal(member.id)
			embed = discord.Embed(title="C&C Bot: Balance", color=0xdfe324, description=f"{member.mention} currently has {format(bal, ',d')} {currency}")
			embed.set_thumbnail(url=member.avatar_url)
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
			bal = data[str(discordId)]
		log(discordId, amnt)
		return bal




	async def checkBal(self, discordId, amnt: int):
		with open('users.json') as f:
				data = json.load(f)

		if data[str(discordId)] >= amnt:
			return True
		else:
			return False


	@commands.command(pass_context=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def start(self, ctx):
		if await self.accCheck(ctx, ctx.author.id) == False:
			newuser = {str(ctx.author.id) : 100}
			with open('users.json') as f:
				data = json.load(f)

			data.update(newuser)

			with open('users.json','w') as f:
				json.dump(data, f, indent=4)

			embed = discord.Embed(title="C&C Bot: New Account", color=0xdfe324, description=f"{ctx.author.mention}, successfully registered!")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

		else:
			embed = discord.Embed(title="C&C Bot: New Account", color=0xff0000, description=f"{ctx.author.mention}, you already have an account registered!")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)


	async def accCheck(self, ctx, discordId):
		with open(r"users.json", 'r') as f:
			users = json.load(f)

		if str(discordId) in users:
			return True
		else:
			if str(ctx.command) != "start": # don't print if user is trying to $start
				ctx.command.reset_cooldown(ctx)
				prefix = await get_prefix(self.bot, ctx.message)
				embed = discord.Embed(title="C&C Bot: New User Alert!", color=0xff0000, description=f"You must `{prefix}start` your account before you can use my commands.")
				embed.set_thumbnail(url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
			return False


	@commands.command(aliases=["lb"], pass_context=True)
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def leaderboard(self, ctx):
		currency = self.getCurrency()
		with open('users.json') as f:
			data = json.load(f)
		lines = sorted(data.items(), key=operator.itemgetter(1), reverse=True) # sorts lines by balance

		lb = [] # leaderboard
		for line in lines: # each line in file
			user = self.bot.get_user(id=int(line[0])) # grab user object from ID 
			if not user:
				user = await self.bot.fetch_user(int(line[0]))

			lb.append(f"{user.name} | {format(line[1], ',d')} {currency}\n") # add username and balance to leaderboard

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
			if pageCount > 1:
				if currPage == 0: # if first page
					await msg.add_reaction("➡")
					print(pageCount)

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