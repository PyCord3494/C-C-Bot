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
extensions = ["cogs.economy", "cogs.earn", "cogs.transfer", "cogs.shop", "cogs.rewards", "cogs.admin", "cogs.error_help", "cogs.slots", "cogs.utils", "cogs.other"]

bot.remove_command('help')

@bot.event
async def on_ready():
	global LogFile
	LogFile = open("Logs.txt", "a")
	
	print(f"{bot.user.name} - {bot.user.id}")
	print(discord.__version__)
	print("Ready...")

	await bot.change_presence(activity=discord.Game(name="Do +help for help!"))


@bot.command(hidden = True)
async def reload(ctx, extension):
	if await bot.is_owner(ctx.author):
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
