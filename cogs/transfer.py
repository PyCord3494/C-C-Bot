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
		currency = self.bot.get_cog("Economy").getCurrency()
		if user is None: # if user is not found
			embed = discord.Embed(title="C&C Bot: Send", color=0xff0000, description="Invalid member.")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return
		if await self.bot.get_cog("Economy").accCheck(author.id) == False: # accCheck for user sending money
			embed = discord.Embed(title="C&C Bot: Send", color=0xff0000, description="You must $start your account before you can use my commands.")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return
		if await self.bot.get_cog("Economy").accCheck(user.id) == False: # accCheck for user receiving the money
			embed = discord.Embed(title="C&C Bot: Send", color=0xff0000, description=f"{user.mention} must $start his account before you can send him any money.")
			embed.set_thumbnail(url=user.avatar_url)
			await ctx.send(embed=embed)
			return
		if author == user: # if user is attempting to send money to himself
			embed = discord.Embed(title="C&C Bot: Send", color=0xff0000, description=f"You can't send {currency} to yourself.")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return
		if amnt < 10: # if user is attempting to send less than 10
			embed = discord.Embed(title="C&C Bot: Send", color=0xff0000, description=f"You need to transfer at least 10 {currency}")
			await ctx.send(embed=embed)
			return

		if await self.bot.get_cog("Economy").checkBal(author.id, amnt) == True: # if sender has enough money
			await self.bot.get_cog("Economy").editBal(author.id, -amnt) # subtract amnt from sender
			await self.bot.get_cog("Economy").editBal(user.id, int(amnt * 0.92)) # subtract taxes from amnt and add amnt to bal of receiver
			embed = discord.Embed(title="C&C Bot: Send", color=0xdfe324, description=f"{author.mention} has sent {amnt} {currency}, and after taxes, {user.mention} has received {int(amnt * 0.92)} {currency}.")
			embed.set_thumbnail(url=user.avatar_url)
		else:
			embed = discord.Embed(title="C&C Bot: Send", color=0xff0000, description=f"You do not have enough {currency} to send that much.")
			embed.set_thumbnail(url=ctx.author.avatar_url)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Transfer(bot))
