import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import time

import ztoken


async def get_prefix(bot, message):
	with open(r"config.json", 'r') as f:
			config = json.load(f)

	prefix = config["prefix"]
	return prefix


bot = commands.Bot(command_prefix = get_prefix)
extensions = ["cogs.economy", "cogs.earn", "cogs.transfer", "cogs.shop", "cogs.rewards", "cogs.admin"]


@bot.event
async def on_ready():
	global LogFile
	LogFile = open("Logs.txt", "a")
	
	print(f"{bot.user.name} - {bot.user.id}")
	print(discord.__version__)
	print("Ready...")

@bot.command(pass_context=True)
async def ping(ctx):
	before = time.monotonic()
	message = await ctx.send("Pong!")
	ping = (time.monotonic() - before) * 1000
	await message.edit(content=f"Pong!  `{round(ping,9)} ms`")

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
