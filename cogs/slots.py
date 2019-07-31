# slots

import discord
from discord.ext import commands
import asyncio
import random

class Slots(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.cooldown(1, 9, commands.BucketType.user)
	async def slots(self, ctx, amnt: int):
		if await self.bot.get_cog("Economy").checkBal(ctx.author.id, amnt) == False: # if sender doesn't have enough money
			embed = discord.Embed(title="C&C Bot: Send", color=0xff0000, description=f"You do not have enough {currency} to play the slots with.")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			return

		# embed = discord.Embed(title="C&C Bot: COUNT RESULTS", color=0xff0000)
		# emojis = ["🍎","🍋","🍇","🍓","🍒", "🥝", "🥭"]
		# while len(emojis) > 2:
		# 	msg = ""
		# 	wins = 0
		# 	loses = 0
		# 	for x in range(0, len(emojis)):
		# 		for y in range(0, len(emojis)):
		# 			for z in range(0, len(emojis)):
		# 				#msg += f"{emojis[x]} {emojis[y]} {emojis[z]}\n"
		# 				if ({emojis[x]} == {emojis[y]} == {emojis[z]}):
		# 					wins += 1
		# 				else:
		# 					loses += 1

		# 	emojislist = ""
		# 	for x in emojis:
		# 		emojislist += f"{x}"
		# 	embed.description = f"Emojis: {emojislist}\n# of Possible Wins: {wins} | Win Chance: {round((wins / (wins + loses)) * 100)}%\n# of Possible Loses: {loses} | Lose Chance: {round((loses / (wins + loses)) * 100)}%"
		# 	await ctx.send(embed=embed)
		# 	await asyncio.sleep(2)
		# 	emojis.pop()


		a = random.choice(emojis)
		b = random.choice(emojis)
		c = random.choice(emojis)

		embed = discord.Embed(color=0xdfe324, title="C&C Bot: Slots")

		embed.add_field(name="----------------------------\n| 🎰  [  ]  [  ]  [  ]  🎰 |\n----------------------------", value="_ _")
		botMsg = await ctx.send(embed=embed)
		await asyncio.sleep(1.5)

		embed.set_field_at(0, name=f"------------------------------\n| 🎰  {a}  [  ]  [  ]  🎰 |\n------------------------------", value="_ _")
		await botMsg.edit(embed=embed)
		await asyncio.sleep(1.5)

		embed.set_field_at(0, name=f"-------------------------------\n| 🎰  {a}  {b}  [  ]  🎰 |\n-------------------------------", value="_ _")
		await botMsg.edit(embed=embed)
		await asyncio.sleep(1.5)

		embed.set_field_at(0, name=f"--------------------------------\n| 🎰  {a}  {b}  {c}  🎰 |\n--------------------------------", value="_ _")
		await botMsg.edit(embed=embed)

		embed.color = discord.Color(0x23f518)
		moneyToAdd = 0
		if (a == b == c): # if all match
			moneyToAdd = int(amnt)
			result = "YOU WON"

		elif (a == b) or (a == c) or (b == c): # if two match
			moneyToAdd = int(amnt * 0.5) # you win 150% your bet
			result = "YOU WON"

		else: # if no match
			moneyToAdd = -amnt
			result = "YOU LOST"
			embed.color = discord.Color(0xff2020)

		await self.bot.get_cog("Economy").editBal(ctx.author.id, moneyToAdd)
		balance = self.bot.get_cog("Economy").getBal(ctx.author.id)
		currency = self.bot.get_cog("Economy").getCurrency()
		embed.add_field(name=f"**--- {result} ---**", value="_ _", inline=False)	
		embed.add_field(name="Profit", value=f"**{moneyToAdd}** {currency}", inline=True)
		embed.add_field(name="Credits", value=f"**{balance}** {currency}", inline=True)

		await botMsg.edit(embed=embed)


def setup(bot):
	bot.add_cog(Slots(bot))