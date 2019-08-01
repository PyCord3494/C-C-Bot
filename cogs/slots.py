# slots
#
### Money isn't taken out at the start; money is only added/removed at the end in the RESULT
#
# POSSIBLE OUTCOMES:
# 3 in a row: 2x your bet ADDED. ex: bet 100, you get 200
# 2 of the same emoji: you get your bet amount ADDED. ex: bet 100, you get 100

import discord
from discord.ext import commands
import asyncio
import random

class Slots(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	@commands.command(aliases=["slot"], pass_context=True)
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def slots(self, ctx, amnt):
		userId = ctx.author.id
		embed = discord.Embed(title="C&C Bot: Slots", color=0xff0000)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		
		if await self.bot.get_cog("Economy").accCheck(ctx, userId) == False: # accCheck for user sending money
			return

		try: # checks to see if: amnt is int, if not: checks to see if amnt is "allin" or "all", if so: their bet = all their money; if not: return error
			amnt = int(amnt)
		except:
			if amnt == "allin" or amnt == "all":
				amnt = self.bot.get_cog("Economy").getBal(userId)
			else:
				embed.description = f"You've provided improper input for the `slots` command. I do not know what `{amnt}` is.\nProper usage: +slots <amount>"
				embed.set_thumbnail(url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
				return

		if amnt < 10:
			embed.description = f"That's not a valid bet amount. You cannot bet an amount lower than 10."
			ctx.command.reset_cooldown(ctx)
			await ctx.send(embed=embed)
			return

		if amnt > 10000:
			embed.description = f"That's not a valid bet amount. You cannot bet an amount higher than 10,000."
			ctx.command.reset_cooldown(ctx)
			await ctx.send(embed=embed)
			return

		if await self.bot.get_cog("Economy").checkBal(ctx.author.id, amnt) == False: # if sender doesn't have enough money
			embed.description=f"You do not have enough {currency} to play the slots with."
			ctx.command.reset_cooldown(ctx)
			await ctx.send(embed=embed)
			return

		if not embed.description: # if no error occurred
			#emojis = ["🍎","🍋","🍇","🍓","🍒", "🥝", "🥭"]
			# emojis = ["🍎","🍋","🍇","🍓"]
			# embed = discord.Embed(title="C&C Bot: COUNT RESULTS", color=0x00ff00)
			# while len(emojis) > 2:
			# 	msg = ""
			# 	threeinarowwins = 0
			# 	twosame = 0
			# 	loses = 0
			# 	for x in range(0, len(emojis)):
			# 		for y in range(0, len(emojis)):
			# 			for z in range(0, len(emojis)):
			# 				a = emojis[x]
			# 				b = emojis[y]
			# 				c = emojis[z]
			# 				#msg += f"{emojis[x]} {emojis[y]} {emojis[z]}\n"
			# 				if (a == b == c):
			# 					threeinarowwins += 1
			# 				elif (b == a) or (b == c) or (a == c):
			# 					twosame += 1
			# 				else:
			# 					loses += 1

			# 	emojislist = ""
			# 	for x in emojis:
			# 		emojislist += f"{x}"
			# 	embed.description = f"Emojis: {emojislist}\n# of 3-in-a-row Possible Wins: {threeinarowwins}" + f"\n# of 2 SAME emojis Possible Wins: {twosame}" + f"\n# of Possible Loses: {loses}" + f"\nWin Chance: {round(((threeinarowwins + twosame) / (threeinarowwins + twosame + loses) * 100))}%" +  f"\nLose Chance: {round((loses / (threeinarowwins + twosame + loses) * 100))}%"
			# 	await ctx.send(embed=embed)
			# 	await asyncio.sleep(2)
			# 	emojis.pop()

			emojis = ["🍎","🍋","🍇","🍓"]
			
			# generates results
			a = random.choice(emojis) 
			b = random.choice(emojis)
			c = random.choice(emojis)

			embed.color = discord.Color(0xdfe324)

			# slowly prints the results (like an actual slot machine)
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

			moneyToAdd = 0
			if (a == b == c): # if all match
				moneyToAdd = int(amnt * 2)
				result = "3 IN A ROW! YOU WON 3x"

			elif (a == b) or (a == c) or (b == c): # if two match
				moneyToAdd = int(amnt) # you win 150% your bet
				result = "YOU WON 2x"

			else: # if no match
				moneyToAdd = -amnt
				result = "YOU LOST"
				embed.color = discord.Color(0xff0000)

			await self.bot.get_cog("Economy").editBal(userId, moneyToAdd)
			bal = self.bot.get_cog("Economy").getBal(userId)
			currency = self.bot.get_cog("Economy").getCurrency()
			embed.add_field(name=f"**--- {result} ---**", value="_ _", inline=False)	
			embed.add_field(name="Outcome:", value=f"**{moneyToAdd:+d}** {currency}", inline=True)
			embed.add_field(name="Balance", value=f"**{format(bal, ',d')}** {currency}", inline=True)

			await botMsg.edit(embed=embed)


def setup(bot):
	bot.add_cog(Slots(bot))