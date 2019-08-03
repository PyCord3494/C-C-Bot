import discord
from discord.ext import commands

import time

class Other(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.cooldown(1, 2, commands.BucketType.user)	
	async def ping(self, ctx):
		embed = discord.Embed(color=0xdfe324, description="Pong!")
		before = time.monotonic()
		message = await ctx.send(embed=embed)
		ping = (time.monotonic() - before) * 1000
		embed.description = f"Pong!  `{round(ping, 9)} ms`"
		await message.edit(embed=embed)


	@commands.command(aliases=["bi", "info"], pass_context=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def botinfo(self, ctx):
		embed = discord.Embed(color=0x00e100)
		embed.add_field(name="Info", value="I was developed by <@547475078082985990> for free to help out the C&C community! (*feel free to tell him his bot says hi!*)")
		embed.add_field(name="Birth", value="I was an idea that started on July 27, 2019 and I was finally fully developed and put into the server on August 2nd.")
		embed.add_field(name="_ _\nSupport me!", value="If you enjoy me and my features, please consider donating ([Click Here](https://www.paypal.me/AutopilotJustin)) to the person who developed me. (｡◕‿◕｡)")
		await ctx.send(f"{ctx.author.mention}, thanks for taking an interest in learning more about me! ヽ(´▽`)/", embed=embed)
		


def setup(bot):
	bot.add_cog(Other(bot))