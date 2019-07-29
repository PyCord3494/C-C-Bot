# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import json

import datetime


class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True, pass_context=True)
	@commands.has_permissions(administrator=True)
	async def addcoins(self, ctx, user: discord.Member, amnt: int):
		currency = self.bot.get_cog("Economy").getCurrency()

		with open('users.json') as f:
				data = json.load(f)

		if str(user.id) in data:
			data[str(user.id)] = data[str(user.id)] + amnt

			with open('users.json','w') as f:
				json.dump(data, f, indent=4)

			await ctx.send(f"Added {amnt} {currency} to user {ctx.author.mention} ({ctx.author.id})")
		else:
			await ctx.send("User not found. Please @mention him or provide me his ID.\nProper format: `+addcoins user amount`")
		
		#log(ctx.author.id, amnt)


	@commands.group(invoke_without_command=True, pass_context=True, hidden=True)
	async def edit(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send("ok")
	

	@edit.command()
	async def currency(self, ctx, *, msg):
		with open(r"config.json", 'r') as f:
			config = json.load(f)

		config["currency"] = msg

		with open(r"config.json", 'w') as f:
			json.dump(config, f, indent=4)

		await ctx.send(f"Successfully changed currency to: {msg}")

	@edit.command()
	async def prefix(self, ctx, *, msg):
		with open(r"config.json", 'r') as f:
			config = json.load(f)

		config["prefix"] = msg

		with open(r"config.json", 'w') as f:
			json.dump(config, f, indent=4)

		await ctx.send(f"Successfully changed prefix to: {msg}")	


def setup(bot):
	bot.add_cog(Admin(bot))
