# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions

import datetime
import json


class Rewards(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(pass_context=True)
	@commands.cooldown(1, 86400, commands.BucketType.user)	
	async def daily(self, ctx):
		author = ctx.author
		discordId = author.id
		if await self.bot.get_cog("Economy").accCheck(discordId) == True:
			currency = self.bot.get_cog("Economy").getCurrency()
			if "Nitro Booster" in [y.name.lower() for y in author.roles]:
				reward = 1000
			else:
				reward = 500

			await self.bot.get_cog("Economy").editBal(discordId, reward)
			bal = self.bot.get_cog("Economy").getBal(discordId)
			await ctx.send(f"You now have {bal} {currency}.")
		else: 
			await ctx.send("You must $start your account before you can buy stuff.")

		




def setup(bot):
	bot.add_cog(Rewards(bot))
