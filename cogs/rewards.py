# Cog for anything related to free money and rewards

import discord
from discord.ext import commands


class Rewards(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(pass_context=True)
	@commands.cooldown(1, 86400, commands.BucketType.user)	
	async def daily(self, ctx):
		author = ctx.author
		discordId = author.id
		if await self.bot.get_cog("Economy").accCheck(ctx, discordId) == False:
			return
		currency = self.bot.get_cog("Economy").getCurrency()
		if "Nitro Booster" in [y.name.lower() for y in author.roles]:
			reward = 1000
		else:
			reward = 500

		bal = await self.bot.get_cog("Economy").editBal(ctx, discordId, reward)
		embed = discord.Embed(title="C&C Bot: Rewards", color=0xdfe324, description=f"{reward} {currency} has been added to your account. You now have {format(bal, ',d')} {currency}")
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		

def setup(bot):
	bot.add_cog(Rewards(bot))