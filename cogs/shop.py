import discord
from discord.ext import commands

import datetime

class Shop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.items = [200000, 500000]


	@commands.group(invoke_without_command=True, pass_context=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def shop(self, ctx):
		if ctx.invoked_subcommand is None:
			if await self.bot.get_cog("Economy").accCheck(ctx, ctx.author.id) == False:
				return
			currency = self.bot.get_cog("Economy").getCurrency()
			#embed = discord.Embed(title="C&C Bot: Shop", color=0xdfe324, description="ID            ITEMS                COST\n1   not seperated custom role!  200,000\n2     seperated custom role!    500,000\n----------------------------------------\nUse +shop buy <id>")
			embed = discord.Embed(color=0xdfe324, author=ctx.author, description = "Buy an item with `+shop buy <ItemID>`")
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"<:Koin:605192353782956052>200,000 - Not Separated Custom Role", value="Buy a custom role not seperated from the list of the people online.\nType `<+shop buy 1>` to purchase.", inline=False)
			embed.add_field(name=f"_ _\n<:Koin:605192353782956052>500,000 - Separated Custom Role", value="Get your self a custom role separated from others!\nType `<+shop buy 2>` to purchase.", inline=False)
			await ctx.send(embed=embed)
			# await ctx.send("```ML\nID            ITEMS                COST\n" # the shop menu
			# 					+ "1   not seperated custom role!  200,000\n"
			# 					+ "2     seperated custom role!    500,000\n"
			# 					+ "----------------------------------------\n"
			# 					+ "Use +shop buy <id>\n```")

	@shop.command()
	async def buy(self, ctx, ID: int):
		currency = self.bot.get_cog("Economy").getCurrency()
		discordId = ctx.message.author.id
		if await self.bot.get_cog("Economy").accCheck(ctx, discordId) == False:
			return
		if ID != 1 and ID != 2: # if ID isn't valid
			embed = discord.Embed(title="C&C Bot: Shop", color=0xff0000, description="Invalid item ID.")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return
		
		bal = self.bot.get_cog("Economy").getBal(discordId) # grabs balance
		price = self.items[ID - 1] # grabs price from array in __init__
		if bal < price: # if cost is too much
			embed = discord.Embed(title="C&C Bot: Shop", color=0xff0000, description=f"That will cost you {format(price, ',d')} {currency}, but you only have {format(bal, ',d')} {currency}")
			embed.set_thumbnail(url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
			return

		bal = await self.bot.get_cog("Economy").editBal(discordId, -price) # subtract price from bal
		
		embed = discord.Embed(title="C&C Bot: Shop", color=0xdfe324, description=f"Purchase successful! Remaining balance: {format(bal, ',d')} {currency}\nI have sent a message to {ctx.guild.owner.mention} and he will be messaging you when he can. Please be patient. :)")
		embed.set_thumbnail(url=ctx.author.avatar_url)
		msg = await ctx.send(embed=embed)


		embed = discord.Embed(title="C&C Bot: NEW PURCHASE", color=0xdfe324)
		if ID == 1: # shop item #1
			embed.add_field(name="Item Bought", value=f"User {ctx.author.mention} ({ctx.author.id}) has purchased \"Not separated Custom Role!\" for {format(price, ',d')} {currency}")
		
		elif ID == 2: # shop item #2
			embed.add_field(name="Item Bought", value=f"User {ctx.author.mention} ({ctx.author.id}) has purchased \"Seperated Custom Role!\" for {format(price, ',d')} {currency}")
		embed.add_field(name="Link", value=f"[Click Me]({ctx.message.jump_url})!")
		embed.set_thumbnail(url=ctx.author.avatar_url)
		embed.timestamp = datetime.datetime.utcnow()
		await ctx.guild.owner.send(embed=embed)

def setup(bot):
	bot.add_cog(Shop(bot))