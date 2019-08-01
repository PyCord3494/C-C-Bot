# Cog for all the commands used to earn money
# Current commands:
#	work
#	crime
#	gamble


import discord
from discord.ext import commands
import random

class Earn(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.cooldown(1, 300, commands.BucketType.user)	
	async def work(self, ctx):
		author = ctx.author
		userId = author.id
		if await self.bot.get_cog("Economy").accCheck(ctx, userId) == False:
			return

		currency = self.bot.get_cog("Economy").getCurrency()
		amnt = random.randint(200, 300)	
		bal = await self.bot.get_cog("Economy").editBal(userId, amnt)
		embed = discord.Embed(title="C&C Bot: Work", color=0xdfe324, description=f"After a long day of work, you earned {amnt} {currency}. You now have {format(bal, ',d')} {currency}.")
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)



	@commands.command(pass_context=True)
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def crime(self, ctx):
		author = ctx.author
		userId = author.id
		embed = discord.Embed(title="C&C Bot: Crime", color=0xff0000)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		if await self.bot.get_cog("Economy").accCheck(ctx, userId) == False:
			return

		amnt = random.randint(0, 300)
		outcome = random.randint(0, 1)
		currency = self.bot.get_cog("Economy").getCurrency()
		oldBal = self.bot.get_cog("Economy").getBal(userId)

		if outcome == 0:
			bal = await self.bot.get_cog("Economy").editBal(userId, amnt)
			embed.color = discord.Color(0xdfe324)
			embed.description = description=f"Successfully robbed {amnt} {currency} from a bank! You went from {format(oldBal, ',d')} {currency} to {format(bal, ',d')} {currency}."

		elif outcome == 1:
			bal = await self.bot.get_cog("Economy").editBal(userId, -amnt)
			embed.description = f"Oh no! You got caught and you were fined {amnt} {currency}. You went from {format(oldBal, ',d')} {currency} to {format(bal, ',d')} {currency}."

		await ctx.send(embed=embed)



	@commands.command(pass_context=True)
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def gamble(self, ctx, amnt):
		currency = self.bot.get_cog("Economy").getCurrency()
		author = ctx.author
		userId = author.id
		if await self.bot.get_cog("Economy").accCheck(ctx, userId) == False:
			return

		try:
			amnt = int(amnt)
		except:
			if amnt == "allin" or amnt == "all":
				amnt = self.bot.get_cog("Economy").getBal(userId)
			else:
				embed = discord.Embed(title="C&C Bot: Gamble", color=0xff0000, description=f"You've provided an improper integer for the `gamble` command. I do not know what `{amnt}` is.\nProper usage: +gamble <amount>")
				embed.set_thumbnail(url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
				ctx.command.reset_cooldown(ctx)
				return


		if amnt < 1:
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xff0000, description=f"That's not a valid bet amount. You must bet a number above 0.")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			ctx.command.reset_cooldown(ctx)
			return

		if amnt > 10000:
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xff0000, description = f"That's not a valid bet amount. You cannot bet an amount higher than 10,000.")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			ctx.command.reset_cooldown(ctx)
			await ctx.send(embed=embed)
			return

		currency = self.bot.get_cog("Economy").getCurrency()
		bal = self.bot.get_cog("Economy").getBal(userId)
		if bal < amnt: # if user doesn't have enough {currency} to gamble specified amnt
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xff0000, description=f"That will cost you {amnt} {currency}, but you only have {format(bal, ',d')} {currency}")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			ctx.command.reset_cooldown(ctx)
			return

		oldBal = self.bot.get_cog("Economy").getBal(userId)
		outcome = random.randint(1, 10) # num between 1 and 10
		if outcome > 4: # 40% win rate
			bal = await self.bot.get_cog("Economy").editBal(userId, amnt)
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xdfe324, description=f"Congrats! You won doubled your bet! You went from {format(oldBal, ',d')} {currency} to {format(bal, ',d')} {currency}.")
		else: # 60% lose rate
			bal = await self.bot.get_cog("Economy").editBal(userId, -amnt)
			embed = discord.Embed(title="C&C Bot: Gamble", color=0xff0000, description=f"Unfortunately, you have lost your {currency} you have bet. You went from {format(oldBal, ',d')} {currency} to {format(bal, ',d')} {currency}.")
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Earn(bot))