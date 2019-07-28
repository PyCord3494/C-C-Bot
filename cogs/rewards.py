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
		




def setup(bot):
	bot.add_cog(Rewards(bot))
