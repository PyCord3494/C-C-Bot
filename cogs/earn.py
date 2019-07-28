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
		pass


	@commands.command(pass_context=True)
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def crime(self, ctx):
		amnt = random.randint(0, 301)
		outcome = random.randint(0, 1)

		if outcome == 0:
			await ctx.send(f"Successfully robbed {amnt} coins from a bank!")

		elif outcome == 1:
			await ctx.send(f"Oh no! You got caught and you were fined {amnt} coins.")

		#bal = 
		#await ctx.send(f"{msg}\nYou now have {bal} coins")


def setup(bot):
	bot.add_cog(Earn(bot))
