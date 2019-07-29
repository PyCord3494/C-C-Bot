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
		embed = discord.Embed(color=0xff0909)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		author = ctx.author
		currency = self.bot.get_cog("Economy").getCurrency()
		if user is None:
			embed.add_field(name="C&C Bot", value="Invalid member.")
			await ctx.send(embed=embed)
			return
		if await self.bot.get_cog("Economy").accCheck(author.id) == False:
			embed.add_field(name="C&C Bot", value=f"{author.mention}, you must +start your account before you can send money.")
			await ctx.send(embed=embed)
			return
		if await self.bot.get_cog("Economy").accCheck(user.id) == False:
			embed.add_field(name="C&C Bot", value=f"{user.mention} must +start his account before he can accept money.")
			await ctx.send(embed=embed)
			return
		if author == user:
			embed.add_field(name="C&C Bot", value="You can't send {currency} to yourself.")
			await ctx.send(embed=embed)
			return
		if amnt < 1:
			embed.add_field(name="C&C Bot", value=f"You need to transfer at least 1. {currency}")
			await ctx.send(embed=embed)
			return

		if await self.bot.get_cog("Economy").checkBal(author.id, amnt) == True:
			embed.color = discord.Color(0xdfe324)
			await self.bot.get_cog("Economy").editBal(author.id, -amnt)
			await self.bot.get_cog("Economy").editBal(user.id, int(amnt * 0.92))
			embed.add_field(name="C&C Bot", value=f"{author.mention} has sent {amnt} {currency} and after taxes, {user.mention} has received {int(amnt * 0.92)}.")
		else:
			embed.add_field(name="C&C Bot", value=f"You do not have enough {currency} to send that much.")

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Transfer(bot))
