# Cog for all the commands used to earn money
# Current commands:
#	work
#	crime
#	gamble


import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random


class Earn(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.cooldown(1, 300, commands.BucketType.user)	
	async def work(self, ctx):
		author = ctx.author
		discordId = author.id
		if await self.bot.get_cog("Economy").accCheck(discordId) == False:
			embed = discord.Embed(title="C&C Bot: Work", color=0xfd0006, description="You must $start your account before you can use my commands.")
			await ctx.send(embed=embed)
			return

		currency = self.bot.get_cog("Economy").getCurrency()
		amnt = random.randint(200, 300)	
		await self.bot.get_cog("Economy").editBal(discordId, amnt)
		bal = self.bot.get_cog("Economy").getBal(discordId)
		await ctx.send(f"After a long day of work, you earned {amnt} {currency}. You now have {bal} {currency}.")



	@commands.command(pass_context=True)
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def crime(self, ctx):
		author = ctx.author
		discordId = author.id
		if await self.bot.get_cog("Economy").accCheck(discordId) == False:
			embed = discord.Embed(title="C&C Bot: Crime", color=0xfd0006, description="You must $start your account before you can use my commands.")
			await ctx.send(embed=embed)
			return
			
		amnt = random.randint(0, 300)
		outcome = random.randint(0, 1)
		currency = self.bot.get_cog("Economy").getCurrency()

		if outcome == 0:
			await self.bot.get_cog("Economy").editBal(discordId, amnt)
			bal = self.bot.get_cog("Economy").getBal(discordId)
			await ctx.send(f"Successfully robbed {amnt} {currency} from a bank! You now have {bal} {currency}.")

		elif outcome == 1:
			await self.bot.get_cog("Economy").editBal(discordId, -amnt)
			bal = self.bot.get_cog("Economy").getBal(discordId)
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xfd0006, description=f"Oh no! You got caught and you were fined {amnt} {currency}. You now have {bal} {currency}.")
			await ctx.send(embed=embed)



	@commands.command(pass_context=True)
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def gamble(self, ctx, amnt):
		currency = self.bot.get_cog("Economy").getCurrency()
		author = ctx.author
		discordId = author.id
		try:
			amnt = int(amnt)
		except:
			await ctx.send("no")

		if amnt < 1:
			await ctx.send("That's not a valid bet amount. You must bet a number above 0.")
			return
		if await self.bot.get_cog("Economy").accCheck(discordId) == False:
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xfd0006, description="You must $start your account before you can use my commands.")
			await ctx.send(embed=embed)
			return
		currency = self.bot.get_cog("Economy").getCurrency()
		bal = self.bot.get_cog("Economy").getBal(discordId)
		if bal < amnt: # if user doesn't have enough {currency} to gamble specified amnt
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xfd0006, description=f"That will cost you {amnt} {currency}, but you only have {bal} {currency}")
			await ctx.send(embed=embed)
			return

		outcome = random.randint(1, 10) # num between 1 and 10
		if outcome < 5: # 40% win rate
			await self.bot.get_cog("Economy").editBal(discordId, amnt)
			bal = self.bot.get_cog("Economy").getBal(discordId)
			await ctx.send(f"Congrats! You won doubled your bet! You now have {bal} {currency}.")
		else: # 60% lose rate
			await self.bot.get_cog("Economy").editBal(discordId, -amnt)
			bal = self.bot.get_cog("Economy").getBal(discordId)
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xfd0006, description=f"Unfortunately, you have lost your {currency} you have bet. You now have {bal} {currency}.")
			await ctx.send(embed=embed)


		



def setup(bot):
	bot.add_cog(Earn(bot))
