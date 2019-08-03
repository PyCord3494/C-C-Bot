# Cog for all the commands related to movement of money
# Current commands:
#	send

import discord
from discord.ext import commands

class Transfer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.cooldown(1, 8, commands.BucketType.user)
	async def send(self, ctx, user: discord.Member, amnt):
		try:
			amnt = int(amnt)
		except:
			embed = discord.Embed(title="C&C Bot: ERROR", color=0xff0000, description=f"Amount to send must be a number. You entered: `{amnt}`")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return
		author = ctx.author
		currency = self.bot.get_cog("Economy").getCurrency()
		embed = discord.Embed(title="C&C Bot: Send", color=0xff0000)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		if user is None: # if user is not found
			embed.description = "Invalid member."
			await ctx.send(embed=embed)
			return
		if await self.bot.get_cog("Economy").accCheck(ctx, author.id) == False: # accCheck for user sending money
			return
		if await self.bot.get_cog("Economy").accCheck(ctx, user.id) == False: # accCheck for user receiving the money
			return
		if author == user: # if user is attempting to send money to himself
			embed.description= f"You can't send {currency} to yourself."
			await ctx.send(embed=embed)
			return
		if amnt < 10: # if user is attempting to send less than 10
			embed.description = f"You need to transfer at least 10 {currency}"
			await ctx.send(embed=embed)
			return

		if await self.bot.get_cog("Economy").checkBal(author.id, amnt) == True: # if sender has enough money
			senderBal = await self.bot.get_cog("Economy").editBal(ctx, author.id, -amnt) # subtract amnt from sender
			receiverBal = await self.bot.get_cog("Economy").editBal(ctx, user.id, int(amnt * 0.92)) # subtract taxes from amnt and add amnt to bal of receiver
			embed = discord.Embed(title="C&C Bot: Send", color=0xdfe324, description=f"{author.mention} has sent {format(amnt, ',d')} {currency}, and after taxes, {user.mention} has received {format(int(amnt * 0.92), ',d')} {currency}.\n{author.mention}, you now have {format(senderBal, ',d')} {currency}, and {user.mention}, you now have {format(receiverBal, ',d')} {currency}")
			embed.set_thumbnail(url=user.avatar_url)
		else:
			embed.description = f"You do not have enough {currency} to send that much."

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Transfer(bot))
