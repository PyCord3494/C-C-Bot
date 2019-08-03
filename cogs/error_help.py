# Global error handling


import discord
from discord.ext import commands

import json
import datetime
import traceback
from difflib import get_close_matches


class ErrorHelp(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def get_prefix(self):
		with open(r"config.json", 'r') as f:
				config = json.load(f)

		prefix = config["prefix"]
		return prefix

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		embed = discord.Embed(title="C&C Bot: ERROR", color=0xff0000)

		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			prefix = self.get_prefix()
			lst = ["ping", "botinfo", "bi", "help", "balance", "bal", "money", "shop", "send", "leaderboard", "lb", "work", "crime", "gamble", "slots", "daily"]
		#	embed.description = "Command not found!"
			cmd = ctx.message.content.split()[0][1:]
			try:
				closest = get_close_matches(cmd.lower(), lst)[0]
			except IndexError:
				embed.description = f"`{prefix}{cmd.lower()}` is not a known command."
			else:
				embed.description = f"`{prefix}{cmd.lower()}` is not a command, did you mean `{prefix}{closest}`?"


		elif isinstance(error, commands.CommandOnCooldown):

			a = datetime.timedelta(seconds=error.retry_after)

			cooldown = str(a).split(".")[0]

			embed.description = f"{str(ctx.command).title()} is on cooldown. Please retry again in {cooldown}"

		elif isinstance(error, commands.MissingRequiredArgument):
			ctx.command.reset_cooldown(ctx)
			err = str(error.param)
			err = err.replace("_", " ")
			err = str(err.split(":")[0])
			if err == "amnt":
				err = "amount"

			firstChar = err[0]
			if firstChar.lower() in "aeiou" and err != "user":
				a_an = "an"
			else:
				a_an = "a"

			embed.description = f"Please specify {a_an} {err} for this command to work."

		elif isinstance(error, commands.TooManyArguments):
			ctx.command.reset_cooldown(ctx)
			embed.description = "You have tried using this command with too many arguments."

		elif isinstance(error, commands.CheckFailure):
			embed.description = "You do not have the required permissions to use this command."

		elif isinstance(error, commands.BadArgument):
			ctx.command.reset_cooldown(ctx)
			embed.description = f"{error}"
		else:
			ctx.command.reset_cooldown(ctx)
			err = str(error)
			err = err.split(':', 2)[-1]

			embed.description = f"Error: `{err}`. \nDeveloper has been contacted with all related details..."
			e = discord.Embed(title='Command Error', colour=0xcc3366)
			command_name = ctx.command.qualified_name
			if command_name: 
				e.add_field(name='Name', value=ctx.command.qualified_name)
			e.add_field(name='Author', value=f'{ctx.author} (ID: {ctx.author.id})')

			fmt = f'Channel: {ctx.channel} (ID: {ctx.channel.id})'
			if ctx.guild:
				fmt = f'{fmt}\nGuild: {ctx.guild} (ID: {ctx.guild.id})'

			e.add_field(name='Location', value=f"{fmt}]\n[Link]({ctx.message.jump_url})", inline=False)

			exc = ''.join(traceback.format_exception(type(error), error, error.__traceback__, chain=False))
			e.description = f'```py\n{exc}\n```'
			e.timestamp = datetime.datetime.utcnow()
			ch = self.bot.get_channel(605921228083167245)
			await ch.send(embed=e)

		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(ErrorHelp(bot))