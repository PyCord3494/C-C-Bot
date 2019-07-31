# Global error handling


import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import json
import datetime
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

		if isinstance(error, commands.CommandNotFound):
			prefix = self.get_prefix()
			lst = ["help", "balance", "bal", "money", "shop", "send", "leaderboard", "lb", "work", "crime", "gamble", "slots", "daily"]
		#	embed.description = "Command not found!"
			cmd = ctx.message.content.split()[0][1:]
			try:
				closest = get_close_matches(cmd.lower(), lst)[0]
			except IndexError:
				embed.description = f"`{prefix}{cmd}` is not a known command."
			else:
				embed.description = f"`{prefix}{cmd}` is not a command, did you mean `{prefix}{closest}`?"
			





		elif isinstance(error, commands.CommandOnCooldown):

			a = datetime.timedelta(seconds=error.retry_after)

			cooldown = str(a).split(".")[0]

			embed.description = f"{str(ctx.command).title()} is on cooldown. Please retry again in {cooldown}"

		elif isinstance(error, commands.MissingRequiredArgument):
			ctx.command.reset_cooldown(ctx)
			err = str(error.param)
			arg = err.replace("_", " ")
			arg = arg.split(":")
			embed.description = f"Please specify a {arg[0]} for this command to work."

		elif isinstance(error, commands.TooManyArguments):
			ctx.command.reset_cooldown(ctx)
			embed.description = "You have tried using this command with too many arguments."

		elif isinstance(error, commands.CheckFailure):
			embed.description = "You do not have the required permissions to use this command."

		else:
			ctx.command.reset_cooldown(ctx)
			embed.description = f"{error}"


		await ctx.send(embed=embed)




def setup(bot):
	bot.add_cog(ErrorHelp(bot))
