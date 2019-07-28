# Cog for all the commands related to movement of money
# Current commands:
#	send

import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions

class Transfer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)	
	async def send(self, ctx, user: discord.Member, amnt: int):
		author = ctx.author
		if user is None:
			await ctx.send("Invalid member.")
			return
		if await self.bot.get_cog("Economy").accCheck(author.id) == False:
			await ctx.send(f"{author.mention}, you must +start your account before you can send money.")
			return
		if await self.bot.get_cog("Economy").accCheck(user.id) == False:
			await ctx.send(f"{user.mention} must +start his account before he can accept money.")
			return
		if author == user:
			await ctx.send("You can't send money to yourself.")
			return
		if amnt < 1:
			await ctx.send("You need to transfer at least 1 credit.")
			return

		if await self.bot.get_cog("Economy").checkBal(author.id, amnt) == True:
			await self.bot.get_cog("Economy").editBal(author.id, -amnt)
			await self.bot.get_cog("Economy").editBal(user.id, int(amnt * 0.92))
			await ctx.send(f"{author.mention} has sent {amnt} credits and after taxes, {user.mention} has received {int(amnt * 0.92)}.")
		else:
			await ctx.send("You do not have enough money to send that much.")

def setup(bot):
	bot.add_cog(Transfer(bot))
