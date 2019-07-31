import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import time
import asyncio

import ztoken


async def get_prefix(bot, message):
	with open(r"config.json", 'r') as f:
			config = json.load(f)

	prefix = config["prefix"]
	return prefix


bot = commands.Bot(command_prefix = get_prefix)
extensions = ["cogs.economy", "cogs.earn", "cogs.transfer", "cogs.shop", "cogs.rewards", "cogs.admin", "cogs.error_help", "cogs.slots"]

bot.remove_command('help')

@bot.group(invoke_without_command=True, pass_context=True)
async def help(ctx):
	prefix = await get_prefix(bot, ctx.message)
	embed = discord.Embed(title="C&C Bot Help", color=0xdfe324, description=f"**My prefix is {prefix}**")
	embed.add_field(name="Money", value=f"{prefix}balance\n{prefix}shop\n{prefix}send\n{prefix}leaderboard")
	embed.add_field(name="Make Money!", value= f"{prefix}work\n{prefix}crime\n{prefix}gamble")
	embed.add_field(name="Free Money!", value= f"{prefix}daily")
	await ctx.send(embed=embed)


@help.command()
async def balance(ctx):
	embed = discord.Embed(title="C&C Bot Help: Balance", color=0xdfe324, description="Displays your balance in the server. You can also type `+bal`")
	await ctx.send(embed=embed)

@help.command()
async def shop(ctx):
	embed = discord.Embed(title="C&C Bot Help: Shop", color=0xdfe324, description="Buy something from the shop! Type +shop for more details.")
	await ctx.send(embed=embed)

@help.command()
async def send(ctx):
	embed = discord.Embed(title="C&C Bot Help: Send", color=0xdfe324, description="Send money to someone else in the server. Type +send for more details.")
	await ctx.send(embed=embed)

@help.command()
async def leaderboard(ctx):
	embed = discord.Embed(title="C&C Bot Help: Daily", color=0xdfe324, description="Show the users with the most money in the server! You can also type `+lb`")
	await ctx.send(embed=embed)

@help.command()
async def work(ctx):
	embed = discord.Embed(title="C&C Bot Help: Work", color=0xdfe324, description="Use this command to quickly earn some money risk-free.")
	await ctx.send(embed=embed)

@help.command()
async def crime(ctx):
	embed = discord.Embed(title="C&C Bot Help: Crime", color=0xdfe324, description="Try to commit a crime to earn some money.\nUsage: `+crime`")
	await ctx.send(embed=embed)


@help.command()
async def gamble(ctx):
	embed = discord.Embed(title="C&C Bot Help: Gamble", color=0xdfe324, description="Risk some of your money to win some money.\nUsage: `+gamble amnt`")
	await ctx.send(embed=embed)

@help.command()
async def daily(ctx):
	embed = discord.Embed(title="C&C Bot Help: Daily", color=0xdfe324, description="Claim your daily reward!")
	await ctx.send(embed=embed)

@bot.event
async def on_ready():
	global LogFile
	LogFile = open("Logs.txt", "a")
	
	print(f"{bot.user.name} - {bot.user.id}")
	print(discord.__version__)
	print("Ready...")

@bot.command(pass_context=True)
async def ping(ctx):
	embed = discord.Embed(color=0xdfe324, description="Pong!")
	before = time.monotonic()
	message = await ctx.send(embed=embed)
	ping = (time.monotonic() - before) * 1000
	embed = discord.Embed(color=0xdfe324, description=f"Pong!  `{round(ping,9)} ms`")
	await message.edit(embed=embed)


@bot.command(hidden = True, pass_context=True)
async def end(ctx):
	if await bot.is_owner(ctx.message.author):
		print("\nGoing to sleep...\n")
		await bot.logout()


@bot.command(hidden = True)
@has_permissions(administrator=True)
async def reload(ctx, extension):
	try:
		bot.reload_extension(extension)
		print(f"Reloaded {extension}.\n")
	except Exception as error:
		print(f"{extension} could not be reloaded. [{error}]")


if __name__ == '__main__':
	for extension in extensions:
		try:
			bot.load_extension(extension)
			print(f"Loaded cog: {extension}")
		except Exception as error:
			print(f"{extension} could not be loaded. [{error}]")
	bot.run(ztoken.token)
