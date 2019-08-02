# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import json


class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden = True, pass_context=True)
	async def end(self, ctx):
		if await self.bot.is_owner(ctx.author):
			print("\nGoing to sleep...\n")
			await self.bot.logout()


	async def msgPycord(self, ctx):
		loggingChnl = self.bot.get_channel(605921228083167245)
		if not loggingChnl:
			loggingChnl = self.bot.fetch_channel(605921228083167245)
		await loggingChnl.send(f"User {ctx.author.mention} ({ctx.author.id}) attempted command `{ctx.command}` in channel {ctx.channel.mention} ({ctx.channel.id})")


	@commands.command(hidden=True, pass_context=True)
	async def addcoins(self, ctx, user: discord.Member, amnt: int):
		if ctx.author.id == 435806214484393996 or ctx.author.id == 547475078082985990:
			currency = self.bot.get_cog("Economy").getCurrency()

			with open('users.json') as f:
					data = json.load(f)

			if str(user.id) in data:
				data[str(user.id)] = data[str(user.id)] + amnt

				with open('users.json','w') as f:
					json.dump(data, f, indent=4)
				bal = self.bot.get_cog("Economy").getBal(user.id)
				embed = discord.Embed(title="C&C Bot: ADMIN", color=0xdfe324, description=f"Added {format(amnt, ',d')} {currency} to user {user.mention} ({user.id})\nUser's new balance: {format(bal, ',d')} {currency}")
				await ctx.send(embed=embed)
			else:
				embed = discord.Embed(title="C&C Bot: ADMIN", color=0xff0000, description="User not found. Please @mention him or provide me his ID.\nProper format: `+addcoins <user> <amount>`")
				await ctx.send(embed=embed)
		else:
			await self.msgPycord(ctx)


	@commands.group(invoke_without_command=True, pass_context=True, hidden=True)
	@has_permissions(administrator=True)
	async def edit(self, ctx):
		if ctx.invoked_subcommand is None:
			embed = discord.Embed(title="C&C Bot: ADMIN", color=0xff0000, description="This is a command that requires subcommands.\nAvailable subcommands: `currency` & `prefix`.\nCorrect usage: `edit prefix <prefix>`")
			await ctx.send(embed=embed)
	

	@edit.command()
	async def currency(self, ctx, *, msg):
		if ctx.author.id == 435806214484393996:
			with open(r"config.json", 'r') as f:
				config = json.load(f)

			config["currency"] = msg

			with open(r"config.json", 'w') as f:
				json.dump(config, f, indent=4)
			embed = discord.Embed(title="C&C Bot: ADMIN", color=0xdfe324, description=f"Successfully changed currency to: {msg}")
			await ctx.send(embed=embed)
		else:
			await self.msgPycord(ctx)

	@edit.command()
	async def prefix(self, ctx, *, msg):
		if ctx.author.id == 435806214484393996:
			with open(r"config.json", 'r') as f:
				config = json.load(f)

			config["prefix"] = msg

			with open(r"config.json", 'w') as f:
				json.dump(config, f, indent=4)

			embed = discord.Embed(title="C&C Bot: ADMIN", color=0xdfe324, description=f"Successfully changed prefix to: {msg}")	
			await ctx.send(embed=embed)
		else:
			await self.msgPycord(ctx)


def setup(bot):
	bot.add_cog(Admin(bot))