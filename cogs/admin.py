# Cog for all the transactions/logging 
# Aka anything dealing with file editing


import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import json

import time
import datetime


class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.cooldown(1, 2, commands.BucketType.user)	
	async def ping(self, ctx):
		embed = discord.Embed(color=0xdfe324, description="Pong!")
		before = time.monotonic()
		message = await ctx.send(embed=embed)
		ping = (time.monotonic() - before) * 1000
		embed.description = f"Pong!  `{round(ping,9)} ms`"
		await message.edit(embed=embed)

	@commands.command(hidden = True, pass_context=True)
	async def end(self, ctx):
		if await self.bot.is_owner(ctx.author):
			print("\nGoing to sleep...\n")
			await self.bot.logout()

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

				embed = discord.Embed(title="C&C Bot: ADMIN", color=0xdfe324, description=f"Added {amnt} {currency} to user {user.mention} ({user.id})")
				await ctx.send(embed=embed)
			else:
				embed = discord.Embed(title="C&C Bot: ADMIN", color=0xff0000, description="User not found. Please @mention him or provide me his ID.\nProper format: `+addcoins user amount`")
				await ctx.send(embed=embed)
		else:
			me = await self.bot.fetch_user(547475078082985990)
			await me.send(f"User {ctx.author.mention}")


	@commands.group(invoke_without_command=True, pass_context=True, hidden=True)
	async def edit(self, ctx):
		if ctx.invoked_subcommand is None:
			embed = discord.Embed(title="C&C Bot: ADMIN", color=0xff0000, description="This is a command that requires subcommands.\nAvailable subcommands: `currency` & `prefix`.\nCorrect usage: `edit prefix +`")
			await ctx.send(embed=embed)
	

	@edit.command()
	async def currency(self, ctx, *, msg):
		with open(r"config.json", 'r') as f:
			config = json.load(f)

		config["currency"] = msg

		with open(r"config.json", 'w') as f:
			json.dump(config, f, indent=4)
		embed = discord.Embed(title="C&C Bot: ADMIN", color=0xdfe324, description=f"Successfully changed currency to: {msg}")
		await ctx.send(embed=embed)

	@edit.command()
	async def prefix(self, ctx, *, msg):
		with open(r"config.json", 'r') as f:
			config = json.load(f)

		config["prefix"] = msg

		with open(r"config.json", 'w') as f:
			json.dump(config, f, indent=4)

		embed = discord.Embed(title="C&C Bot: ADMIN", color=0xdfe324, description=f"Successfully changed prefix to: {msg}")	
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Admin(bot))